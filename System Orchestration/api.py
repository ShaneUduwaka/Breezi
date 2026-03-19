# api.py
"""
FastAPI server for Breezi System Orchestration
Handles REST API endpoints and WebSocket connections for real-time audio
"""

import asyncio
import logging
from fastapi import FastAPI, WebSocket, HTTPException, status
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from system.bootsrap import build_system


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Global system instance
system = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for FastAPI startup/shutdown"""
    
    # Startup
    logger.info("🚀 Starting Breezi API server...")
    global system
    system = build_system(use_phase1=True)
    logger.info("✅ System initialized")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down Breezi API server...")
    # Add cleanup code here if needed
    logger.info("✅ Shutdown complete")


# Create FastAPI app
app = FastAPI(
    title="Breezi AI Call Agent",
    description="Real-time conversational AI system for fast-food ordering",
    version="1.0.0",
    lifespan=lifespan
)


# ==================== REST API ENDPOINTS ====================

@app.get("/health")
async def health_check():
    """
    Health check endpoint
    Returns system status
    """
    if system is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="System not initialized"
        )
    
    return {
        "status": "healthy",
        "service": "breezi-orchestration",
        "components": {
            "audio_gateway": "ready" if "audio_gateway" in system else "not_available",
            "call_ingestor": "ready" if "call_ingestor" in system else "not_available",
            "stt_client": "ready" if "stt_client" in system else "not_available",
            "tts_client": "ready" if "tts_client" in system else "not_available",
            "nlu": "ready",
            "conversation": "ready",
        }
    }


@app.get("/config")
async def get_config():
    """
    Get system configuration
    Returns business data and configuration
    """
    if system is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="System not initialized"
        )
    
    config = system.get("business_config", {})
    return {
        "business_name": config.get("business_config", {}).get("name"),
        "business_type": config.get("business_config", {}).get("type"),
        "intents_count": len(config.get("intents", {})),
        "nlu_config": config.get("nlu_config", {}),
    }


@app.post("/text-message")
async def handle_text_message(message: dict):
    """
    Handle text message from user
    
    Request body:
    {
        "text": "I want to order pizza",
        "session_id": "user_123"
    }
    """
    if system is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="System not initialized"
        )
    
    try:
        text = message.get("text", "").strip()
        session_id = message.get("session_id", "default")
        
        if not text:
            raise ValueError("Message text is required")
        
        # Process through conversation manager
        conversation = system["conversation"]
        response = conversation.handle_message(text, session_id=session_id)
        
        # Get current state
        state_dict = {}
        if conversation.state:
            state_dict = {
                "intent": conversation.state.intent,
                "slots": conversation.state.slots,
                "missing_slots": conversation.state.missing_slots(),
            }
        
        return {
            "success": True,
            "session_id": session_id,
            "response": response,
            "state": state_dict,
        }
    
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@app.get("/session/{session_id}")
async def get_session_state(session_id: str):
    """
    Get current conversation state for a session
    """
    if system is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="System not initialized"
        )
    
    try:
        conversation = system["conversation"]
        
        # This is a simplified version - in production, retrieve from Redis
        if conversation.state and hasattr(conversation.state, 'to_dict'):
            state = conversation.state.to_dict()
        else:
            state = {}
        
        return {
            "session_id": session_id,
            "state": state,
        }
    
    except Exception as e:
        logger.error(f"Error retrieving session: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# ==================== WEBSOCKET ENDPOINTS ====================

@app.websocket("/ws/audio/{session_id}")
async def websocket_audio_endpoint(websocket: WebSocket, session_id: str):
    """
    WebSocket endpoint for real-time audio streaming
    Handles bidirectional audio between caller and system
    
    Protocol:
    - Client sends: {"type": "audio", "data": base64_audio}
    - Server sends: {"type": "response", "text": "...", "audio": base64_audio}
    """
    
    if system is None:
        await websocket.close(code=status.WS_1011_SERVER_ERROR)
        return
    
    await websocket.accept()
    logger.info(f"📞 WebSocket connected: {session_id}")
    
    try:
        # Create audio session
        audio_gateway = system.get("audio_gateway")
        if audio_gateway:
            audio_session = await audio_gateway.create_session(session_id)
            logger.info(f"✅ Audio session created: {session_id}")
        
        # Process messages
        while True:
            # Receive message from client
            data = await websocket.receive_json()
            
            if data.get("type") == "audio":
                # Handle audio data
                audio_data = data.get("data", "")
                logger.debug(f"📥 Received audio chunk for {session_id}: {len(audio_data)} bytes")
                
                # Process through audio gateway
                if audio_gateway:
                    await audio_gateway.handle_incoming_audio(session_id, audio_data)
                
                # TODO: In Phase 2
                # - Stream to STT service
                # - Get transcription
                # - Pass to conversation
                # - Generate response via TTS
                # - Send back via WebSocket
                
                # Send acknowledgment
                await websocket.send_json({
                    "type": "ack",
                    "status": "received",
                    "session_id": session_id,
                })
            
            elif data.get("type") == "text":
                # Handle text input (for debugging)
                text = data.get("text", "")
                logger.info(f"💬 Text message from {session_id}: {text}")
                
                conversation = system["conversation"]
                response = conversation.handle_message(text, session_id=session_id)
                
                await websocket.send_json({
                    "type": "response",
                    "text": response,
                    "session_id": session_id,
                })
            
            elif data.get("type") == "end":
                logger.info(f"📞 Client requested end of session: {session_id}")
                break
    
    except Exception as e:
        logger.error(f"❌ WebSocket error for {session_id}: {e}")
    
    finally:
        # Cleanup
        if audio_gateway:
            await audio_gateway.close_session(session_id)
        
        logger.info(f"📞 WebSocket disconnected: {session_id}")


@app.websocket("/ws/call/{session_id}")
async def websocket_call_endpoint(websocket: WebSocket, session_id: str):
    """
    WebSocket endpoint for incoming calls
    Simplified version for testing real-time conversation
    
    Connect and start sending:
    {"type": "text", "message": "I want to order pizza"}
    """
    
    if system is None:
        await websocket.close(code=status.WS_1011_SERVER_ERROR)
        return
    
    await websocket.accept()
    logger.info(f"📞 Call connected: {session_id}")
    
    try:
        conversation = system["conversation"]
        
        # Initial greeting
        await websocket.send_json({
            "type": "greeting",
            "message": "👋 Welcome to Breezi! How can I help you today?",
            "session_id": session_id,
        })
        
        # Process messages
        while True:
            data = await websocket.receive_json()
            
            if data.get("type") == "text":
                user_message = data.get("message", "").strip()
                
                if not user_message:
                    await websocket.send_json({
                        "type": "error",
                        "message": "Please provide a message",
                    })
                    continue
                
                logger.info(f"💬 {session_id}: {user_message}")
                
                # Process through conversation
                response = conversation.handle_message(user_message, session_id=session_id)
                
                # Get state
                state = {}
                if conversation.state:
                    state = {
                        "intent": conversation.state.intent,
                        "slots": conversation.state.slots,
                        "missing_slots": conversation.state.missing_slots(),
                    }
                
                # Send response
                await websocket.send_json({
                    "type": "response",
                    "message": response,
                    "state": state,
                    "session_id": session_id,
                })
            
            elif data.get("type") == "end":
                logger.info(f"📞 {session_id}: Call ended")
                break
    
    except Exception as e:
        logger.error(f"❌ Call error for {session_id}: {e}")
        try:
            await websocket.send_json({
                "type": "error",
                "message": f"Server error: {str(e)}",
            })
        except:
            pass
    
    finally:
        logger.info(f"📞 Call disconnected: {session_id}")


# ==================== ERROR HANDLERS ====================

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )


if __name__ == "__main__":
    import uvicorn
    
    # Run server
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
