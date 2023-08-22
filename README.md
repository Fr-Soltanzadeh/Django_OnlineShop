# Django_OnlineShop
Django project 

initialization:
- creaate virtual enviroment and activate it 
python -m venv venv
./venv/Scripts/activate.bat
- install requirements
pip install -r requirements.txt
-run redis and celery
Redis:
redis-cli
Celery:
celery -A OnlineShop worker -l info

commands:
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

Coverage Test:
coverage run --source='.' manage.py test .
coverage report

Deploy:
docker-compose up --build

