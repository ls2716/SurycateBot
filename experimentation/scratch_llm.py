import os

from surycate_bot_ls2716.llm import get_llm
from langchain_openai import OpenAI, ChatOpenAI
print('finished imports')

llm = get_llm(temperature=0, max_tokens=100, model="gpt-4o-mini")


response = llm.invoke(
    "What is two plus two?")
print(response)
