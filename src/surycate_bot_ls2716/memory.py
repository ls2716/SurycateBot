"""Implementation of memory objects.

This file specifies two memory classes: Memory and KeyValueMemory.

Memory class is used to store memories in a folder and perform similarity search on them.
The Memory searches by the whole content of the document.

KeyValueMemory class is used to store key-value pairs in a folder
and perform similarity search on the keys. 
This is implemented so that the content of the document does not affect the similarity search.
For example, if we want to search similar tasks as the current task, we only care about
the task and optionally the context but not the whole execution experience which is not 
relevant for the similarity search.

"""
import surycate_bot_ls2716.utils as utils

# Set the logger
logger = utils.get_logger(__name__)
logger.setLevel("DEBUG")
logger.debug("Logger set up.")


import os
from typing import Callable, List

from langchain_community.document_loaders import DirectoryLoader
from pathlib import Path
from langchain_community.vectorstores import FAISS
logger.debug("Imported FAISS.")
from langchain_openai import OpenAIEmbeddings
logger.debug("Imported OpenAIEmbeddings.")




class Memory(object):
    """Memory class."""

    def __init__(self, memory_folder: str, db_filename: str = None,
                 get_embeddings: Callable = OpenAIEmbeddings) -> None:
        """Initialize the Memory class.

        Args:
            memory_folder: str
                The folder with the memories.
            db_filename: str, default=None
                The filename of the FAISS index.
            get_embeddings: Callable, default=OpenAIEmbeddings
                The callable that returns the embeddings.

        """
        # Define the embeddings
        self.embeddings = get_embeddings()
        # Set the memory folder
        self.memory_folder = memory_folder
        # Get the filenames in the memory folder
        filenames = os.listdir(memory_folder)
        # The filenames are of the form memory_<number>.md
        # Parse the memory numbers
        memory_numbers = [int(filename.split("_")[1].split(".")[0])
                          for filename in filenames if filename.endswith(".md")]
        # Get the maximum memory number
        self.id = max(memory_numbers)
        # Load the memories
        self.loader = DirectoryLoader(memory_folder, glob="*.md")
        self.docs = self.loader.load()
        if db_filename is not None:
            self.db = FAISS.load_local(
                db_filename, self.embeddings, allow_dangerous_deserialization=True)
        else:
            self.db = FAISS.from_documents(self.docs, embeddings)

    def save_index(self, filename="faiss_index"):
        """Save the index to a file.

        Args:
            filename: str, default="faiss_index"
                The filename of the index.
        """
        self.db.save_local(filename)

    def get_memories(self, query: str) -> List[str]:
        """Return the memories regarding the query."""
        return self.db.similarity_search(query)


class KeyValueMemory():
    """Define a key-value memory."""

    def __init__(self, memory_folder: str, db_filename: str = None,
                 get_embeddings: Callable = OpenAIEmbeddings) -> None:
        """Initialize the memory - the memory takes a folder with memories as input.
        The memory folder should have a subdirectory keys with the keys and a subdirectory values with the values.

        The 'keys' documents are used for keys for the embeddings and the 'values'
         documents are used for the values for the embeddings.

        The joining of keys and values are done through metadata.
        Key files are named memory_<number>.key.md and value files are named memory_<number>.value.md.

        Args:
            memory_folder: str
                The folder with the memories. It should contain subfolders 'keys' and 'values'.
            db_filename: str, default=None
                The filename of the FAISS index.
            get_embeddings: Callable, default=OpenAIEmbeddings
                The callable that returns the embeddings.

        """
        # # Define the embeddings
        embeddings = get_embeddings()
        # Set the memory folder
        self.memory_folder = memory_folder
        # Get the key folder
        key_folder = os.path.join(memory_folder, 'keys')
        # Get the value folder
        value_folder = os.path.join(memory_folder, 'values')

        # Get the filenames in the key folder
        filenames = os.listdir(key_folder)
        # The filenames are of the form memory_<number>.key.md
        # Parse the memory numbers
        memory_numbers = [int(filename.split("_")[1].split(".")[0])
                          for filename in filenames if filename.endswith(".md")]
        # Get the maximum memory number
        self.id = max(memory_numbers)
        # Load the keys
        self.key_loader = DirectoryLoader(key_folder, glob="*.md")
        self.key_docs = self.key_loader.load()
        # If the db_filename is not None, load the db from the faiss file
        if db_filename is not None:
            try:
                self.db = FAISS.load_local(
                    db_filename, embeddings, allow_dangerous_deserialization=True)
            except Exception as e:
                logger.error(e)
                logger.error(
                    "Could not load the index from the file. Creating a new index.")
                self.db = FAISS.from_documents(self.key_docs, embeddings)
        else:
            self.db = FAISS.from_documents(self.key_docs, embeddings)

        # Load the values
        self.value_loader = DirectoryLoader(value_folder, glob="*.md")
        self.value_docs = self.value_loader.load()

        # Create dictionaries for the keys and values which contain the memory number as the key
        # and the langchain_community document as the value
        self.keys_dict = {}
        self.values_dict = {}

        # For each document in key_docs, add the id to the metadata
        for doc in self.key_docs:
            # Get filename from the source
            filename = Path(doc.metadata["source"]).name
            # Get the memory number from the path
            memory_number = int(
                filename.split("_")[1].split(".")[0])
            doc.metadata["key_id"] = memory_number
            # Add the document to the keys_dict
            self.keys_dict[memory_number] = doc
        # Perform the same for the value docs
        for doc in self.value_docs:
            # Get filename from the source
            filename = Path(doc.metadata["source"]).name
            # Get the memory number from the path
            memory_number = int(
                filename.split("_")[1].split(".")[0])
            doc.metadata["value_id"] = memory_number
            # Add the document to the values_dict
            self.values_dict[memory_number] = doc

    def save_index(self, filename="faiss_index"):
        """Save the index to a file.

        Args:
            filename: str, default="faiss_index"
                The filename of the index.
            path: str, default=None
                The path to save the index.
        """
        self.db.save_local(filename)

    def get_memory(self, key: str):
        """Get the memory value for the key."""
        # Get the key
        key_doc = self.db.similarity_search(key, k=1)[0]
        key_id = key_doc.metadata["key_id"]
        # Get the value
        value_doc = self.values_dict[key_id]
        return key_doc, value_doc

    def get_memories(self, query: str, k=3) -> list:
        """Return the key documents and value documents regarding the query."""
        # Get the key documents
        key_docs = self.db.similarity_search(query, k=k)
        # Get the corresponding value documents
        value_docs = [self.values_dict[key.metadata["key_id"]]
                      for key in key_docs]
        # Return both the key and value documents
        return key_docs, value_docs


