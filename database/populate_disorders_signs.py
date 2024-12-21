import os
import sys
import json
from sqlalchemy.dialects.postgresql import insert

# Dynamically add the `src` directory to Python's module search path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../"))
sys.path.insert(0, project_root)

from src.application.models import db, DisorderSign  # Import relevant model
from src.main.app import app  # Import the Flask app from app.py

# # Path to the JSON file
# json_file_path = os.path.join(current_dir, "disorders_signs.json")

# def populate_disorders_signs():
#     """Populate the disorders_signs table from a JSON file."""
#     with app.app_context():
#         try:
#             # Load data from JSON file
#             with open(json_file_path, "r", encoding="utf-8") as file:
#                 data = json.load(file)

#             print(f"Loaded {len(data)} records from {json_file_path}.")

#             for record in data:
#                 disorder_id = record["disorder_id"]
#                 sign_id = record["sign_id"]

#                 # Prepare the insert statement
#                 insert_stmt = insert(DisorderSign).values(
#                     disorder_id=disorder_id,
#                     sign_id=sign_id
#                 )

#                 # Handle conflicts by doing nothing (e.g., if data already exists)
#                 on_conflict_stmt = insert_stmt.on_conflict_do_nothing()

#                 # Execute the statement
#                 db.session.execute(on_conflict_stmt)

#             # Commit the transaction
#             db.session.commit()
#             print("disorders_signs table populated successfully.")

#         except Exception as e:
#             db.session.rollback()  # Roll back on error
#             print(f"An error occurred: {e}")

#         finally:
#             db.session.close()  # Close the session to release resources

# if __name__ == "__main__":
#     populate_disorders_signs()



# NEW VERSION
# Path to the JSON file
json_file_path = os.path.join(current_dir, "disorders_signs.json")

def validate_disorder_sign(record):
    """Ensure disorder_sign record is valid."""
    if record.get("disorder_id") is None or record.get("sign_id") is None:
        print(f"Skipping invalid record: {record}")
        return False
    return True

def populate_disorders_signs():
    """Populate the disorders_signs table from a JSON file."""
    with app.app_context():
        try:
            # Load data from JSON file
            with open(json_file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            print(f"Loaded {len(data)} records from {json_file_path}.")

            # Validate and filter records
            valid_records = [record for record in data if validate_disorder_sign(record)]
            print(f"{len(valid_records)} valid records to insert.")

            for record in valid_records:
                disorder_id = record["disorder_id"]
                sign_id = record["sign_id"]

                # Prepare the insert statement
                insert_stmt = insert(DisorderSign).values(
                    disorder_id=disorder_id,
                    sign_id=sign_id
                )

                # Handle conflicts by doing nothing (e.g., if data already exists)
                on_conflict_stmt = insert_stmt.on_conflict_do_nothing()

                # Execute the statement
                db.session.execute(on_conflict_stmt)

            # Commit the transaction
            db.session.commit()
            print("disorders_signs table populated successfully.")

        except Exception as e:
            db.session.rollback()  # Roll back on error
            print(f"An error occurred: {e}")

        finally:
            db.session.close()  # Close the session to release resources

if __name__ == "__main__":
    populate_disorders_signs()
