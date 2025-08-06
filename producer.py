# ---------------------------------
# Purpose: Producer script for a local data pipeline using Dockerized PostgreSQL and Python
# Target: Local Data Pipeline using Dockerized (PostgreSQL + Python)
# This is personal work for educational purposes.
# ---------------------------------

import os
import psycopg2
import time
from faker import Faker

fake = Faker()

# Dev note: this function establishes a connection to the PostgreSQL database
# and retries if the connection fails.


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
            print(
                f"Producer: Connection failed: {e}. Retrying in 5 seconds...")
            time.sleep(5)


# Dev note: this function creates the 'users' table if it doesn't already exist.
# It basically uses a simple schema with an auto-incrementing ID, name, email, and created_at timestamp.

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

# Dev note: this function inserts a new fake user into the database.
# It uses the Faker library to generate random names and emails.


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

# Dev note: The main execution block
# It first establishes a connection to the database, sets up the table,
# and then enters a loop to insert fake data every 2 seconds for demonstration purposes.


if __name__ == "__main__":
    connection = get_db_connection()
    setup_database(connection)

    # Run the insertion loop 5 times for demonstration
    for i in range(5):
        insert_fake_data(connection)
        time.sleep(2)  # Wait 2 seconds between insertions

    connection.close()
    print("Producer: Finished inserting data and closed connection.")
