import pytest
from typing import Dict, List

import surycate_bot_ls2716.actions as actions
import surycate_bot_ls2716.shell as shell


@pytest.fixture(scope="module")
def state():
    return {}


@pytest.fixture(scope="module")
def action_executor():
    return actions.ActionExecutor(action_set=actions.DEFAULT_ACTION_SET)


def test_finish(state: Dict, action_executor: actions.ActionExecutor):
    """Test finishing a task"""
    observation, task_done = action_executor.execute("exit", state)
    # assert that the observation is correct
    assert observation == "Task is done."
    # assert that the task is done
    assert task_done is True


def test_time(state: Dict, action_executor: actions.ActionExecutor):
    """Test getting the time"""
    observation, task_done = action_executor.execute("get_time", state)
    # assert that the observation is correct
    assert observation.startswith("Current time is:")
    # assert that the task is not done
    assert task_done is False


@pytest.fixture(scope="module")
def bash():
    shell_obj = shell.PexpectShell(command_timeout=1.)
    yield shell_obj
    shell_obj.close()


def test_bash_command(state: Dict, bash: shell.PexpectShell, action_executor: actions.ActionExecutor):
    # Test successful bash command
    action = 'cmd ls -la'
    state['shell'] = bash
    observation, task_done = action_executor.execute(action, state)

    # Debugging statements
    print(f"Observation: {observation}")
    print(f"Task Done: {task_done}")

    # assert that the observation is correct and contains "drwxrwxrwx"
    assert observation.find("drwxrwxrwx") != -1
    assert task_done is False
