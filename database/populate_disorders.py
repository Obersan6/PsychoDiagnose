import os
import sys
import json
from sqlalchemy.dialects.postgresql import insert

# Dynamically add the `src` directory to Python's module search path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../"))
sys.path.insert(0, project_root)

from src.application.models import db, Disorder  # Correct import for database models
from src.main.app import app  # Import the Flask app from app.py

# Path to the JSON file
json_file_path = os.path.join(current_dir, "disorders.json")

# Constants for field length validation (adjust based on your DB schema)
MAX_CRITERIA_LENGTH = 5000  # Example max length for 'criteria'
MAX_DESCRIPTION_LENGTH = 5000  # Example max length for 'description'


def truncate_field(value, max_length):
    """Truncate a string to the specified maximum length."""
    if value and len(value) > max_length:
        print(f"Truncating field value to {max_length} characters.")
        return value[:max_length]
    return value


def validate_disorder(disorder):
    """Validate a disorder record before inserting it."""
    # Ensure required fields are present
    if not disorder.get("name") or not disorder.get("category_id"):
        print(f"Skipping disorder with missing 'name' or 'category_id': {disorder}")
        return False

    # Ensure `criteria` retains formatting with `\n\n`
    disorder["criteria"] = truncate_field(disorder.get("criteria", ""), MAX_CRITERIA_LENGTH)
    disorder["description"] = truncate_field(disorder.get("description", ""), MAX_DESCRIPTION_LENGTH)

    return True


def populate_disorders():
    """Populate the disorders table from a JSON file."""
    with app.app_context():  # Use the app context to access Flask and SQLAlchemy functionality
        try:
            # Load disorders from the JSON file
            with open(json_file_path, "r", encoding="utf-8") as file:
                disorders_data = json.load(file)

            print(f"Loaded {len(disorders_data)} disorders from {json_file_path}.")
            valid_disorders = [disorder for disorder in disorders_data if validate_disorder(disorder)]

            if not valid_disorders:
                print("No valid disorders to insert.")
                return

            for disorder in valid_disorders:
                # Prepare the insert statement
                insert_stmt = insert(Disorder).values(
                    id=disorder["id"],
                    name=disorder["name"],
                    description=disorder["description"],
                    criteria=disorder["criteria"],
                    category_id=disorder["category_id"],
                    cluster_id=disorder.get("cluster_id"),  # Cluster ID can be None
                )

                # Handle conflicts by updating the row
                on_conflict_stmt = insert_stmt.on_conflict_do_update(
                    index_elements=["id"],  # Primary key conflict resolution
                    set_={
                        "name": insert_stmt.excluded.name,
                        "description": insert_stmt.excluded.description,
                        "criteria": insert_stmt.excluded.criteria,
                        "category_id": insert_stmt.excluded.category_id,
                        "cluster_id": insert_stmt.excluded.cluster_id,
                    },
                )

                # Execute the statement
                db.session.execute(on_conflict_stmt)

            # Commit the transaction
            db.session.commit()
            print("Disorders table populated successfully.")

        except Exception as e:
            db.session.rollback()  # Roll back on error
            print(f"An error occurred: {e}")

        finally:
            db.session.close()  # Close the session to release resources


if __name__ == "__main__":
    populate_disorders()

