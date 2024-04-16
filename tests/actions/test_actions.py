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
def powershell():
    shell_obj = shell.Shell(sh=['powershell'])
    # _ = shell_obj.get_stdout()
    # print(_)
    yield shell_obj
    shell_obj.close()


def test_powershell_command(state: Dict, powershell: shell.Shell, action_executor: actions.ActionExecutor):
    action = 'cmd ls'
    state['shell'] = powershell
    observation, task_done = action_executor.execute(action, state)
    # assert that the observation is correct and contains Name"
    assert observation.find("Name") != -1
    # assert task_done is False


def test_powershell_error(state: Dict, powershell: shell.Shell, action_executor: actions.ActionExecutor):
    action = 'cmd ll'
    state['shell'] = powershell
    observation, task_done = action_executor.execute(action, state)
    # assert that the observation is not correct
    assert observation.find("ll") != -1
    assert observation.find("ObjectNotFound") != -1
    # assert task_done is False


@pytest.fixture(scope="module")
def bash():
    shell_obj = shell.Shell(sh=['bash'])
    yield shell_obj
    shell_obj.close()


def test_bash_command(state: Dict, bash: shell.Shell, action_executor: actions.ActionExecutor):
    # Test successful bash command
    action = 'cmd ll'
    state['shell'] = bash
    observation, task_done = action_executor.execute(action, state)
    # print(observation)
    # assert that the observation is correct and contains "drwxrwxrwx"
    assert observation.find("drwxrwxrwx") != -1
    assert task_done is False
    assert observation.find("was executed successfully") != -1


def test_bash_error(state: Dict, bash: shell.Shell, action_executor: actions.ActionExecutor):
    # Test unsuccessful bash command
    action = 'cmd lq'
    state['shell'] = bash
    observation, task_done = action_executor.execute(action, state)
    # assert that the observation is not correct
    assert observation.find("lq") != -1
    assert observation.find("command not found") != -1
    assert task_done is False
    assert observation.find("resulted in error") != -1
