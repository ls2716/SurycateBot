import pytest

from surycate_bot_ls2716.llm import get_llm


def test_llm_initialisation():
    """Test llm initialisation"""
    llm = get_llm()
    print(type(llm))
    assert type(llm).__name__ == "RunnableBinding"


@pytest.fixture(scope="module")
def llm():
    """Open an llm process"""
    llm = get_llm(temperature=0)
    return llm


def test_simple_completion(llm):
    """Test simple completion"""
    completion = llm.invoke("What is two plus two?")
    print(completion)
    assert completion.content.find("Two plus two equals four.") != -1
    # Assert that model name is correct
    assert completion.response_metadata["model_name"].find("gpt-4o-mini") != -1
