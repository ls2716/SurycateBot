"""This script defines the prompt for the bot."""
# Import the prompt template from langchain
from langchain.prompts.prompt import PromptTemplate
from typing import List

# Import the logging module
import surycate_bot_ls2716.utils as utils

# Set the logger
logger = utils.get_logger(__name__)


def format_memories(memories: List) -> str:
    """Format the memories."""
    return "\n".join('- ' + memory for memory in memories)


def format_similar_tasks(similar_tasks: List) -> str:
    """Format the similar tasks."""
    return "\n----------------\n".join(
        similar_task for similar_task in similar_tasks)


def build_prompt(similar_tasks: list, execution: str) -> str:
    """Build the prompt."""
    prompt = context_info_template.format(
        similar_tasks=format_similar_tasks(similar_tasks[::-1]),
        execution=execution
    )
    return prompt


context_info_template_str = """Complete the next line in sequence using the following pattern:

CONTEXT:
<context>
INFORMATION:
- <information_1>
- <information_2>
- <information_3>
ACTION:
<action>
ACTION THOUGHT:
<action_thought>
OBSERVATION:
<observation>
OBSERVATION THOUGHT:
<observation_thought>
NEW CONTEXT:
<new_context>

Here are some examples that you should base the completions on:
---
{similar_tasks}
---

{execution}"""

context_info_template = PromptTemplate(
    input_variables=["similar_tasks", "execution"],
    template=context_info_template_str
)
