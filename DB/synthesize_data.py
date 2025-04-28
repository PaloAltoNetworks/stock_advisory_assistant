import random
import argparse
from user_manager import UserManager
from stock_manager import StockManager

# List of artificial usernames
usernames = ["alice", "bob", "charlie", "david", "eve", "frank", "grace", "henry", "irene", "jack"]

# List of S&P 50 stocks (sample selection)
sp50_stocks = ["AAPL", "MSFT", "GOOGL", "AMZN", "FB", "TSLA", "BRK.B", "NVDA", "JNJ", "V", "WMT", "JPM", "PG", "UNH", "MA", "HD", "DIS", "PYPL", "VZ", "ADBE", "NFLX", "KO", "PFE", "PEP", "INTC", "MRK", "XOM", "T", "ABBV", "CVX", "CMCSA", "ABT", "ACN", "DHR", "NKE", "MCD", "COST", "TMO", "TXN", "LIN", "NEE", "HON", "UNP", "MDT", "BMY", "LOW", "UPS", "IBM", "CAT", "GS"]

def synthesize_data():
    for username in usernames:
        email = f"{username}@example.com"
        password = f"{username.upper()}_2025"
        create_fake_user_and_transactions(username, email, password)
        
def create_fake_user_and_transactions(username, email, password):
    # Register user
    UserManager.register_user(username, email, password)
    
    # Log in user to get their ID
    user_id = UserManager.login_user(username, password)
    
    if user_id:
        print(f"User {username} logged in successfully.")
        
        # Make 5 random stock purchases for each user
        for _ in range(5):
            stock_symbol = random.choice(sp50_stocks)
            shares = random.randint(5, 50)  # Purchase a reasonable number of shares
            StockManager.buy_stock(user_id, stock_symbol, shares)
            StockManager.sell_stock(user_id, stock_symbol, random.randint(1, (int)(shares/2.0)))  # Sell a random number of shares            
    else:
        print(f"Failed to log in user {username}.")

def interactive_cli():
    while True:
        print("\nWelcome to the Stock Management System")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Select an option: ")
        
        if choice == "1":
            username = input("Enter a username: ")
            email = input("Enter your email: ")
            password = input("Enter a password: ")
            UserManager.register_user(username, email, password)
        
        elif choice == "2":
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            user_id = UserManager.login_user(username, password)
            
            if user_id:
                while True:
                    print("\nStock Management Options:")
                    print("1. View Portfolio")
                    print("2. Buy Stock")
                    print("3. Sell Stock")
                    print("4. View Transactions by in the past X days")
                    print("5. View Transaction by ID")
                    print("6. Logout")
                    action = input("Select an option: ")
                    
                    if action == "1":
                        portfolio = StockManager.view_portfolio(user_id)
                        print("\nYour Portfolio:")
                        for stock in portfolio:
                            print(f"{stock[0]}: {stock[1]} shares")
                    elif action == "2":
                        stock_symbol = input("Enter stock symbol: ").upper()
                        shares = int(input("Enter number of shares: "))
                        StockManager.buy_stock(user_id, stock_symbol, shares)
                    elif action == "3":
                        stock_symbol = input("Enter stock symbol: ").upper()
                        shares = int(input("Enter number of shares: "))
                        StockManager.sell_stock(user_id, stock_symbol, shares)
                    elif action == "4":
                        days = input("Enter the number of days :")
                        trans = StockManager.view_transactions(user_id, days)
                        for tran in trans:
                            print(f"Transaction ID: {tran[0]}, UserID: {user_id}, Stock Symbol: {tran[2]}, Shares: {tran[3]}, Type: {tran[4]}, Timestamp: {tran[5]}")
                    elif action == "5":
                        tran_id = input("Enter the transaction ID :")
                        tran = StockManager.get_transaction(tran_id)
                        print(f"Transaction ID: {tran[0]}, UserID: {user_id}, Stock Symbol: {tran[2]}, Shares: {tran[3]}, Type: {tran[4]}, Timestamp: {tran[5]}")
                    elif action == "6":
                        UserManager.logout_user(username)
                        break
            else:
                print("Invalid login credentials!")
        
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid option! Please try again.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stock Management System")
    parser.add_argument("--mode", choices=["synthesize", "interactive"], required=True, help="Choose whether to synthesize data or run interactive mode")
    args = parser.parse_args()
    
    if args.mode == "synthesize":
        synthesize_data()
    elif args.mode == "interactive":
        interactive_cli()
