import os
import shutil

import pytest
from langchain_openai import OpenAIEmbeddings  # type: ignore

import surycate_bot_ls2716.memory_faiss as memory_faiss


@pytest.fixture(scope="module")
def memory_path():
    """Pytest fixture to create a path to the memory folder."""
    path = os.path.abspath(__file__)
    path = os.path.dirname(path)
    memory_path = os.path.join(path, "multi_key_memories")
    # Clear the faiss index directory if it exists from the memory_path
    yield memory_path
    to_delete = [f for f in os.listdir(memory_path) if f.startswith("faiss")]
    for f in to_delete:
        shutil.rmtree(os.path.join(memory_path, f))

    # # Clear the memory_dict.json file if it exists from the memory_path
    # if os.path.exists(os.path.join(memory_path, "memory_dict.json")):
    #     os.remove(os.path.join(memory_path, "memory_dict.json"))


@pytest.fixture(scope="module")
def embeddings():
    """Pytest fixture to create an embeddings object."""
    return OpenAIEmbeddings()


def test_memory_init(memory_path, embeddings):
    """Test the initialisation of MultiKeyMemory object."""
    mem = memory_faiss.MultiKeyMemory(
        memory_path, embeddings=embeddings, keys=["context", "observation"], load=False
    )
    mem.save_memory()

    assert mem.memory_folder == memory_path
    assert mem.keys == ["context", "observation"]
    # Assert that there are 7 documents loaded
    assert len(mem.value_dict) == 7
    # Assert that faiss index is created
    for key in mem.keys:
        assert os.path.exists(os.path.join(mem.memory_folder, f"faiss_{key}"))
    # Asset that the memory_dict.yaml file is created
    assert os.path.exists(os.path.join(mem.memory_folder, "memory_dict.json"))

    # Test the load_memory method
    mem2 = memory_faiss.MultiKeyMemory(
        memory_path, embeddings=embeddings, keys=["context", "observation"], load=True
    )
    assert mem2.memory_folder == memory_path
    assert mem2.keys == ["context", "observation"]
    # Assert that there are 7 documents loaded
    assert len(mem2.value_dict) == 7


def test_memory_fail(memory_path, embeddings):
    """Test the failure of the initialisation of MultiKeyMemory object."""
    with pytest.raises(ValueError):
        _ = memory_faiss.MultiKeyMemory(
            memory_path,
            embeddings=embeddings,
            keys=["context", "observation", "action"],
        )


@pytest.fixture(scope="module")
def memory_fixture(memory_path, embeddings):
    """Pytest fixture to create a MultiKeyMemory object."""
    mem = memory_faiss.MultiKeyMemory(
        memory_path, embeddings=embeddings, keys=["context", "observation"], load=True
    )
    return mem


def test_memory_get_memory(memory_fixture):
    """Test the get memory method of MultiKeyMemory object."""
    mem = memory_fixture
    # Get one memory using context key
    key_id, key_doc, value_doc = mem.get_memory(
        "I am being tasked to update the packages on my linux server ls314.com. I have successfully sshed into the server and send the command to update the packages. I have been prompted for a password. I will have to enter it first.",
        key_type="context",
    )

    assert (
        key_doc.page_content.strip()
        == "I am being tasked to update the packages on my linux server ls314.com. I have successfully sshed into the server and send the command to update the packages. I have been prompted for a password. I will have to enter it first."
    )
    assert value_doc.find("Context:") != -1
    assert value_doc.find("Action Thought:") != -1
    assert value_doc.find("Action:") != -1
    assert value_doc.find("Observation:") != -1
    assert value_doc.find("Observation Thought:") != -1
    assert value_doc.find("New Context:") != -1
    assert (
        value_doc.find(
            "I have sent the password but it didn't respond yet. I have to wait for the response."
        )
        != -1
    )
    assert key_doc.page_content.find("Observation:") == -1

    # Get one memory using observation key
    key_id, key_doc, value_doc = mem.get_memory(
        """Context:
I am being tasked to update the packages on my linux server ls314.com. I have successfully sshed into the server and send the command to update the packages. I have been prompted for a password and I have sent it. I have to wait for the response.
Action Thought:
I can just wait for the response and use the get_output command to see the output.
Action:
get_output
Observation:
[sudo] password for lukasz: 
Sorry, try again
""",
        key_type="observation",
    )
    print(key_doc.page_content)
    assert (
        key_doc.page_content.strip()
        == """Context:
I am being tasked to update the packages on my linux server ls314.com. I have successfully sshed into the server and send the command to update the packages. I have been prompted for a password and I have sent it. I have to wait for the response.
Action Thought:
I can just wait for the response and use the get_output command to see the output.
Action:
get_output
Observation:
[sudo] password for lukasz: 
Sorry, try again"""
    )
    assert value_doc.find("Context:") != -1
    assert value_doc.find("Action Thought:") != -1
    assert value_doc.find("Action:") != -1
    assert value_doc.find("Observation:") != -1
    assert value_doc.find("Observation Thought:") != -1
    assert value_doc.find("New Context:") != -1
    assert (
        value_doc.find(
            "I got the output now and it looks like the password is incorrect."
        )
        != -1
    )
    assert key_doc.page_content.find("Observation:") != -1


def test_get_memories(memory_fixture):
    """Test the get memories method of MultiKeyMemory object."""
    key_ids, key_docs, value_docs = memory_fixture.get_memories(
        "I am being tasked to update the packages on my linux server "
        + "ls314.com. I am on local machine.",
        key_type="context",
    )
    assert len(key_docs) == 3
    assert len(value_docs) == 3
    assert key_docs[0].page_content.find("Context:") == -1
    assert key_docs[1].page_content.find("Context:") == -1
    assert value_docs[0].find("Context:") != -1
    assert value_docs[0].find("Action Thought:") != -1
    assert value_docs[0].find("Action:") != -1
    assert value_docs[0].find("Observation:") != -1
    assert value_docs[0].find("Observation Thought:") != -1
    assert value_docs[0].find("New Context:") != -1


def test_delete_memory(memory_fixture):
    """Test the delete memory method of MultiKeyMemory object."""
    key_id, key_doc, value_doc = memory_fixture.get_memory(
        "I am being tasked to update the packages on my linux server ls314.com. I am on local machine.",
        key_type="context",
    )
    memory_fixture.delete_memory(key_id)
    assert key_id not in memory_fixture.value_dict

    new_key_id, new_key_doc, new_value_doc = memory_fixture.get_memory(
        "I am being tasked to update the packages on my linux server ls314.com. I am on local machine.",
        key_type="context",
    )
    assert key_id != new_key_id
    assert key_doc.page_content != new_key_doc.page_content
    assert value_doc != new_value_doc

def test_add_memory(memory_fixture):
    """Test the add memory method of MultiKeyMemory object."""
    key_docs = {
        "context": "Who is the president of the United States?",
        "observation": "The president of the United States is Joe Biden.",
    }
    value_doc = "Joe Biden is the president of the United States."
    memory_fixture.add_memory(key_docs, value_doc)
    key_id, key_doc, value_doc = memory_fixture.get_memory(
        "Who is the president of the United States?", key_type="context"
    )
    assert key_doc.page_content == "Who is the president of the United States?"
    assert value_doc == "Joe Biden is the president of the United States."

    key_id, key_doc, value_doc = memory_fixture.get_memory(
        "The president of the United States is Joe Biden.", key_type="observation"
    )
    assert key_doc.page_content == "The president of the United States is Joe Biden."
    assert value_doc == "Joe Biden is the president of the United States."

