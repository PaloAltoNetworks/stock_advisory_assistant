import sys
import os
import readline
import asyncio
import utils
from colorama import Fore, Style
from stock_advisory import StockAdvisory
from autogen_core.models import UserMessage, AssistantMessage, LLMMessage
from typing import List

sys.path.append(os.path.join(os.path.dirname(__file__), '../DB'))
from user_manager import UserManager

# Enable basic readline features
readline.parse_and_bind("set editing-mode emacs")
readline.set_auto_history(False)

login_required = True   # Set to False to disable login requirement
utils.load_env('../.env')
my_docker_base = 'unix://Users/jaychen/.orbstack/run/docker.sock'   # set the path if running docker on non-default socket. For example, when using OrbStack
db_path = '../DB/stock_advisor.db'
message_history: List[LLMMessage] = []  
advisory = StockAdvisory(db_path, docker_base=my_docker_base)


async def chat_with_agent(user_input: str) -> str:
    advisory.set_context(message_history) 
    response = await advisory.run(user_input)
    agent_response = response.messages[-1].content

    message_history.append(UserMessage(content=user_input, source="user"))
    message_history.append(AssistantMessage(content=agent_response, source="orchestrator_agent"))
    await advisory.reset_all()
    return agent_response

async def main() -> None:
    await advisory.start_executor_container()
    advisory.create_team()
    print(Fore.YELLOW + "Start chatting with the Stock Advisor Agent. \nType exit or use ctrl+c to terminate the chat.\n" + Style.RESET_ALL)
    while True:
        try:
            sys.stdin.flush()
            user_input = input(Fore.GREEN + "You: " + Style.RESET_ALL)
            if user_input.lower() == "exit":
                print(Fore.YELLOW + "Goodbye!" + Style.RESET_ALL)
                break
            response = await chat_with_agent(user_input)
            print(Fore.LIGHTBLUE_EX + f"Assistant: {response}" + Style.RESET_ALL)

        except KeyboardInterrupt:
            print(Fore.YELLOW + "\nGoodbye!" + Style.RESET_ALL)
            break
        except Exception as e:
            print(Fore.RED + f"An error occurred: {e}" + Style.RESET_ALL)
            break
    await advisory.stop_executor_container()

def user_login():
    user_manager = UserManager(db_path=db_path)
    user_id = user_manager.cli_login()
    return user_id

if __name__ == "__main__":
    if login_required:    
        user_id = user_login()
        if user_id:
            advisory.set_user_id(user_id)
            asyncio.run(main())
    else:
        # default user_id is 1
        asyncio.run(main())
    