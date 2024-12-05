"""
Parse and read yaml memories from memories folder.
"""

import yaml
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

def formmat_information(information):
    """Format information to key-value pairs."""
    information_md = '- ' + '\n- '.join(information)
    return information_md


def format_memory(memory, template):
    """Format memory to key-value pairs."""
    memory_md = template.format(
        context=memory['context'],
        information=formmat_information(memory.get('information', [])),
        action_thought=memory['action_thought'],
        action=memory['action'],
        observation=memory['observation'],
        observation_thought=memory['thought'],
        new_context=memory['new_context']
    )
    return memory_md

def main():

    value_template = """CONTEXT:
{context}
INFORMATION:
{information}
ACTION THOUGHT:
{action_thought}
ACTION:
{action}
OBSERVATION:
{observation}
OBSERVATION THOUGHT:
{observation_thought}
NEW CONTEXT:
{new_context}
"""

    context_template = """{context}
INFORMATION:
{information}
"""

    observation_template = """CONTEXT:
{context}
INFORMATION:
{information}
ACTION THOUGHT:
{action_thought}
ACTION:
{action}
OBSERVATION:
{observation}
"""



    # Create a memory folder and clear it
    try:
        shutil.rmtree('key_value_experiences')
    except:
        pass
    os.makedirs('key_value_experiences')
    os.makedirs('key_value_experiences/keys_context')
    os.makedirs('key_value_experiences/keys_observation')
    os.makedirs('key_value_experiences/values')


    # Iterate through all memories and create key files
    for i, filename in enumerate(get_filenames('experiences')):
        print(f'Processing {filename} ... ', end='')
        memory = read_memory(filename)
        key_context = format_memory(memory, template=context_template)
        key_observation = format_memory(memory, template=observation_template)
        value = format_memory(memory, template=value_template)
        index = str(i).zfill(4)
        with open(f'key_value_experiences/keys_context/mem_{index}.md', 'w+') as f:
            f.write(key_context)
        with open(f'key_value_experiences/keys_observation/mem_{index}.md', 'w+') as f:
            f.write(key_observation)
        with open(f'key_value_experiences/values/mem_{index}.md', 'w+') as f:
            f.write(value)
        print(f'Done')


if __name__=='__main__':
    main()