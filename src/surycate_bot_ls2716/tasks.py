"""Implements a task list for the bot."""


# Define the task list class
class TaskList(object):
    """Task list class.

    The task list class holds a list of tasks that the bot can do.
    """

    def __init__(self, tasks: list) -> None:
        """Initialize the task list."""
        # Set the tasks
        self.tasks = []
        self.task_no = 0

    def get_current_task(self) -> str:
        """Return the current."""
        return self.tasks[self.task_no]

    def insert_task(self, task: str):
        """Insert a task."""
        self.tasks.insert(self.task_no, task)

    def next_task(self):
        """Move to the next task."""
        self.task_no += 1

    def _get_tasks(self) -> list:
        """Return the tasks."""
        return self.tasks


class Task(object):
    """Task class."""

    def __init__(self, task: str, context: str) -> None:
        """Initialize the task."""
        self.task = task
        self.context = context
        self.task_done = False
        self.experience = None
        self.history = "START:\nThought: "

    def __str__(self) -> str:
        """Return the string representation of the task."""
        return f"{self.task}: {self.context}"

    def finish_task(self, experience: str):
        """Finish the task."""
        self.task_done = True
        self.experience = experience

    def format_task(self) -> str:
        """Format the task."""
        return f"Task: {self.task}.\nContext:{self.context}\n{self.history}"
