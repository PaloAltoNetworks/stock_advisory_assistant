from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from tools.stock_tool import ViewPortfolioTool, ViewTransactionsTool, ViewTransactionByIdTool, BuyStockTool, SellStockTool, FetchStockHistoryTool
from crewai_tools import CodeInterpreterTool, SerperDevTool, ScrapeWebsiteTool, FileReadTool
from llm_manager import LLMManager
import os
import platform
# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class StockAdvisor():
	"""Stock Advisory crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'
	llm_manager = LLMManager()
	llm = llm_manager.get_openai_gpt4o()

	def __init__(self, docker_base: str = None, user_id: int = 1, db_path: str = None):
		"""Initialize the crew"""
		self.user_id = user_id
		self.my_docker_base = docker_base
		self.db_path = db_path

	@agent
	def orchestrator(self) -> Agent:
		return Agent(
			config=self.agents_config['orchestrator'],
			llm=self.llm,
			verbose=False
		)

	@agent
	def news_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['news_agent'],			
			llm=self.llm,
			tools=[
				SerperDevTool(),
				ScrapeWebsiteTool(),
				FileReadTool()
			],
			verbose=False
		)

	@agent
	def portfolio_agent(self) -> Agent:
		view_portfolio = ViewPortfolioTool(db_path=self.db_path, user_id=self.user_id)
		view_transactions = ViewTransactionsTool(db_path=self.db_path, user_id=self.user_id)
		view_transaction_by_id = ViewTransactionByIdTool(db_path=self.db_path)
		buy_stock = BuyStockTool(db_path=self.db_path, user_id=self.user_id)
		sell_stock = SellStockTool(db_path=self.db_path, user_id=self.user_id)
		fetch_stock_history = FetchStockHistoryTool()
		code_interpreter = CodeInterpreterTool(
			user_docker_base_url=self.my_docker_base,
			user_dockerfile_path='./'
		)
		
		return Agent(
			config=self.agents_config['portfolio_agent'],			
			llm=self.llm,
			tools=[view_portfolio, view_transactions, view_transaction_by_id, buy_stock, sell_stock, fetch_stock_history, code_interpreter],
			verbose=False
		)
	
	@task
	def orchestrator_task(self) -> Task:
		return Task(
			config=self.tasks_config['orchestrator_task']
		)
	
	
	@crew
	def crew(self) -> Crew:
		"""Creates the StockAdvisor crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential, 
			verbose=False
		)
