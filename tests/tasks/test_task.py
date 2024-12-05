import os
import shutil

import pytest

import surycate_bot_ls2716.tasks as tasks


def test_task_init():
    """Test initialisation of a task."""
    task = tasks.Task(task="Create a directory named test",
                      context="This task is part of a project to create a website.")
    assert task.task == "Create a directory named test"
    assert task.context == "This task is part of a project to create a website."
    assert task.task_done is False


def test_task_done():
    """Test setting a task as done."""
    task = tasks.Task(task="Create a directory named test",
                      context="This task is part of a project to create a website.")
    task.finish_task(
        experience="Thought: I need to create a directory named 'test'.\n" +
        "Action: cmd mkdir test\n" +
        "Observation: Directory 'test' has been created.")
    assert task.task_done is True


def test_format_task():
    """Test formatting a task."""
    task = tasks.Task(task="Create a directory named test",
                      context="This task is part of a project to create a website.")
    assert task.format_task() == "Task: Create a directory named test.\nContext:" +\
        "This task is part of a project to create a website.\nSTART:\nThought: "


@pytest.fixture(scope="module")
def finished_task():
    task = tasks.Task(task="Create a directory named test",
                      context="This task is part of a project to create a website.")
    task.finish_task(
        experience="Thought: I need to create a directory named 'test'.\n" +
        "Action: cmd mkdir test\n" +
        "Observation: Directory 'test' has been created.")
    return task
