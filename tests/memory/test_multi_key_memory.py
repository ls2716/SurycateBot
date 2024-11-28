import os
import shutil
import pytest
import surycate_bot_ls2716.memory_faiss as memory_faiss


# Define fixture which creates a path to the memory folder
@pytest.fixture(scope="module")
def memory_path():
    path = os.path.abspath(__file__)
    path = os.path.dirname(path)
    memory_path = os.path.join(path, "multi_key_memories")
    return memory_path


def test_memory_init(memory_path):
    """Test the init method."""
    mem = memory_faiss.MultiKeyMemory(memory_path, keys=["context", "observation"])
    assert mem.memory_folder == memory_path
    assert mem.keys == ["context", "observation"]
    # Assert that there are 7 documents loaded
    assert len(mem.value_dict) == 7
    # Assert that faiss index is created
    for key in mem.keys:
        assert os.path.exists(os.path.join(mem.memory_folder, f"faiss_{key}"))


def test_memory_fail(memory_path):
    """Test the init method."""
    with pytest.raises(ValueError):
        mem = memory_faiss.MultiKeyMemory(
            memory_path, keys=["context", "observation", "action"])

# Define a memory fixture


@pytest.fixture(scope="module")
def memory_fixture(memory_path):
    mem = memory_faiss.MultiKeyMemory(memory_path, keys=["context", "observation"])
    return mem


def test_memory_get_memory(memory_fixture):
    """Test the get method."""
    mem = memory_fixture
    # Get one memory using context key
    key_doc, value_doc = mem.get_memory("I am being tasked to update the packages on my linux server ls314.com. I have successfully sshed into the server and send the command to update the packages. I have been prompted for a password. I will have to enter it first.",
                                        key_type="context")
    print(value_doc)
    assert key_doc.page_content == "I am being tasked to update the packages on my linux server ls314.com. I have successfully sshed into the server and send the command to update the packages. I have been prompted for a password. I will have to enter it first."
    assert value_doc.page_content.find("Context:")!=-1
    assert value_doc.page_content.find("Action Thought:")!=-1
    assert value_doc.page_content.find("Action:")!=-1
    assert value_doc.page_content.find("Observation:")!=-1
    assert value_doc.page_content.find("Observation Thought:")!=-1
    assert value_doc.page_content.find("New Context:")!=-1
    assert value_doc.page_content.find("I have sent the password but it didn't respond yet. I have to wait for the response.")!=-1
    assert key_doc.page_content.find("Observation:")==-1

    # Get one memory using observation key
    key_doc, value_doc = mem.get_memory("""Context:
I am being tasked to update the packages on my linux server ls314.com. I have successfully sshed into the server and send the command to update the packages. I have been prompted for a password and I have sent it. I have to wait for the response.
Action Thought:
I can just wait for the response and use the get_output command to see the output.
Action:
get_output
Observation:
[sudo] password for lukasz: 
Sorry, try again
""", key_type="observation")
    assert key_doc.page_content == """Context:
I am being tasked to update the packages on my linux server ls314.com. I have successfully sshed into the server and send the command to update the packages. I have been prompted for a password and I have sent it. I have to wait for the response.
Action Thought:
I can just wait for the response and use the get_output command to see the output.
Action:
get_output
Observation:
[sudo] password for lukasz: 
Sorry, try again"""
    assert value_doc.page_content.find("Context:")!=-1
    assert value_doc.page_content.find("Action Thought:")!=-1
    assert value_doc.page_content.find("Action:")!=-1
    assert value_doc.page_content.find("Observation:")!=-1
    assert value_doc.page_content.find("Observation Thought:")!=-1
    assert value_doc.page_content.find("New Context:")!=-1
    assert value_doc.page_content.find("I got the output now and it looks like the password is incorrect.")!=-1
    assert key_doc.page_content.find("Observation:")!=-1

def test_get_memories(memory_fixture):
    # Test get memories

    key_docs, value_docs = memory_fixture.get_memories("I am being tasked to update the packages on my linux server ls314.com. I am on local machine.",
                                        key_type="context")
    assert len(key_docs) == 3
    assert len(value_docs) == 3
    assert key_docs[0].page_content.find("Context:")==-1
    assert key_docs[1].page_content.find("Context:")==-1
    assert value_docs[0].page_content.find("Context:")!=-1
    assert value_docs[0].page_content.find("Action Thought:")!=-1
    assert value_docs[0].page_content.find("Action:")!=-1
    assert value_docs[0].page_content.find("Observation:")!=-1
    assert value_docs[0].page_content.find("Observation Thought:")!=-1
    assert value_docs[0].page_content.find("New Context:")!=-1

