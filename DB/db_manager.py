import sqlite3


def create_db():        
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect("stock_advisor.db")
    cursor = conn.cursor()

    # Enable foreign key support in SQLite
    cursor.execute("PRAGMA foreign_keys = ON")

    # Create users table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL)''')

    # Create transactions table
    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        stock_symbol TEXT NOT NULL,
                        shares INTEGER NOT NULL,
                        transaction_type TEXT NOT NULL CHECK(transaction_type IN ('BUY', 'SELL')),
                        timestamp TEXT NOT NULL,
                        FOREIGN KEY(user_id) REFERENCES users(id))''')

    # Commit and close connection
    conn.commit()
    conn.close()

    print("Database and tables created successfully!")

def drop_db():
    conn = sqlite3.connect("stock_advisor.db")
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("DROP TABLE IF EXISTS transactions")

    conn.commit()
    conn.close()

    print("Tables dropped successfully!")

if __name__ == "__main__":
    drop_db()
    create_db()