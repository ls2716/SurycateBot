# Surycate Bot Package

This is a surycate bot package which is used to create a text-based llm-powered
automation bot within a linux terminal.

The package contains basic functionalities for the bot to be used within the script that
runs automation.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/ls2716/SurycateBot.git
cd SurycateBot
```

2. (Optional) Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install the package using pip:

```bash
pip install -e .
```

4. Install required dependencies:

```bash
pip install -r requirements.txt
```

5. Set up environment variables for OpenAI API:

```bash
export OPENAI_API_KEY='your_openai_api_key_here'
```

### Testing the Installation

To test that setup was successful, run the tests:
```bash
pytest tests -v
```

This should run all the tests and confirm that everything is working as expected.
```
========================================================== test session starts ===========================================================
platform linux -- Python 3.12.11, pytest-8.3.3, pluggy-1.5.0
rootdir: /home/lukasz/LS314/SurycateBot
configfile: pyproject.toml
plugins: anyio-4.6.2.post1
collected 21 items                                                                                                                       

tests/actions/test_actions.py ...                                                                                                  [ 14%]
tests/llm/test_llm.py ..                                                                                                           [ 23%]
tests/memory/test_multi_key_memory.py ......                                                                                       [ 52%]
tests/shell/test_pexpect.py .......                                                                                                [ 85%]
tests/tasks/test_task.py ...                                                                                                       [100%]

========================================================== 21 passed in 10.57s ===========================================================
```


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


### Examples

For an example of the context prompting iteration, see
[/examples/context_info_prompts/](./examples/context_info_prompts/).

To run the example, execute:

```bash
cd examples/context_info_prompts/
python loop.py --task_name tasks/tell_datetime.txt
```

Execution will follow, stopping at each step. Press enter to continue.

Below is an example prompt obtained during execution:

```
@@@ Prompt @@@
Complete the next line in sequence using the following pattern:

CONTEXT:
<context>
INFORMATION:
- <information_1>
- <information_2>
- <information_3>
ACTION:
<action>
ACTION THOUGHT:
<action_thought>
OBSERVATION:
<observation>
OBSERVATION THOUGHT:
<observation_thought>
NEW CONTEXT:
<new_context>

Here are some examples that you should base the completions on:
---
CONTEXT:
The user has asked me what the current time is.
INFORMATION:
- I know how to tell time.
- There is a Linux command 'date' that can be used to measure the time it takes to run a command.
ACTION THOUGHT:
I can just use the date command to learn the time which I can then tell to the user.
ACTION:
cmd date
OBSERVATION:
Thu Nov 28 12:45:25 CET 2024
OBSERVATION THOUGHT:
I can tell the user that the current time is Thu Nov 28 12:45:25 CET 2024.
NEW CONTEXT:
The user has asked me what the current time is. Using the date command, I have learned that the current time is Thu Nov 28 12:45:25 CET 2024. I can now tell the user this information.

----------------
CONTEXT:
The user has asked me what the current time is. Using the date command, I have learned that the current time is Thu Nov 28 12:45:25 CET 2024. I told the user this information and completed the task.
INFORMATION:
- I know how to tell time.
- There is a Linux command 'date' that can be used to measure the time it takes to run a command.
ACTION THOUGHT:
I can end the execution since I have already told the user the time.
ACTION:
exit
OBSERVATION:
None
OBSERVATION THOUGHT:
None
NEW CONTEXT:
None

----------------
CONTEXT:
The user has asked me what is the current date and time. I have used the date command and found that the current date and time is Fri 07 Nov 2025 11:44:38 AM GMT. I can now share this information with the user.
INFORMATION:
- I know how to tell time.
- There is a Linux command 'date' that can be used to measure the time it takes to run a command.
ACTION THOUGHT:
I can just tell the user the date.
ACTION:
tell "The current date and time is Fri 07 Nov 2025 11:44:38 AM GMT."
OBSERVATION:
None
OBSERVATION THOUGHT:
I just told the user the current date and time. I can finish this task now.
NEW CONTEXT:
The user has asked me what the current time is. Using the date command, I have learned that the current time is Thu Nov 28 12:45:25 CET 2024. I told the user this information and completed the task.

---

CONTEXT:
The user has asked me what is the current date and time.
INFORMATION:
- There is a Linux command 'date' that can be used to measure the time it takes to run a command.
ACTION THOUGHT:
I need to use the date command to find out the current date and time so I can inform the user.  
ACTION:
cmd date  
OBSERVATION:
lukasz@lukasz-HP:~/LS314/SurycateBot/examples/context_info_prompts$ date
Fri 07 Nov 2025 03:05:20 PM GMT
lukasz@lukasz-HP:~/LS314/SurycateBot/examples/context_info_prompts$ 
OBSERVATION THOUGHT:
I can now tell the user the current date and time based on the output I received.  
NEW CONTEXT:
The user has asked me what is the current date and time. Using the date command, I have learned that the current date and time is Fri 07 Nov 2025 03:05:20 PM GMT. I can now share this information with the user.
INFORMATION:
- There is a Linux command 'date' that can be used to measure the time it takes to run a command.
ACTION THOUGHT:
I can simply inform the user of the current date and time based on the output I received.  
ACTION:

@@@ End of prompt @@@
```