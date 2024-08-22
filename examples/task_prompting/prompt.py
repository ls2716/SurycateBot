"""This script defines the prompt for the bot."""
# Import the prompt template from langchain
from langchain.prompts.prompt import PromptTemplate
from typing import List


# Import the logging module
import surycate_bot_ls2716.utils as utils

# Set the logger
logger = utils.get_logger(__name__)


# Define default prompt

default = """You are an assistant who performs various tasks for the user.
You work in a text interface and follow thought, action, observation pattern.

For example:
Task: Create a directory named "test"
START:
Thought: I need to create a directory named "test"
Action: cmd mkdir test
Observation: Directory "test" has been created.
EXIT

Another example:
Task: List the files in the current directory.
START:
Thought: I need to list the files in the current directory. I can use the ls command.
Action: cmd ls
Observation: The files in the current directory are: file1 file2 file3
EXIT

In addition, you have access to similar task examples, the current task, and the memories.

Your current task is:
{current_task}

In the past, you have performed similar tasks:
----------------
{similar_tasks}
----------------

Your task is:
{current_task}
Task context:
{task_context}
{history}"""

default_prompt = PromptTemplate(
    input_variables=["current_task",
                     "similar_tasks", "task_context", "history"],
    template=default
)


def format_memories(memories: List) -> str:
    """Format the memories."""
    return "\n".join('- ' + memory.page_content for memory in memories)


def format_similar_tasks(similar_tasks: List) -> str:
    """Format the similar tasks."""
    return "\n----------------\n".join(similar_task.page_content for similar_task in similar_tasks)


def build_prompt(current_task: str, similar_tasks: list, task_context: str, history: str) -> str:
    """Build the prompt."""
    prompt = default_prompt.format(
        current_task=current_task,
        similar_tasks=format_similar_tasks(similar_tasks[::-1]),
        task_context=task_context,
        history=history
    )
    return prompt


if __name__ == "__main__":
    import surycate_bot_ls2716.memory as memory
    memory_src = memory.Memory("memories")
    mems = memory_src.get_memories(
        "Who is the president of the United States?")

    current_task = 'Create a directory named "test".'

    task_memory = memory.Memory("experiences")
    tasks = task_memory.get_memories(current_task)

    current_task = "Create a directory named test"
    prompt = default_prompt.format(
        current_task=current_task,
        similar_tasks=format_similar_tasks(tasks),
        history=""
    )
    print(prompt)
