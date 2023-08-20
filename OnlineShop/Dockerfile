FROM python:3.10
LABEL Maintainer="f.soltanzade72@gmail.com"
LABEL Owner="Farzaneh Soltanzadeh"
LABEL version="v1"
WORKDIR /djangoonlineshop
COPY requirements.txt .
RUN pip install -U pip
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# CMD ["gunicorn", "A.wsgi", ":8000"]