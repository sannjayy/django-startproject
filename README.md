# Django Init Project v1.0
- Znas Solutions Team

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

## Enabling the ASGI Mode (Web Socket)

To activate ASGI mode, enable `USE_ASGI_MODE=True` and install Django Channels:


```bash
pip install 'channels[daphne]'
```

Redis Channels layers are also required for this. To enable Redis, set `ENABLE_REDIS=True` and `REDIS_CHANNEL_LAYER=True`, and install Django Channels Channel Layers:

```bash
pip install channels-redis
```
