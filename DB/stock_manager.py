import sqlite3
from datetime import datetime, timedelta

class StockManager:

    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = self.connect_db()

    def connect_db(self):
        return sqlite3.connect(self.db_path)
    
    def close_db(self):
        if self.conn is not None:
            self.conn.close()

    def __enter__(self):
        if self.conn is None or not self.conn:
            self.conn = self.connect_db()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_db()
        return False


    def view_portfolio(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT stock_symbol, SUM(shares) FROM transactions 
                          WHERE user_id = ? GROUP BY stock_symbol HAVING SUM(shares) > 0''', (user_id,))
        column_names = [desc[0] for desc in cursor.description]  # Extract column names
        portfolio = [dict(zip(column_names, row)) for row in cursor.fetchall()]  # Convert to list of dicts
        return portfolio
    

    def view_transactions(self, user_id, days):
        '''
        SQLInject payload: "0') UNION SELECT * FROM transactions --"
        SQLInject payload: "0') OR 1=1 --"

        SELECT * FROM transactions 
        WHERE user_id = 1 
        AND timestamp >= datetime('now', '-0') 
        UNION 
        SELECT id, stock_symbol, transaction_type, timestamp FROM transactions -- days')        
        '''
        
        cursor = self.conn.cursor()
        # start_date = (datetime.now() - timedelta(days=days)).isoformat()
        # cursor.execute("SELECT * FROM transactions WHERE user_id = ? AND timestamp >= ?", (user_id, start_date))
        
        # VULNERABLE: Formatting 'days' directly into the query string
        query = f"SELECT * FROM transactions WHERE user_id = {user_id} AND timestamp >= datetime('now', '-{days} days')"
        
        cursor.execute(query)          
        column_names = [desc[0] for desc in cursor.description]  # Extract column names
        transactions = [dict(zip(column_names, row)) for row in cursor.fetchall()]  # Convert to list of dicts
        
        return transactions

    def get_transaction(self, transaction_id):
        # Vulnerable to BOLA. It does not check user_id.
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM transactions WHERE id = ?", (transaction_id,))
        transaction = cursor.fetchone()
        column_names = [desc[0] for desc in cursor.description]  # Extract column names
        transaction = dict(zip(column_names, transaction))
        return transaction


    def buy_stock(self, user_id, stock_symbol, shares):
        cursor = self.conn.cursor()
        try:
            cursor.execute("INSERT INTO transactions (user_id, stock_symbol, shares, transaction_type, timestamp) VALUES (?, ?, ?, 'BUY', ?)",
                           (user_id, stock_symbol, shares, datetime.now().isoformat()))
            self.conn.commit()
            if cursor.rowcount > 0:  # Check if any rows were affected
                return "Stock purchased successfully!"
            else:
                return "Failed to purchase stock!"
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            self.conn.rollback()  # Rollback in case of an error
            return "Failed to purchase stock!"


    def sell_stock(self, user_id, stock_symbol, shares):
        cursor = self.conn.cursor()
        cursor.execute('''SELECT SUM(shares) FROM transactions WHERE user_id = ? AND stock_symbol = ?''', (user_id, stock_symbol))
        total_shares = cursor.fetchone()[0] or 0
        
        if total_shares >= shares:
            try:
                cursor.execute("INSERT INTO transactions (user_id, stock_symbol, shares, transaction_type, timestamp) VALUES (?, ?, ?, 'SELL', ?)",
                               (user_id, stock_symbol, -shares, datetime.now().isoformat()))
                self.conn.commit()
                if cursor.rowcount > 0:  # Check if any rows were affected
                    return "Stock sold successfully!"
                else:
                    return "Failed to sell stock!"
            except sqlite3.Error as e:
                print(f"An error occurred: {e}")
                self.conn.rollback()  # Rollback in case of an error
                return "Failed to sell stock!"
        else:
            return "Not enough shares to sell!"
        

    def __delete_user_transactions(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM transactions WHERE user_id = ?", (user_id,))
        self.conn.commit()
        print("User transactions deleted successfully!")

def _sql_inject_test():
    manager = StockManager('stock_advisor.db')
    payload = "0') UNION SELECT * FROM transactions where user_id = 5 -- This is a safe test query"
    payload = "0') OR 1=1 --"
    payload = "5') OR 2>1 --The past 5"
    payload = "0') UNION SELECT *,1,2 FROM users -- "
    manager.view_transactions(1, payload)

