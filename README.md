# Аннотация


Схема проекта: [Parse](https://postimg.cc/47qmNZJN)



### Описание структуры

**AirFlow**

`dags`: задачи которые выполняем по расписанию.

`plugins`: основной код проекта.

`plugins/utils/db.py`: запись DataFrame в базу данных.

`plugins/utils/parse_<name>.py`: парсеры сайтов.

`plugins/utils/tools.py`: общие функции для парсеров.

`plugins/airflow.cfg`: конфигурационный файл для AirFlow.

`plugins/Dockerfile`: докерфайл для построения AirFlow, окружение
строиться в нем.

`plugins/entrypoint.sh`: запускает работу AirFlow, запуск прописан
в `plugins/Dockerfile`.

`plugins/unittests.cfg`: юниттесты для AirFlow.

`plugins/webserver_config.py`: конфигурационный файл для AirFlow.

**Другие**

`docker-compose.yml`: сборка Docker микросервисов.

`poetry.lock` & `pyproject.toml`: конфигурационные файлы менеджера пакетов poetry.


### Предподготовка


Требования для [AirFlow](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html).

Установить Docker on Linux: https://docs.docker.com/engine/install/ubuntu/.

Установить Docker on Windows: https://docs.docker.com/desktop/windows/install/

Установить Docker Compose: https://docs.docker.com/compose/install/


### Установка окружения


**Install poetry**

```shell
curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
```

**Add path to poetry**

```shell
export PATH="$HOME/.poetry/bin:$PATH"
```

Войти в дирректорию с файлом `.toml` и установить окружение:

```shell
poetry install
```

Войти в окружение:

```shell
poetry shell
```

Далее работаем в созданном окружении.


### Запустить AirFlow


Переходим в дирректорию, где лежит файл `docker-compose.yml`. В консоле
вбиваем команду:

```shell
docker-compose up --build -d
```

После чего должны подняться 3 контейнера, проверить можно командой:

```shell
docker ps
```

Должно быть три ocker контейнера:

1. `<name_project>_airflow_1`: сервис AirFlow.
2. `<name_project>_database_1`: база мета-данных для AirFlow.
3. `<name_project>_postgres_1`: база данных.


### Создать юзера AirFlow


Необходимо войти в контейнер с AirFlow:

```shell
docker exec -it <name_container> bash
```

Внутри контейнера создаем юзера:

```shell
airflow users create -e example@gmail.com -f airflow -l airflow -p test -r Admin -u user
```


### AirFlow интерфейс


Вбиваем в браузер `localhost:8080` и логинимся. Логин и пароль мы указывали
на предыдущем шаге, при создании юзера.


### Создание соединения с базой данных


Перед тем как добавлять DAGs, необходимо создать соединение с базой данных
в интерфейсе AirFlow. Заходим в интерфейс AirFlow, вверху в панеле меню нажимаем
`Admin > Connections`, далее нажимаем на `+`.

**Заполняем поля**

```buildoutcfg
Connection id: <any name> (это будет наш CONN_ID в /dags/load_<any_name>.py)

Connection Type: Postgress

Host: postgres (docker-compose.yml > название контейнера (в нашем случае postgres)

Schema: from POSTGRES_DB in docker-compose.yml

Login: from POSTGRES_USER in docker-compose.yml
name
Password: from POSTGRES_PASSWORD in docker-compose.yml

Port: 5432 from docker-compose.yml > postgres > ports
```

Сохраняем. После этого проект готов к работе.