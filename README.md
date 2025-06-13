# iTerm Splitter (ITS)

A utility for automatically splitting iTerm2 windows and running multiple commands in separate panes. While it's built with Python, it's distributed as a standalone binary so you don't need Python installed to use it.

## Features

- Create multiple split panes in iTerm2 automatically
- Run different commands in each pane
- Configure maximum number of vertical panes before creating new columns
- Interactive mode to initialize command lists
- Support for command input via file or command line arguments

## Requirements

- iTerm2
- macOS

## Installation

### Option 1: Download the binary (Recommended)

1. Download `iterm-splitter` from the [releases page](../../releases/latest)
2. Make it executable:

```bash
chmod +x iterm-splitter
```

3. Move it to a directory in your PATH (optional):

```bash
sudo mv iterm-splitter /usr/local/bin/
```

4. Set up the alias (optional but recommended):

```bash
echo 'alias its="iterm-splitter"' >> ~/.zshrc
source ~/.zshrc
```

### Option 2: Build from source

If you want to build from source, you'll need:

- Python 3.x
- `venv` (usually comes with Python 3)
- `iterm2` Python package

1. Clone this repository
2. Create and activate a virtual environment:

```bash
# Create new virtual environment
python3 -m venv venv
# On macOS/Linux
source venv/bin/activate
# On Windows
# .\venv\Scripts\activate
```

If you get "python: command not found" after activation, try:

- Delete the existing venv directory: `rm -rf venv`
- Make sure you're using the correct Python path:

```bash
which python3
# Use the path from above command
/usr/local/bin/python3 -m venv venv
source venv/bin/activate
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Build the binary:

```bash
pyinstaller iterm-splitter.spec
```

The binary will be created in the `dist` directory.

Note: After you're done building, you can deactivate the virtual environment:

```bash
deactivate
```

## Usage

### Basic Usage

Run multiple commands in split panes:

```bash
its "ls -la" "htop" "df -h"
# or use the full command
iterm-splitter "ls -la" "htop" "df -h"
```

### Set Maximum Vertical Panes

Limit the number of vertical panes before creating a new column:

```bash
its --max-v-pane 3 "top" "htop" "vim" "ps aux" "tail -f /var/log/system.log"
```

### Initialize Command File

Create or update a command file interactively:

```bash
its --init
```

This will create `its.txt` in the current directory with your specified commands.

## Command File Format

The command file (`its.txt`) should contain one command per line. Empty lines are ignored.

Example:

```
ls -la
htop
df -h
top
```

## Building from Source

The project includes PyInstaller spec file for creating standalone executables:

```bash
pyinstaller iterm-splitter.spec
```

### Local Testing with Symlink

After building, you can create a symlink to test the binary without moving it:

```bash
# Create symlink in a directory that's in your PATH
ln -s "$(pwd)/dist/iterm-splitter" /usr/local/bin/iterm-splitter-dev
# Now you can test using
iterm-splitter-dev --help
```

This creates a development version alongside any stable version you may have installed.

### Troubleshooting Build Issues

1. If you renamed the project directory or main Python file:

   - Update the paths in `iterm-splitter.spec` to match your new file names
   - If using a virtual environment, create a new one in the new location

2. Virtual Environment issues:
   - If you get "python/pip not found" errors:
     ```bash
     # First, deactivate if you're in a broken venv
     deactivate
     # Remove the broken venv
     rm -rf venv
     # Create new venv with explicit Python path
     /usr/local/bin/python3 -m venv venv
     source venv/bin/activate
     ```
   - Always create the virtual environment in the project directory
   - Don't move/rename the `venv` directory after creation

## Version Management

The project version is maintained in multiple places:

- `version.py`: The single source of truth for version number
- `Formula/iterm-splitter.rb`: The Homebrew formula
- Binary releases

To update the version across all files:

```bash
./update_version.py NEW_VERSION
```

For example:

```bash
./update_version.py 1.1.0
```

This will automatically update the version number in all necessary files.

## Project Structure

- `main.py` - Main application code
- `its.txt` - Command list file
- `requirements.txt` - Python dependencies
- `iterm-splitter.spec` - PyInstaller specification file
- `version.py` - Version information
- `update_version.py` - Script to update version numbers across the project
- `Formula/iterm-splitter.rb` - Homebrew formula file

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
