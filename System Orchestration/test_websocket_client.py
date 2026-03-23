# test_websocket_client.py
"""
WebSocket client for testing real-time conversations
Connects to the FastAPI WebSocket endpoint and sends messages
"""

import asyncio
import websockets
import json
import sys
from datetime import datetime


async def run_call_websocket(uri: str, session_id: str):
    """
    Test real-time conversation via WebSocket
    
    Args:
        uri: WebSocket URI (e.g., ws://localhost:8000/ws/call/test-session)
        session_id: Session identifier
    """
    
    print(f"\n{'='*70}")
    print(f"🎤 Breezi WebSocket Call Test")
    print(f"{'='*70}")
    print(f"📍 Connecting to: {uri}")
    print(f"🆔 Session ID: {session_id}")
    print(f"💡 Type 'exit' or 'quit' to end the call")
    print(f"{'='*70}\n")
    
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ Connected to server\n")
            
            # Receive initial greeting
            message = await websocket.recv()
            data = json.loads(message)
            if data.get("type") == "greeting":
                print(f"🤖 {data.get('message')}\n")
            
            turn_count = 0
            
            # Conversation loop
            while True:
                # Get user input
                user_input = input("👤 You: ").strip()
                
                if not user_input:
                    print("⚠️  Please enter something...\n")
                    continue
                
                if user_input.lower() in ["exit", "quit"]:
                    print("\n👋 Ending call...")
                    await websocket.send(json.dumps({"type": "end"}))
                    break
                
                turn_count += 1
                
                # Send message
                await websocket.send(json.dumps({
                    "type": "text",
                    "message": user_input,
                }))
                
                # Receive response
                response_msg = await websocket.recv()
                response_data = json.loads(response_msg)
                
                # Display response
                if response_data.get("type") == "response":
                    print(f"\n🤖 Breezi: {response_data.get('message')}\n")
                    
                    # Display state if available
                    state = response_data.get("state", {})
                    if state:
                        print(f"📊 State Update:")
                        print(f"   Intent: {state.get('intent')}")
                        print(f"   Slots: {state.get('slots')}")
                        if state.get('missing_slots'):
                            print(f"   ⏳ Still waiting for: {', '.join(state.get('missing_slots'))}")
                        print()
                
                elif response_data.get("type") == "error":
                    print(f"\n❌ Error: {response_data.get('message')}\n")
            
            print(f"\n✅ Call ended. Total turns: {turn_count}")
    
    except ConnectionRefusedError:
        print(f"❌ Connection refused. Make sure server is running at {uri}")
        print("\n💡 Start server with: docker-compose -f docker-compose.mock.yml up -d")
        sys.exit(1)
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


async def run_audio_websocket(uri: str, session_id: str):
    """
    Test audio streaming via WebSocket
    
    Args:
        uri: WebSocket URI for audio
        session_id: Session identifier
    """
    
    print(f"\n{'='*70}")
    print(f"🎵 Breezi WebSocket Audio Test")
    print(f"{'='*70}")
    print(f"📍 Connecting to: {uri}")
    print(f"🆔 Session ID: {session_id}")
    print(f"{'='*70}\n")
    
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ Connected to audio stream\n")
            
            # Send some test audio (placeholder)
            test_audio = b"test_audio_data"
            
            await websocket.send(json.dumps({
                "type": "audio",
                "data": test_audio.decode('latin-1'),
            }))
            
            print("📤 Sent test audio chunk\n")
            
            # Receive acknowledgment
            response = await websocket.recv()
            data = json.loads(response)
            print(f"📥 Server response: {data}\n")
            
            print("✅ Audio endpoint test complete")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


async def main():
    """Main entry point"""
    
    if len(sys.argv) > 1:
        test_type = sys.argv[1].lower()
    else:
        test_type = "call"
    
    session_id = f"test-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    
    if test_type == "audio":
        uri = f"ws://localhost:8000/ws/audio/{session_id}"
        await run_audio_websocket(uri, session_id)
    else:
        uri = f"ws://localhost:8000/ws/call/{session_id}"
        await run_call_websocket(uri, session_id)


if __name__ == "__main__":
    asyncio.run(main())
