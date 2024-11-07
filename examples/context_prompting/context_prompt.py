"""This script defines the prompt for the bot."""
# Import the prompt template from langchain
from langchain.prompts.prompt import PromptTemplate
from typing import List


# Import the logging module
import surycate_bot_ls2716.utils as utils

# Set the logger
logger = utils.get_logger(__name__)


# Define default prompt

default_old = """You are an agent with an available terminal who performs various tasks.
 Given context information that includes the task, you should generate an action which will result in an observation. 
 Given the previous context, action and the observation, first generate a thought about the observation.
Then, generate an updated context which contains a summary of previous information and the idea what to do next.

For example:

Context:
I am working on a project to create a website. I already have created a folder named "Website". I want to create a markdown file with the description of the website but I am now in the parent folder of the "Website" folder. I need to change the directory to the "Website" folder.
Action:
cmd cd Website
Observation:
lukasz@Smith:~/Projects$ cd Website
lukasz@Smith:~/Projects/Website$
Thought:
I have changed the directory to the "Website" folder. I can now create the markdown file.
New Context:
I am working on a project to create a website. I am in the "Website" folder. I want to create a markdown file with the description of the website. To do that, I have to create a markdown file in the "Website" folder called README.md.

In above, given the context "I am working on a project to create a website.
 I already have created a folder named "Website". I want to create a markdown file with the description of the website
   but I am now in the parent folder of the "Website" folder. I need to change the directory to the "Website" folder."
you generate an action "cmd cd Website" which results in an observation. This results in an observation:
"lukasz@Smith:~/Projects$ cd Website
lukasz@Smith:~/Projects/Website$"
Following the observation, you generate a thought about the observation and how it relates to the context:
 "I have changed the directory to the "Website" folder. I can now create the markdown file."
Finally, you generate an updated context which contains a summary of previous information and the idea what to do next:
"I am working on a project to create a website. I am in the "Website" folder.
 I want to create a markdown file with the description of the website.
 To do that, I have to create a markdown file in the "Website" folder called README.md."

Always follow this pattern when generating actions, observations, thoughts, and new contexts, that is
Context -> Action -> Observation -> Thought -> New Context.
It should always be in this order and look like following:

Context:
<context>
Action:
<action>
Observation:
<observation>
Thought:
<thought>
New Context:
<new_context>


In addition, you have access to past experiences and memories in the form of Context, Action, Observation, Thought, and New Context.
Use this information.

Past memories similar to the current context:
----------------
{similar_tasks}
----------------

Context:
{task_context}
{history}"""

default = """Complete using the following template:

Context:
<context>
Action:
<action>
Observation:
<observation>
Thought:
<thought>
New Context:
<new_context>


Here are some examples that you should base the completions on:
----------------
{similar_tasks}
----------------

Context:
{task_context}
{history}"""

default_prompt = PromptTemplate(
    input_variables=["similar_tasks", "task_context", "history"],
    template=default
)


def format_memories(memories: List) -> str:
    """Format the memories."""
    return "\n".join('- ' + memory.page_content for memory in memories)


def format_similar_tasks(similar_tasks: List) -> str:
    """Format the similar tasks."""
    return "\n----------------\n".join(similar_task.page_content for similar_task in similar_tasks)


def build_prompt(similar_tasks: list, task_context: str, history: str) -> str:
    """Build the prompt."""
    prompt = default_prompt.format(
        similar_tasks=format_similar_tasks(similar_tasks[::-1]),
        task_context=task_context,
        history=history
    )
    return prompt


# if __name__ == "__main__":
#     import surycate_bot_ls2716.memory as memory
#     memory_src = memory.Memory("memories")
#     mems = memory_src.get_memories(
#         "Who is the president of the United States?")

#     current_task = 'Create a directory named "test".'

#     task_memory = memory.Memory("experiences")
#     tasks = task_memory.get_memories(current_task)

#     current_task = "Create a directory named test"
#     prompt = default_prompt.format(
#         current_task=current_task,
#         similar_tasks=format_similar_tasks(tasks),
#         history=""
#     )
#     print(prompt)
