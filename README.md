# Django Init Project v1.0
- Znas Solutions Team

---

## Enabling Celery & Celery Beat

To activate Celery, enable `ENABLE_CELERY=True` and make sure redis is working properly.
 run the following commands:

```bash
pip install celery
python manage.py makemigrations
python manage.py migrate
```

open a new instance of terminal and fun the following code:

```bash
// Windows
source zenv/Scripts/activate && celery -A project worker -l info -P eventlet 

// Ubuntu | Mac
celery -A project worker -l info
```



## Enabling the ASGI Mode (Web Socket)

To activate ASGI mode, enable `USE_ASGI_MODE=True` and install Django Channels:


```bash
pip install 'channels[daphne]'
```

Redis Channels layers are also required for this. To enable Redis, set `ENABLE_REDIS=True` and `REDIS_CHANNEL_LAYER=True`, and install Django Channels Channel Layers:

```bash
pip install channels-redis
```
