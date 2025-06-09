import os
import psycopg2
import time

def get_db_connection():
    """Establishes a connection to the PostgreSQL database."""
    while True:
        try:
            conn = psycopg2.connect(
                host=os.environ.get("DB_HOST"),
                database=os.environ.get("DB_NAME"),
                user=os.environ.get("DB_USER"),
                password=os.environ.get("DB_PASSWORD")
            )
            print("Consumer: Database connection established.")
            return conn
        except psycopg2.OperationalError as e:
            print(f"Consumer: Connection failed: {e}. Retrying in 5 seconds...")
            time.sleep(5)

def process_data(conn):
    """Fetches all users from the database and prints them."""
    print("\n--- Reading data from database ---")
    with conn.cursor() as cur:
        cur.execute("SELECT id, name, email, created_at FROM users ORDER BY created_at DESC;")
        users = cur.fetchall()
        
        if not users:
            print("Consumer: No users found in the database yet.")
        else:
            print(f"Consumer: Found {len(users)} user(s) in the database.")
            for user in users:
                print(f"  - ID: {user[0]}, Name: {user[1]}, Email: {user[2]}, Joined: {user[3]}")
    print("--- Finished reading data ---\n")

if __name__ == "__main__":
    # Give the producer a head start to insert some data
    print("Consumer: Waiting for 10 seconds before starting...")
    time.sleep(10)

    connection = get_db_connection()
    process_data(connection)
    connection.close()
    print("Consumer: Finished processing and closed connection.")
