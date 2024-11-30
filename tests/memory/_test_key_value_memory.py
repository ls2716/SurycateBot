import os
import shutil
import pytest
import surycate_bot_ls2716.memory_faiss as memory_faiss


# Define fixture which creates a path to the memory folder
@pytest.fixture(scope="module")
def memory_path():
    path = os.path.abspath(__file__)
    path = os.path.dirname(path)
    memory_path = os.path.join(path, "key_value_experiences")
    return memory_path


def test_memory_init(memory_path):
    """Test the initialisation of the memory."""
    mem = memory_faiss.KeyValueMemory(memory_path)
    assert len(mem.key_docs) == 2, "Not all key documents were loaded!"
    assert len(mem.value_docs) == 2, "Not all value documents were loaded!"
    # Check that dictionaries are correctly linked
    # Get the keys from the key dict
    keys = mem.keys_dict.keys()
    assert len(keys) == 2, "Not all keys were loaded!"
    # Check that all keys are also in the values dict
    for key in keys:
        assert key in mem.values_dict, "Key not in values dict!"
    # Check that the id is correctly set
    doc_content = mem.values_dict[1].page_content
    print(doc_content)
    assert doc_content == \
        """Task: Assimilate information from the following text. "Olaf Scholz is the chancellor of Germany."

Memories:
- Joe Biden is the president of United States.
- Who is the president of Poland? Andrzej Duda is currently the president of Poland.

Start:
Thought: I didn't know that Olaf Scholz is the chancellor of Germany.
Action: create_memory "Olaf Scholz is the chancellor of Germany".
Observation: Success.
Thought: I have completed the task.
Action: EXIT"""

# Define fixture which creates a memory object


@pytest.fixture(scope="module")
def mem(memory_path):
    mem = memory_faiss.KeyValueMemory(memory_path)
    return mem


def test_get_memory(mem):
    """Test the get memory method."""
    # Create path to the folder
    key_doc, value_doc = mem.get_memory("Create a directory named test.")
    assert key_doc.page_content == 'Task: Create a folder named "Code".'
    assert value_doc.page_content == \
        """Task: Create a folder named "Code".

Memories:
- Code folders contain code.
- I can use mkdir command to create a folder.

START:
Thought: I need to create a folder named 'Code'.
Action: cmd mkdir Code
Observation: The folder 'Code' was created.
EXIT"""


def test_get_memories(mem):
    """Test the get memories method."""
    key_docs, value_docs = mem.get_memories("Create a directory named test.")
    assert key_docs[0].page_content == 'Task: Create a folder named "Code".'
    assert value_docs[0].page_content == \
        """Task: Create a folder named "Code".

Memories:
- Code folders contain code.
- I can use mkdir command to create a folder.

START:
Thought: I need to create a folder named 'Code'.
Action: cmd mkdir Code
Observation: The folder 'Code' was created.
EXIT"""


# Define fixture which creates a tmp folder, yields the path and deletes the folder after the test
@pytest.fixture(scope="module")
def temp_folder():
    path = os.path.abspath(__file__)
    path = os.path.dirname(path)
    temp_folder = os.path.join(path, "tmp")
    os.mkdir(temp_folder)
    yield temp_folder
    # Remove the folder
    shutil.rmtree(temp_folder)


def test_memory_save(mem, temp_folder):
    """Test the save method of the memory."""
    mem.save_index(os.path.join(temp_folder, 'faiss_index'))
    print(os.listdir(temp_folder))
    assert os.path.exists(os.path.join(
        temp_folder, "faiss_index")), "Memory file was not saved!"


# Create fixture which creates an index in the tmp folder
@pytest.fixture(scope="module")
def index(temp_folder, mem):
    index = os.path.join(temp_folder, "faiss_index")
    mem.save_index(index)
    return index


def test_load_index(memory_path, index):
    """Test loading the index."""
    mem = memory_faiss.KeyValueMemory(memory_path, db_filename=index)
    assert len(mem.key_docs) == 2, "Not all documents were loaded!"
