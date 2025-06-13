#!/usr/bin/env python3
"""Script to handle the release process."""
import argparse
import subprocess
import sys
from pathlib import Path

def run_command(command, check=True):
    """Run a shell command and return its output."""
    try:
        result = subprocess.run(
            command,
            check=check,
            shell=True,
            text=True,
            capture_output=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(f"Error output: {e.stderr}")
        sys.exit(1)

def validate_version(version):
    """Validate that the version string is in the correct format."""
    import re
    if not re.match(r'^\d+\.\d+\.\d+$', version):
        print(f"Error: Version {version} is not in the format X.Y.Z")
        sys.exit(1)

def ensure_clean_repo():
    """Ensure the git repository is clean."""
    if run_command("git status --porcelain"):
        print("Error: Git repository has uncommitted changes.")
        print("Please commit or stash your changes first.")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Release a new version.")
    parser.add_argument("version", help="New version number (e.g., 1.1.0)")
    args = parser.parse_args()

    version = args.version
    validate_version(version)

    print(f"Starting release process for version {version}")
    
    # Ensure git repository is clean
    ensure_clean_repo()

    # Update version numbers
    print("\nUpdating version numbers...")
    run_command(f"python3 update_version.py {version}")

    # Commit the version changes
    print("\nCommitting version changes...")
    run_command('git add version.py Formula/iterm-splitter.rb')
    run_command(f'git commit -m "chore: bump version to {version}"')

    # Create and push the tag
    print(f"\nCreating and pushing tag v{version}...")
    run_command(f'git tag -a "v{version}" -m "Release version {version}"')
    run_command('git push origin main --tags')

    print(f"\nRelease {version} process completed!")
    print("The GitHub Action will now:")
    print("1. Build the binary")
    print("2. Calculate and update the SHA256 in the formula")
    print("3. Create the release with the binary")
    print("\nMonitor the progress at: https://github.com/dejavu1987/iterm-splitter/actions")

if __name__ == "__main__":
    main()
