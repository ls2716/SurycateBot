"""Execution of the bot"""

# Import the logging module
import surycate_bot_ls2716.utils as utils
import surycate_bot_ls2716.actions as actions
import surycate_bot_ls2716.prompt as prompt
import surycate_bot_ls2716.memory as memory
import surycate_bot_ls2716.tasks as tasks
from surycate_bot_ls2716.llm import get_llm
from surycate_bot_ls2716.shell import Shell

# Set the logger
logger = utils.get_logger(__name__)


def loop(llm, experiences: memory.KeyValueMemory, task: tasks.Task, actions, state: dict):
    """Execute one task."""

    # Get the experiences related to the task
    _, related_experiences = experiences.get_memories(task.task)
    logger.debug(f"Related experiences: {related_experiences}")
    # Get the task context
    task_context = task.context
    logger.debug(f"Task context: {task_context}")
    # Get the current task
    current_task = task.task
    logger.debug(f"Current task: {current_task}")

    history = task.history
    logger.debug(f"History: {history}")
    task_done = False

    # Loop until the task is done
    while not task_done:
        # Get the prompt
        prompt_text = prompt.build_prompt(
            current_task, related_experiences, task_context, history)
        response = ""
        logger.debug(f"Prompt: \n{prompt_text}")
        input("prompt ok?")
        # Loop until the response starts with "Action:"
        while not response.startswith("Action:"):
            # Append the response to the prompt
            prompt_text += response + "\n"
            history += response + "\n"
            # Get the response
            response = llm.invoke(prompt_text).content
            logger.debug(f"Response: {response}")

        input("response ok?")
        prompt_text += response + "\n"
        history += response + "\n"

        # Get the action
        action = response.split(":")[1].strip()
        # Execute the action
        observation, task_done = actions.execute(action, state)
        # Append the observation to the prompt if the task is not done
        if not task_done:
            prompt_text += "Observation: " + observation + "\nThought: "
            history += "Observation: " + observation + "\nThought: "
        # Update the history
        task.history = history
    # Return the task
    return task


if __name__ == "__main__":
    # Set up an LLM
    llm = get_llm()
    logger.debug(f"LLM: {llm}")
    # Set up the memory
    mem = memory.KeyValueMemory(
        'key_value_experiences')
    logger.debug(f"Memory: {mem}")
    # Set a task
    task = tasks.Task("Create a folder named 'lolapaloza' in the current directory",
                      "You are in the current directory and working on a project to create a website.")
    # Set up actions
    actions = actions.ActionExecutor(action_set=actions.DEFAULT_ACTION_SET)
    logger.debug(f"Actions: {actions}")

    # set up shell
    shell = Shell()
    logger.debug(f"Shell: {shell}")

    state = {
        "llm": llm,
        "shell": shell,
        'task': task,
        'experiences': mem
    }

    # Execute the task
    loop(llm, mem, task, actions, state)
