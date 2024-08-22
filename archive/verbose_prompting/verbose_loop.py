"""Execution of the bot"""

# Import the logging module
import surycate_bot_ls2716.utils as utils
import surycate_bot_ls2716.actions as actions
import surycate_bot_ls2716.memory as memory
from surycate_bot_ls2716.llm import get_llm
from surycate_bot_ls2716.shell import PexpectShell
import verbose_prompt as prompt

# Set the logger
logger = utils.get_logger(__name__)


def loop(context, llm, experiences: memory.KeyValueMemory, actions, state: dict):
    """Execute one task."""

    history = "Action:\n"

    while True:
        # Get the related experiences
        _, related_experiences = experiences.get_memories(context)
        # Build the prompt
        prompt_text = prompt.build_prompt(
            related_experiences, context, history=history)
        logger.debug(f"Prompt: \n{prompt_text}")
        input("Prompt ok?")
        # Get the response
        response = llm.invoke(prompt_text).content
        logger.debug(f"Response: {response}")
        input("Response ok?")
        # Add the response to the history
        history += response + "\n"
        # Get the action
        action = response.strip()
        # Execute the action
        observation, task_done = actions.execute(action, state)
        # Append the observation to the prompt if the task is not done
        if not task_done:
            history += "Observation:\n" + observation + "\nThought:\n"
        else:
            break
        prompt_text = prompt.build_prompt(
            related_experiences, context, history=history)
        # Get the thought
        thought = llm.invoke(prompt_text).content
        logger.debug(f"Thought:\n{thought}")
        input("Thought ok?")
        # Add the thought to the history
        history += thought + "\nNew Context:\n"
        # Get the new context
        prompt_text = prompt.build_prompt(
            related_experiences, context, history=history)
        new_context = llm.invoke(prompt_text).content
        logger.debug(f"New context: {new_context}")
        input("New context ok?")
        # Update the context
        context = new_context
        # Reset the history
        history = "Action: "
    # Return the task
    return context


if __name__ == "__main__":
    # Set up an LLM
    llm = get_llm()
    logger.debug("LLM set up")
    # Set up the memory
    mem = memory.KeyValueMemory(
        'verbose_memory_by_context', db_filename='verbose_memory_faiss')
    logger.debug("Memory set up")
    # mem.save_index("verbose_memory_faiss")
    # Set a task
    context = """I am working on my personal website.
      I have created a folder named "Website". I want to create a markdown
        file with the description of the website but I am now in the parent 
        folder of the "Website" folder. I need to change the directory to the "Website" folder.
        """
    # Strip the additional whitespace from the context and extra spaces between words
    context = ' '.join(context.split())
    logger.debug(f"Context: {context}")

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
        'context': context,
        'experiences': mem
    }

    # Execute the task
    loop(context, llm, mem, actions, state)
