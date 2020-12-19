# Dockerizing Django with Celery, Redis, Gunicorn, and Nginx
Uses gunicorn + nginx + celery + redis.

1. Build the images and run the containers:

    ```sh
    $ docker-compose up -d --build
    ```


Test it out at [http://localhost](http://localhost).
Test check site at [http://localhost/api/site_check?url=example.com](http://localhost/api/site_check?url=example.com)