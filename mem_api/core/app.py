import logging

from core.settings import AppSettings
from fastapi import FastAPI
from fastapi import Request as FastAPIRequest
from store.database.postgres import Postgres
from store.store import Store


class Application(FastAPI):
    """The main application class.

    This class is responsible for initializing the FastAPI application,
    as well as managing the dependencies and configuration of the application.

    Attributes:
        store (Store): The store instance.
        settings (AppSettings): The application settings.
        logger (logging.Logger): The application logger.
        docs_url (str): The URL of the documentation.
        postgres (Postgres): The database instance.
    """

    store: Store
    settings: AppSettings
    logger: logging.Logger
    docs_url: str
    postgres: Postgres


class Request(FastAPIRequest):
    """Request overrides.

    To correctly prompt the IDE for the `Application` methods.
    """

    app: Application
