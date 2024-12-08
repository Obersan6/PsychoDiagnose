import os
import sys
import json
from sqlalchemy.dialects.postgresql import insert

# Dynamically add the `src` directory to Python's module search path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../"))
sys.path.insert(0, project_root)

from src.application.models import db, DifferentialDiagnosis  # Correct import for database models
from src.main.app import app  # Import the Flask app from app.py

# Path to the JSON file
json_file_path = os.path.join(current_dir, "differential_diagnosis.json")

MAX_DESCRIPTION_LENGTH = 5000  # Adjust this based on your DB schema


def truncate_field(value, max_length):
    """Truncate a string to the specified maximum length."""
    if value and len(value) > max_length:
        print(f"Truncating field value to {max_length} characters.")
        return value[:max_length]
    return value


def validate_differential_diagnosis(record):
    """Validate a differential diagnosis record before inserting it."""
    # Ensure required fields are present
    if not record.get("disorder_id") or not record.get("disorder_name"):
        print(f"Skipping record with missing 'disorder_id' or 'disorder_name': {record}")
        return False

    record["description"] = truncate_field(record.get("description", ""), MAX_DESCRIPTION_LENGTH)
    return True


def populate_differential_diagnosis():
    """Populate the differential_diagnosis table from a JSON file."""
    with app.app_context():  # Use the app context to access Flask and SQLAlchemy functionality
        try:
            # Load data from the JSON file
            with open(json_file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            print(f"Loaded {len(data)} records from {json_file_path}.")
            valid_records = [record for record in data if validate_differential_diagnosis(record)]

            if not valid_records:
                print("No valid records to insert.")
                return

            for record in valid_records:
                # Prepare the insert statement
                insert_stmt = insert(DifferentialDiagnosis).values(
                    id=record["id"],
                    disorder_id=record["disorder_id"],
                    differential_disorder_id=record.get("differential_disorder_id"),  # Can be None
                    disorder_name=record["disorder_name"],
                    description=record["description"],
                )

                # Handle conflicts by updating the row
                on_conflict_stmt = insert_stmt.on_conflict_do_update(
                    index_elements=["id"],  # Primary key conflict resolution
                    set_={
                        "disorder_id": insert_stmt.excluded.disorder_id,
                        "differential_disorder_id": insert_stmt.excluded.differential_disorder_id,
                        "disorder_name": insert_stmt.excluded.disorder_name,
                        "description": insert_stmt.excluded.description,
                    },
                )

                # Execute the statement
                db.session.execute(on_conflict_stmt)

            # Commit the transaction
            db.session.commit()
            print("DifferentialDiagnosis table populated successfully.")

        except Exception as e:
            db.session.rollback()  # Roll back on error
            print(f"An error occurred: {e}")

        finally:
            db.session.close()  # Close the session to release resources


if __name__ == "__main__":
    populate_differential_diagnosis()


