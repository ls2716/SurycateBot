"""Test shell commands"""
import time
import pytest

from surycate_bot_ls2716.shell import Shell


def test_shell_initialisation():
    """Test shell initialisation"""
    shell = Shell()
    assert shell is not None


@pytest.fixture(scope="module")
def powershell():
    """Open a shell process"""
    shell = Shell(sh=['powershell'])
    time.sleep(0.5)
    output = shell.get_stdout()

    yield shell
    # Close the shell process
    shell.close()


def test_powershell_command(powershell):
    powershell.send_command("ls")
    output = powershell.get_stdout()
    # Assert that the output contains "Directory: "
    assert output.find("Directory: ") != -1


def test_powershell_command_error(powershell):
    powershell.send_command("ll")
    output = powershell.get_stdout()
    errors = powershell.get_stderr()
    # Assert that the term ll is not recognized
    assert errors.find("ObjectNotFound") != -1


@pytest.fixture(scope="module")
def bash():
    """Open a shell process"""
    shell = Shell()
    time.sleep(0.5)
    output = shell.get_stdout()

    yield shell
    # Close the shell process
    shell.close()


def test_bash_command(bash):
    bash.send_command("ll")
    output = bash.get_stdout()
    # Assert that the output contains "drwxrwxrwx "
    assert output.find("drwxrwxrwx") != -1
