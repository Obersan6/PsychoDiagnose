# Explanations and Steps 

In this file I have all the notes regarding steps and procedures I followed to build or execute certain aspects of my application.

## Steps to Initialize Flask-Migrate 

1- **Navigate to the Root Directory: From your terminal, navigate to the root of your project directory:**

```cd onedrive/desktop/springboard-projects/capstone-project-one-a594b10cc10749ee801fe8f275555050```

2- **Set the FLASK_APP Environment Variable: Set the FLASK_APP environment variable to point to src/main/app.py. This tells Flask which file contains the application instance.**

```export FLASK_APP=src/main/app.py```

3- **Initialize Flask-Migrate: Now, from the root of your project directory, initialize the migrations directory by running:**

```flask db init```

4- **Continue with Migration Steps: After initialization, continue with the remaining steps:**

- **Create an Initial Migration:**

    ```flask db migrate -m "Initial migration"```

- **Apply the Migration:**

    ```flask db upgrade```

<u>SUMMARY OF COMMANDS</u>:

From the root directory (```capstone-project-one-a594b10cc10749ee801fe8f275555050```), run these commands in sequence:
```
bash
Copy code
export FLASK_APP=src/main/app.py   # or use the Windows equivalent
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```
This should set up your migrations successfully and create the tables in your database as defined in ```models.py```.