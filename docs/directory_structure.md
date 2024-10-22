# Directory Structure Using a Blueprint Structure

This would be the directory structure if I decided to use a blueprint structure for my routes (separated by files)

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
