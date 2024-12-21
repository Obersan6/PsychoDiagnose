import secrets

# Generate a 32-byte SECRET_KEY
SECRET_KEY = secrets.token_hex(32)

# Define my SQLALCHEMY_DATABASE_URI
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Caccolino5@localhost/diagnosis_db'



