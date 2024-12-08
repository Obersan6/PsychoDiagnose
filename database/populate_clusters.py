# Populate table 'clusters'

import os
import sys
import json

# Add the root directory to Python's module search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.application.models import Cluster, db
from src.main.app import app  # Import app

# Path to the JSON file
JSON_FILE_PATH = os.path.join(os.path.dirname(__file__), "clusters.json")

def load_clusters():
    """
    Load clusters data from the JSON file and seed the database.
    """
    if not os.path.exists(JSON_FILE_PATH):
        print(f"Error: File {JSON_FILE_PATH} not found.")
        return

    # Open and read the JSON file
    with open(JSON_FILE_PATH, "r") as file:
        try:
            clusters_data = json.load(file)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return

    # Load data into the database
    try:
        for cluster in clusters_data:
            new_cluster = Cluster(
                id=cluster.get("id"),
                name=cluster.get("name"),
                description=cluster.get("description"),
                category_id=cluster.get("category_id"),
            )
            db.session.add(new_cluster)

        # Commit the session
        db.session.commit()
        print(f"Successfully seeded {len(clusters_data)} clusters.")
    except Exception as e:
        db.session.rollback()
        print(f"Error seeding clusters: {e}")

if __name__ == "__main__":
    with app.app_context():
        load_clusters()
