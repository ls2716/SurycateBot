"""Implement actions for the bot."""

import shlex  # For splitting the command into a list of arguments
from datetime import datetime
from typing import Callable, Dict, List, Tuple

import surycate_bot_ls2716.shell as shell_lib

# Import the logging module
import surycate_bot_ls2716.utils as utils

# Set the logger
logger = utils.get_logger(__name__)


def execute_shell_command(state, arguments) -> str:
    """Execute a shell command using the shell in the state."""
    # Get the command
    command = " ".join(arguments)
    # Get the shell object
    shell = state["shell"]
    if type(shell) is not shell_lib.PexpectShell:
        raise TypeError("Shell object in the state is not of type Shell.")

    # Log the command
    logger.debug(f"Shell command: {command}")
    # Execute the command
    output = shell.execute_command(command)

    # Log the output, error, and status code
    logger.debug(f"Shell output: {output}")

    # Return the observation and the task_done flag set to False
    # Shell commands never end the task
    return output, False


def get_time(state: Dict, arguments: List[str]) -> Tuple[str, bool]:
    """Get the current time action."""
    # Get the current time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Return the time and the task_done flag set to False
    return "Current time is: " + current_time, False


def task_done(state: Dict, arguments: List[str]) -> Tuple[str, bool]:
    """Task is done.
    Return the observation that the task is done and a boolean True indicating
    that the task is done.
    """
    return "Task is done.", True


def tell(state: Dict, arguments: List[str]) -> Tuple[str, bool]:
    """Tell the user something."""
    # TODO: Implement the tell action
    # Return the message and the task_done flag set to False
    return "None", False


# Specify the available actions in the action_set dictionary
DEFAULT_ACTION_SET = {
    "get_time": get_time,
    "exit": task_done,
    "cmd": execute_shell_command,
    "tell": tell,
    "no_action": lambda state, arguments: ("None", False),
}


class ActionExecutor(object):
    """ActionExecutor class.

    This class is responsible for executing actions.
    It is set up with the possible actions in the form of a dictionary.

    Given an action string "command arg1 arg2 arg3 ...", the
    ActionExecutor will execute the command with the arguments.

    The ActionExecutor will return the observation and a boolean indicating
    whether the task is done.
    """

    def __init__(self, action_set: Dict[str, Callable]) -> None:
        # Set the actions available to the ActionExecutor
        self.action_set = action_set

    def execute(self, action: str, state: Dict) -> Tuple[str, bool]:
        """Execute the action."""
        # Log the action
        logger.info(f"Executing action {action}")
        # Split the action into the command and the arguments
        # The action format follows the pattern
        # command arg1 arg2 arg3 ...
        # will respect quotation marks and get keep them
        action_parts: List[str] = shlex.split(action, posix=True)
        # Get the command
        command: str = action_parts[0]
        # Check that the action is available
        if command not in self.action_set:
            raise ValueError(f"Action '{command}' is not available.")
        # Get the arguments as strings
        if len(action_parts) > 1:  # If there are arguments
            arguments = action_parts[1:]
        else:  # If there are no arguments
            arguments = []  # Set the arguments to an empty list
        # Execute the command
        observation, task_done = self.action_set[command](state, arguments)
        return observation, task_done


if __name__ == "__main__":
    # Initialise the shell
    shell = shell_lib.PexpectShell()
    # Set the state
    state = {"shell": shell}
    # Set up the ActionExecutor
    actions = ActionExecutor(DEFAULT_ACTION_SET)
    # Execute the command
    action = "cmd ls -la"
    observation, task_done = actions.execute(action, state)
    print(observation)
    # Close the shell
    shell.close()
