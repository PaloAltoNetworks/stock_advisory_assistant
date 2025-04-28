from autogen_agentchat.agents import AssistantAgent, BaseChatAgent
from autogen_agentchat.messages import ChatMessage
from autogen_core import CancellationToken
from autogen_agentchat.teams import Swarm
from autogen_agentchat.conditions import MaxMessageTermination, TextMessageTermination
from autogen_core.model_context import BufferedChatCompletionContext, UnboundedChatCompletionContext
from autogen_ext.tools.code_execution import PythonCodeExecutionTool
from tools.scrape_website_tool import scrape_website
from tools.serper_dev_tool import google_search
from tools.stock_tool import StockPorfolioTools
from autogen_core.models import LLMMessage
from typing import List, Sequence
import utils
from autogen_ext.code_executors.docker._docker_code_executor import DockerCommandLineCodeExecutor
from my_model_clients import get_openai_client, get_azure_gpt4o_client, get_anthropic_client, get_bedrock_client, get_gemini_client
import copy


class StockAdvisory:
    def __init__(self, db_path: str, docker_base: str = None, user_id: int = 1):       
        self.db_path = db_path 
        self.user_id = user_id
        self.prompts = utils.load_prompts('prompts.yaml')
        self.model_client = get_openai_client(parallel_tool_calls=True)
        self.docker_base = docker_base
        self.docker_executor = self.init_docker_executor()
        self.team = None
        self.participants = []

    def set_user_id(self, user_id: int):
        self.user_id = user_id

    def init_docker_executor(self):
        return DockerCommandLineCodeExecutor(
            image="python:3.12-slim",
            container_name="autogen_python_executor",
            timeout=1200,
            work_dir='./container_data',
            base_url=self.docker_base,
        )
    
    async def start_executor_container(self):
        return await self.docker_executor.start()
    
    async def stop_executor_container(self):
        return await self.docker_executor.stop()
        

    def create_team(self) -> Swarm:
        from autogen_agentchat.base._handoff import Handoff
        """Creates a research team with orchestrator, news, and portfolio agents."""
        orchestrator_agent_name = 'orchestrator_agent'
        news_agent_name = 'news_agent'
        portfolio_agent_name = 'portfolio_agent'
        
        orchestrator_agent = AssistantAgent(
            name=orchestrator_agent_name,
            description=self.prompts[orchestrator_agent_name]['descriptions'],
            model_client=get_openai_client(parallel_tool_calls=False),  # Disable paraellel tool calls to avoid transfering to multple multiple sub-agents at once.
            system_message=self.prompts[orchestrator_agent_name]['instructions'],
            handoffs=[
                Handoff(target=news_agent_name, description=self.prompts[news_agent_name]['descriptions']),
                Handoff(target=portfolio_agent_name, description=self.prompts[portfolio_agent_name]['descriptions'])
            ]
        )

        news_agent = AssistantAgent(
            name=news_agent_name,
            description=self.prompts[news_agent_name]['descriptions'],
            model_client=self.model_client,
            tools=[scrape_website, google_search],
            system_message=self.prompts[news_agent_name]['instructions'],
            handoffs=[
                Handoff(target=orchestrator_agent_name, description=self.prompts[orchestrator_agent_name]['descriptions'])
            ]
        )          
        
        stock = StockPorfolioTools(db_path=self.db_path, user_id=self.user_id)        
        code_tool = PythonCodeExecutionTool(executor=self.docker_executor)
        portfolio_agent = AssistantAgent(
            name=portfolio_agent_name,
            description=self.prompts[portfolio_agent_name]['descriptions'],
            model_client=self.model_client,
            tools=[code_tool, stock.view_portfolio, stock.view_transactions, stock.view_transaction_by_id, stock.buy_stock, stock.sell_stock, stock.fetch_stock_history],
            system_message=self.prompts[portfolio_agent_name]['instructions'],
            handoffs=[
                Handoff(target=orchestrator_agent_name, description=self.prompts[orchestrator_agent_name]['descriptions'])
            ]
        )        

        termination = TextMessageTermination(source=orchestrator_agent_name) | MaxMessageTermination(max_messages=30)

        team = Swarm(
            participants=[orchestrator_agent, portfolio_agent, news_agent],
            termination_condition=termination
        )
        self.participants = [orchestrator_agent, news_agent, portfolio_agent]
        self.team = team
        return team
    
    async def run(self, input: ChatMessage | str | Sequence[ChatMessage]):
        return await self.team.run(task = input)
    
    def set_context(self, message_history: List[LLMMessage]):
        ''' Keep only the user input and agent ouput in the context. All the intermediate messages and function ouputs are removed. '''
        # Must use deep copy to avoid modifying the original message history. Each agent must have its own copy of the message history.
        for participant in self.participants:
            participant._model_context = UnboundedChatCompletionContext(initial_messages=copy.deepcopy(message_history))
        
    
    async def reset_all(self):
        for participant in self.participants:
            await participant.on_reset(CancellationToken())
        await self.team.reset()

