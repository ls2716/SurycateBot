"""Test shell commands"""
import time
import pytest

from surycate_bot_ls2716.shell import Shell


def test_shell_initialisation():
    """Test shell initialisation"""
    shell = Shell()
    assert shell is not None
    output = shell._get_stdout()
    assert output == ""

    shell.close()


@pytest.fixture(scope="module")
def bash():
    """Open a shell process"""
    shell = Shell()
    yield shell
    # Close the shell process
    shell.close()


def test_bash_command(bash):
    """Test a bash command "ll" that should return a list of files and directories
    in the current directory."""
    output, error, status_code = bash.execute_command("ll")
    # Assert that the output contains "drwxrwxrwx "
    assert output.find("drwxrwxrwx") != -1


def test_bash_command_error(bash):
    """Test a bash command that should return an error"""
    output, error, status_code = bash.execute_command("not_a_command")
    assert status_code != 0
    assert error.__contains__("not_a_command: command not found")


def test_bash_command_timeout(bash):
    """Test the timeout of a command"""
    with pytest.raises(TimeoutError):
        bash.execute_command("sleep 0.2", timeout=0.1)