class MultiKeyMemory(object):
    """MultiKeyMemory class."""

    def __init__(self, memory_folder: str, keys: List[str], db_filename: str = None,
                 get_embeddings: Callable = OpenAIEmbeddings, try_load=False) -> None:
        """Initialize the MultiKeyMemory class.

        Args:
            memory_folder: str
                The folder with the memories.
            keys: List[str]
                The types of keys to use for the memory.
            db_filename: str, default=None
                The filename of the FAISS index.
            get_embeddings: Callable, default=OpenAIEmbeddings
                The callable that returns the embeddings.

        """
        # Define the embeddings
        self.embeddings = get_embeddings()
        # Set the memory folder
        self.memory_folder = memory_folder
        self.keys = keys
        # Raise an error if there are no keys
        if len(keys) == 0:
            raise ValueError("No keys specified.")
        # Raise an error if the keys are not strings
        if not all(isinstance(key, str) for key in keys):
            raise ValueError("Keys should be strings.")
        # Raise an error if the keys are not unique
        if len(keys) != len(set(keys)):
            raise ValueError("Keys should be unique.")
        # Get the key folders
        key_folders = [os.path.join(
            memory_folder, f'keys_{key}') for key in keys]
        key_folder_dict = dict(zip(keys, key_folders))
        # Raise an error if the key folders do not exist
        if not all(os.path.exists(key_folder) for key_folder in key_folders):
            raise ValueError("Key folders do not exist.")

        value_folder = os.path.join(memory_folder, 'values')
        # Raise an error if the value folder does not exist
        if not os.path.exists(value_folder):
            raise ValueError("Value folder does not exist.")
        # Get the filenames in the memory folder
        filenames = os.listdir(key_folders[0])
        # The filenames are of the form memory_<number>.md
        # Parse the memory numbers
        memory_numbers = [int(filename.split("_")[1].split(".")[0])
                          for filename in filenames if filename.endswith(".md")]
        # Get the maximum memory number
        self.id = max(memory_numbers)
        # Load the keys
        self.key_doc_dict = {}
        # For each key, create a FAISS index
        self.faiss_dict = {}
        for key in keys:
            if try_load:
                try:
                    self.faiss_dict[key] = FAISS.load_local(
                        os.path.join(db_filename, f"{key}_faiss"),
                        self.embeddings,
                        allow_dangerous_deserialization=True)
                    continue
                except Exception as e:
                    logger.error(e)
                    logger.error(
                        f"Could not load the index for key {key} from the file. Creating a new index.")
            loader = DirectoryLoader(key_folder_dict[key], glob="*.md")
            docs = loader.load()
            self.key_doc_dict[key] = {}
            for doc in docs:
                # Get filename from the source
                filename = Path(doc.metadata["source"]).name
                # Get the memory number from the path
                memory_number = int(
                    filename.split("_")[1].split(".")[0])
                doc.metadata["key_id"] = memory_number
                self.key_doc_dict[key][memory_number] = doc
            self.faiss_dict[key] = FAISS.from_documents(docs, self.embeddings)
        logger.debug("Loaded all keys. Saving.")
        # Save the index
        self.save_index()
        # Load value dicts
        self.value_dict = {}
        value_loader = DirectoryLoader(value_folder, glob="*.md")
        value_docs = value_loader.load()
        for doc in value_docs:
            # Get filename from the source
            filename = Path(doc.metadata["source"]).name
            # Get the memory number from the path
            memory_number = int(
                filename.split("_")[1].split(".")[0])
            doc.metadata["value_id"] = memory_number
            self.value_dict[memory_number] = doc

    def get_memory(self, query: str, key_type: str):
        """Get the memory value for the key."""
        # Check if key_type is in keys
        if key_type not in self.keys:
            raise ValueError(
                f"Key type {key_type} not in keys {self.keys}.")
        # Get the key
        key_doc = self.faiss_dict[key_type].similarity_search(query, k=1)[0]
        key_id = key_doc.metadata["key_id"]
        # Get the value
        value_doc = self.value_dict[key_id]
        return key_doc, value_doc

    def get_memories(self, query: str, key_type: str, k=3) -> List:
        """Return the key documents and value documents regarding the query."""
        # Check if key_type is in keys
        if key_type not in self.keys:
            raise ValueError(
                f"Key type {key_type} not in keys {self.keys}.")
        # Get the key documents
        key_docs = self.faiss_dict[key_type].similarity_search(query, k=k)
        # Get the corresponding value documents
        value_docs = [self.value_dict[key.metadata["key_id"]]
                      for key in key_docs]
        # Return both the key and value documents
        return key_docs, value_docs

    def save_index(self):
        """Save the index to a file for every key."""
        for key in self.keys:
            self.faiss_dict[key].save_local(
                os.path.join(self.memory_folder, f"faiss_{key}"))


