from call_handler import (
    start_call,
    end_call,
    save_user_message,
    save_agent_message,
    get_recent_context_text,
    get_full_transcript_text,
    build_prompt_for_ai,
    get_call_info,
)


def fake_ai_reply(user_text: str) -> str:
    """
    Temporary fake reply so you can test memory first
    without adding an LLM yet.
    """
    return f"I heard you say: {user_text}"


def show_call_info(call_id: str) -> None:
    """Display call metadata and stats."""
    info = get_call_info(call_id)
    print(f"\n--- CALL INFO: {call_id} ---")
    for key, value in info.items():
        print(f"{key}: {value}")
    print()


def main():
    """Interactive multi-call demo."""
    current_call_id = "CALL_001"
    calls = {}  # Track active calls

    print("=" * 60)
    print("Redis Multi-Call Memory Demo")
    print("=" * 60)
    print("\nCommands:")
    print("  new <call_id> [phone] [name] - Start a new call")
    print("  switch <call_id>              - Switch to a different call")
    print("  active                        - Show active calls")
    print("  recent                        - Show recent context")
    print("  full                          - Show full transcript")
    print("  info                          - Show call metadata")
    print("  prompt                        - Show AI prompt")
    print("  end                           - End current call")
    print("  exit                          - Quit\n")

    # Start with a default call
    start_call(current_call_id)
    calls[current_call_id] = True
    print(f"Started {current_call_id}\n")

    while True:
        prompt_text = f"[{current_call_id}] Caller: "
        user_input = input(prompt_text).strip()

        if not user_input:
            continue

        # Parse commands
        parts = user_input.split(maxsplit=3)
        command = parts[0].lower()

        if command == "exit":
            print("Ending all calls. Goodbye!")
            break

        if command == "new":
            if len(parts) < 2:
                print("Usage: new <call_id> [phone] [name]")
                continue
            new_call_id = parts[1]
            phone = parts[2] if len(parts) > 2 else None
            name = parts[3] if len(parts) > 3 else None
            start_call(new_call_id, phone_number=phone, caller_name=name)
            calls[new_call_id] = True
            current_call_id = new_call_id
            print(f"Started new call: {current_call_id}\n")
            continue

        if command == "switch":
            if len(parts) < 2:
                print("Usage: switch <call_id>")
                continue
            call_id = parts[1]
            if call_id in calls:
                current_call_id = call_id
                print(f"Switched to {current_call_id}\n")
            else:
                print(f"Call {call_id} not found. Active calls: {list(calls.keys())}\n")
            continue

        if command == "active":
            print(f"\nActive calls: {list(calls.keys())}\n")
            continue

        if command == "recent":
            print("\n--- RECENT CONTEXT ---")
            print(get_recent_context_text(current_call_id))
            print()
            continue

        if command == "full":
            print("\n--- FULL TRANSCRIPT ---")
            print(get_full_transcript_text(current_call_id))
            print()
            continue

        if command == "info":
            show_call_info(current_call_id)
            continue

        if command == "prompt":
            prompt = build_prompt_for_ai(current_call_id, latest_user_input="Please continue helping.")
            print("\n--- PROMPT FOR AI ---")
            print(prompt)
            print()
            continue

        if command == "end":
            end_call(current_call_id)
            print(f"Ended call {current_call_id}\n")
            continue

        # Regular message - save and reply
        save_user_message(current_call_id, user_input)
        agent_reply = fake_ai_reply(user_input)
        save_agent_message(current_call_id, agent_reply)
        print(f"Agent: {agent_reply}\n")


if __name__ == "__main__":
    main()

