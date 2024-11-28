"""Execution of the bot"""

# Import the logging module
from surycate_bot_ls2716.shell import PexpectShell
from surycate_bot_ls2716.llm import get_llm
import surycate_bot_ls2716.tasks as tasks
import surycate_bot_ls2716.memory_faiss as memory_faiss
import prompt
import surycate_bot_ls2716.actions as actions
import surycate_bot_ls2716.utils as utils
# Set the logger
logger = utils.get_logger(__name__)

# Import the necessary modules
logger.debug("Imports done.")


def loop(task, llm, experiences: memory_faiss.KeyValueMemory, actions, state: dict):
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
        action = response.replace("Action:", "").strip()
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
    logger.debug("LLM set up.")
    # Set up the memory
    mem = memory_faiss.KeyValueMemory(
        'key_value_experiences', db_filename='faiss_single_task')
    logger.debug("Memory set up")
    mem.save_index("faiss_single_task")
    # Set a task
    task = tasks.Task("What is the current time?",
                      "No context available for this task.")
    logger.debug("Task set up.")
    # Set up actions
    actions = actions.ActionExecutor(actions.DEFAULT_ACTION_SET)
    logger.debug("Actions set up.")

    # Set up shell
    shell = PexpectShell()
    logger.debug("Shell set up.")

    state = {
        "llm": llm,
        "shell": shell,
        'task': task,
        'experiences': mem
    }

    # Execute the task
    loop(task, llm, mem, actions, state)
