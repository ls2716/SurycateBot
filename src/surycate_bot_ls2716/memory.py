"""Module which serves as a memory for the bot."""

# Import the utils
import surycate_bot_ls2716.utils as utils
import os

from langchain_community.document_loaders import DirectoryLoader
from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

# Set the logger
logger = utils.get_logger(__name__)

embeddings = OpenAIEmbeddings()


class Memory(object):
    """Memory class."""

    def __init__(self, memory_folder, db_filename=None) -> None:
        """Initialize the memory."""
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
                db_filename, embeddings, allow_dangerous_deserialization=True)
        else:
            self.db = FAISS.from_documents(self.docs, embeddings)

    def save_index(self, filename="faiss_index"):
        self.db.save_local(filename)

    def get_memories(self, query: str) -> list:
        """Return the memories regarding the query."""
        return self.db.similarity_search(query)


class KeyValueMemory():
    """Define a key-value memory."""

    def __init__(self, memory_folder, db_filename=None) -> None:
        """Initialize the memory - the memory takes a folder with memories as input.
        The memory folder should have a subdirectory keys with the keys and a subdirectory values with the values.

        The 'keys' documents are used for keys for the embeddings and the 'values'
         documents are used for the values for the embeddings.

        The joining of keys and values are done through metadata.
        Key files are named memory_<number>.key.md and value files are named memory_<number>.value.md.
        """

        self.memory_folder = memory_folder
        # Get the key folder
        key_folder = os.path.join(memory_folder, "keys")
        # Get the value folder
        value_folder = os.path.join(memory_folder, "values")

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
            self.db = FAISS.load_local(
                db_filename, embeddings, allow_dangerous_deserialization=True)
        else:
            self.db = FAISS.from_documents(self.key_docs, embeddings)

        # Load the values
        self.value_loader = DirectoryLoader(value_folder, glob="*.md")
        self.value_docs = self.value_loader.load()

        self.keys_dict = {}
        self.values_dict = {}

        # For each document in key_docs, add the id to the metadata
        for doc in self.key_docs:
            # Get the memory number from the path
            # Get filename from the source
            filename = Path(doc.metadata["source"]).name
            memory_number = int(
                filename.split("_")[1].split(".")[0])
            doc.metadata["key_id"] = memory_number
            # Add the document to the keys_dict
            self.keys_dict[memory_number] = doc
        # Perform the same for the value docs
        for doc in self.value_docs:
            # Get the memory number from the path
            # Get filename from the source
            filename = Path(doc.metadata["source"]).name
            memory_number = int(
                filename.split("_")[1].split(".")[0])
            doc.metadata["value_id"] = memory_number
            # Add the document to the values_dict
            self.values_dict[memory_number] = doc

    def save_index(self, filename="faiss_index", path=None):
        if path is None:
            path = os.path.join(self.memory_folder, filename)
        self.db.save_local(path)

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
