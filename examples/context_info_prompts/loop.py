"""Execution of the bot"""
import surycate_bot_ls2716.utils as utils
import surycate_bot_ls2716.actions as actions
import surycate_bot_ls2716.memory_faiss as memory_faiss
from surycate_bot_ls2716.llm import get_llm
from surycate_bot_ls2716.shell import PexpectShell
from prompt_template import build_prompt, context_info_template
from langchain_openai import OpenAIEmbeddings # type: ignore

# Import the command line arguments utility argparse
import argparse

# Set the logger
logger = utils.get_logger(__name__)


def print_execution(execution):
    """Print the execution."""
    print("@@@ Current execution history @@@")
    print(execution)
    print("@@@ End of current execution history @@@")

def print_prompt(prompt):
    """Print the prompt."""
    print("@@@ Prompt @@@")
    print(prompt)
    print("@@@ End of prompt @@@")


def loop(context, llm, knowledge: memory_faiss.MultiKeyMemory, experiences: memory_faiss.MultiKeyMemory,
         actions, shell):
    """Execute one task.

    The input to each loop is a context, a set of experiences, a set of actions, state and prompt template.
    Each loop of the task consists of the following steps:
    1. Get information regarding the context from the knowledge memory.
    2. Get similar experiences from the experience memory.
    3. Build the prompt and first get the action thought from LLM.
    4. Get the action response from LLM.
    5. Execute the action and receive the observation.
    6. Get the thought regarding the action form LLM.
    7. Get the new context from LLM.

    """

    execution = f"CONTEXT:\n{context}\n"
    logger.debug("Starting the task loop")
    print_execution(execution)

    while True:
        # STEP 1: Get the information regarding the context from the knowledge memory
        _, context_info = knowledge.get_memories(execution, key_type="context")
        # STEP 2: Get the similar experiences from the experience memory based on context and information
        # First add the information to the execution
        execution += "INFORMATION:\n" + \
            "\n".join(f"- {info}" for info in context_info)
        print_execution(execution)
        # Get the similar experiences
        _, similar_experiences = experiences.get_memories(
            execution, key_type="context")
        
        # STEP 3: Build the prompt and first get the action thought from LLM
        execution += "\nACTION THOUGHT:\n"
        prompt = build_prompt(similar_tasks=similar_experiences, execution=execution)
        print_prompt(prompt)
        input("Is the prompt ok? [y]")

        # Get the action thought from LLM
        action_thought = llm.invoke(prompt).content
        execution += f"{action_thought}\n"
        print_execution(execution)
        input("Is the action thought ok? [y]")

        # STEP 4: Get the action response from LLM
        execution += "ACTION:\n"
        prompt = build_prompt(similar_tasks=similar_experiences, execution=execution)
        print_prompt(prompt)
        input("Is the prompt ok? [y]")
        # Get the action response from LLM
        action_response = llm.invoke(prompt).content
        execution += f"{action_response}\n"
        print_execution(execution)
        input("Is the action ok? [y]")

        # STEP 5: Execute the action and receive the observation
        observation, task_done = actions.execute(action_response, state={"shell": shell})
        execution += f"OBSERVATION:\n{observation}\n"
        print_execution(execution)
        input("Is the observation ok? [y]")

        # STEP 6: Get the thought regarding the action form LLM
        execution += "OBSERVATION THOUGHT:\n"
        prompt = build_prompt(similar_tasks=similar_experiences, execution=execution)
        print_prompt(prompt)
        input("Is the prompt ok? [y]")
        # Get the thought regarding the action from LLM
        observation_thought = llm.invoke(prompt).content
        execution += f"{observation_thought}\n"
        print_execution(execution)
        input("Is the observation thought ok? [y]")

        # STEP 7: Get the new context from LLM
        execution += "NEW CONTEXT:\n"
        prompt = build_prompt(similar_tasks=similar_experiences, execution=execution)
        print_prompt(prompt)
        input("Is the prompt ok? [y]")
        # Get the new context from LLM
        new_context = llm.invoke(prompt).content
        execution += f"{new_context}\n"
        print_execution(execution)
        input("Is the new context ok? [y]")
        



        exit(0)
    # Return the task
    return context


if __name__ == "__main__":
    # Get the task name from the command line as well as the prompt type
    parser = argparse.ArgumentParser()
    parser.add_argument("--task_name", type=str,
                        help="The name of the task", required=True)
    args = parser.parse_args()
    # Get the task name
    task_name = args.task_name

    # Get the starting context
    with open(f"{task_name}", "r") as f:
        context = f.read().strip()
    logger.debug(f"Starting context: {context}")
    input("Is the starting context ok? [y]")

    # Set up an LLM
    llm = get_llm(model="gpt-4o-mini")
    logger.debug("LLM set up")

    # Set up the experiences memory
    experiences = memory_faiss.MultiKeyMemory(
        'experiences', keys=["context", "observation"], embeddings=OpenAIEmbeddings(), load=False)
    logger.debug("Experiences set up")

    # Set up the knowledge memory
    knowledge = memory_faiss.MultiKeyMemory(
        'memories', keys=["context"], embeddings=OpenAIEmbeddings(), load=False)

    # Set up actions
    actions = actions.ActionExecutor(action_set=actions.DEFAULT_ACTION_SET)


    # Set up shell
    shell = PexpectShell()

    # Execute the task
    loop(context=context, llm=llm, knowledge=knowledge,
         experiences=experiences, actions=actions, shell=shell)
