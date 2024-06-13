# Toolbox-backend Application

#### README

Can't run the application without the config/config.py file. 
Please create a config.py in the config directory of the project.

```python3
# config file example

import os

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    ENV: str = "development"
    DEBUG: bool = True
    APP_HOST: str = ""
    APP_PORT: int = 8000
    WRITER_DB_URL: str = "mysql+aiomysql://"
    READER_DB_URL: str = "mysql+aiomysql://"
    JWT_SECRET_KEY: str = "YOUR SECRET KEY"
    JWT_ALGORITHM: str = ""
    SENTRY_SDN: str = ""
    CELERY_BROKER_URL: str = "amqp://"
    CELERY_BACKEND_URL: str = "redis://"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379


class TestConfig(Config):
    WRITER_DB_URL: str = "mysql+aiomysql://"
    READER_DB_URL: str = "mysql+aiomysql://"


class LocalConfig(Config):
    ...


class ProductionConfig(Config):
    DEBUG: bool = False


def get_config():
    env = os.getenv("ENV", "local")
    config_type = {
        "test": TestConfig(),
        "local": LocalConfig(),
        "prod": ProductionConfig(),
    }
    return config_type[env]


config: Config = get_config()

```

#### How to run the application

```poetry install && poetry shell```

```python3 main.py```

#### How to run the application with PM2

```pm2 start main.py --interpreter python3 --name toolbox-backend```