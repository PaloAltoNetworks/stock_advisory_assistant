#!/usr/bin/env python
import sys
import os
import warnings
import readline  # For better input handling
from dotenv import load_dotenv
from colorama import Fore, Style  # For colored output
from collections import deque
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from stock_advisor.crew import StockAdvisor

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../DB'))
from user_manager import UserManager

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")
warnings.filterwarnings("ignore", module="pydantic")
warnings.filterwarnings("ignore", module="crewai_tools")

# Enable basic readline features
readline.parse_and_bind("set editing-mode emacs")  # Use emacs-style keybindings
readline.set_auto_history(False)  # Automatically save input history

# Configurations
login_required = True   # Set to False to disable login requirement. Default user_id is 1
my_docker_base = None   # set the path if running docker on non-default socket. For example, when using OrbStack, the path is usually unix://Users/jaychen/.orbstack/run/docker.sock
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../DB/stock_advisor.db'))
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../.env'))

current_year = datetime.now().year

def load_env(self):
    """Load environment variables from a .env file."""
    if load_dotenv(env_path):
        print("Loaded .env file")
    else:
        print("Failed to load .env file")
        exit(1)

def config_short_memory(max_size=10):
    global short_term_memory
    short_term_memory = deque(maxlen=max_size)
    

def chat_with_agent(user_input: str, user_id: int) -> str:
    # Retreive short-term memories
    memories_str = "\n".join(f"{entry['role'].upper()}: {entry['content']}\n" for entry in short_term_memory)

    # Generate Assistant response    
    inputs = {
        "user_message": f"{user_input}",
        "context": f"{memories_str}",
        "current_year": current_year
    }
    try:
        assistant_response = StockAdvisor(docker_base=my_docker_base, user_id = user_id, db_path=db_path).crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

    # Add new memories from the conversation
    messages = [
        {"role": "user", "content": user_input},
        {"role": "assistant", "content": assistant_response.raw}
    ]
    short_term_memory.extend(messages)
    
    return assistant_response.raw


def run(user_id: int = 1):
    """
    Run the crew.
    """
    print(Fore.CYAN + "Welcome to the Stock Advisory Assistant Powered by CrewAI! Type 'exit' to quit." + Style.RESET_ALL)
    while True:
        try:
            # Clear input buffer
            sys.stdin.flush()
            user_input = input(Fore.GREEN + "You: " + Style.RESET_ALL)
            if user_input.lower() == "exit":
                print(Fore.YELLOW + "Goodbye!" + Style.RESET_ALL)
                break
            response = chat_with_agent(user_input, user_id)
            print(Fore.LIGHTBLUE_EX + f"Assistant: {response}" + Style.RESET_ALL)
        except KeyboardInterrupt:
            print(Fore.YELLOW + "\nGoodbye!" + Style.RESET_ALL)
            break

def user_login():
    user_manager = UserManager(db_path=db_path)
    user_id = user_manager.cli_login()
    return user_id

if __name__ == "__main__":
    config_short_memory()
    if login_required:    
        user_id = user_login()
        if user_id:
            run(user_id)
    else:
        run()