import pytest
import sqlite3

import avalon.database as db
from avalon.data import database as data


# get_database_connection() should return he same database connection
# each time it is called within an application's context.
def test_get_database_connection(app):
    with app.app_context():
        database = db.get_database_connection()
        assert database is db.get_database_connection()


# The database connection should not be open outside of an application's
# context.
def test_close_database_connection(app):
    with app.app_context():
        database = db.get_database_connection()

    with pytest.raises(sqlite3.ProgrammingError) as error:
        database.execute("SELECT 1")

    assert "closed" in str(error.value)


tables = list(data.keys())


# execute_read_query() should execute the select query passed and return
# the expected results.
@pytest.mark.parametrize("table", tables)
def test_execute_read_query(app, table):
    with app.app_context():
        database = db.get_database_connection()
        entity_id = database.execute(data[table]["queries"]["write"],
                                     data[table]["test_data"]).lastrowid
        database.commit()

        entity = db.execute_read_query(query=data[table]["queries"]["read"]["all"],
                                       data=(entity_id,))

        for index, value in enumerate(data[table]["columns"]):
            assert entity[0][value] == data[table]["test_data"][index]


# execute_write_query() should execute the insert query passed and
# return the database id of the new entity.
@pytest.mark.parametrize("table", tables)
def test_execute_write_query(app, table):
    with app.app_context():
        entity_id = db.execute_write_query(query=data[table]["queries"]["write"],
                                           data=data[table]["test_data"])

        database = db.get_database_connection()
        entity = database.execute(data[table]["queries"]["read"]["all"],
                                  (entity_id,)).fetchone()

        assert entity["id"] == entity_id
        for index, value in enumerate(data[table]["columns"]):
            assert entity[value] == data[table]["test_data"][index]


# The "initialize-database" CLI command should call
# initialize_database() and output "Database initialized." upon
# completion.
def test_initialize_database_cli_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_initialize_database():
        Recorder.called = True

    monkeypatch.setattr("avalon.database.initialize_database",
                        fake_initialize_database)
    result = runner.invoke(args=["initialize-database"])
    assert Recorder.called
    assert "Database initialized." in result.output
