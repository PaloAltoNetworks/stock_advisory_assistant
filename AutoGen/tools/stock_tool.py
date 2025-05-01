import sys 
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../DB'))
from stock_manager import StockManager
from query_stock import fetch_historical_stock_past_days

class StockPorfolioTools():

    def __init__(self, db_path:str, user_id:int):
        self.user_id = user_id
        self.db_path = db_path
        
    def view_portfolio(self):
        '''Retrieve and list the current stock holdsings of the user.'''
        with StockManager(self.db_path) as stock_manager:
            return stock_manager.view_portfolio(self.user_id)
        
 
    def view_transactions(self, days:str):
        '''Retrieve the transactions history of the user in the past N days.'''
        with StockManager(self.db_path) as stock_manager:
            return stock_manager.view_transactions(self.user_id, days)
    
    def view_transaction_by_id(self, transaction_id:str):
        '''Retrieve the transaction details by transaction ID.'''
        with StockManager(self.db_path) as stock_manager:
            return stock_manager.get_transaction(transaction_id)
        
    def buy_stock(self, stock_symbol:str, shares:int):
        '''Buy a certain shares of a stock.'''
        with StockManager(self.db_path) as stock_manager:
            return stock_manager.buy_stock(self.user_id, stock_symbol, shares)
    
    def sell_stock(self, stock_symbol:str, shares:int):
        '''Sell a certain shares of a stock.'''
        with StockManager(self.db_path) as stock_manager:
            return stock_manager.sell_stock(self.user_id, stock_symbol, shares)
        
    def fetch_stock_history(self, stock_symbol:str, days:int):
        '''Get the historical stock data for a list of stock symbols in the past N days.'''
        return fetch_historical_stock_past_days(stock_symbol, days)

