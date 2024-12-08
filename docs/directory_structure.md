# Directory Structure Using a Blueprint Structure

This would be the directory structure if I decided to use a blueprint structure for my routes (separated by files)

**V1**

```
your_project/
│
├── app.py
├── config.py
├── requirements.txt
├── /templates
├── /static
└── /blueprints
    ├── __init__.py
    ├── homepage/
    │   ├── __init__.py
    │   └── routes.py
    ├── users/
    │   ├── __init__.py
    │   └── routes.py
    ├── dsm/
    │   ├── __init__.py
    │   └── routes.py
    └── psychopathology/
        ├── __init__.py
        └── routes.py
```

**V2**
```
Src/
├── blueprints/
│   ├── homepage/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── users/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── dsm/
│   │   ├── __init__.py
│   │   └── routes.py
│   └── psychopathology/
│       ├── __init__.py
│       └── routes.py
├── static/
│   ├── css/
│   ├── images/
│   └── js/
├── templates/
│   ├── homepage/
│   │   └── home.html
│   ├── users/
│   │   ├── signup.html
│   │   ├── signin.html
│   │   ├── profile.html
│   ├── dsm/
│   │   ├── dsm.html
│   │   ├── categories.html
│   └── psychopathology/
│       ├── sign.html
│       └── symptom.html
├── __init__.py
├── app.py
├── models.py
├── forms.py
├── secret_keys.py

```

**V3**
```
your_project/
│
├── database/
│   ├── diagrams/
│   └── schema.sql
│
├── docs/
│   ├── Capstone-guidelines.pdf
│   └── README.md
│
├── venv/
│
├── .gitignore
│
├── requirements.txt
│
└── src/
    ├── application/
    │   ├── __init__.py       # Application Factory lives here
    │   ├── models.py         # Database models
    │   ├── forms.py          # WTForms classes
    │   ├── secret_keys.py    # Secret keys for security
    │   ├── static/
    │   ├── templates/
    │   └── blueprints/
    ├── config.py             # Configuration settings
    └── app.py                # Main entry point for running the app
```

**CURRENT VERSION**
```
my_project/
│
├── database/
|   |__ __init__.py
│   ├── diagrams/
│   └── schema.sql
|   |__ categories.json
|   |__ clusters.json
|   |__ disorders.json
|   |__ populate_data.py
|   |__ populate_diff_diagnosis.py
|   |__ more json files ...
│
├── docs/
│   ├── Capstone-guidelines.pdf
│   └── README.md
│
├── venv/
│
├── .gitignore
│
├── requirements.txt
│
└── src/
    |__ __init__.py
    ├── application/ 
    │   └── __init__.py   
    │   ├── models.py         # Database models
    │   ├── forms.py          # WTForms classes
    │   ├── secret_keys.py    # Secret keys for security
    │   ├── static/
    |   |__|__css
    |   |__|__|__style.css
    |   |__|__js
    |   |__|__|__autocomplete.js
    │   └── blueprints/
    ├── config.py             # Configuration settings
    └── main/ 
    |   |__ __init__.py
    │   ├── templates/
    │   ├── app.py
                  # Main entry point for running the app
```
