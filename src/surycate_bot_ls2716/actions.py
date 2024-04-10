"""Implement actions for the bot."""
from typing import List, Tuple

import time
from datetime import datetime
import subprocess

# Import the logging module
import surycate_bot_ls2716.utils as utils

# Set the logger
logger = utils.get_logger(__name__)


def execute_command(state, arguments) -> str:
    """Execute a command."""
    # Get the command
    command = arguments
    # Execute the command
    return_value = subprocess.run(command, shell=True, capture_output=True)
    # Get the output
    output = return_value.stdout.decode("utf-8")
    # Get the error
    error = return_value.stderr.decode("utf-8")
    # Get the command status
    status = return_value.returncode
    # If the command was successful
    if status == 0:
        observation = f"Command: {command}\nOutput: {output}"
    else:
        observation = f"Command: {command}\nError: {error}"
    # Return the observation
    return observation, False


def execute_shell_command(state, arguments) -> str:
    """Execute a shell command."""
    # Get the command
    command = " ".join(arguments)
    # Get the shell object
    shell = state['shell']

    # Log the command
    logger.debug(f"Shell command: {command}")

    # Execute the command
    shell.send_command(command)
    # Get the output
    output = shell.get_stdout()
    # Get the error
    error = shell.get_stderr()
    # If the command was successful
    if output == "":
        output = "None"
    if error == "":
        observation = f"Command '{command}'"\
            + f" was executed successfully.\nOUTPUT:\n```{output}```"
    else:
        observation = f"Command '{command}'"\
            + f" resulted in error.\nERROR:\n```{error}```"
    # Return the observation
    return observation, False


def get_time(state, arguments) -> str:
    """Get the current time."""
    # Get the current time
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # Return the time
    return "Current time is: " + current_time, False


actions = {
    "os_cmd": execute_command,
    "get_time": get_time,
    "exit": lambda state, arguments: ("Task is done.", True),
    "cmd": execute_shell_command
}


class Actions(object):
    """Actions class"""

    def __init__(self) -> None:
        self.actions = []

    def execute(self, action: str, state: dict) -> Tuple[str, bool]:
        """Execute the action."""
        # Log the action
        logger.info(f"Executing action {action}")
        # Split the action into the command and the arguments
        # The action format follows the pattern
        # COMMAND ARG1 ARG2 ARG3 ...
        action_parts = action.split(" ")
        # Get the command
        command = action_parts[0]
        # Get the arguments
        if len(action_parts) > 1:
            arguments = action_parts[1:]
        else:
            arguments = []
        # Execute the command
        observation, task_done = actions[command](state, arguments)
        return observation, task_done
