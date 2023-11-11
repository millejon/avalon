import os
from flask import Flask


def create_app(test_config: dict = None) -> Flask:
    """Initialize and return the Avalon application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="should_put_your_own_value_in_config",
        DATABASE=os.path.join(app.instance_path, "avalon.sqlite"),
    )

    if test_config is None:
        # Load instance config when not testing.
        app.config.from_pyfile("config.py", silent=True)
    else:
        # Load test config when testing.
        app.config.from_mapping(test_config)

    # Ensure that instance subdirectory exists in project directory.
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app
