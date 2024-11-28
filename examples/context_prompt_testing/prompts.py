"""This script defines the prompt for the bot."""
# Import the prompt template from langchain
from langchain.prompts.prompt import PromptTemplate
from typing import List
from prompt_templates import default_prompt, concise_prompt


# Import the logging module
import surycate_bot_ls2716.utils as utils

# Set the logger
logger = utils.get_logger(__name__)




def format_memories(memories: List) -> str:
    """Format the memories."""
    return "\n".join('- ' + memory.page_content for memory in memories)


def format_similar_tasks(similar_tasks: List) -> str:
    """Format the similar tasks."""
    return "\n----------------\n".join(similar_task.page_content for similar_task in similar_tasks)


def build_prompt(prompt_template, similar_tasks: list, task_context: str, history: str) -> str:
    """Build the prompt."""
    prompt = prompt_template.format(
        similar_tasks=format_similar_tasks(similar_tasks[::-1]),
        task_context=task_context,
        history=history
    )
    return prompt

def get_prompt(prompt_type: str = 'default') -> PromptTemplate:
    """Get the prompt.
    
    Args:
    - prompt_type: str: The type of the prompt to get.
    
    Returns:
    - PromptTemplate: The prompt template.

    Available prompt types:
    - default (default): The default prompt.
    - default_old: The old default prompt.
    - concise: The concise prompt.

    """
    if prompt_type == 'default':
        return default_prompt.template
    elif prompt_type == 'concise':
        return concise_prompt.template
    else:
        raise ValueError(f"Unknown prompt type: {prompt_type}. "+\
                         "The available prompt types are: default, default_old, concise.")