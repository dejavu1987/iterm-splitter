#!/usr/bin/env python3
"""Script to update version numbers across the project."""
import re
import sys
from pathlib import Path

def update_version(new_version):
    # Update version.py
    version_file = Path('version.py')
    content = version_file.read_text()
    content = re.sub(r'__version__ = "[^"]+"', f'__version__ = "{new_version}"', content)
    version_file.write_text(content)
    
    # Update Formula/iterm-splitter.rb
    formula_file = Path('Formula/iterm-splitter.rb')
    content = formula_file.read_text()
    content = re.sub(r'version "[^"]+"', f'version "{new_version}"', content)
    formula_file.write_text(content)
    
    print(f"Updated version to {new_version} in:")
    print("- version.py")
    print("- Formula/iterm-splitter.rb")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: update_version.py NEW_VERSION")
        print("Example: update_version.py 1.1.0")
        sys.exit(1)
    
    update_version(sys.argv[1])
