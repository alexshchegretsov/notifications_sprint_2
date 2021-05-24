## Запуск проекта
### Запуск сервиса "Notify" (docker-compose)
1. Для запуска `Notification service`необходимо:
    * Создать `.env` файл согласно [инструкции п1.](#start-notify-local)
    * Запустить в консоли команду:
      ```bash
      $ sudo docker-compose up -d
      ```
    
2. #### Сервисы которые запустятся:
    1. `api_service` - Сервис получающий `event` по API и далее передаётся обработчику
    2. `rabbitmq_server` - Брокер сообщений 
    3. `admin_panel` - Админ панель для ручного управления рассылками
    4. `Celery` - фреймворк управляющий задачами
    5. `notify_db` - база данных
    
3. После того как все сервисы успешно стартуют, они будут доступны по адресам:
    ##### API service `http://<ip-addres>:<port>/`
    ##### Admin panel `http://<ip-addres>:8000/`
    ##### RabbitMQ panel `http://<ip-addres>:15672/`
    
### Start notify local
#### Запуск сервиса "Notify" (на локальном компе)

1. Необходимо в корне директории `notifications_sprint_1` создать `.env` файл со следующим содержимым:  
   ```dotenv
        # App settings
        CONFIG_ENV=<django_settings_by_env> # DEV by default. Choice: PROD, DEV
        DJANGO_SECRET_KEY=<secret_key>
        
        # Databse connections settings
        PG_DBNAME=<db_name>
        PG_USER=<db_username>
        PG_PASSWD=<db_user_password>
        PG_HOST=<URL_address>               # 127.0.0.1 by default
        PG_PORT=<port_number>               # 5432 by default
   
        SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://${PG_USER}:${PG_PASSWD}@${PG_HOST}:${PG_PORT}/${PG_DBNAME}

        AUTH_DB_URL=<URL_address_to_auth_db>
        
        # SMTP settings
        SMTP_SSL_PORT=<smtp_port>
        SMTP_SERVER=<smtp_server>
        SENDER_EMAIL=<smtp_user_email>
        SENDER_PASSWORD=<smtp_user_password>
        
        API_PORT=3000
        
        # RabbitMQ connections settings
        RMQ_USER=<username>
        RMQ_PASSWORD=<password>
        RMQ_VHOST=<vhost_name>
        RMQ_HOST=<host>                     # localhost by default
        RMQ_PORT=<port>                     # 5672 by default
    ```
   Сгенерировать `SECRET_KEY` можно следующим способом:
   ```python
   >>> import secrets
   >>> secrets.token_urlsafe(32)
   ```
2. Переменные окружения:
   ```dotenv
    PYTHONUNBUFFERED=1;
    DJANGO_SETTINGS_MODULE=config.settings.dev
   ```
3. Установка необходимый пакетов:
   ```bash
   $ pipenv install --ignore-pipfile
   ```
4. Локальный запуск RabbitMQ (используется как `broker` для `Celery`)
   ```bash
   $ sudo docker run -d -p 5672:5672 rabbitmq
   ```
   #### Setting up RabbitMQ
   * https://docs.celeryproject.org/en/stable/getting-started/brokers/rabbitmq.html#setting-up-rabbitmq
   ```bash
   $ sudo docker exec <CONTAINER_ID> rabbitmqctl add_user <username> <password>
   $ sudo docker exec <CONTAINER_ID> rabbitmqctl add_vhost <vhost_name>
   $ sudo docker exec <CONTAINER_ID> rabbitmqctl set_user_tags <username> <user_tag>
   $ sudo docker exec <CONTAINER_ID> rabbitmqctl set_permissions -p <vhost_name> <username> ".*" ".*" ".*"
   ```
   `CONTAINER_ID` можно выяснить набрав в консоле команду:
   ```bash
   $ sudo docker ps
   ```
5. Запуск `Celery`:
   Находясь в директории `notifications_sprint_1/notify` выполнить в терминале:
   ```bash
   $ celery -A config worker -l INFO
   ```