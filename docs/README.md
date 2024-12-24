# PsychoDiagnose

**PsychoDiagnose** is an educational application designed to guide students of psychology and psychiatry  through the structured diagnostic process of mental disorders. Rooted in the standards and criteria outlined by the ***DSM-5-TR*** (Diagnostic and Statistical Manual of Mental Disorders, Fifth Edition, Text Revision), it provides an intuitive platform to explore the step-by-step methodology used by mental health professionals.

The tool features an intuitive design, ensuring that users can easily navigate through the diagnostic process and access the information they need. While PsychoDiagnose draws from the ***DSM-5-TR*** guidelines to ensure accuracy and consistency, it is intended solely for learning purposes and does not replace the official manual. This strictly educational approach and does not provide medical diagnoses to ensure a safe and focused learning environment for users as they deepen their understanding of psychopathologies and the diagnostic process.


## Motivation

The inspiration for this application comes from my experience as a psychology student studying "Psychopathology." During that time, I often felt overwhelmed by the sheer volume of material and the complexity of mastering all the elements involved, including how to effectively use the DSM and navigate the diagnostic process. I realized how valuable it would have been to have a tool that distilled the most important concepts into a clear and comprehensive resource.

This app is designed to support students facing similar challenges. By guiding users through the structured diagnostic process without providing direct diagnoses, it fosters critical thinking and self-reflection. Its goal is to simplify the learning process, assist with assignments and papers, and provide clarity in the study of psychopathology, diagnostics, therapy, and related subjects. My hope is that this tool saves time and enhances understanding for students, just as I wished it had during my own studies.

