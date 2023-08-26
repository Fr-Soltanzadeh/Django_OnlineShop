# Django Online Shop

Welcome to the Django Online Shop project!

## About project

This is my first comprehensive django project. This Django-based web application provides a seamless online shopping experience. It aims to be a feature-rich, user-friendly, and secure e-commerce platform.
If you have any questions, suggestions, or issues regarding the project, please feel free to reach out to me.

- [f.soltanzade72@gmail.com](mailto:f.soltanzade72@gmail.com)
- [![LinkedIn](https://commons.wikimedia.org/wiki/File:LinkedIn_logo_initials.png)](https://www.linkedin.com/in/farzaneh-soltanzadeh-28a193280/)

## Technologies Used

- Django: The web framework used for building the online shop project.
- PostgreSQL: The database management system used for storing data.
- Redis: Used for caching and as the Celery message broker.
- Celery: Used for task management, such as sending emails to customers asynchronously.
- Docker: Used for containerization and deployment of the project.
- Gunicorn: A Python WSGI HTTP server used for serving the Django application.
- Nginx: A web server used as a reverse proxy and for serving static files.
- HTML5, CSS, and JavaScript: The trio of technologies employed for front-end development, providing structure, styling, and interactivity to the web pages.
- Yasg: Swagger library used for API documentation.

## Initialization

To get started with the project, follow these steps:

1. Create a virtual environment and activate it:

   - On Windows:
     ```shell
     python -m venv venv
     .\venv\Scripts\activate.bat
     ```
   - On Linux:
     ```shell
     python -m venv venv
     source venv/bin/activate
     ```

2. Install the project requirements:
   
   ```shell
   pip install -r requirements.txt
   
## Running the Project

To run the project locally, perform the following commands:

1. Start Redis for caching and as the Celery message broker:

   ```shell
   sudo service redis-server start

2. Start the Celery worker:
   - On Windows:
    ```shell
    celery -A OnlineShop worker -l info -P solo
    ```
   - On Linux:
    ```shell
    celery -A OnlineShop worker -l info
    ````

3. Apply database migrations:

    ```shell
    python manage.py makemigrations
    python manage.py migrate
    ```

4. Run the development server:

    ````shell
    python manage.py runserver
    ````


## Test Coverage

To run the unit tests and obtain the test coverage report, use the following command:


````shell
coverage run --source='.' manage.py test .
coverage report

````

The coverage report will provide information about the test coverage achieved by the project which covers more than 90% of the codebase.

## Deployment

The project can be deployed using Docker, Gunicorn, and Nginx. To deploy the project, use the following command:

```shell
docker-compose up --build
````

## API Documentation

API documentation for the project is available through Swagger.


## Contributing

We welcome contributions from the community to improve the project. If you would like to contribute, please follow these steps:

1. Fork the repository and clone it to your local machine.
2. Create a new branch for your feature or bug fix.
3. Make the necessary changes and commit them.
4. Push your changes to your forked repository.
5. Submit a pull request describing the changes you've made.
