from langchain.prompts.prompt import PromptTemplate


concise_template = """Complete the next line in sequence using the following pattern:

CONTEXT:
<context>
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
----------------
{similar_tasks}
----------------

CONTEXT:
{task_context}
{history}"""

template = PromptTemplate(
    input_variables=["similar_tasks", "task_context", "history"],
    template=concise_template
)