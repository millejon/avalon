from avalon import create_app


# Test mode should not be enabled unless explicitly enabled at app
# creation.
def test_config():
    assert not create_app().testing
    assert create_app({"TESTING": True}).testing
