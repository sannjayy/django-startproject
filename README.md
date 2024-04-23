# django-startproject v1.0

Set up a fresh Django project to build your large or small app, with everything configured to be controlled simply from environment variables. 

# How to Start?

- Clone or download [django-startproject](https://github.com/sannjayy/django-startproject) 

`git clone git@github.com:sannjayy/django-startproject.git`

- Create a virtual environment
```bash
python -m venv zenv
source zenv/Scripts/activate # Windows
source zenv/bin/activate # Mac
```

- Install basic requirements
```bash
pip install -r requirements.txt

# OR INITIAL INSTALLATION 
pip install --upgrade pip
pip install --upgrade setuptools
pip install django "django-phonenumber-field[phonenumberslite]" django-import-export django-filter django-cleanup gunicorn whitenoise django-cors-headers python-dotenv
```

- To create a .env file from the .env.Example file

```python
ENABLE_TEST_PANEL = True  # It will enable the testing panel (http://localhost:8000/test/admin).
ENABLE_DRF = False # It will enable the django rest framework and simple-jwt.
ENABLE_SWAGGER = False # It Enables Swagger-UI (drf-yasg)
USE_ASGI_MODE = False # Need to enable the redis for django channels // pip install 'channels[daphne]'
ENABLE_CRON_JOBS = False # Enables Django Crontab // pip install django_crontab
ENABLE_CELERY = False # enables the celery
ENABLE_CELERY_BEAT = False # Enables the celery beat
ENABLE_MONGO_ENGINE = False # Enables the MongoDB
```
- Start Server

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

python manage.py runserver
```

---

## Enabling Database (PostgreSQL, MySQL, SQLite)

To use **PostgreSQL**, set `DB_TYPE = 'PostgreSQL'` and `ENABLE_DB = True` make sure you have installed `psycopg2`:

```bash
# stand-alone package
pip install psycopg2
# OR binary package
pip install psycopg2-binary
```

To use **MySQL**, set `DB_TYPE = 'MySQL'` and `ENABLE_DB = True` make sure you have installed `pymysql`:

```bash
pip install pymysql
```

To use **SQLite**, set `ENABLE_DB = False` 

It will automatically use SQLite by default.

---

## Enabling the Mongo Engine

Install `mongoengine` 

```bash
pip install mongoengine
```

Apply the following changes to your `.env` file.

```python
ENABLE_MONGO_ENGINE = True
MONGODB_CONNECTION_STRING = 'mongodb://username:password@host:27017/db?authSource=admin'
```

You can test the connection from `TEST_PANEL`.

---

## Enabling the ASGI Mode (WebSocket)

To activate ASGI mode, enable `USE_ASGI_MODE=True` and install Django Channels:


```bash
pip install 'channels[daphne]'
```

Redis Channels layers are also required for this. To enable Redis, set `ENABLE_REDIS=True` and `REDIS_CHANNEL_LAYER=True`, and install Django Channels Channel Layers:

```bash
pip install channels-redis
```

You can test the socket connections from `TEST_PANEL`.

---

## Enabling Celery & Celery Beat

To activate Celery, enable `ENABLE_CELERY=True` and make sure Redis is working properly. Run the following commands:

```bash
pip install celery
python manage.py makemigrations
python manage.py migrate
```

Open a new instance of terminal and run the following code:

```bash
# Windows
source zenv/Scripts/activate && celery -A project worker -l info -P eventlet 

# Ubuntu | Mac
celery -A project worker -l info
```

You can test the celery tasks from `TEST_PANEL`.

## For Enabling Celery Beat

Enable `ENABLE_CELERY_BEAT=True` and then install:

```bash
pip install django-celery-beat
pip install django-celery-results
python manage.py makemigrations
python manage.py migrate
```

Open a new instance of terminal and run the following code:

```bash
# Windows
source zenv/Scripts/activate && celery -A project beat -l info  

# Ubuntu | Mac
celery -A project beat -l info
```

--- 
---

- 🌏 [GitHub Repo](https://github.com/sannjayy/django-startproject) 
- 🌏 [Website](https://www.sanjaysikdar.dev) 
- 📫 <me@sanjaysikdar.dev>
- 📖 [read.sanjaysikdar.dev](https://read.sanjaysikdar.dev)
- 📦 [pypi releases](https://pypi.org/user/sannjayy/) | [npm releases](https://www.npmjs.com/~sannjayy)

---

[![](https://img.shields.io/github/followers/sannjayy?style=social)](https://github.com/sannjayy)  
Developed with ❤️ by *[sanjaysikdar.dev](https://www.sanjaysikdar.dev)*.
