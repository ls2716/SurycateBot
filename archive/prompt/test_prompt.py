import pytest
import os
import shutil


import surycate_bot_ls2716.prompt as prompt
import surycate_bot_ls2716.memory as memory
import surycate_bot_ls2716.tasks as tasks


# Define fixture which creates a path to the memory folder
@pytest.fixture(scope="module")
def memory_path():
    path = os.path.abspath(__file__)
    # Go up two directories
    path = os.path.dirname(path)
    path = os.path.dirname(path)
    path = os.path.join(path, "memory", "key_value_experiences")
    return path

# Define fixture which creates a memory object


@pytest.fixture(scope="module")
def mem(memory_path):
    mem = memory.KeyValueMemory(memory_path)
    return mem

# Define a fixture which creates a task object


@pytest.fixture(scope="module")
def task():
    task = tasks.Task(task="Create a directory named test",
                      context="This task is part of a project to create a website.")
    return task


def test_create_prompt(mem, task):
    """Test creating a prompt."""
    _, related_experiences = mem.get_memories(task.task)
    prompt_text = prompt.build_prompt(
        task.task, related_experiences, task.context, task.history)
    print(prompt_text)
    assert prompt_text == \
        """You are an assistant who performs various tasks for the user.
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
Create a directory named test

In the past, you have performed similar tasks:
----------------
Task: Assimilate information from the following text. "Olaf Scholz is the chancellor of Germany."

Memories:
- Joe Biden is the president of United States.
- Who is the president of Poland? Andrzej Duda is currently the president of Poland.

Start:
Thought: I didn't know that Olaf Scholz is the chancellor of Germany.
Action: create_memory "Olaf Scholz is the chancellor of Germany".
Observation: Success.
Thought: I have completed the task.
Action: EXIT
----------------
Task: Create a folder named "Code".

Memories:
- Code folders contain code.
- I can use mkdir command to create a folder.

START:
Thought: I need to create a folder named 'Code'.
Action: cmd mkdir Code
Observation: The folder 'Code' was created.
EXIT
----------------

Your task is:
Create a directory named test
Task context:
This task is part of a project to create a website.
START:
Thought: """
