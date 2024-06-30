import pytest
from fastapi.testclient import TestClient

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from core.settings import PostgresSettings, S3Settings
from core.setup import setup_app
from core.app import Application
from store.database.postgres import Base


def connect_db(app: Application) -> None:
    """Configuring the connection to the database."""
    app.postgres.settings = PostgresSettings()
    app.postgres._db = Base
    app.postgres._engine = create_async_engine(
        app.postgres.settings.dsn(True),
        echo=False,
        future=True,
    )


def connect_s3(app: Application) -> None:
    app.store.s3.settings = S3Settings()
    app.store.s3.BASE_PATH = (
        f"http://{app.store.s3.settings.s3_host}:{app.store.s3.settings.s3_port}/"
    )


@pytest.fixture(autouse=True)
async def clean_db(application) -> None:
    tables = application.postgres._db.metadata.tables
    query = ""
    for table in tables:
        query += f"TRUNCATE TABLE {table} cascade;"
        await application.postgres.query_execute(text(query))
    await application.postgres._engine.dispose()


@pytest.fixture(autouse=True)
def application() -> Application:
    """Creates and configures the main FastAPI application.

    Returns:
        Application: The main FastAPI application.
    """
    """Creates and configures the main FastAPI application.

       Returns:
           Application: The main FastAPI application.
       """
    app = setup_app()
    connect_db(app)
    connect_s3(app)
    return app


@pytest.fixture()
def client(application) -> TestClient:
    return TestClient(application)
