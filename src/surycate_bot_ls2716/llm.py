"""Declare the language model to be used by the bot."""
import os

from langchain_openai import ChatOpenAI


def get_llm(temperature: float = 0.7, max_tokens: int = 100, model="gpt-4o-mini", **kwargs) -> ChatOpenAI:
    """Return the language model as chat model and bind \n as a stop token.

    Args:
    temperature: float, default=0.7
        The temperature parameter for the language model.
    max_tokens: int, default=100
        The maximum number of tokens to generate.

    Returns:
    llm: ChatOpenAI
        The language model as a chat model.

    There needs to be an environment variable OPENAI_API_KEY set to the OpenAI API key.
    """
    # Get the language model
    llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"),
                     temperature=temperature, max_tokens=max_tokens, model=model, **kwargs)
    # Bind \n as a stop token
    llm = llm.bind(stop=['\n'])
    return llm
