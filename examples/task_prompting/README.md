<<<<<<< HEAD:examples/task_prompting/README.md
# Surycate bot package explanation

This file specifies how to use the SurycateBot package to execute a single task using one task prompting.

Let us start with an example, simplistic use case.

## Example case

The example case is a simple task:
'Create a folder in the current directory named "lolapaloza"'.
Task context: None.

The procedure to execute this task is as follows:

1. Step 1: Initialise the components of the agent:
   1. prompt template - a PromptTemplate object used to generate prompts for the LLM engine. For more information on the prompt, see prompt.py module.
   2. LLM engine - an LLM object which receives a prompt and generates one line of response finished with newline character '\n'. For more information see llm.py module.
   3. memory - a memory object which takes a query and returns documents corresponding to the query. The query is a task in question and documents are histories of similar tasks. The memory object is implemented as a vectorstore. For more information see memory.py module.
   4. task - a simple Task object which contains the task, context and the task history as strings.
   5. actions - an Actions object whose purpose is to take an action string e.g. "Action: get_time", execute the action and return observation to the user. Together with the observation, the action return a task_done boolean which controls the end of the execution.
   6. shell - a Shell object which connects the agent to the shell. Specifically, the shell is used by the Actions object which sends commands to the shell and returns stdout, stderrr.
2. Set up the Thought-Action-Observation procedure:
   1. Get the related experiences from the memory using the task.
   2. Set the task_done to False.
   3. Build the prompt using the task, task context and the related experiences. The prompt will end with 'Thought: ' which is a starting point for the agent.
3. Loop through the Thought-Action-Observation procedure while the task is not done:
   1. Get the action. While the response returned by the LLM does not start with "Action: "
      1. Get the next response and append to the prompt.
   2. Execute the action using the Actions object.
   3. Append the observation and set the task_done boolean variable.


### Task execution process

Below is the task execution process:

#### Initial prompt:

```
You are an assistant who performs various tasks for the user.
You work in a text interface and follow thought, action, observation pattern.

For example:
Task: Create a directory named "test"
START:
Thought: I need to create a directory named "test"
Action: cmd mkdir test
Observation: Directory "test" has been created.
EXIT

Another example:
Task: List the files in the current directory.
START:
Thought: I need to list the files in the current directory. I can use the ls command.
Action: cmd ls
Observation: The files in the current directory are: file1 file2 file3
EXIT

In addition, you have access to similar task examples, the current task, and the memories.

Your current task is:
Create a folder named 'lolapaloza' in the current directory

In the past, you have performed similar tasks:
----------------
Task: Tell me the current time.
Task context:
There is no context specific to this task.
START:
Thought: I need to find out what is the current time.
Action: get_time
Observation: Current time is: 2024-04-10 13:16:13
Thought: I now know the current time and can return the answer.
Action: tell "Current time is 2024-04-10 13:16.
Observation: None
Thought: I have completed the task.
Action: exit
----------------
Task: Create a folder named "Code".
Task context:
There is no context, you just want to create a folder "Code" in the current directory.
START:
Thought: I need to create a folder named "Code".
Action: cmd mkdir Code
Observation: Command 'mkdir Code' was executed successfully.
OUTPUT:
None
Thought: I finished the task.
Action: exit
----------------

Your task is:
Create a folder named 'lolapaloza' in the current directory
Task context:
You are in the current directory and working on a project to create a website.
START:
Thought:
```
Above is the initial prompt evaluated using the past observations. We can see two observations (more relevant observations last), second of which shows the very similar task. The prompt ends with 'Thought: ' which starts the reasoning process.

```
I need to create a folder named 'lolapaloza' in the current directory for my website project.
```
Agent correctly analyses the task.
```
Action: cmd mkdir lolapaloza
```
Identifies the correct action to be executed. This is reported to the Actions object.
```
Observation: Command 'mkdir lolapaloza' was executed successfully.
OUTPUT:
```None```
Thought:
```
The actions object returns the observation, together with the output of the command. Since the task is not finished, new 'Thought: ' is appended to the prompt.
```
I have successfully created the folder named 'lolapaloza'.
```
Again, correct thought.
```
Action: exit
```
The agent executes the exit action which sets the task_done to false and ends the execution.

=======
# Surycate bot package explanation

