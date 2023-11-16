import sqlite3
import click
from flask import current_app, Flask, g


def get_database_connection() -> sqlite3.Connection:
    """Return current database connection or, if one does not exist,
    open and return a new database connection.
    """
    if "database" not in g:
        g.database = sqlite3.connect(
            database=current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        # Return database rows as dictionaries.
        g.database.row_factory = sqlite3.Row

    return g.database


def close_database_connection(e=None) -> None:
    """Close current database connection."""
    # Check if there is an open database connection.
    database = g.pop("database", None)

    if database is not None:
        database.close()


def initialize_database() -> None:
    """Initialize database according to schema.sql."""
    database = get_database_connection()

    with current_app.open_resource("schema.sql") as schema:
        database.executescript(schema.read().decode("utf8"))


def execute_read_query(query: str, data: tuple = ()) -> list:
    """Execute read query on database and return results."""
    return get_database_connection().execute(query, data).fetchall()


def execute_write_query(query: str, data: tuple = ()) -> int:
    """Execute write query on database and return database id of new
    entity.
    """
    database = get_database_connection()
    new_entity_id = database.execute(query, data).lastrowid
    database.commit()

    return new_entity_id


@click.command("initialize-database")
def initialize_database_cli_command() -> None:
    """Initialize database from the command line."""
    initialize_database()
    click.echo("Database initialized.")


def initialize_app(app: Flask) -> None:
    """Initialize application with database-related rules and
    commands.
    """
    # Close database connection after returning a response.
    app.teardown_appcontext(close_database_connection)
    # Add initialize-database CLI command to app.
    app.cli.add_command(initialize_database_cli_command)
