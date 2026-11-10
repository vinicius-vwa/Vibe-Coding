from src.database import get_database_url, get_engine


def test_database_url_defaults_to_sqlite():
    url = get_database_url("sqlite:///test.db")
    assert url.startswith("sqlite")


def test_engine_is_created():
    engine = get_engine("sqlite:///test.db")
    assert engine is not None
