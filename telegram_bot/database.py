import sqlite3

DATABASE_NAME = "users.db"

def initialize_database():
    """Initializes the SQLite database and creates the users table if it doesn't exist."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            role TEXT NOT NULL
        ),
        channels (
            channel_id INTEGER PRIMARY KEY,
            channel_name TEXT
        )
    """)
    # Create channels table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS channels (
            channel_id INTEGER PRIMARY KEY,
            channel_name TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_user(user_id: int, role: str):
    """Adds a new user to the database or updates the role if the user already exists."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (user_id, role) VALUES (?, ?)
        ON CONFLICT(user_id) DO UPDATE SET role=excluded.role
    """, (user_id, role))
    conn.commit()
    conn.close()
    # logger.info(f"User {user_id} added/updated with role {role}") # Commented out to avoid duplicate logging if logger is configured in bot.py


def remove_user(user_id: int):
    """Removes a user from the database."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()
    # logger.info(f"User {user_id} removed from database.") # Commented out to avoid duplicate logging


def get_user_role(user_id: int) -> str | None:
    """Gets the role of a user by user_id."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT role FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    return None

def list_users_by_role(role: str) -> list[int]:
    """Lists all user_ids with a specific role."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users WHERE role = ?", (role,))
    results = cursor.fetchall()
    conn.close()
    return [result[0] for result in results]

# Basic logging for database operations (can be integrated with the bot's logger)
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

if __name__ == '__main__':
    # Example usage:
    initialize_database()
    add_user(12345, 'member')
    add_user(67890, 'developer')
    add_user(24770515, 'owner')
    print(f"Role of 12345: {get_user_role(12345)}")
    print(f"Role of 67890: {get_user_role(67890)}")
    print(f"Role of 24770515: {get_user_role(24770515)}")
    print(f"Developers: {list_users_by_role('developer')}")
    remove_user(12345)
    print(f"Role of 12345 after removal: {get_user_role(12345)}")
    print(f"Owners: {list_users_by_role('owner')}")

    # Example Channel operations have been removed as they will be handled by the bot commands.
    pass # Keep the main block for potential future testing if needed.
