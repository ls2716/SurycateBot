"""Test shell commands"""
import time
import pytest

from surycate_bot_ls2716.shell import PexpectShell
import io


def print_to_string(*args, **kwargs):
    output = io.StringIO()
    print(*args, file=output, **kwargs)
    contents = output.getvalue()
    output.close()
    return contents


def test_pexpectshell_initialisation():
    """Test shell initialisation"""
    shell = PexpectShell()
    assert shell is not None
    output = shell.get_output()
    assert output.endswith("$ ")
    shell.close()


@pytest.fixture(scope="module")
def bash():
    """Open a shell process"""
    shell = PexpectShell()
    output = shell.get_output()
    yield shell
    # Close the shell process
    shell.close()


def test_bash_command(bash):
    """Test a bash command "ll" that should return a list of files and directories
    in the current directory."""
    # Send the command
    bash.send_command("ls -al")
    # Get the output of the command
    output = bash.get_output()
    print(output)
    # Assert that the output contains "drwxrwxrwx "
    assert output.find("drwxrwxrwx") != -1


def test_get_last_lines(bash):
    """Test the get_last_lines method."""
    # Send the command
    bash.send_command("ls -al")
    _ = bash.get_output()
    # Get the last 2 lines of the output
    output = bash.get_last_lines(2)
    print(output)
    # Assert that the output contains "drwxrwxrwx "
    assert output.find("rwxrwx") != -1
    assert len(output.split("\n")) == 2
    assert output.find("total") == -1


def test_execute_command(bash):
    """Test the execute_command method."""
    # Execute the command and get the output
    output = bash.execute_command("ls /")
    print(output)
    # Assert that the output contains "/home"
    assert output.find("home") != -1
    assert output.find("bin") != -1
    assert output.endswith("$ ")


def test_bad_command(bash):
    """Test a bad command."""
    # Execute the command and get the output
    output = bash.execute_command("ls nonexistent")
    print(output)
    # Assert that the output contains "No such file or directory"
    assert output.find("No such file or directory") != -1
    assert output.endswith("$ ")


def test_timeout(bash):
    """Test a command that times out."""
    bash.command_timeout = 0.2
    output = bash.execute_command("sleep 0.5", command_time=0.0)
    print(output)
    assert output.find("sleep 0.5") != -1
    assert output.split("\n")[-1] == ""
    bash.command_timeout = 1.
    output = bash.get_output()
    print('---')
    print(output)
    assert output.endswith("$ ")
    assert output.find("sleep 0.5") == -1
    # Get the last two lines of the output
    output = bash.get_last_lines(2).split("\n")
    print('---')
    print(output)
    assert output[0].endswith("sleep 0.5")
    assert output[1].endswith("$ ")
    assert output[1].startswith("lukasz")
