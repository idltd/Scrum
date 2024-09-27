import os
import sys
import importlib.util
import inspect

# Get the directory of the current script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Define the path to the commands directory relative to the script
COMMANDS_DIR = os.path.join(SCRIPT_DIR, 'commands')

def load_commands():
    commands = {}
    modules = []
    for filename in os.listdir(COMMANDS_DIR):
        if filename.endswith('_commands.py'):
            module_name = filename[:-3]  # Remove '.py'
            module_path = os.path.join(COMMANDS_DIR, filename)
            # Use importlib.util for more robust importing
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
  
            entity = module_name.split('_')[0]
            for attr_name in dir(module):
                if attr_name.startswith(f'{entity}_'):
                    command_name = attr_name[len(entity)+1:]
                    commands[f'{entity} {command_name}'] = getattr(module, attr_name)
            modules.append((module, entity))
    return commands, modules

def find_command(commands, input_command):
    input_parts = input_command.split()
    matches = []

    for cmd in commands:
        cmd_parts = cmd.split()
        if len(input_parts) >= len(cmd_parts):
            if all(ip.startswith(cp) for ip, cp in zip(input_parts[:len(cmd_parts)], cmd_parts)):
                matches.append(cmd)

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

def main(args=None):
    commands, modules = load_commands()
    if args is None:
        args = sys.argv[1:]

    if args:
        # Command-line mode
        if args[0] in ['-h', '--help']:
            print_help(commands, modules)
            return

        input_command = ' '.join(args)
        full_command = find_command(commands, input_command)
        if full_command:
            if full_command != input_command:
                print(f"Executing: {full_command}")
            command_parts = full_command.split()
            command_args = args[len(full_command.split()):]
            if command_args and command_args[0] in ['-h', '--help']:
                print_command_help(full_command, commands[full_command])
            else:
                commands[full_command](*command_args)
        return  # Exit after executing the command

    # Interactive mode (only entered if no arguments were provided)
    print("Entering interactive mode. Type 'exit' to quit or 'help' for a list of commands.")
    while True:
        user_input = input("scrum> ").strip()
        if user_input.lower() == 'exit':
            print("Exiting Scrum CLI.")
            break
        if not user_input:
            continue
        if user_input.lower() == 'help':
            print_help(commands, modules)
            continue
        
        full_command = find_command(commands, user_input)
        if full_command:
            if full_command != user_input:
                print(f"Executing: {full_command}")
            command_parts = full_command.split()
            command_args = user_input.split()[len(command_parts):]
            if command_args and command_args[0] in ['-h', '--help']:
                print_command_help(full_command, commands[full_command])
            else:
                commands[full_command](*command_args)

if __name__ == "__main__":
    main()