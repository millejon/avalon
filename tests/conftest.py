import pytest
import tempfile
import os

from avalon import create_app
from avalon.database import initialize_database


@pytest.fixture
def app(tmp_path):
    # Create a temporary database for testing purposes.
    database_file, database_path = tempfile.mkstemp()

    app = create_app(test_config={"TESTING": True,
                                  "DATABASE": database_path,
                                  "MUSIC_DIRECTORY": tmp_path})

    with app.app_context():
        initialize_database()

    yield app

    # Close and delete temporary database.
    os.close(database_file)
    os.unlink(database_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
