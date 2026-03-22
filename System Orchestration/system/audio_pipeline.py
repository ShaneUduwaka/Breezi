import asyncio
import logging
import numpy as np
from typing import AsyncGenerator
from collections import deque

# Defer torch import to avoid failing if not installed yet
try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

# Defer silero-vad import
try:
    from silero_vad import load_silero_vad #IGNORE
    SILERO_AVAILABLE = True
except ImportError:
    SILERO_AVAILABLE = False

logger = logging.getLogger(__name__)


class AudioPipelineManager:
    """
    Manages the core bidirectional streaming logic.
    Receives raw audio packets, proxies them to STT, feeds text to Orchestrator,
    extracts reply, streams to TTS, and outputs raw audio packets.
    """

    # ── VAD tuning ────────────────────────────────────────────────────────────
    VAD_RMS_THRESHOLD      = 800   # ignore quiet background noise (raise to reduce sensitivity)
    VAD_CONFIDENCE         = 0.90  # Silero confidence to count as speech (raise to reduce false positives)
    VAD_CONSECUTIVE_CHUNKS = 5     # chunks in a row needed to trigger barge-in (raise to require more sustained speech)
    VAD_SILENCE_CHUNKS     = 40    # chunks of silence needed after speech to force a turn end (approx 1.2s)
    # ─────────────────────────────────────────────────────────────────────────

    def __init__(self, system):
        self.system = system
        self.sessions: dict = {}

        # Load Silero VAD once at startup (shared across sessions)
        self.vad_model = None
        if TORCH_AVAILABLE and SILERO_AVAILABLE:
            try:
                logger.info("🧠 Loading Silero VAD model...")
                # Use the silero-vad pip package (no GitHub network access needed)
                self.vad_model = load_silero_vad()
                logger.info("✅ Silero VAD ready")
            except Exception as e:
                logger.error(f"Failed to load VAD model: {e}")
        elif not SILERO_AVAILABLE:
            logger.warning("⚠️ silero-vad package not installed – VAD/barge-in disabled. Run: pip install silero-vad")
        elif not TORCH_AVAILABLE:
            logger.warning("⚠️ torch not installed – VAD/barge-in disabled. Run: pip install torch")

    # ── Session management ────────────────────────────────────────────────────

    async def start_session(self, session_id: str):
        if session_id in self.sessions:
            return
        logger.info(f"Starting audio pipeline session: {session_id}")
        
        from dialog.call_state_machine import CallStateMachine
        sm = CallStateMachine(session_id)

        self.sessions[session_id] = {
            "in_queue":             asyncio.Queue(),
            "out_queue":            asyncio.Queue(),
            "preroll_buffer":       deque(maxlen=40),  # ~1.2s of audio to catch speech while bot speaks
            "barge_in":             False,
            "vad_consecutive":      0,
            "silence_consecutive":  0,
            "speech_ever_detected": False,
            "end_of_turn":          False,
            "state_machine":        sm,
        }
        # Start the pipeline task AFTER the session dict is in place
        self.sessions[session_id]["task"] = asyncio.create_task(
            self._run_pipeline(session_id)
        )

    async def stop_session(self, session_id: str):
        if session_id not in self.sessions:
            return
        logger.info(f"Stopping audio pipeline session: {session_id}")
        self.sessions[session_id]["task"].cancel()
        # Unblock any waiters
        await self.sessions[session_id]["in_queue"].put(None)
        await self.sessions[session_id]["out_queue"].put(None)
        del self.sessions[session_id]

    # ── VAD helpers ───────────────────────────────────────────────────────────

    def _detect_speech(self, chunk: bytes, session_id: str) -> tuple[bool, bool]:
        """Return (is_currently_speaking, is_endpoint_detected)."""
        if not self.vad_model or session_id not in self.sessions:
            return False, False

        sess = self.sessions[session_id]
        try:
            audio_int16 = np.frombuffer(chunk, dtype=np.int16)

            # 1. Volume gate – ignore quiet background / fan noise
            rms = float(np.sqrt(np.mean(audio_int16.astype(np.float32) ** 2)))
            if rms < self.VAD_RMS_THRESHOLD:
                sess["vad_consecutive"] = 0
                if sess.get("speech_ever_detected", False):
                    sess["silence_consecutive"] = sess.get("silence_consecutive", 0) + 1
                    if sess["silence_consecutive"] >= self.VAD_SILENCE_CHUNKS:
                        return False, True
                return False, False

            audio_f32 = audio_int16.astype(np.float32) / 32768.0

            # Silero requires ≥ 512 samples at 16 kHz
            if len(audio_f32) >= 512:
                tensor = torch.from_numpy(audio_f32[:512]).unsqueeze(0)
                prob = self.vad_model(tensor, 16000).item()

                if prob > self.VAD_CONFIDENCE:
                    sess["vad_consecutive"] = sess.get("vad_consecutive", 0) + 1
                    sess["silence_consecutive"] = 0
                    if sess["vad_consecutive"] >= self.VAD_CONSECUTIVE_CHUNKS:
                        sess["speech_ever_detected"] = True
                        return True, False
                else:
                    sess["vad_consecutive"] = 0
                    if sess.get("speech_ever_detected", False):
                        sess["silence_consecutive"] = sess.get("silence_consecutive", 0) + 1
                        if sess["silence_consecutive"] >= self.VAD_SILENCE_CHUNKS:
                            return False, True

        except Exception as e:
            logger.warning(f"VAD inference error for {session_id}: {e}")
            sess["vad_consecutive"] = 0
            sess["silence_consecutive"] = 0

        return False, False

    def _flush_out_queue(self, session_id: str):
        """Drain any pending TTS audio so the bot stops speaking immediately."""
        q = self.sessions[session_id]["out_queue"]
        while not q.empty():
            try:
                q.get_nowait()
            except asyncio.QueueEmpty:
                break

    # ── Public audio I/O ──────────────────────────────────────────────────────

    async def feed_audio_chunk(self, session_id: str, chunk: bytes):
        """Push a raw PCM chunk from the mic / WebSocket into the pipeline."""
        if session_id not in self.sessions:
            await self.start_session(session_id)

        sess = self.sessions[session_id]

        # Echo Suppression: If bot is speaking (out_queue not empty), ignore VAD and don't buffer for STT
        bot_is_speaking = not sess["out_queue"].empty()
        
        # Barge-in and endpoint detection
        is_speech, is_endpoint = self._detect_speech(chunk, session_id)
        
        if is_speech and not bot_is_speaking:
            if not sess["barge_in"]:
                logger.info("⚠️  Barge-in! Flushing output buffer.")
                sess["barge_in"] = True
                self._flush_out_queue(session_id)
        
        if is_endpoint and not sess["end_of_turn"] and not bot_is_speaking:
            logger.info("🎯  VAD endpoint detected – signaling end of turn.")
            sess["end_of_turn"] = True
            await sess["in_queue"].put(None) # Sentinel to break the STT generator
            return

        if bot_is_speaking:
            # Buffer audio while bot speaks so we don't lose the start of the next sentence
            sess["preroll_buffer"].append(chunk)
        else:
            # Bot just stopped or isn't speaking — flush the pre-roll buffer first if needed
            while sess["preroll_buffer"]:
                await sess["in_queue"].put(sess["preroll_buffer"].popleft())
            await sess["in_queue"].put(chunk)

    async def get_audio_stream(self, session_id: str) -> AsyncGenerator[bytes, None]:
        """Yield TTS audio chunks for playback on speakers / WebSocket."""
        if session_id not in self.sessions:
            await self.start_session(session_id)

        q = self.sessions[session_id]["out_queue"]
        while True:
            chunk = await q.get()
            if chunk is None:
                break
            yield chunk

    # ── Internal helpers ──────────────────────────────────────────────────────

    async def _audio_generator(self, session_id: str) -> AsyncGenerator[bytes, None]:
        """Drain in_queue and yield raw PCM chunks to STT until a None sentinel is reached."""
        q = self.sessions[session_id]["in_queue"]
        while True:
            chunk = await q.get()
            if chunk is None:
                break
            yield chunk

    # ── Core pipeline ─────────────────────────────────────────────────────────

    async def _run_pipeline(self, session_id: str):
        """
        Main pipeline loop:
          mic audio → STT → NLU / dialogue → TTS → speaker audio

        The STT stream is wrapped in an infinite reconnect loop because Google
        Cloud STT hard-limits each streaming session to ~5 minutes.
        """
        try:
            stt          = self.system.get("stt_client")
            tts          = self.system.get("tts_client")
            conversation = self.system.get("conversation")
            if not stt or not tts or not conversation:
                missing = [k for k, v in {"stt_client": stt, "tts_client": tts, "conversation": conversation}.items() if not v]
                logger.error(f"Pipeline cannot start for {session_id} – missing system components: {missing}")
                return

            while True:
                try:
                    logger.info(f"🎙️  Opening STT stream for {session_id}")
                    # Reset turn-level VAD results
                    sess = self.sessions[session_id]
                    sess["speech_ever_detected"] = False
                    sess["vad_consecutive"]      = 0      # Critical Bug 4 fix
                    sess["silence_consecutive"]  = 0
                    sess["end_of_turn"]           = False
                    
                    # Drain any stale audio from the queue to start fresh
                    while not sess["in_queue"].empty():
                        try:
                            sess["in_queue"].get_nowait()
                        except asyncio.QueueEmpty:
                            break

                    # Create a FRESH generator each time we (re-)connect to STT
                    audio_stream = self._audio_generator(session_id)
                    got_result = False

                    sess = self.sessions[session_id]
                    sm = sess["state_machine"]
                    
                    # Proactive greeting (only happens once because state changes)
                    greeting = sm.get_proactive_greeting()
                    if greeting:
                        logger.info(f"👋 Triggering proactive greeting for {session_id}")
                        async for tts_chunk in tts.synthesize_stream(
                            session_id=session_id, text=greeting, language="si-LK"
                        ):
                            if sess.get("barge_in", False):
                                break
                            await sess["out_queue"].put(tts_chunk)

                    # Timeout task to monitor 15 seconds of silence
                    async def silence_monitor():
                        while session_id in self.sessions:
                            await asyncio.sleep(1)
                            s = self.sessions.get(session_id)
                            if not s: break
                            if not s["out_queue"].empty() or s.get("barge_in", False):
                                s["last_user_speech"] = asyncio.get_event_loop().time()
                            else:
                                elapsed = asyncio.get_event_loop().time() - s.get("last_user_speech", 0)
                                if elapsed > 15.0:
                                    logger.info(f"⏳ 15 seconds silence timeout for {session_id}")
                                    if sm.state.name in ["ACTIVE", "WRAPUP"]:
                                        timeout_text = "I haven't heard anything for a while, so I am ending the call. Goodbye!"
                                        async for tts_chunk in tts.synthesize_stream(
                                            session_id=session_id, text=timeout_text, language="en-US"
                                        ):
                                            await s["out_queue"].put(tts_chunk)
                                        await asyncio.sleep(2)
                                    await s["out_queue"].put(None)
                                    # We don't need to break out of STT loop directly, returning None to out_queue ends the WS!
                                    # But to be safe, cancel the stt stream
                                    my_task = s.get("task")
                                    if my_task: my_task.cancel()
                                    break

                    sess["last_user_speech"] = asyncio.get_event_loop().time()
                    monitor_task = asyncio.create_task(silence_monitor())

                    try:
                        cleaned = None
                        async for result in stt.transcribe_stream(
                            audio_stream, session_id, language="si-LK"
                        ):
                            got_result = True
                            sess["last_user_speech"] = asyncio.get_event_loop().time()
                            
                            cleaned = result.text.strip()
    
                            # Drop interim / empty / noise transcripts
                            if not result.is_final or len(cleaned) < 2:
                                continue

                        # Reset barge-in so the reply can play in full
                        self.sessions[session_id]["barge_in"] = False

                        if not cleaned or len(cleaned) < 2:
                            logger.info(f"🔇 Ignoring empty/short utterance for {session_id}")
                            continue

                        # ── Debug logging ──────────────────────────────────
                        prev_intent = getattr(conversation.state, "intent", "None") if conversation.state else "None"
                        prev_slots  = getattr(conversation.state, "slots",  {})     if conversation.state else {}

                        reply_text, should_end = sm.handle(cleaned, conversation)

                        new_intent = getattr(conversation.state, "intent", "None") if conversation.state else "None"
                        new_slots  = getattr(conversation.state, "slots",  {})     if conversation.state else {}

                        print("\n" + "=" * 50)
                        print(f"🎙️  UTTERANCE : {cleaned}")
                        print(f"🎯  INTENT    : {new_intent} (was {prev_intent})")
                        print(f"🧩  SLOTS     : {new_slots}")
                        print(f"🤖  REPLY     : {reply_text}")
                        print("=" * 50 + "\n")
                        # ──────────────────────────────────────────────────

                        if reply_text:
                            async for tts_chunk in tts.synthesize_stream(
                                session_id=session_id,
                                text=reply_text,
                                language="si-LK",
                            ):
                                # Stop TTS if user barged in
                                if self.sessions[session_id].get("barge_in", False):
                                    logger.info("🛑 TTS halted – barge-in")
                                    break
                                await self.sessions[session_id]["out_queue"].put(tts_chunk)

                        if should_end:
                            logger.info(f"👋 Session {session_id} ended by state machine.")
                            # Push None to close the WS stream ungracefully/gracefully
                            await self.sessions[session_id]["out_queue"].put(None)
                            return
                    finally:
                        monitor_task.cancel()


                except asyncio.CancelledError:
                    raise  # propagate so stop_session works cleanly
                except Exception as e:
                    logger.warning(
                        f"STT stream ended for {session_id} (will reconnect): {e}"
                    )
                    await asyncio.sleep(0.5)   # brief pause before reconnect
                else:
                    # STT stream ended cleanly (e.g. Google's 5-min limit);
                    # back off a moment before reconnecting to avoid a tight spin loop
                    if not got_result:
                        logger.warning(f"STT stream for {session_id} ended with no results – backing off")
                        await asyncio.sleep(1.0)
                    else:
                        await asyncio.sleep(0.1)

        except asyncio.CancelledError:
            pass
        except Exception as e:
            logger.error(f"Pipeline fatal error for {session_id}: {e}", exc_info=True)
