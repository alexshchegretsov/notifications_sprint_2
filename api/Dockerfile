# Скачиваем официальный образ с Docker Hub
FROM python:3.8.10-slim

# устанавливаем пременные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH $APP_HOME

# устанавливаем psycopg2 зависимости
RUN apt-get update \
    && apt-get upgrade -y && apt-get install -y gcc python3-dev supervisor

# Обновляем `pip`
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install pipenv
RUN pipenv run pip install psycopg2-binary

# Устанавливаем зависимости
COPY ./Pipfile .
RUN pipenv lock
RUN pipenv install --system --deploy --ignore-pipfile

# Копируем настройки supervisor
COPY ./supervisord.conf /etc/supervisor/conf.d/supervisord.conf

#########
# FINAL #
#########

# Запускаем приложение от пользователя `app`,
# т.к. от пользователя `root` запускать приложение совершенно не секурно >.<

# создатем соответствующие каталоги
ENV APP_HOME=/home/app/api
RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME

# создаем пользователя `app`
RUN groupadd -g 1234 -r app && \
    useradd -u 1234 -r -g app -d /home/app -s /sbin/nologin -c "Docker image user" app


# копируем проект
COPY . $APP_HOME

# даем права на все файлы приложения пользователю `app`
RUN chown -R app:app $APP_HOME
RUN chmod +x $APP_HOME/async_api.py

# меняем на пользователя `app`
USER app

# запускаем supervisord
CMD ["/usr/bin/supervisord"]