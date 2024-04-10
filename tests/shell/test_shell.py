"""Test shell commands"""
import time
import pytest

from surycate_bot_ls2716.shell import Shell


def test_shell_initialisation():
    """Test shell initialisation"""
    shell = Shell()
    assert shell is not None


@pytest.fixture(scope="module")
def shell():
    """Open a shell process"""
    shell = Shell()
    time.sleep(0.5)
    output = shell.get_stdout()

    yield shell
    # Close the shell process
    shell.close()


def test_shell_command(shell):
    shell.send_command("ls")
    output = shell.get_stdout()
    # Assert that the output contains "Directory: "
    assert output.find("Directory: ") != -1


def test_shell_command_error(shell):
    shell.send_command("ll")
    output = shell.get_stdout()
    errors = shell.get_stderr()
    print(output)
    print(errors)
    # Asser that the term ll is not recognized
    assert errors.find("ObjectNotFound") != -1
