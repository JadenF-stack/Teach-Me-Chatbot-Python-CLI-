import json
from pathlib import Path

# This is the file where the chatbot will store its "memory"
# (questions and answers) so it can remember them next time.
MEMORY_FILE = Path("memory.json")


def load_memory() -> dict:
    """Load saved Q->A pairs from disk."""
    if MEMORY_FILE.exists():
        try:
            return json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            # If the JSON file is broken/corrupted, start with empty memory
            # (prevents the program crashing for the user)
            return {}
        # If the file doesn't exist yet, start with empty memory
    return {}


def save_memory(memory: dict) -> None:
    """ Save Q -> A pairs to disk.

    Args:
        memory: dictionary of question/answer pairs to save"""
    MEMORY_FILE.write_text(
        json.dumps(memory, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def normalize(text: str) -> str:
    """Make matching easier (ignore case + extra spaces)."""
    return " ".join(text.strip().lower().split())


def main():
    # Load saved memory at the start of the program
    memory = load_memory()

    # Basic instructions for the user
    print("Teach-Me Chatbot")
    print("- Type a question.")
    print("- If I don't know it, teach me the answer and I'll remember.")
    print("- Commands: /list, /forget, /clear, /quit")
    print()

    while True:
        # Get a question/command from the user
        question_raw = input("You: ").strip()
        # If user just presses enter, restart the loop
        if not question_raw:
            continue

        # Commands
        cmd = question_raw.lower()
        
        # Quit the chatbot
        if cmd == "/quit":
            print("Bot: Bye!")
            break

        # List all stored questions
        if cmd == "/list":
            if not memory:
                print("Bot: I haven't learned anything yet.")
            else:
                print("Bot: I know these questions:")
                for q in sorted(memory.keys()):
                    print(f" - {q}")
            continue
        # Forget one specific question
        if cmd == "/forget":
            q = input("Bot: Which question should I forget? ").strip()
            key = normalize(q)

            if key in memory:
                # Remove it from the dictionary
                del memory[key]
                # Save the updated memory to disk
                save_memory(memory)
                print("Bot: Forgot it.")
            else:
                print("Bot: I don't have that stored.")
            continue
             
        # Clear all memory
        if cmd == "/clear":
            confirm = input("Bot: Clear ALL memory? type YES to confirm: ").strip()
            if confirm == "YES":
                # Reset memory to an empty dictionary
                memory = {}
                save_memory(memory)
                print("Bot: Memory cleared.")
            else:
                print("Bot: Cancelled.")
            continue

        # Normalise the question so matching is consistent
        key = normalize(question_raw)
        # If we already know the answer, reply with it
        if key in memory:
            print(f"Bot: {memory[key]}")
        else:
            print("Bot: I don't know that yet. Teach me the answer.")
            answer = input("You (answer): ").strip()
            
            # Don't store empty answers (keeps data cleaner)
            if not answer:
                print("Bot: Ok, I won't store an empty answer.")
                continue
            
            # Save the new question and answer
            memory[key] = answer
            save_memory(memory)
            print("Bot: Got it. I'll remember that next time.")


if __name__ == "__main__":
    main()
