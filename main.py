#!/usr/bin/env python3

import iterm2
import sys
import argparse
import os
import time
from version import __version__

def initialize_commands_file():
    file_path = os.path.join(os.getcwd(), "its.txt")
    if os.path.exists(file_path):
        response = input(f"{file_path} already exists. Do you want to overwrite it? (y/N): ")
        if response.lower() != 'y':
            print("Initialization cancelled.")
            return False
    
    commands = []
    print("Enter commands (one per line). Press Ctrl+D when done:")
    while True:
        try:
            command = input("> ").strip()
            if command:
                commands.append(command)
        except EOFError:
            break
    
    if not commands:
        print("No commands entered. Initialization cancelled.")
        return False
    
    with open(file_path, 'w') as f:
        for cmd in commands:
            f.write(f"{cmd}\n")
    print(f"\nCreated {file_path} with {len(commands)} commands.")
    return True

def read_commands_from_file(file_path=None):
    if file_path is None:
        file_path = os.path.join(os.getcwd(), "its.txt")
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found")
        sys.exit(1)
    with open(file_path, 'r') as f:
        commands = [line.strip() for line in f if line.strip()]
    return commands

def parse_args():
    parser = argparse.ArgumentParser(description='iTerm Splitter - Run multiple commands in split panes')
    parser.add_argument('commands', nargs='*', help='Commands to run in split panes')
    parser.add_argument('--max-v-pane', type=int, default=4, 
                      help='Maximum number of vertical panes before creating a new column (default: 4)')
    parser.add_argument('--init', action='store_true',
                      help='Initialize its.txt in the current directory')
    parser.add_argument('--file', type=str,
                      help='Path to commands file (default: its.txt in current directory)')
    parser.add_argument('-v', '--version', action='version',
                      version=f'iterm-splitter {__version__}',
                      help='Show version number and exit')
    return parser.parse_args()

def print_help():
    help_text = """
iTerm Splitter - Run multiple commands in split panes

Usage:
    iterm-splitter [--max-v-pane N] <command1> <command2> ...
    iterm-splitter [--file path/to/commands.txt]
    iterm-splitter --init

Examples:
    iterm-splitter "ls -la" "htop" "df -h"
    iterm-splitter --max-v-pane 3 "top" "htop" "vim" "ps aux" "tail -f /var/log/system.log"
    iterm-splitter --file my-commands.txt
    iterm-splitter --init    # Create its.txt interactively

Each command will run in its own pane, split vertically.
Commands can be provided as arguments or read from a file.
If no commands are provided as arguments, defaults to reading from its.txt 
or the file specified with --file.
"""
    print(help_text)
    sys.exit(0)

async def main(connection):
    args = parse_args()
    
    if args.init:
        initialize_commands_file()
        return
    
    commands = args.commands
    
    if not commands:
        # If no commands provided as arguments, try reading from file
        commands = read_commands_from_file(args.file)
        if not commands:
            print(f"No commands found in {args.file if args.file else 'its.txt'}")
            print_help()
            return
    
    # Get the iTerm2 app instance
    app = await iterm2.async_get_app(connection)
    window = app.current_terminal_window
    if window is None:
        window = await iterm2.Window.async_create(connection)
    
    # Create a new tab to start fresh
    tab = await window.async_create_tab()
    
    # Get the initial session
    first_panes = [tab.current_session]
    
    # Run first command in the initial session
    await first_panes[0].async_send_text(commands[0] + '\n')
    
    # First create horizontal splits up to max_v_pane
    for i in range(1, min(args.max_v_pane, len(commands))):
        # Create horizontal split for each primary pane
        new_session = await first_panes[0].async_split_pane(vertical=False)
        first_panes.append(new_session)
        await new_session.async_send_text(commands[i] + '\n')
    
    # Now handle remaining commands by creating vertical splits
    for i, cmd in enumerate(commands[args.max_v_pane:], start=args.max_v_pane):
        # Calculate which primary pane to split (cycling through them)
        primary_pane_index = i % args.max_v_pane
        # Create vertical split from the corresponding primary pane
        new_session = await first_panes[primary_pane_index].async_split_pane(vertical=True)
        await new_session.async_send_text(cmd + '\n')

if __name__ == '__main__':
    args = parse_args()
    if args.init:
        initialize_commands_file()
    else:
        print("Connecting to iTerm2...", file=sys.stderr, flush=True)
        start_time = time.time()
        iterm2.run_until_complete(main)
        end_time = time.time()
        if end_time - start_time > 1:  # Only show timing if it took more than 1 second
            print(f"Done in {end_time - start_time:.1f}s", file=sys.stderr)
