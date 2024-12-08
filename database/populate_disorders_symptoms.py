import os
import sys
import json
from sqlalchemy.dialects.postgresql import insert

# Dynamically add the `src` directory to Python's module search path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../"))
sys.path.insert(0, project_root)

from src.application.models import db, DisorderSymptom  # Import DisorderSymptom model
from src.main.app import app  # Import the Flask app

# Path to the JSON file
json_file_path = os.path.join(current_dir, "disorders_symptoms.json")

def populate_disorders_symptoms():
    """Populate the disorders_symptoms table from a JSON file."""
    with app.app_context():  # Use Flask app context
        try:
            # Load data from the JSON file
            with open(json_file_path, "r", encoding="utf-8") as file:
                disorders_symptoms_data = json.load(file)

            print(f"Loaded {len(disorders_symptoms_data)} records from {json_file_path}.")

            # Insert data into the table
            for record in disorders_symptoms_data:
                disorder_id = record.get("disorder_id")
                symptom_id = record.get("symptom_id")

                # Skip invalid records
                if not disorder_id or not symptom_id:
                    print(f"Skipping invalid record: {record}")
                    continue

                # Prepare the insert statement
                insert_stmt = insert(DisorderSymptom).values(
                    disorder_id=disorder_id,
                    symptom_id=symptom_id,
                )

                # Handle conflicts by ignoring duplicates
                on_conflict_stmt = insert_stmt.on_conflict_do_nothing()

                # Execute the statement
                db.session.execute(on_conflict_stmt)

            # Commit the transaction
            db.session.commit()
            print("disorders_symptoms table populated successfully.")

        except Exception as e:
            db.session.rollback()  # Rollback the transaction on error
            print(f"An error occurred: {e}")

        finally:
            db.session.close()  # Close the session

if __name__ == "__main__":
    populate_disorders_symptoms()
