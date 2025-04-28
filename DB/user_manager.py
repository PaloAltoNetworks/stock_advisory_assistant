import sqlite3
import bcrypt
import getpass

class UserManager:
    def __init__(self, db_path="stock_advisor.db"):
        self.db_path = db_path
        self.sessions = {}

    def connect_db(self):
        return sqlite3.connect(self.db_path)

    def register_user(self, username, email, password):
        conn = self.connect_db()
        cursor = conn.cursor()
        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        
        try:
            cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, hashed_pw))
            conn.commit()
            print("User registered successfully!")
        except sqlite3.IntegrityError:
            print("Username or email already exists!")
        finally:
            conn.close()

    def login_user(self, username, password):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, password FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()
        if user and bcrypt.checkpw(password.encode(), user[1]):
            # print("Login successful!")
            self.sessions[username] = user[0]
            return user[0]
        else:
            # print("Invalid credentials!")
            return None   

    def logout_user(self, username):
        if username in self.sessions:
            del self.sessions[username]
            print("User logged out successfully!")
        else:
            print("No active session found!")

    def is_logged_in(self, username):
        return username in self.sessions
    
    def get_user_id(self, username):
        return self.sessions.get(username, None)
    
    def delete_user(self, username):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE username = ?", (username,))
        conn.commit()
        conn.close()
        print("User deleted successfully!")

    def cli_login(self):
        try:
            while True:
                # print("\n--- Login Console ---")
                username = input("Username (or type 'REGISTER' to create a new account): ").strip()
                
                if username.upper() == "REGISTER":
                    print("\n--- Registration ---")
                    new_username = input("Enter new username: ").strip()
                    new_email = input("Enter email: ").strip()
                    new_password = getpass.getpass("Enter new password: ").strip()  # Hide password input
                    
                    # Attempt to register the user
                    self.register_user(new_username, new_email, new_password)
                    print("You can now log in with your new account.\n")
                    continue  # Return to the login console
                
                password = getpass.getpass("Password: ").strip()  # Hide password input
                
                # Attempt to log in
                user_id = self.login_user(username, password)
                if user_id:
                    print(f"Welcome, {username}! You are now logged in.")
                    return user_id  # Return the user_id on successful login
                else:
                    print("Invalid username or password. Please try again.")
        except KeyboardInterrupt:
            print("\nExiting... Goodbye!")
            return None  # Return None if interrupted

def test():
    user_manager = UserManager()
    user_manager.cli_login()

if __name__ == "__main__":   
    test()