# REVIXA Backend

This repository contains the API developed using Django REST Framework for the REVIXA application, an interactive system for reviews and social interactions.

## Table of Contents
  - [User Stories](#user-stories)
  - [Database](#database)
  - [Technologies Used](#technologies-used)
  - [Validation](#validation)
  - [Testing](#testing)
  - [Credits](#credits)

## User Stories

This project was designed with a focus on user interaction with reviewed content and social interactions, including:
- As a user, I want to be able to register, authenticate, and manage my profile to interact with the platform.
- As an administrator, I want to manage reviews, posts, and interactions to maintain content integrity.

## Database

The database model includes:
- **User:** Stores user information.
- **Review:** Stores reviews made by users.
- **Post:** Related to reviews for discussions and social interactions.
- **Like:** Allows users to like posts.

![Database Model](docs/drf_models_revixa.png)

#### User Model

- The User model contains information about users and is managed through the `django.contrib.auth` library for authentication and user management.
- Admin users can create `Review` entries.
- Regular users can create `Post` entries and `Like` other users' `Post` entries.
- One-to-many relation with the `Review` model through the `author` field (admin users).
- One-to-many relation with the `Post` model through the `author` field (regular users).
- One-to-many relation with the `Like` model through the `user` field (regular users).

#### Review Model

- The `Review` model contains the following fields: `title`, `content`, `framework_name`, `framework_version`, `created_at`, `updated_at`, and `author`.
- ForeignKey relation with the `User` model through the `author` field, which only allows admin users to create reviews.

#### Post Model

- The `Post` model represents user-created posts associated with specific `Review` entries. It contains the following fields: `content`, `created_at`, `updated_at`, `author`, and `review`.
- ForeignKey relation with the `User` model through the `author` field, allowing regular users to create posts.
- Optional ForeignKey relation with the `Review` model through the `review` field, indicating the specific review the post relates to.

#### Like Model

- The `Like` model represents user interactions with `Post` entries, indicating that a user liked a specific post. It contains the following fields: `user`, `post`, and `created_at`.
- ForeignKey relation with the `User` model through the `user` field.
- ForeignKey relation with the `Post` model through the `post` field.

## Technologies Used

### Languages & Frameworks

- Python
- Django

### Libraries & Tools

- [Django REST Framework](https://www.django-rest-framework.org/) - API toolkit. **Justification**: Used to build the back-end API.
- [dj-rest-auth](https://dj-rest-auth.readthedocs.io/en/latest/) - Authentication library. **Justification**: Used to provide endpoints for user authentication.
- [djangorestframework-simplejwt](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/) - JSON Web Token authentication. **Justification**: Used for JWT-based authentication.
- [django-cors-headers](https://pypi.org/project/django-cors-headers/) - CORS handling for Django. **Justification**: Used to handle Cross-Origin Resource Sharing (CORS) for API requests.
- [Gunicorn](https://gunicorn.org/) - WSGI HTTP server. **Justification**: Used as a server for deploying the project.
- [Psycopg2](https://www.psycopg.org/docs/) - PostgreSQL database adapter. **Justification**: Used to connect to and interact with PostgreSQL databases.
- [ElephantSQL](https://www.elephantsql.com/) - Database hosting service. **Justification**: Used as a cloud-based PostgreSQL database for the deployed project.
- [Python-dotenv](https://pypi.org/project/python-dotenv/) - Environment variable management. **Justification**: Used to manage environment variables during development.
- [dj-database-url](https://pypi.org/project/dj-database-url/) - Database configuration utility. **Justification**: Simplifies database configuration for different environments.
- [Git](https://git-scm.com/) - Version control system. **Justification**: Used for version control and to push code to GitHub.
- [GitHub](https://github.com/) - Cloud-based hosting service. **Justification**: Used as a remote repository to store project code.
- [Graphviz](https://graphviz.org/) - Graph visualization software. **Justification**: Used for creating database model diagrams.
- [Heroku](https://www.heroku.com/) - Cloud platform for deployment. **Justification**: Used to deploy the project in a live environment.
- [tzdata](https://pypi.org/project/tzdata/) - Time zone data for Python. **Justification**: Used for managing time zones in the application.
