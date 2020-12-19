# Dockerizing Django with Celery, Redis, Gunicorn, and Nginx
Uses gunicorn + nginx + celery + redis.

1. Build the images and run the containers:

    ```sh
    $ docker-compose up -d --build
    ```

2. Run the collectstatic management command:

    ```sh
    $ docker-compose exec web python manage.py collectstatic
    ```


1. Test it out at [http://localhost](http://localhost)
1. Test check site at [http://localhost/api/site_check?url=example.com](http://localhost/api/site_check?url=example.com)
1. Admin at [http://localhost/admin](http://localhost/admin) 
```sh
username: admin
password: 123
```

1. working server at [http://91.210.169.153](http://91.210.169.153)