[Click here to visit PsychoDiagnose](https://www.example.com)

## Features

### Core Functionalities

#### User Authentication

- Secure user authentication allows users to sign up, log in, and log out.
- Ensures personalized access, enhances user experience, and maintains data privacy.

#### Edit and Delete User Profile

- Users can edit their first and last name, change or remove their profile photo, and delete their account.
- Provides a personalized experience by giving users control over their profiles.

#### File Upload 

- Enables users to upload a profile photo during registration or profile editing.
- Enhances user convenience and profile personalization.

#### Default Photo Icon

- A default icon is assigned to users who don’t upload a profile photo.
- Improves visual appeal and avoids bare or unstyled profiles.

### UI/UX Features

#### Responsive Design 

- Ensures the website adapts to various screen sizes, enhancing readability and usability across devices.

#### Static Navigation Bar 

- This eases the navigation of the application, providing fast access to any areas of the application, and making a better user experince.

#### Sign-In/Sign-Up Access Points

- Users can sign in or sign up directly from the navigation bar or the landing page.
- Provides flexibility and ease of access for both new and returning users.

#### Search Bars and Autocomplete

- Integrated into sections like the symptoms or disorders pages to help users quickly locate specific elements.
- Saves time by minimizing scrolling and manual searching.
- Lists without logical display orders are sorted alphabetically to improve navigation.

### Multiple Hyperlinks

- Key sections include multiple hyperlinks for quick cross-referencing, enhancing usability.

#### Landing Page for Non-Logged-In Users

- Provides an overview of the application, its purpose, how it works, and key features.
- Highlights the app’s free-to-use nature and the importance of the DSM-5-TR.

### Custom Features

#### API Development

- Custom API developed to adhere to the guidelines of the DSM-5-TR, as no official DSM API exists.
- Ensures accurate, up-to-date information aligned with the most widely used diagnostic manual in the US and globally. 

##### Key Endpoints

**User Management**

```
/signup: Allows users to create a new account by providing their first name, last name, email, and a password. Optionally, users can upload a profile photo.
/signin: Authenticates users by verifying their credentials (email and password) and logs them into the application.
/logout: Logs the user out and invalidates their session for security purposes.
/user/<int:user_id>/profile: Fetches the profile details of a specific user, including their first name, last name, and profile photo.
/user/<int:user_id>/profile/edit: Allows a logged-in user to edit their profile details, such as their name and profile photo.
/user/<int:user_id>/profile/delete: Permanently deletes the user's account, removing all associated data.
```
**Diagnostic Categories**

```
/categories: Returns a comprehensive list of diagnostic categories along with relevant information, such as the category name and description.
/categories/<int:category_id>: Fetches detailed information about a specific category, including associated disorders and any clusters within the category.
```

**Disorders**
```
/disorders: Returns a complete list of disorders with relevant information, such as disorder names, descriptions, and associated criteria.
/disorders/<int:disorder_id>: Provides detailed information about a specific disorder, including:
- The diagnostic category and cluster (if applicable).
- A description of the disorder.
- Diagnostic criteria.
- Related signs and symptoms.
- Differential diagnoses.
```

**Clusters**
```
/clusters: Returns the entire list of clusters. Clusters are sub-groupings within diagnostic categories that further classify disorders (e.g., personality disorder clusters).
/cluster/<int:cluster_id>: Provides detailed information about a specific cluster, including its name, description, and the list of associated disorders.
```

**Steps**

```
/steps: Returns an ordered list of the diagnostic steps, providing a structured guide to navigate the DSM-5-TR diagnostic process.
/step/<int:step_id>: Fetches detailed instructions and guidelines for a specific diagnostic step.
```

**Signs**

```
/signs: Returns a list of all signs used in diagnostics, including their names and descriptions.
/signs/<int:sign_id>: Provides detailed information about a specific sign.
```

**Symptoms**
```
/symptom: Returns a list of all symptoms used in diagnostics, including their names and descriptions.
/symptom/<int:symptom_id>: Provides detailed information about a specific symptom.
```

#### Custom Database

- A bespoke database design organizes critical information such as categories, disorders, signs, symptoms, and steps.
- Essential for managing structured and searchable data within the application.

### Educational and Functional Features

#### Concise Descriptions

- Provides brief and clear definitions of key terms and concepts, aiding comprehension.

#### Guided Diagnostic Steps

- Offers a structured guide through diagnostic steps applicable to the DSM-5-TR or other frameworks.
- Users can navigate steps individually, move between steps, or view all steps as a list.
- ***Future feature***: Users will be able to add selected steps and notes to a personalized pad for case tracking.

#### Dynamic Content

- Pages dynamically display content based on user interaction, ensuring a seamless experience.
- Key features and navigation options are accessible from every page, improving usability.

## User Flow

![User Flow](https://github.com/hatchways-community/capstone-project-one-a594b10cc10749ee801fe8f275555050/blob/dev/docs/userflow.jpeg?raw=true)

### Testing

The application includes robust testing functionality to ensure the reliability and correctness of key features.

## Technology Stack

### Frontend

- **HTML5 & CSS3**: Used to structure and style the web pages.
- **Bootstrap 5**: Utilized for responsive design and prebuilt UI components to ensure a user-friendly experience.
- **Bootstrap Icons**: Used for consistent and visually appealing icons across the site.
- **JavaScript**: Added interactivity to certain areas of the website, such as search functionality and autocomplete for dropdown menus in the following pages: categories, disorders, signs, and symptoms.

### Backend

- **Python**: The primary programming language used to build the server-side of the application.
- **Flask**: Python web framework used for routing, server-side logic, and handling requests.
- **Flask Blueprints**: Used to modularize and organize the app into smaller, manageable sections.
- **Jinja2**: Flask’s templating engine for dynamically rendering HTML pages.
- **WTForms**: Used for creating and validating forms easily.

#### Authentication

- **Flask-WTF**: Used for form validation and handling secure user inputs.
- **Flask-Bcrypt**: Used for password hashing to ensure user data security.

### Database

- **PostgreSQL**: Used as the relational database for storing user data, ***DSM-5-TR*** such as categories, clusters, disorders, signs, symptoms, steps, ..., and their relationships.
- **SQLAlchemy**: ORM (Object-Relational Mapping) library used to interact with the database and handle complex queries.
- **Alembic**: Used for database migrations and schema management.

#### Data Population

- **JSON Files**: JSON data files were used to store structured information for populating the database tables, such as categories, disorders, signs, and symptoms, programmatically.
- **JavaScript Scripts**: Custom JavaScript scripts were developed to automate the process of populating database tables by parsing and inserting JSON data into the database.

#### Testing

- **unittest**: The built-in Python testing framework used to create and run unit tests for the application. 

### API

- **Custom API**: Developed to allow interaction with the database, enabling search and retrieval of diagnostic information programmatically.

### File Management

- **Flask-WTF with FileField**: Used to upload and handle user profile images.

### Development Tools

- **VS Code**: The primary IDE used for development.
- **Git & GitHub**: Version control and collaboration tools used to track changes and manage the project repository.
- **flask_debugtoolbar**: Extension to enable debug output during development.

### Deployment

- **Render**: Used to deploy the website and make it accessible online.
- **Supabase**: Used as a scalable backend service for authentication and database hosting.

## How to Run the Application

### 1. Clone the repository

```
git clone <my-repository-url>
cd <your-repository-folder>
```
**Note: Ensure you have appropriate permissions to access this repository.**

### 2. Set Up the Environment

#### Install Python

Ensure you have `Python 3.10 `or later installed. You can download it from [Python's official website](https://www.python.org/)

#### Create a Virtual Environment

```
python -m venv venv
```

#### Activate the virtual environment

**On Windows using Hyper**

```
source venv/Scripts/activate 
```

**On Standard Windows Command Prompt**:

```
venv\Scripts\activate
```

**On macOS/Linux**:
```
source venv/bin/activate
```
#### Install Dependencies

Use `pip` to install the required dependencies:

```
pip install -r requirements.txt
```
### 3. Configure the Flask Application

Because of the way the Flask app is structured, you need to set the following environment variables before running the app:

#### On macOS/Linux

```
export FLASK_APP=src.main.app:app
export FLASK_ENV=development  # Optional: Enables debug mode
```

#### On Windows (Command Prompt)

```
set FLASK_APP=src.main.app:app
set FLASK_ENV=development  # Optional: Enables debug mode
```

### On Windows (PowerShell)

```
$env:FLASK_APP="src.main.app:app"
$env:FLASK_ENV="development"  # Optional: Enables debug mode
```

### 4. Set Up the Database

#### Configure the Database URL

Edit the `config.py` file to include your database connection string. For example:

```
SQLALCHEMY_DATABASE_URI = "postgresql://username:password@localhost:5432/your_database_name"
```

#### Initialize the Database

Run the following commands to create the database schema:

```
flask db init
flask db migrate
flask db upgrade
```

### 5. Populate the Database Tables

#### Using `schema.sql`

Execute the SQL file schema.sql to create initial database tables:
psql -U your_username -d your_database_name -f database/schema.sql

#### Using Python and JSON Files

Navigate to the `database/` directory and run the scripts to populate the tables. Each script uses JSON files to programmatically populate the database.

For example:

```
python database/populate_data.py  # Populates the "categories" table
python database/populate_disorders.py  # Populates the "disorders" table
```

Populate the database tables running the ```scripts``` inside the folder `database`. For example:

###  6. Run the Application

#### Start the Flask application

From the project directory, run:

```
flask run
```
Open your browser and navigate to `http://127.0.0.1:5000` to access the application.

#### Run the Flask Application in Debug Mode:

Ensure debug mode is set in your config.py. Then run:

```
flask run --debug
```
Open your browser and navigate to `http://127.0.0.1:5000` to access the application.

### 7. Run Tests

The testing framework used for this application is **Python's built-in** `unittest` **module**.

**Test File Structure**: All test files are stored in the `tests/` directory, and each test file is named following the `test_*.py` convention.


#### Run All Test Files

```
python -m unittest discover -s tests -p "*.py"
```
#### Run a Specific Test File

```
python -m unittest tests/test_dsm.py # Runs the routes for the dsm blueprint
```

### 6. Troubleshooting Tips

- **Database Connection Issues**: Ensure that the `SQLALCHEMY_DATABASE_URI` in `config.py` is correct and that PostgreSQL is running on your system.
- *Dependency Installation Errors*: Double-check the `requirements.txt file` and ensure all dependencies are installed correctly.
- *Debugging JavaScript*: Use the browser's developer tools (e.g., Chrome DevTools) to debug JavaScript scripts.
- *Application Not Running*: Ensure that the virtual environment is activated and all migrations have been applied before starting the app.
- *Tests Not Passing*: Verify that the test database is properly configured and contains the required test data.

## Future Enchancements or Versions

### Phase 1: Immediate Improvements

- **Database Refinement**: Update and refine certain elements of the database, such as the diagnostic steps, to ensure they are more precise and accurate.

- **Interactive Diagnostic Steps**: Enhance the diagnostic steps by adding:
    * Embedded links at each step that direct users to relevant resources or details without leaving the page.
    * A side "pad" feature for users to take notes, add essential elements for each step, and organize their thoughts.
    * Editing and deletion functionality for the notes to ensure flexibility and usability.

- **User Profile Integration**: Extend the pad feature to the user profile page, allowing users to save their notes and progress for future reference.

### Phase 2: Long-Term Goals

- **Database Expansion**: Significantly increase the amount of content in the database, particularly the descriptive text and examples, to offer a more comprehensive resource.
- **Dynamic Route Enhancements**: Convert currently static routes into dynamic ones to provide a more interactive and tailored experience for users.
- **Improve Current Responsive design**
- **Additional Routes**: Add new routes to align more closely with the structure and guidelines of the DSM-5-TR, improving accuracy and user experience.
- **Aesthetic Enhancements**: Improve the visual design 

### Phase 3 Mobile App Development 








