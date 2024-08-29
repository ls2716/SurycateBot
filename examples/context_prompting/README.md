# Context prompting

This directory contains an example of context prompting. It is based on the idea that
every action should be based on a broad context which contains all information necessary
to choose an action and then create a new context based on the results of the action.

The agent chooses the new action based on the previous experiences and the current
context.

## Example: Moving to a folder Website

The example case is a simple task, to move to a folder named "Website" when in parent
directory.

```
You are an agent with an available terminal who performs various tasks.
Given context information that includes the task, you should generate an action which will result in an observation.
Given the previous context, action and the observation, first generate a thought about the observation.
Then, generate an updated context which contains a summary of previous information and the idea what to do next.

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

In above, given the context "I am working on a project to create a website.
 I already have created a folder named "Website". I want to create a markdown file with the description of the website
   but I am now in the parent folder of the "Website" folder. I need to change the directory to the "Website" folder."
you generate an action "cmd cd Website" which results in an observation. This results in an observation:
"lukasz@Smith:~/Projects$ cd Website
lukasz@Smith:~/Projects/Website$"
Following the observation, you generate a thought about the observation and how it relates to the context:
 "I have changed the directory to the "Website" folder. I can now create the markdown file."
Finally, you generate an updated context which contains a summary of previous information and the idea what to do next:
"I am working on a project to create a website. I am in the "Website" folder.
 I want to create a markdown file with the description of the website.
 To do that, I have to create a markdown file in the "Website" folder called README.md."

Always follow this pattern when generating actions, observations, thoughts, and new contexts, that is
Context -> Action -> Observation -> Thought -> New Context.
It should always be in this order and look like following:
``
Context:
<context>
Action:
<action>
Observation:
<observation>
Thought:
<thought>
New Context:
<new_context>
``

In addition, you have access to past experiences and memories in the form of Context, Action, Observation, Thought, and New Context.
Use this information.

Past memories similar to the current context:
----------------
Context:
I am working on a project to create a website. I have just created a REAMDME.md file in the "WebsitePersonal" folder. I want to write the description of the website in the README.md file. I am currently in the "WebsitePersonal" folder which also contains the REAMDME.md file.
Action:
cmd echo "# Lukasz's personal website" > README.md
Observation:
lukasz@Smith:~/Projects/WebsitePersonal$ echo "# Lukasz's personal website" > README.md
lukasz@Smith:~/Projects/WebsitePersonal$
Thought:
I have written the description of the website in the README.md file. I can now start writing the content of the website in the README.md file.
New Context:
I am working on a project to create a website. I am in the "WebsitePersonal" folder. I have written the description of the website in the README.md file. I can now start writing the content of the website in the README.md file. The content of the website should include the different sections of the website such as the home page, about page, contact page, and other relevant information.
----------------
Context:
I am working on a project to create a website. I have created a folder called Website and now I want to create a README.md file in the Website folder. I am in the parent folder of the Website folder. I have to change the directory to the Website folder.
Action:
cmd cd Website
Observation:
lukasz@Smith:/mnt/c/Users/luki3/Projects/LS314/Projects/Surycate/SurycateBot/verbose_prompting$ cd Website
lukasz@Smith:/mnt/c/Users/luki3/Projects/LS314/Projects/Surycate/SurycateBot/verbose_prompting/Website$
Thought:
I have successfully changed the directory to the Website directory. I can now create the README.md file.
New Context:
I am working on a project to create a website. I am in website's folder called "Website" and I want to create a README.md file with the description of the website.
----------------
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
----------------

Your current context is following:
I am working on my personal website. I am now in the "Website" folder. I want to create a markdown file with the description of the website. To do that, I need to create a markdown file in the "Website" folder called README.md.
Action:
cmd cd Website
Observation:
lukasz@Smith:/mnt/c/Users/luki3/Projects/LS314/Projects/Surycate/SurycateBot/examples/context_prompting$ cd Website
lukasz@Smith:/mnt/c/Users/luki3/Projects/LS314/Projects/Surycate/SurycateBot/examples/context_prompting/Website$
Thought:
I have successfully changed the directory to the "Website" folder. Now I can proceed with creating the markdown file for the website description.
New Context:
I am working on my personal website. I am now in the "Website" folder. I want to create a markdown file with the description of the website. To do that, I need to create a markdown file in the "Website" folder called README.md.
```

### Toughts

- I have finished the example with telling the time - it works.
- Should there be an after through after the context and before the action? To decide what to do?
- Context lenght might be too long
- Separation sign is a problem when generating contexts: CHATGPT might generate a split.