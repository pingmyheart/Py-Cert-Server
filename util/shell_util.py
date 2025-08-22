import subprocess


def run_command(command: str):
    """
    Run a shell command and return the result.
    """
    command_result = subprocess.run(command,
                                    capture_output=True,
                                    text=True,
                                    shell=True)
    return command_result.returncode, command_result.stdout.strip()
