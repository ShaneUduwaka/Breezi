import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from system.bootsrap import build_system
from dialog.call_state_machine import CallStateMachine, CallState

def test_full_call_lifecycle():
    print("Building system...")
    system = build_system(use_phase1=False)
    conversation = system["conversation"]
    
    session_id = "test-session-123"
    sm = CallStateMachine(session_id)
    
    print("\n--- TEST: Proactive Greeting ---")
    assert sm.state == CallState.GREETING
    greeting = sm.get_proactive_greeting()
    assert greeting == CallStateMachine.GREETING_MSG
    assert sm.state == CallState.ACTIVE
    print("PASS: Proactive greeting is fetched, state -> ACTIVE")
    
    print("\n--- TEST: Active Phase - Intent with Missing Slots ---")
    # Initiate an order, which has missing slots
    response, end_call = sm.handle("I want to place an order", conversation)
    assert not end_call
    assert sm.state == CallState.ACTIVE
    print("PASS: Handled start_order intent, state -> ACTIVE (waiting for slots)")
    
    print("\n--- TEST: Active Phase - Complete Slots -> Transition to Wrapup ---")
    # Fulfill slots
    response, end_call = sm.handle("pickup, downtown, one burger", conversation)
    assert sm.state == CallState.WRAPUP
    assert CallStateMachine.WRAPUP_MSG in response
    assert not end_call
    print("PASS: Slots fulfilled, state -> WRAPUP")
    
    print("\n--- TEST: Wrapup Phase - Say Yes -> Transition to Active ---")
    # Tell bot we want something else
    response, end_call = sm.handle("yes", conversation)
    assert sm.state == CallState.ACTIVE
    assert not end_call
    assert conversation.state is None  # Should be reset!
    print("PASS: Answered yes to wrapup, state -> ACTIVE, conversation state wiped")
    
    print("\n--- TEST: Active Phase 2 - Simple Intent -> Immediate Wrapup ---")
    # Ask a simple intent (view_hours)
    response, end_call = sm.handle("what are your hours", conversation)
    assert sm.state == CallState.WRAPUP
    assert CallStateMachine.WRAPUP_MSG in response
    assert not end_call
    print("PASS: Answered simple question, state -> WRAPUP")
    
    print("\n--- TEST: Wrapup Phase 2 - Say No -> Transition to Ended ---")
    # Tell bot we are done
    response, end_call = sm.handle("no that's all", conversation)
    assert sm.state == CallState.ENDED
    assert response == CallStateMachine.GOODBYE_MSG
    assert end_call
    print("PASS: Answered no to wrapup, state -> ENDED")
    
    print("\nALL TESTS PASSED!")

if __name__ == "__main__":
    test_full_call_lifecycle()
