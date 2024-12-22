import pytest
from src.rag_pipeline.llms import get_llm

def test_llm_basic():
    llm = get_llm()
    resp = llm.call("Hello world?")
    assert isinstance(resp, str)
    assert len(resp) > 0
