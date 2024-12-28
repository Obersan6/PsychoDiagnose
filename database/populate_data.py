# Populate the table 'categories' in my machine

# import os
# import sys
# import json

# # Add the root directory to Python's module search path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# from src.application.models import Category, db
# from src.main.app import app  # Correct import

# # Path to the JSON file
# JSON_FILE_PATH = os.path.join(os.path.dirname(__file__), "categories.json")

# def load_categories():
#     """
#     Load categories data from the JSON file and seed the database.
#     """
#     if not os.path.exists(JSON_FILE_PATH):
#         print(f"Error: File {JSON_FILE_PATH} not found.")
#         return

#     # Open and read the JSON file
#     with open(JSON_FILE_PATH, "r") as file:
#         try:
#             categories_data = json.load(file)
#         except json.JSONDecodeError as e:
#             print(f"Error decoding JSON: {e}")
#             return

#     # Load data into the database
#     try:
#         for category in categories_data:
#             new_category = Category(
#                 id=category.get("id"),
#                 name=category.get("name"),
#                 description=category.get("description"),
#             )
#             db.session.add(new_category)

#         # Commit the session
#         db.session.commit()
#         print(f"Successfully seeded {len(categories_data)} categories.")
#     except Exception as e:
#         db.session.rollback()
#         print(f"Error seeding categories: {e}")

# if __name__ == "__main__":
#     with app.app_context():
#         load_categories()



# Populate the table 'categories' to Supabase
import os
import json
import psycopg2

# Supabase database connection details
DB_HOST = "aws-0-eu-west-2.pooler.supabase.com"
DB_PORT = 6543
DB_NAME = "postgres"
DB_USER = "postgres.rdsnxgihfwemtrdynqol"
DB_PASSWORD = "MySecurePass123!"

# Path to the JSON file
JSON_FILE_PATH = os.path.join(os.path.dirname(__file__), "categories.json")

def load_categories():
    """
    Load categories data from the JSON file and seed the Supabase database.
    """
    if not os.path.exists(JSON_FILE_PATH):
        print(f"Error: File {JSON_FILE_PATH} not found.")
        return

    # Open and read the JSON file
    with open(JSON_FILE_PATH, "r") as file:
        try:
            categories_data = json.load(file)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return

    # Connect to the Supabase database
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
        )
        cursor = conn.cursor()

        # Insert data into the 'categories' table
        for category in categories_data:
            cursor.execute(
                """
                INSERT INTO categories (id, name, description)
                VALUES (%s, %s, %s)
                ON CONFLICT (id) DO NOTHING;
                """,
                (
                    category.get("id"),
                    category.get("name"),
                    category.get("description"),
                ),
            )

        # Commit the transaction
        conn.commit()
        print(f"Successfully seeded {len(categories_data)} categories.")

    except psycopg2.Error as e:
        print(f"Database error: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    load_categories()
