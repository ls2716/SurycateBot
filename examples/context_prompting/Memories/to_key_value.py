"""
Parse and read yaml memories.
"""

import yaml
# Import pretty printer for dictionary
from pprint import pprint
import os
import shutil


def read_memory(path):
    """Read single yaml file."""
    with open(path, 'r') as stream:
        try:
            return yaml.load(stream, Loader=yaml.FullLoader)
        except yaml.YAMLError as exc:
            print(exc)


def get_filenames(path):
    """Get all filenames in a directory and recursively in all subdirectories."""
    filenames = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.yaml'):
                filenames.append(os.path.join(root, file))
    return filenames

value_template = """Context:
{context}
Action Thought:
{action_thought}
Action:
{action}
Observation:
{observation}
Observation Thought:
{observation_thought}
New Context:
{new_context}
"""

context_template = """{context}
"""
observation_template = """Context:
{context}
Action Thought:
{action_thought}
Action:
{action}
Observation:
{observation}
"""

def format_memory(memory, template):
    """Format memory to key-value pairs."""
    memory_md = template.format(
        context=memory['context'],
        action_thought=memory['action_thought'],
        action=memory['action'],
        observation=memory['observation'],
        observation_thought=memory['thought'],
        new_context=memory['new_context']
    )
    return memory_md


# memory = read_memory(
#     'memories/update_linux/task_update.yaml')  # Read one memory
# pprint(memory)
# print(memory)


# print(format_memory(memory, template=value_template))  # Format memory to key-value pairs

# # Get all filenames in a directory and recursively in all subdirectories
# print(get_filenames('memories'))

# Create a memory folder and clear it
try:
    shutil.rmtree('key_value_memories')
except:
    pass
os.makedirs('key_value_memories')
os.makedirs('key_value_memories/keys_context')
os.makedirs('key_value_memories/keys_observation')
os.makedirs('key_value_memories/values')


# Iterate through all memories and create key files
for i, filename in enumerate(get_filenames('memories')):
    print(f'Processing {filename}')
    memory = read_memory(filename)
    key_context = format_memory(memory, template=context_template)
    key_observation = format_memory(memory, template=observation_template)
    value = format_memory(memory, template=value_template)
    index = str(i).zfill(4)
    with open(f'key_value_memories/keys_context/mem_{index}.md', 'w+') as f:
        f.write(key_context)
    with open(f'key_value_memories/keys_observation/mem_{index}.md', 'w+') as f:
        f.write(key_observation)
    with open(f'key_value_memories/values/mem_{index}.md', 'w+') as f:
        f.write(value)
    print(f'Processed {filename}')


