import logging
from typing import AsyncGenerator, Optional
import asyncio
import os
from google import genai
from google.genai import types

logger = logging.getLogger(__name__)


class STTResult:
    """STT transcription result"""
    def __init__(self, text: str, confidence: float, is_final: bool):
        self.text = text
        self.confidence = confidence
        self.is_final = is_final


class STTClient:
    """
    Gemini 2.5 Live STT client (v1beta) using google-genai SDK.

    Uses a PERSISTENT WebSocket session — opened once at connect() and reused
    across every transcribe_stream() call.

    Bug fixes applied vs. previous version:
      • Bug 1: receive loop now breaks on turn_complete so the pipeline can
               proceed to NLU/TTS after each utterance.
      • Bug 5: non-transcription server messages are skipped fast with an
               early continue rather than falling through all the getattr calls.
    """

    def __init__(self, provider: str = "gemini_live", config: dict = None):
        self.provider = "gemini_live"
        self.config = config or {}
        self.is_connected = False
        self.api_key: Optional[str] = None
        self.client: Optional[genai.Client] = None
        self.model = "models/gemini-2.5-flash-native-audio-preview-12-2025"

        # Persistent session — kept alive across turns
        self._session_ctx = None
        self._session = None

    # ─── Lifecycle ────────────────────────────────────────────────────────────

    async def connect(self) -> bool:
        """Open the SDK client AND pre-warm the WebSocket session."""
        try:
            self.api_key = self.config.get("gemini_api_key") or os.getenv("GEMINI_API_KEY")
            if not self.api_key:
                logger.error("❌ Gemini API Key missing!")
                return False

            self.client = genai.Client(
                http_options={"api_version": "v1beta"},
                api_key=self.api_key,
            )

            await self._open_session()
            logger.info(f"✨ Gemini Live persistent session ready (Model: {self.model})")
            self.is_connected = True
            return True
        except Exception as e:
            logger.error(f"❌ Gemini connect failed: {e}")
            return False

    async def _open_session(self):
        """Open (or re-open) the persistent WebSocket session."""
        config = types.LiveConnectConfig(
            response_modalities=["AUDIO"],
            input_audio_transcription=types.AudioTranscriptionConfig(),
        )
        self._session_ctx = self.client.aio.live.connect(
            model=self.model, config=config
        )
        self._session = await self._session_ctx.__aenter__()
        logger.debug("🔌 Gemini Live WebSocket opened")

    async def close(self):
        """Gracefully close the persistent session."""
        self.is_connected = False
        if self._session_ctx:
            try:
                await self._session_ctx.__aexit__(None, None, None)
            except Exception:
                pass
        self._session = None
        self._session_ctx = None
        self.client = None

    # ─── Transcription ────────────────────────────────────────────────────────

    async def transcribe_stream(
        self,
        audio_stream: AsyncGenerator[bytes, None],
        session_id: str,
        language: str = "si-LK",
    ) -> AsyncGenerator[STTResult, None]:
        """
        Relay PCM audio into the persistent Gemini Live session and yield
        STTResult objects as input_transcription text arrives.

        FIX (Bug 1): The receive loop now breaks on `turn_complete=True` so
        this generator returns after each utterance, letting the pipeline
        proceed to NLU → TTS and then re-enter for the next turn.

        FIX (Bug 5): Non-transcription messages (model audio, setup acks, etc.)
        are skipped with an early `continue` to avoid unnecessary work.
        """
        if not self._session:
            if not await self.connect():
                return

        session = self._session

        async def sender():
            """Forward PCM chunks to Gemini as fast as they arrive."""
            try:
                async for chunk in audio_stream:
                    if chunk is None:
                        break
                    await session.send_realtime_input(
                        media=types.Blob(data=chunk, mime_type="audio/pcm;rate=16000")
                    )
            except asyncio.CancelledError:
                pass
            except Exception as e:
                logger.error(f"❌ STT sender error [{session_id}]: {e}")

        sender_task = asyncio.create_task(sender())

        last_text = ""
        try:
            async for response in session.receive():

                # ── Bug 5 fix: skip fast if no server content ──────────────
                sc = getattr(response, "server_content", None)
                if not sc:
                    continue

                # ── Bug 1 & 6 fix: handle turn_complete and interim results ──
                turn_complete = getattr(sc, "turn_complete", False)

                it = getattr(sc, "input_transcription", None)
                if it:
                    text = getattr(it, "text", None)
                    if text:
                        text = text.strip()
                        if text:
                            last_text = text
                            logger.debug(f"📝 [{session_id}] (interim) {text}")
                            # Yield intermediate results as NOT final so the pipeline keeps buffering
                            yield STTResult(text=text, confidence=1.0, is_final=False)

                if turn_complete:
                    logger.debug(f"✅ turn_complete received for [{session_id}] — exiting receive loop")
                    # Yield the final buffered text with is_final=True to trigger the state machine
                    # Only yield if we actually have some text to process.
                    if last_text:
                        yield STTResult(text=last_text, confidence=1.0, is_final=True)
                    break

        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error(f"❌ STT receiver error [{session_id}]: {e}")
            # Session likely dropped — clear so next call reconnects cleanly.
            self._session = None
            self._session_ctx = None
        finally:
            sender_task.cancel()
            try:
                await sender_task
            except asyncio.CancelledError:
                pass

    async def transcribe_file(self, audio_file_path: str, language: str = "si-LK") -> str:
        return "Streaming only – use transcribe_stream()"
