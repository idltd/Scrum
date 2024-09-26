import os
import sys
import importlib
import inspect

COMMANDS_DIR = 'commands'

def load_commands():
    commands = {}
    modules = []
    for filename in os.listdir(COMMANDS_DIR):
        if filename.endswith('_commands.py'):
            module_name = filename[:-3]  # Remove '.py'
            module = importlib.import_module(f'{COMMANDS_DIR}.{module_name}')
            entity = module_name.split('_')[0]
            for attr_name in dir(module):
                if attr_name.startswith(f'{entity}_'):
                    command_name = attr_name[len(entity)+1:]
                    commands[f'{entity} {command_name}'] = getattr(module, attr_name)
            modules.append((module, entity))
    return commands, modules

def find_command(commands, input_command):
    matches = [cmd for cmd in commands if cmd.startswith(input_command)]
    if len(matches) == 1:
        return matches[0]
    elif len(matches) > 1:
        print(f"Ambiguous command '{input_command}'. Did you mean one of these?")
        for match in matches:
            print(f"  {match}")
        return None
    else:
        print(f"Unknown command: {input_command}")
        return None

def print_help(commands, modules):
    print("Usage: scrum <command> [args]")
    print("\nAvailable commands:")
    
    sorted_modules = sorted(modules, key=lambda m: getattr(m[0], '__module_importance__', 999))
    
    for module, entity in sorted_modules:
        print(f"\n{entity.capitalize()} - {getattr(module, '__module_description__', 'No description')}")
        entity_commands = [cmd for cmd in commands if cmd.startswith(f"{entity} ")]
        for cmd in sorted(entity_commands):
            func = commands[cmd]
            doc = func.__doc__.strip().split('\n')[0] if func.__doc__ else 'No description'
            print(f"  {cmd:<20} {doc}")

def print_command_help(command, func):
    print(f"Help for '{command}':")
    if func.__doc__:
        print(inspect.cleandoc(func.__doc__))
    else:
        print("No help available for this command.")

def main():
    commands, modules = load_commands()
    if len(sys.argv) < 2 or sys.argv[1] in ['-h', '--help']:
        print_help(commands, modules)
        return

    input_command = ' '.join(sys.argv[1:3])
    full_command = find_command(commands, input_command)
    if full_command:
        if len(sys.argv) > 3 and sys.argv[3] in ['-h', '--help']:
            print_command_help(full_command, commands[full_command])
        else:
            commands[full_command](*sys.argv[3:])

if __name__ == "__main__":
    main()