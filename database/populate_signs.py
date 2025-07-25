import os
import sys
import json
from sqlalchemy.dialects.postgresql import insert

# Dynamically add the `src` directory to Python's module search path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../"))
sys.path.insert(0, project_root)

from src.application.models import db, Sign  # Correct import for the Sign model
from src.main.app import app  # Import the Flask app from app.py

# Path to the JSON file
json_file_path = os.path.join(current_dir, "signs.json")


def validate_sign(sign):
    """Validate a sign record before inserting it."""
    # Ensure required fields are present
    if not sign.get("name") or not sign.get("description"):
        print(f"Skipping sign with missing 'name' or 'description': {sign}")
        return False

    return True


def populate_signs():
    """Populate the signs table from a JSON file."""
    with app.app_context():  # Use the app context to access Flask and SQLAlchemy functionality
        try:
            # Load signs from the JSON file
            with open(json_file_path, "r", encoding="utf-8") as file:
                signs_data = json.load(file)

            print(f"Loaded {len(signs_data)} signs from {json_file_path}.")
            valid_signs = [sign for sign in signs_data if validate_sign(sign)]

            if not valid_signs:
                print("No valid signs to insert.")
                return

            for sign in valid_signs:
                # Prepare the insert statement
                insert_stmt = insert(Sign).values(
                    id=sign["id"],
                    name=sign["name"],
                    description=sign["description"],
                )

                # Handle conflicts by updating the row
                on_conflict_stmt = insert_stmt.on_conflict_do_update(
                    index_elements=["id"],  # Primary key conflict resolution
                    set_={
                        "name": insert_stmt.excluded.name,
                        "description": insert_stmt.excluded.description,
                    },
                )

                # Execute the statement
                db.session.execute(on_conflict_stmt)

            # Commit the transaction
            db.session.commit()
            print("Signs table populated successfully.")

        except Exception as e:
            db.session.rollback()  # Roll back on error
            print(f"An error occurred: {e}")

        finally:
            db.session.close()  # Close the session to release resources


if __name__ == "__main__":
    populate_signs()
