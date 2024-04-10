import pytest
import subprocess
import time

import surycate_bot_ls2716.actions as actions
import surycate_bot_ls2716.shell as shell


@pytest.fixture(scope="module")
def state():
    return {}


@pytest.fixture(scope="module")
def action_object():
    return actions.Actions()


def test_execute(state, action_object):
    """Test action parsing"""
    action = "os_cmd dir"
    observation, task_done = action_object.execute(action, state)
    print(observation)
    # assert that the observation is correct and contains <DIR>
    assert observation.find("<DIR>") != -1
    # assert that the task is not done
    assert task_done is False


def test_finish(state, action_object):
    """Test finishing a task"""
    observation, task_done = action_object.execute("exit", state)
    # assert that the observation is correct
    assert observation == "Task is done."
    # assert that the task is done
    assert task_done is True


def test_time(state, action_object):
    """Test getting the time"""
    observation, task_done = action_object.execute("get_time", state)
    # assert that the observation is correct
    assert observation.startswith("Current time is:")
    # assert that the task is not done
    assert task_done is False


@pytest.fixture(scope="module")
def shell_object():
    shell_obj = shell.Shell()
    _ = shell_obj.get_stdout()
    print(_)
    yield shell_obj
    shell_obj.close()


def test_shell_command(state, shell_object, action_object):
    action = 'cmd ls'
    state['shell'] = shell_object
    observation, task_done = action_object.execute(action, state)
    # assert that the observation is correct and contains Name"
    assert observation.find("Name") != -1
    assert task_done is False


def test_shell_error(state, shell_object, action_object):
    action = 'cmd ll'
    state['shell'] = shell_object
    observation, task_done = action_object.execute(action, state)
    # assert that the observation is not correct
    assert observation.find("ll") != -1
    assert observation.find("ObjectNotFound") != -1
    assert task_done is False
