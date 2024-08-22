# Verbose prompting

In this subproject, we explore the idea of verbose prompting. 

## What is verbose prompting?

In the current form of the surycate_bot package the bot is given task and context. Using the task and the context it encodes the task and context into a query. The query is then sent to the key_value memory to retrieve the memories of similar experiences along with their contexts if there are ones. The bot then uses the retrieved memories to fill its own prompt and use it to generate response using Thought Action Observation procedure.

The main idea is that the prompt is unchanging and the memories have to contain all the information:
- task
- the context
- the whole experience.

This is okay for small tasks but for more complex tasks, the memories (context, task, experience) can be quite large. This can lead to the memory being filled with a lot of information that is not relevant to the task. This is then even worse if we think about adding visual information to the memories.

In the verbose prompting, we focus on more memories that correspond to single or two actions. The memories should have larger context but the experience should be smaller. Then, at each loop of the bot, the prompt should be regenerated based on the current large context, observation and the action. This way the bot can focus on the current task and context and not be overwhelmed by the large memories.

###  Example

Let's say we have a task: "Tell me the current time." and the context is "The user is asking for the current time."

The current experience would look like following. 

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
What is the current time?

In the past, you have performed similar tasks:
----------------
Task: Create a folder named "Code".
Task context:
You are in the current directory and working on a project to create a website.
START:
Thought: I need to create a folder named "Code".
Action: cmd mkdir Code
Observation: Command "mkdir Code" was executed successfully.
OUTPUT:
~
STATUS_CODE=0
~
Thought: I finished the task.
Action: exit
----------------
Task: Assimilate information from the following text. "Olaf Scholz is the chancellor of Germany."

Memories:
- Joe Biden is the president of United States.
- Who is the president of Poland? Andrzej Duda is currently the president of Poland.

Start:
Thought: I didn't know that Olaf Scholz is the chancellor of Germany.
Action: create_memory "Olaf Scholz is the chancellor of Germany".
Observation: Success.
Thought: I have completed the task.
Action: exit
----------------
Task: Tell me the current time.
Task context:
There is no context specific to this task.
START:
Thought: I need to find out what is the current time.
Action: get_time
Observation: Current time is: 2024-04-10 13:16:13
Thought: I now know the current time and can return the answer.
Action: tell "Current time is 2024-04-10 13:16."
Observation: None
Thought: I have completed the task.
Action: exit
----------------

Your task is:
What is the current time?
Task context:
No context available for this task.
START:
Thought: I need to find out what the current time is.
Action: get_time
Observation: Current time is: 2024-08-22 14:26:23
Thought: I now know the current time and can return the answer.
Action: tell "Current time is 2024-08-22 14:26."
Observation: None
Thought: I have completed the task.
Action: exit
```

This is okay for the simple task of telling time. Now, how it should look like for verbose prompting.


The prompt:
```
You are an assistant who performs various tasks for the user. Given context information that includes the task, you should generate an action which will result in an observation. Given the previous context, action and generation, first generate a thought about the observation. Then, generate an updated context.

For example:

Context:
I am working on a project to create a website. I already have created a folder named "Website". I want to create a markdown file with the description of the website but I am now in the parent folder of the "Website" folder. I need to change the directory to the "Website" folder.
Action:
cmd cd Website
Observation:
lukasz@Smith:~/Projects$ cd Website
lukasz@Smith:~/Projects/Website$
Thought:
I have changed the directory to the "Website" folder. I can now create the markdown file.
New Context:
I am working on a project to create a website. I am in the "Website" folder. I want to create a markdown file with the description of the website. To do that, I have to create a markdown file in the "Website" folder called README.md.

In addition, you have access to past experiences and memories in the form of Context, Action, Observation, Thought, and New Context.

Past memories and experiences similar to the current task:

---
Context:
I am working on a project to create a website. I already have created a folder named "LS314_Website". I want to create a markdown file with the description of the website but I am now in the parent folder of the "LS314_Website" folder. I need to change the directory to the "LS314_Website" folder.
Action:
cmd cd LS314_Website
Observation:
lukasz@Smith:~/LS314/Projects$ cd LS314_Website
lukasz@Smith:~/LS314/Projects/LS314_Website$
Thought:
I have changed the directory to the "LS314_Website" folder. I can now create the markdown file.
New Context:
I am working on a project to create a website. I am in the "LS314_Website" folder. I want to create a markdown file with the description of the website. To do that, I have to create a markdown file in the "LS314_Website" folder called README.md.
---
Context:
I am working on a project to create a website. I already have created a folder named "New_Website". I want to create a markdown file with the description of the website but I don't know where I am in the file system. I need to find out where I am.
Action:
cmd pwd
Observation:
lukasz@Smith:~/LS314/Projects/New_Website/Code$
Thought:
I am in the "Code" folder which is inside the "New_Website" folder. I have to change the directory to the "New_Website" folder.
New Context:
I am working on a project to create a website. I am in the "Code" folder which is inside the "New_Website" folder. I want to create a markdown file with the description of the website. To do that, I have to change the directory to the "New_Website" folder which is the parent folder of the "Code" folder.
---


Your current context is following:
Context:
I just started a project to create my personal website. I have created a folder named "WebsitePersonal". I want to create a markdown file with the description of the website but I am now in the parent folder of the "WebsitePersonal" folder. I need to change the directory to the "WebsitePersonal" folder.
Action:
cmd cd WebsitePersonal
Observation:
lukasz@Smith:~/Projects$ cd WebsitePersonal
lukasz@Smith:~/Projects/WebsitePersonal$
Thought:
I have changed the directory to the "WebsitePersonal" folder. I can now create the markdown file.
New Context:
I am working on a project to create a website. I am in the "WebsitePersonal" folder. I want to create a markdown file with the description of the website. To do that, I have to create a markdown file in the "WebsitePersonal" folder called README.md.
```

In the verbose prompting, the memories are smaller and the prompt is generated at each loop of the bot. This way the bot can focus on the current task and context and not be overwhelmed by the large memories.

## Development of the verbose prompting feature

The feature requires the following new components:
1. New promting module which assembles the prompt based on the current context, action, observation, and thought as well as the memories.
2. The memories folder which contains the memories of the experiences - this folder will be used to generate the KeyValueMemory object.


## Results

The verbose prompting feature is implemented and briefly tested. The bot can now generate the prompt based on the current context, action, observation, and thought as well as the memories. The memories are stored in the memories folder and are used to generate the KeyValueMemory object. The bot can now focus on the current task and context and not be overwhelmed by the large memories.

The current use case is changing a directory to a folder which is very limited. The next step is to expand the use cases and test the bot on more complex tasks.

The experiments indicate that the idea can be implemented. For now, the memory retrieval is based on the context only which
is enough, but in the future, the memory retrieval should be based on the context and the observation after the action.
This is because depending on the outcome of the action, the next step might be different.

## Possible tasks for demonstration

- Break down tasks into smaller tasks
- Ge through the emails and report important emails.
- Tell the time.