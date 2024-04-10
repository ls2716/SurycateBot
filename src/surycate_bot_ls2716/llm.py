"""Implementation of LLM engine"""
import os

from langchain_openai import OpenAI, ChatOpenAI


# Define a class which returns OpenAI's model as langchain


def get_llm(temperature=0.7, max_tokens=100):
    """Return the language model and bind \n as a stop token."""
    # Return the language model
    llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"),
                     temperature=temperature, max_tokens=max_tokens)
    llm = llm.bind(stop=['\n'])
    return llm
