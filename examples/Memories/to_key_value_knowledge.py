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



def format_memory(memory, template):
    """Format memory to key-value pairs."""
    memory_md = template.format(
        information = memory['information']
    )
    return memory_md

def main():

    value_template = """{information}"""

    context_template = """{information}"""



    # Create a memory folder and clear it
    try:
        shutil.rmtree('key_value_memories')
    except:
        pass
    os.makedirs('key_value_memories')
    os.makedirs('key_value_memories/keys_context')
    os.makedirs('key_value_memories/values')


    # Iterate through all memories and create key files
    for i, filename in enumerate(get_filenames('knowledge')):
        print(f'Processing {filename} ... ', end='')
        memory = read_memory(filename)
        key_context = format_memory(memory, template=context_template)
        value = format_memory(memory, template=value_template)
        index = str(i).zfill(4)
        with open(f'key_value_memories/keys_context/mem_{index}.md', 'w+') as f:
            f.write(key_context)
        with open(f'key_value_memories/values/mem_{index}.md', 'w+') as f:
            f.write(value)
        print(f'Done')


if __name__=='__main__':
    main()