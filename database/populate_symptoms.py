import os
import sys
import json
from sqlalchemy.dialects.postgresql import insert

# Dynamically add the `src` directory to Python's module search path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../"))
sys.path.insert(0, project_root)

from src.application.models import db, Symptom  # Correct import for database models
from src.main.app import app  # Import the Flask app from app.py

# Path to the JSON file
json_file_path = os.path.join(current_dir, "symptoms.json")

def populate_symptoms():
    """Populate the symptoms table from a JSON file."""
    with app.app_context():  # Use the app context to access Flask and SQLAlchemy functionality
        try:
            # Load symptoms from the JSON file
            with open(json_file_path, "r", encoding="utf-8") as file:
                symptoms_data = json.load(file)

            print(f"Loaded {len(symptoms_data)} symptoms from {json_file_path}.")

            for symptom in symptoms_data:
                # Prepare the insert statement
                insert_stmt = insert(Symptom).values(
                    id=symptom["id"],
                    name=symptom["name"],
                    description=symptom["description"],
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
            print("Symptoms table populated successfully.")

        except Exception as e:
            db.session.rollback()  # Roll back on error
            print(f"An error occurred: {e}")

        finally:
            db.session.close()  # Close the session to release resources


if __name__ == "__main__":
    populate_symptoms()
