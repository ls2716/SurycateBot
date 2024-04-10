"""Implementation of the bot."""

import logging
import surycate_bot_ls2716.utils

# Define the default logger using utils
logger = surycate_bot_ls2716.utils.get_logger(__name__)

logger.debug("This is a debug message")
logger.info("This is an info message")
logger.warning("This is a warning message")


# Define the simple bot class
class Bot:
    """Simple bot class.

    The bot operates on a simple text interface between the user and the bot.
    """

    def __init__(self, name: str
                 ) -> None:
        """Initialize the bot."""
        # Set the name
        self.name = name
        # Set the logger
        self.logger = logging.getLogger(f"{__name__}.{self.name}")
        self.logger.debug("Bot has been initialised")

    def set_llm(self, llm: str) -> None:
        """Set the LLM."""
        self.llm = llm
        self.logger.debug(f"LLM has been set to {self.llm}")

    def set_embedding(self, embedding: str) -> None:
        """Set the embedding."""
        self.embedding = embedding
        self.logger.debug(f"Embedding has been set to {self.embedding}")

    def set_instructions(self, instructions: str) -> None:
        """Set the instructions."""
        self.instructions = instructions
        self.logger.debug(f"Instructions have been set to {self.instructions}")

    def set_actions(self, actions: str) -> None:
        """Set the actions."""
        self.actions = actions
        self.logger.debug(f"Actions have been set to {self.actions}")

    def do_task(self, task: str) -> None:
        """Do the task function.

        The bot takes a task from the user and does it,
          informing the user about the progress and the output."""
        ...
        # Step 1: Explain the task
        # Step 2: Find the instruction
        # Step 3: Execute the instruction

    def execute_instruction(self, instruction):
        """Execute the instruction."""
        # Step 1: Parse the instruction into a set of steps
        # Step 2: Execute the steps
        ...


if __name__ == "__main__":
    # Create the bot
    bot = Bot('bot')
