import os
import psycopg2
import time
from faker import Faker

# Initialize Faker to generate fake data
fake = Faker()

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
            print("Producer: Database connection established.")
            return conn
        except psycopg2.OperationalError as e:
            print(f"Producer: Connection failed: {e}. Retrying in 5 seconds...")
            time.sleep(5)

def setup_database(conn):
    """Creates the 'users' table if it doesn't already exist."""
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        print("Producer: 'users' table is ready.")

def insert_fake_data(conn):
    """Inserts a new fake user into the database."""
    with conn.cursor() as cur:
        name = fake.name()
        email = fake.unique.email()
        cur.execute(
            "INSERT INTO users (name, email) VALUES (%s, %s)",
            (name, email)
        )
        conn.commit()
        print(f"Producer: Inserted user {name} with email {email}")

if __name__ == "__main__":
    connection = get_db_connection()
    setup_database(connection)
    
    # Run the insertion loop 5 times for demonstration
    for i in range(5):
        insert_fake_data(connection)
        time.sleep(2) # Wait 2 seconds between insertions
        
    connection.close()
    print("Producer: Finished inserting data and closed connection.")
