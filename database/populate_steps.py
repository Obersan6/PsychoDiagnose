import os
import sys
import json
from sqlalchemy.dialects.postgresql import insert

# Dynamically add the `src` directory to Python's module search path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../"))
sys.path.insert(0, project_root)

from src.application.models import db, Step  # Correct import for database models
from src.main.app import app  # Import the Flask app from app.py

# Path to the JSON file
json_file_path = os.path.join(current_dir, "steps.json")

def populate_steps():
    """Populate the steps table from a JSON file."""
    with app.app_context():  # Use the app context to access Flask and SQLAlchemy functionality
        try:
            # Load steps from the JSON file
            with open(json_file_path, "r", encoding="utf-8") as file:
                steps_data = json.load(file)

            print(f"Loaded {len(steps_data)} records from {json_file_path}.")
            for step in steps_data:
                # Prepare the insert statement
                insert_stmt = insert(Step).values(
                    id=step["id"],
                    step_number=step["step_number"],
                    step_name=step["step_name"],
                    description=step["description"],
                    disorder_id=step.get("disorder_id"),  # Keep `None` if not provided
                )

                # Handle conflicts by updating the row
                on_conflict_stmt = insert_stmt.on_conflict_do_update(
                    index_elements=["id"],  # Primary key conflict resolution
                    set_={
                        "step_number": insert_stmt.excluded.step_number,
                        "step_name": insert_stmt.excluded.step_name,
                        "description": insert_stmt.excluded.description,
                        "disorder_id": insert_stmt.excluded.disorder_id,
                    },
                )

                # Execute the statement
                db.session.execute(on_conflict_stmt)

            # Commit the transaction
            db.session.commit()
            print("Steps table populated successfully.")

        except Exception as e:
            db.session.rollback()  # Roll back on error
            print(f"An error occurred: {e}")

        finally:
            db.session.close()  # Close the session to release resources

if __name__ == "__main__":
    populate_steps()
