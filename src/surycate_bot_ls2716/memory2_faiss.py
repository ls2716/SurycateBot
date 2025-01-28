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

import  json
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_core.documents import Document

import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings  # type: ignore

import surycate_bot_ls2716.utils as utils

# Set the logger
logger = utils.get_logger(__name__)
logger.setLevel("DEBUG")
logger.debug("Logger set up.")

class MultiKeyMemory(object):
    """MultiKeyMemory class."""

    def __init__(
        self, memory_folder: str, vectorstore_dict, regenerate=True
    ) -> None:
        """Initialize the MultiKeyMemory class.

        Args:
            memory_folder: str
                The folder with the memories.
            key_vectorstore_dict: Dict[str, VectorStore]
                A dictionary with keys as strings and VectorStore objects as values
            regenerate: bool, default=True

        """
        # Set the memory folder
        self.memory_folder = memory_folder
        self.keys = list(vectorstore_dict.keys())
        self.id = 1
        self.vectorstore_dict = vectorstore_dict

        # Raise an error if there are no keys
        if len(self.keys) == 0:
            raise ValueError("No keys specified.")
        # Raise an error if the keys are not strings
        if not all(isinstance(key, str) for key in self.keys):
            raise ValueError("Keys should be strings.")
        # Raise an error if the keys are not unique
        if len(self.keys) != len(set(self.keys)):
            raise ValueError("Keys should be unique.")

        self.load_memory_dict()
        if regenerate:
            self.regenerate()

    def load_memory_dict(self):
        """Regenerate the memory.
        
        Generate the memories from json files.
        """
        # Get a list of json files in the memory folder that start with 'memory'
        memory_files = [
            f
            for f in os.listdir(self.memory_folder)
            if f.startswith("memory") and f.endswith(".json")
        ]
        # Load the memories from the json files
        self.memory_dict = {}
        for memory_file in memory_files:
            memory_path = os.path.join(self.memory_folder, memory_file)
            with open(memory_path, "r") as f:
                memory = json.load(f)
            key_id = memory["key_id"]
            self.memory_dict[key_id] = memory
        
        self.dump_memory_dict()
        

    def dump_memory_dict(self):
        # Dump the memory_dict to a json file
        memory_dict_path = os.path.join(self.memory_folder, "dump_memory.json")
        with open(memory_dict_path, "w") as f:
            json.dump(self.memory_dict, f, indent=4)
        
    def regenerate(self):
        """Generate the vectorstores for the keys.
        
        """
        memory_keys = list(self.memory_dict.keys())
        # For each key:
        for key in self.keys:
            # Create Document objects for the key
            key_docs = [
                Document(
                    self.memory_dict[key_id][key],
                    metadata={"key_id": key_id},
                )
                for key_id in memory_keys
            ]
            # Add documents to the vectorstore
            self.vectorstore_dict[key].add_documents(key_docs)


    def get_memory(self, query: str, key_type: str):
        """Get the memory value for the key."""
        # Check if key_type is in keys
        if key_type not in self.keys:
            raise ValueError(f"Key type {key_type} not in keys {self.keys}.")
        # Get the key
        key_doc = self.vectorstore_dict[key_type].similarity_search(query, k=1)[0]
        key_id = key_doc.metadata["key_id"]
        # Get the value
        value_doc = self.memory_dict[key_id]["value"]
        return key_id, key_doc, value_doc

    def get_memories(self, query: str, key_type: str, k=3) -> List:
        """Return the key documents and value documents regarding the query."""
        # Check if key_type is in keys
        if key_type not in self.keys:
            raise ValueError(f"Key type {key_type} not in keys {self.keys}.")
        # Get the key documents
        key_docs = self.vectorstore_dict[key_type].similarity_search(query, k=k)
        # Get the key ids
        key_ids = [key.metadata["key_id"] for key in key_docs]
        # Get the corresponding value documents
        value_docs = [self.memory_dict[key_id]["value"] for key_id in key_ids]
        # Return both the key and value documents
        return key_ids, key_docs, value_docs
    
    def delete_memory(self, key_id: str):
        """Delete the memory from the memory."""
        # Delete the key documents
        for key in self.keys:
            self.vectorstore_dict[key].delete(ids=[key_id])
        # Delete the value document
        del self.memory_dict[key_id]
    
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
        while key_id in self.memory_dict:
            self.id += 1
            key_id = str(self.id).zfill(4)
        self.memory_dict[key_id] = {"key_id": key_id}
        # Add the key documents
        for key in self.keys:
            # Initialise a Document object
            key_doc = Document(key_docs[key], metadata={"key_id": key_id},)
            self.vectorstore_dict[key].add_documents([key_doc])
            # Add the key to the memory_dict
            self.memory_dict[key_id][key] = key_docs[key]
        # Add the value document
        self.memory_dict[key_id]["value"] = value_doc

        # Create a new memory file
        memory_path = os.path.join(self.memory_folder, f"memory_{key_id}.json")
        with open(memory_path, "w") as f:
            json.dump(self.memory_dict[key_id], f, indent=4)
    
    


if __name__ == "__main__":
    memory_folder = "memories2"
    embeddings = OpenAIEmbeddings()
    index = faiss.IndexFlatL2(len(OpenAIEmbeddings().embed_query("hello world")))

    vector_store = FAISS(
        embedding_function=OpenAIEmbeddings(),
        index=index,
        docstore= InMemoryDocstore(),
        index_to_docstore_id={}
    )
    vectorstore_dict = {
        "context": vector_store
    }
    mem = MultiKeyMemory(
        memory_folder,
        vectorstore_dict=vectorstore_dict,
    )

    key_id, key_doc, value_doc = mem.get_memory("Who are you", "context")

    print(key_id)
    print(key_doc)
    print(value_doc)

    mem.add_memory({"context": "hello world"}, "value")

    key_id, key_doc, value_doc = mem.get_memory("hello world", "context")

    print(key_id)
    print(key_doc)
    print(value_doc)
