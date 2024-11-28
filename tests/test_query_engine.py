import pytest
from pathlib import Path
from app.core.query_engine import QueryEngine

@pytest.fixture
def query_engine():
    return QueryEngine()

def test_basic_query(query_engine):
    # This is a basic test. You'll need to add a sample PDF to test with
    question = "What is the main topic of the document?"
    response = query_engine.query(question)
    assert isinstance(response, str)
    assert len(response) > 0