---
applyTo: '**'
---
# Project Context
This project is a Django application designed to provide a RESTful API for managing a collection of resources. The API follows the principles of REST and is designed to be easily consumable by frontend applications.

## Folder Structure
The project follows a standard Django folder structure:

```
project/
├── api/
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   └── views.py
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── manage.py
```
## Key Components
- **api/**: Contains the Django app responsible for the API functionality.
- **migrations/**: Contains database migration files.
