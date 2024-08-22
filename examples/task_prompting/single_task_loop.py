"""Execution of the bot"""

# Import the logging module
import surycate_bot_ls2716.utils as utils
import surycate_bot_ls2716.actions as actions
import prompt
import surycate_bot_ls2716.memory as memory
import surycate_bot_ls2716.tasks as tasks
from surycate_bot_ls2716.llm import get_llm
from surycate_bot_ls2716.shell import PexpectShell

# Set the logger
logger = utils.get_logger(__name__)

def loop(task, llm, experiences: memory.KeyValueMemory, actions, state: dict):
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
        input("Prompt ok?")
        # Loop until the response starts with "Action:"
        while not response.startswith("Action:"):
            # Append the response to the prompt
            prompt_text += response + "\n"
            history += response + "\n"
            # Get the response
            response = llm.invoke(prompt_text).content
            logger.debug(f"Response: {response}")

        input("Response ok?")
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
    logger.debug("LLM set up")
    # Set up the memory
    mem = memory.KeyValueMemory(
        'key_value_experiences', db_filename='faiss_single_task')
    logger.debug("Memory set up")
    mem.save_index("faiss_single_task")
    # Set a task
    task = tasks.Task("Create a folder named 'lolapaloza' in the current directory",
                      "You are in the current directory and working on a project to create a website.")
    # Set up actions
    actions = actions.ActionExecutor(action_set=actions.DEFAULT_ACTION_SET)

    # Set up shell
    shell = PexpectShell()
    output = shell.get_output()
    print("Dummy output of the shell")
    print(output)

    state = {
        "llm": llm,
        "shell": shell,
        'task': task,
        'experiences': mem
    }

    # Execute the task
    loop(task, llm, mem, actions, state)
