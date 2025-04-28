from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
import os
import sys

# sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../..'))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../../DB')))
from stock_manager import StockManager
from query_stock import fetch_historical_stock_past_days

class ViewTransactionsInput(BaseModel):
    """Input schema for ViewTransactionsTool"""
    days: str = Field(..., description="The number of in the past days to view the transactions for.")

class GetTransactionByIdInput(BaseModel):
    """Input schema for ViewTransactionsTool"""
    tran_id: int = Field(..., description="The transaction ID of the transaction to retrieve.")

class BuySellStockInput(BaseModel):
    """Input schema for ViewTransactionsTool"""    
    stock_symbol: str = Field(..., description="The symbol of the stock to sell or buy.")
    shares: int = Field(..., description="The number of stock shares to sell or buy.")

class FetchHistoricalStockInput(BaseModel):
    symbol_list: List[str] = Field(..., description="List of stock symbols to fetch data for.")
    days: int = Field(..., description="Number of days to fetch data for from today.")




class ViewPortfolioTool(BaseTool):
    name: str = "View Portfolio Tool"
    description: str = (
        "Retrieve and list the current stock holdsings of the user."
    )    
    db_path: str = Field(..., description="Path to the database file.")
    user_id: int = Field(..., description="User ID of the user.")       

    def _run(self) -> Dict:
        # Implementation goes here   
        stock_manager = StockManager(self.db_path) 
        return stock_manager.view_portfolio(self.user_id)
    
class ViewTransactionsTool(BaseTool):
    name: str = "View Transactions Tool"
    description: str = (
        "Retrieve the transactions history of the user in the past N days."
    )    
    db_path: str = Field(..., description="Path to the database file.")
    user_id: int = Field(..., description="User ID of the user.")   
    args_schema: Type[BaseModel] = ViewTransactionsInput    

    def _run(self, days:str) -> List[Dict]:
        # Implementation goes here   
        stock_manager = StockManager(self.db_path) 
        return stock_manager.view_transactions(self.user_id, days)
    
class ViewTransactionByIdTool(BaseTool):
    name: str = "Get TransactionByID Tool"
    description: str = (
        "Retrieve the specific transaction by the transaction ID."
    )    
    db_path: str = Field(..., description="Path to the database file.")
    args_schema: Type[BaseModel] = GetTransactionByIdInput    

    def _run(self, tran_id:int) -> List[Dict]:
        # Implementation goes here   
        stock_manager = StockManager(self.db_path) 
        return stock_manager.get_transaction(tran_id)
    

class BuyStockTool(BaseTool):
    name: str = "Buy Stock Tool"
    description: str = (
        "Buy a certain shares of a stock."
    )
    db_path: str = Field(..., description="Path to the database file.")
    user_id: int = Field(..., description="User ID of the user.")  
    args_schema: Type[BaseModel] = BuySellStockInput    

    def _run(self, stock_symbol:str, shares:int) -> str:
        # Implementation goes here   
        stock_manager = StockManager(self.db_path) 
        return stock_manager.buy_stock(self.user_id, stock_symbol, shares)
    
class SellStockTool(BaseTool):
    name: str = "Sell Stock Tool"
    description: str = (
        "Sell a certain shares of a stock."
    )
    db_path: str = Field(..., description="Path to the database file.")
    user_id: int = Field(..., description="User ID of the user.")  
    args_schema: Type[BaseModel] = BuySellStockInput    

    def _run(self, stock_symbol:str, shares:int) -> str:
        # Implementation goes here   
        stock_manager = StockManager(self.db_path) 
        return stock_manager.sell_stock(self.user_id, stock_symbol, shares)
    
class FetchStockHistoryTool(BaseTool):
    name: str = "Get Stock History Tool"
    description: str = (
        "Get the historical stock data for a list of stock symbols in the past N days."
    )    
    args_schema: Type[BaseModel] = FetchHistoricalStockInput    

    def _run(self, symbol_list:List[str], days:int) -> List[Dict]:
        # Implementation goes here   
        return fetch_historical_stock_past_days(symbol_list, days)

if __name__ == "__main__":
    # Test the tools
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../../', 'DB/stock_advisor.db'))
    print("DB Path:", db_path)
    user_id = 2
    view_portfolio_tool = ViewPortfolioTool(db_path=db_path, user_id=user_id)
    print(view_portfolio_tool.run())
    
    fetch_history = FetchStockHistoryTool()
    print(fetch_history.run(symbol_list=['AAPL', 'GOOGL'], days=14))

 