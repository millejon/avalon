import pytest
import os
import tempfile

from avalon import create_app

@pytest.fixture
def app(tmp_path):
    # Create a temporary database for testing purposes.
    database_file, database_path = tempfile.mkstemp()

    app = create_app(test_config={"TESTING": True,
                                  "DATABASE": database_path,
                                  "MUSIC_DIRECTORY": tmp_path})

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
