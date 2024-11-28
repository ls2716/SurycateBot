"""Execution of the bot"""
import prompts
# Import the logging module
import surycate_bot_ls2716.utils as utils
import surycate_bot_ls2716.actions as actions
import surycate_bot_ls2716.memory_faiss as memory_faiss
from surycate_bot_ls2716.llm import get_llm
from surycate_bot_ls2716.shell import PexpectShell

# Import the command line arguments utility argparse
import argparse

# Set the logger
logger = utils.get_logger(__name__)


def loop(context, llm, experiences: memory_faiss.KeyValueMemory, actions, state: dict, prompt_template):
    """Execute one task."""

    history = "ACTION THOUGHT:\n"

    while True:
        # Get the related experiences
        _, related_experiences = experiences.get_memories(context, key_type="context")
        # Build the prompt
        prompt_text = prompts.build_prompt(prompt_template,
            related_experiences, context, history=history)
        logger.debug(f"PROMPT: #####")
        print(prompt_text)
        logger.debug(f"#####")
        input("Is the prompt ok? [y]")
        # Get the response
        action_thought = llm.invoke(prompt_text).content
        logger.debug(f"ACTION THOUGHT: {action_thought}")
        input("Is the action thought ok? [y]")
        # Add the response to the history
        history += action_thought + "\nACTION:\n"
        # Build the prompt
        prompt_text = prompts.build_prompt(prompt_template,
            related_experiences, context, history=history)
        print(prompt_text)
        input("Is the prompt ok? [y]")
        action_response = llm.invoke(prompt_text).content
        logger.debug(f"ACTION: {action_response}")
        input("Is the action ok? [y]")
        # Add the action to the history
        history += action_response + "\n"
        # Get the action
        action = action_response.strip()
        # Execute the action
        observation, task_done = actions.execute(action, state)
        # Append the observation to the prompt if the task is not done
        if not task_done:
            history += "OBSERVATION:\n" + observation + "\nTHOUGHT:\n"
        else:
            break
        prompt_text = prompts.build_prompt(prompt_template,
            related_experiences, context, history=history)
        # Get the thought
        thought = llm.invoke(prompt_text).content
        logger.debug(f"THOUGHT:\n{thought}")
        input("Is the action thought ok? [y]")
        # Add the thought to the history
        history += thought + "\nNEW CONTEXT:\n"
        # Get the new context
        prompt_text = prompts.build_prompt(prompt_template,
            related_experiences, context, history=history)
        print(prompt_text)
        input("Prompt ok?")
        new_context = llm.invoke(prompt_text).content
        logger.debug(f"New context: {new_context}")
        input("New context ok?")
        # Update the context
        context = new_context
        # Print the whole output to a log file
        history += new_context + "\n"
        prompt_text = prompts.build_prompt(prompt_template,
            related_experiences, context, history=history)
        with open("task_log.txt", "w+") as f:
            f.write(prompt_text)        
        # Reset the history
        history = "Action: "
    # Return the task
    return context




if __name__ == "__main__":
    # Get the task name from the command line as well as the prompt type
    parser = argparse.ArgumentParser()
    parser.add_argument("--task_name", type=str, help="The name of the task")
    parser.add_argument(
        "--prompt_type", type=str, help="The type of the prompt to use. "+\
        "The available prompt types are: default, concise")
    args = parser.parse_args()
    # Get the task name
    task_name = args.task_name
    # Get the prompt type
    prompt_type = args.prompt_type
    # Get the prompt
    prompt_template = prompts.get_prompt(prompt_type)
    logger.debug(f"Prompt:")
    print(prompt_template.template)
    input("Is the prompt ok? [y]")
    # Get the task
    with open(f"tasks/{task_name}.txt", "r") as f:
        task = f.read()
    logger.debug(f"Task: {task}")
    input("Is the task ok? [y]")
    # Set up an LLM
    llm = get_llm(model="gpt-4o-mini")
    logger.debug("LLM set up")
    # Set up the memory
    mem = memory_faiss.MultiKeyMemory(
        'key_value_memories', keys=["context","observation"], db_filename='memory_faiss')
    logger.debug("Memory set up")
    # Get the context
    context = task
    # Strip the additional whitespace from the context and extra spaces between words
    context = ' '.join(context.split())
    logger.debug(f"Context: {context}")

    # Set up actions
    actions = actions.ActionExecutor(action_set=actions.DEFAULT_ACTION_SET)

    # Set up shell
    shell = PexpectShell()
    output = shell.get_output()
    print("Dummy output of the shell:")
    print(output)
    print("STARTING THE TASK")

    state = {
        "llm": llm,
        "shell": shell,
        'context': context,
        'experiences': mem
    }

    # Execute the task
    loop(context, llm, mem, actions, state, prompt_template)
