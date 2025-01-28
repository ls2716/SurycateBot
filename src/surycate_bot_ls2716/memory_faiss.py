"""Implementation of memory objects.

This file specifies the implementation of a MultiKeyMemory object that stores
memories with multiple keys and values.

The MultiKeyMemory object is a wrapper around FAISS vectorstore which extends the
functionality of FAISS. Specifically, it allows for specification of keys for the given memory (value) and thus giving
the possibility to search for a memory based on the context and not just the potential
output of the context.


"""

import os
from pathlib import Path
from typing import List

import yaml, json
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings  # type: ignore
from langchain_core.documents import Document

import surycate_bot_ls2716.utils as utils

# Set the logger
logger = utils.get_logger(__name__)
logger.setLevel("DEBUG")
logger.debug("Logger set up.")

logger.debug("Imported OpenAIEmbeddings.")
logger.debug("Imported FAISS.")
# import msgpack


class MultiKeyMemory(object):
    """MultiKeyMemory class."""

    def __init__(
        self, memory_folder: str, keys: List[str], embeddings, load=False
    ) -> None:
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
        self.embeddings = embeddings
        # Set the memory folder
        self.memory_folder = memory_folder
        self.keys = keys
        self.id = 1001
        # Raise an error if there are no keys
        if len(keys) == 0:
            raise ValueError("No keys specified.")
        # Raise an error if the keys are not strings
        if not all(isinstance(key, str) for key in keys):
            raise ValueError("Keys should be strings.")
        # Raise an error if the keys are not unique
        if len(keys) != len(set(keys)):
            raise ValueError("Keys should be unique.")

        if load:
            self.load_memory()
        else:
            self.create_memory()

    def create_memory(self):
        # Get the key folders
        key_folders = [
            os.path.join(self.memory_folder, f"keys_{key}") for key in self.keys
        ]
        logger.debug(f"Key folders: {key_folders}")
        key_folder_dict = dict(zip(self.keys, key_folders))
        # Raise an error if the key folders do not exist
        if not all(os.path.exists(key_folder) for key_folder in key_folders):
            raise ValueError("Key folders do not exist.")

        value_folder = os.path.join(self.memory_folder, "values")
        # Raise an error if the value folder does not exist
        if not os.path.exists(value_folder):
            raise ValueError("Value folder does not exist.")

        # Get the filenames in the memory folder
        filenames = os.listdir(key_folders[0])
        # The filenames are of the form memory_<number>.md

        # Load the keys
        self.key_doc_dict = {}
        # For each key, create a FAISS index
        self.faiss_dict = {}
        for key in self.keys:
            loader = DirectoryLoader(
                key_folder_dict[key], glob="*.md", loader_cls=TextLoader
            )
            docs = loader.load()
            self.key_doc_dict[key] = {}
            for doc in docs:
                # Get filename from the source
                filename = Path(doc.metadata["source"]).name
                # Get the memory number from the path
                memory_number = filename.split("_")[1].split(".")[0]
                doc.metadata["key_id"] = memory_number
                doc.id = memory_number
                self.key_doc_dict[key][memory_number] = doc.page_content

            self.faiss_dict[key] = FAISS.from_documents(docs, self.embeddings)
            logger.debug(f"Created key {key}")
        # Load value dicts
        self.value_dict = {}
        value_loader = DirectoryLoader(value_folder, glob="*.md", loader_cls=TextLoader)
        value_docs = value_loader.load()
        for doc in value_docs:
            # Get filename from the source
            filename = Path(doc.metadata["source"]).name
            # Get the memory number from the path
            memory_number = filename.split("_")[1].split(".")[0]
            doc.metadata["value_id"] = memory_number
            doc.id = memory_number
            self.value_dict[memory_number] = doc.page_content

    def load_memory(self):
        """Load the memory from json and faiss indices."""

        try:
            self.faiss_dict = {}
            for key in self.keys:
                self.faiss_dict[key] = FAISS.load_local(
                    os.path.join(self.memory_folder, f"faiss_{key}"),
                    self.embeddings,
                    allow_dangerous_deserialization=True,
                )
                logger.debug(f"Loaded index for key {key}.")
        except Exception as e:
            logger.error(e)
            raise ValueError(
                "Could not load the index from the file. Create a new index."
            )

        # Load the value dictionary from json
        data_dict_path = os.path.join(self.memory_folder, "memory_dict.json")
        with open(data_dict_path, "r") as f:
            data_dict = yaml.safe_load(f)
        self.value_dict = data_dict["value_dict"]
        self.key_doc_dict = data_dict["key_doc_dict"]

    def save_memory(self):
        """Save the memory to json and faiss indices."""
        # Save the value dictionary to json
        data_dict = {"value_dict": self.value_dict, "key_doc_dict": self.key_doc_dict}
        data_dict_path = os.path.join(self.memory_folder, "memory_dict.json")
        with open(data_dict_path, "w") as f:
            json.dump(data_dict, f, indent=4)

        # Save the FAISS indices
        for key in self.keys:
            self.faiss_dict[key].save_local(
                os.path.join(self.memory_folder, f"faiss_{key}")
            )

    def get_memory(self, query: str, key_type: str):
        """Get the memory value for the key."""
        # Check if key_type is in keys
        if key_type not in self.keys:
            raise ValueError(f"Key type {key_type} not in keys {self.keys}.")
        # Get the key
        key_doc = self.faiss_dict[key_type].similarity_search(query, k=1)[0]
        key_id = key_doc.metadata["key_id"]
        # Get the value
        value_doc = self.value_dict[key_id]
        return key_id, key_doc, value_doc

    def get_memories(self, query: str, key_type: str, k=3) -> List:
        """Return the key documents and value documents regarding the query."""
        # Check if key_type is in keys
        if key_type not in self.keys:
            raise ValueError(f"Key type {key_type} not in keys {self.keys}.")
        # Get the key documents
        key_docs = self.faiss_dict[key_type].similarity_search(query, k=k)
        # Get the key ids
        key_ids = [key.metadata["key_id"] for key in key_docs]
        # Get the corresponding value documents
        value_docs = [self.value_dict[key_id] for key_id in key_ids]
        # Return both the key and value documents
        return key_ids, key_docs, value_docs
    
    def delete_memory(self, key_id: str):
        """Delete the memory from the memory."""
        # Delete the key documents
        for key in self.keys:
            self.faiss_dict[key].delete(ids=[key_id])
        # Delete the value document
        del self.value_dict[key_id]
    
    def add_memory(self, key_docs, value_doc):
        """Add the memory to the memory.
        
        Args:
            key_docs: Dict with str keys and str values
                The key documents.
            value_doc: string
                The value document.
        """
        # Generate a new key id (pad with zeros until 4 digits)
        key_id = str(self.id).zfill(4)
        self.id += 1
        # Add the key documents
        for key in self.keys:
            # Initialise a Document object
            key_doc = Document(key_docs[key], metadata={"key_id": key_id},)
            self.faiss_dict[key].add_documents([key_doc])
        # Add the value document
        self.value_dict[key_id] = value_doc


if __name__ == "__main__":
    memory_folder = "tests/memory/multi_key_memories"
    mem = MultiKeyMemory(
        memory_folder,
        keys=["context", "observation"],
        load=False,
        embeddings=OpenAIEmbeddings(),
    )
    mem.save_memory()
