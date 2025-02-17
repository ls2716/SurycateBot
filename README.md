# Surycate Bot Package

This is a surycate bot package which is used to create a text-based llm-powered
automation bot within a linux terminal.

The package contains basic functionalities for the bot to be used within the script that
runs automation.

## Installation

...

## Usage

To use the package, one needs to decide on the form of the iteration. Below is an
example of context prompting iteration.

### Context Prompting Iteration

Context prompting iteration requires the user to provide an initial context to the task
but more importantly memories based on which the bot will generate responses. The bot
will then generate responses based on the context and memories provided.

Each memory is formed by a sequence of: context, thought, action, observation, thought
and next context. For example, see a yaml version of a sample memory below:

```yaml
metadata:
  title: Got task to update linux and logged in.
  description:
    This is a memory of getting a task to update linux. This is after successful login.
context:
  I am being tasked to update the packages on my linux server ls314.com. I have
  successfully sshed into the server. I can now update the packages.
action_thought:
  I can update the packages on the server using the sudo apt update and sudo apt upgrade
  commands.
action: cmd sudo apt update && sudo apt upgrade
observation: |
  lukasz@ls314:~$ sudo apt update && sudo apt upgrade
  [sudo] password for lukasz:
thought: I have been prompted for a password. I will have to enter it first.
new_context:
  I am being tasked to update the packages on my linux server ls314.com. I have
  successfully sshed into the server and send the command to update the packages. I have
  been prompted for a password. I will have to enter it first.
```

The basic structure of the context prompting iteration is then as follows:

1. Initialize the bot with the context and memories.
2. Loop:
   1. Given the context, the bot fetches similar memories and loose informations.
   2. Based on the memoriesL experiences and information, as well as the context, the
      bot generates an action thought.
   3. The bot then generates an action based on the thought.
   4. The bot observes the action.
   5. The bot generates a new thought based on the observation.
   6. The bot generates a new context based on observation and the thought.

For an example of the context prompting iteration, see
[/examples/context_info_prompts/](./examples/context_info_prompts/).
