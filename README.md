# Product aggregator

### Requirements:
- Python 3.10
- redis

### DB:
```
db.sqlite3
```

### Environment variables
Create `.env` file in base project directory. Use `.env-example` template file.

### Run:
```
$ python3 -m venv .env
$ source .env/bin/activate
(.env) $ pip install -r requirements.txt
(.env) $ cd product_aggregator/
(.env) $ python manage.py makemigrations
(.env) $ python manage.py migrate
(.env) $ python manage.py runserver
```

### Celery
Requires redis server started.
```console
$ sudo systemctl start redis-server.service
```
Start the Celery worker and beat processes in separate terminal windows:
```console
$ celery -A product_aggregator worker -l info
$ celery -A product_aggregator beat -l info
```
Task `update_product_offers` checks for new product offers via Applifting API every 60 seconds.

### API Usage

Add and register new product:
- POST `http://127.0.0.1:8000/api/products/`

    ```
    {
        "name": "string",
        "description": "string"
    }
    ```

Get products:
- GET `http://127.0.0.1:8000/api/products/`

Single product operations:
- GET | PUT | DELETE `http://127.0.0.1:8000/api/products/<uuid:product_id>/`

Get product offers:
- GET `http://127.0.0.1:8000/api/<uuid:product_id>/offers/`