This file specifies how to use the SurycateBot package to execute a single task using one task prompting.

Let us start with an example, simplistic use case.

## Example case

The example case is a simple task:
'Create a folder in the current directory named "lolapaloza"'.
Task context: None.

The procedure to execute this task is as follows:

1. Step 1: Initialise the components of the agent:
   1. prompt template - a PromptTemplate object used to generate prompts for the LLM engine. For more information on the prompt, see prompt.py module.
   2. LLM engine - an LLM object which receives a prompt and generates one line of response finished with newline character '\n'. For more information see llm.py module.
   3. memory - a memory object which takes a query and returns documents corresponding to the query. The query is a task in question and documents are histories of similar tasks. The memory object is implemented as a vectorstore. For more information see memory.py module.
   4. task - a simple Task object which contains the task, context and the task history as strings.
   5. actions - an Actions object whose purpose is to take an action string e.g. "Action: get_time", execute the action and return observation to the user. Together with the observation, the action return a task_done boolean which controls the end of the execution.
   6. shell - a Shell object which connects the agent to the shell. Specifically, the shell is used by the Actions object which sends commands to the shell and returns stdout, stderrr.
2. Set up the Thought-Action-Observation procedure:
   1. Get the related experiences from the memory using the task.
   2. Set the task_done to False.
   3. Build the prompt using the task, task context and the related experiences. The prompt will end with 'Thought: ' which is a starting point for the agent.
3. Loop through the Thought-Action-Observation procedure while the task is not done:
   1. Get the action. While the response returned by the LLM does not start with "Action: "
      1. Get the next response and append to the prompt.
   2. Execute the action using the Actions object.
   3. Append the observation and set the task_done boolean variable.


### Task execution process

Below is the task execution process:

#### Initial prompt:

```
You are an assistant who performs various tasks for the user.
You work in a text interface and follow thought, action, observation pattern.

For example:
Task: Create a directory named "test"
START:
Thought: I need to create a directory named "test"
Action: cmd mkdir test
Observation: Directory "test" has been created.
EXIT

Another example:
Task: List the files in the current directory.
START:
Thought: I need to list the files in the current directory. I can use the ls command.
Action: cmd ls
Observation: The files in the current directory are: file1 file2 file3
EXIT

In addition, you have access to similar task examples, the current task, and the memories.

Your current task is:
Create a folder named 'lolapaloza' in the current directory

In the past, you have performed similar tasks:
----------------
Task: Tell me the current time.
Task context:
There is no context specific to this task.
START:
Thought: I need to find out what is the current time.
Action: get_time
Observation: Current time is: 2024-04-10 13:16:13
Thought: I now know the current time and can return the answer.
Action: tell "Current time is 2024-04-10 13:16.
Observation: None
Thought: I have completed the task.
Action: exit
----------------
Task: Create a folder named "Code".
Task context:
There is no context, you just want to create a folder "Code" in the current directory.
START:
Thought: I need to create a folder named "Code".
Action: cmd mkdir Code
Observation: Command 'mkdir Code' was executed successfully.
OUTPUT:
None
Thought: I finished the task.
Action: exit
----------------

Your task is:
Create a folder named 'lolapaloza' in the current directory
Task context:
You are in the current directory and working on a project to create a website.
START:
Thought:
```
Above is the initial prompt evaluated using the past observations. We can see two observations (more relevant observations last), second of which shows the very similar task. The prompt ends with 'Thought: ' which starts the reasoning process.

```
I need to create a folder named 'lolapaloza' in the current directory for my website project.
```
Agent correctly analyses the task.
```
Action: cmd mkdir lolapaloza
```
Identifies the correct action to be executed. This is reported to the Actions object.
```
Observation: Command 'mkdir lolapaloza' was executed successfully.
OUTPUT:
```None```
Thought:
```
The actions object returns the observation, together with the output of the command. Since the task is not finished, new 'Thought: ' is appended to the prompt.
```
I have successfully created the folder named 'lolapaloza'.
```
Again, correct thought.
```
Action: exit
```
The agent executes the exit action which sets the task_done to false and ends the execution.

>>>>>>> 95f748be726e33da70c205f9a593e912c779f6f9:src/surycate_bot_ls2716/readme_flow.md
