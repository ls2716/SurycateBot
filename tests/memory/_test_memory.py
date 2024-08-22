import os
import shutil
import pytest
import surycate_bot_ls2716.memory as memory


# Define fixture which creates a path to the memory folder
@pytest.fixture(scope="module")
def memory_path():
    path = os.path.abspath(__file__)
    path = os.path.dirname(path)
    memory_path = os.path.join(path, "experiences")
    return memory_path


def test_memory_init(memory_path):
    """Test the initialisation of the memory."""
    mem = memory.Memory(memory_path)
    assert len(mem.docs) == 2, "Correct number of documents loaded!"


# Define fixture which creates a memory object
@pytest.fixture(scope="module")
def mem(memory_path):
    mem = memory.Memory(memory_path)
    return mem


def test_memory_get(mem):
    """Test the get memories method."""
    # Create path to the folder
    memories = mem.get_memories("Create a directory named test.")
    assert memories[0].page_content == 'Task: Create a directory named "Code" in the "Home" folder".'

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
# Set test to test saving of the memory


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
    mem = memory.Memory(memory_path, db_filename=index)
    assert len(mem.docs) == 2, "Not all documents were loaded!"
