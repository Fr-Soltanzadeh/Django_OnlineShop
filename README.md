# Django Online Shop

Welcome to the Django Online Shop project!

## About project

This is my first comprehensive django project. This Django-based web application provides a seamless online shopping experience. It aims to be a feature-rich, user-friendly, and secure e-commerce platform.
If you have any questions, suggestions, or issues regarding the project, please feel free to reach out to me.

[f.soltanzade72@gmail.com](mailto:f.soltanzade72@gmail.com)

[<svg alt="LinkedIn" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="111" height="28" role="img" aria-label="LINKEDIN"><title>LINKEDIN</title><g shape-rendering="crispEdges"><rect width="111" height="28" fill="#0077b5"/></g><g fill="#fff" text-anchor="middle" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" text-rendering="geometricPrecision" font-size="100"><image x="9" y="7" width="14" height="14" xlink:href="data:image/svg+xml;base64,PHN2ZyBmaWxsPSJ3aGl0ZSIgcm9sZT0iaW1nIiB2aWV3Qm94PSIwIDAgMjQgMjQiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHRpdGxlPkxpbmtlZEluPC90aXRsZT48cGF0aCBkPSJNMjAuNDQ3IDIwLjQ1MmgtMy41NTR2LTUuNTY5YzAtMS4zMjgtLjAyNy0zLjAzNy0xLjg1Mi0zLjAzNy0xLjg1MyAwLTIuMTM2IDEuNDQ1LTIuMTM2IDIuOTM5djUuNjY3SDkuMzUxVjloMy40MTR2MS41NjFoLjA0NmMuNDc3LS45IDEuNjM3LTEuODUgMy4zNy0xLjg1IDMuNjAxIDAgNC4yNjcgMi4zNyA0LjI2NyA1LjQ1NXY2LjI4NnpNNS4zMzcgNy40MzNjLTEuMTQ0IDAtMi4wNjMtLjkyNi0yLjA2My0yLjA2NSAwLTEuMTM4LjkyLTIuMDYzIDIuMDYzLTIuMDYzIDEuMTQgMCAyLjA2NC45MjUgMi4wNjQgMi4wNjMgMCAxLjEzOS0uOTI1IDIuMDY1LTIuMDY0IDIuMDY1em0xLjc4MiAxMy4wMTlIMy41NTVWOWgzLjU2NHYxMS40NTJ6TTIyLjIyNSAwSDEuNzcxQy43OTIgMCAwIC43NzQgMCAxLjcyOXYyMC41NDJDMCAyMy4yMjcuNzkyIDI0IDEuNzcxIDI0aDIwLjQ1MUMyMy4yIDI0IDI0IDIzLjIyNyAyNCAyMi4yNzFWMS43MjlDMjQgLjc3NCAyMy4yIDAgMjIuMjIyIDBoLjAwM3oiLz48L3N2Zz4="/><text transform="scale(.1)" x="655" y="175" textLength="670" fill="#fff" font-weight="bold">LINKEDIN</text></g></svg>](https://www.linkedin.com/in/farzaneh-soltanzadeh-28a193280/)

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
