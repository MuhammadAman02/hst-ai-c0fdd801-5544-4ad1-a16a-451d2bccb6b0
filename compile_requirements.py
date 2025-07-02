#!/usr/bin/env python
"""
Requirements Compiler Script

This script installs pip-tools and uses pip-compile to generate a pinned requirements.txt
file from requirements.in, resolving all dependencies and their compatible versions.

Usage:
    python compile_requirements.py
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def get_python_executable():
    """Get the appropriate Python executable path based on the platform and environment."""
    # If running in a virtual environment, use that Python
    if sys.prefix != sys.base_prefix:
        if platform.system() == "Windows":
            return sys.executable
        return sys.executable
    
    # Otherwise, use the system Python that's running this script
    return sys.executable

def get_pip_executable():
    """Get the appropriate pip executable path based on the platform and environment."""
    python_path = get_python_executable()
    if platform.system() == "Windows":
        pip_path = os.path.join(os.path.dirname(python_path), "pip.exe")
    else:
        pip_path = os.path.join(os.path.dirname(python_path), "pip")
    
    # If pip isn't in the same directory as python, fall back to using python -m pip
    if not os.path.exists(pip_path):
        return [python_path, "-m", "pip"]
    
    return [pip_path]

def install_pip_tools():
    """Install pip-tools if not already installed."""
    try:
        # Check if pip-tools is installed
        subprocess.run(
            [*get_python_executable(), "-c", "import piptools"], 
            check=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        print("✓ pip-tools is already installed")
        return True
    except subprocess.CalledProcessError:
        print("Installing pip-tools...")
        try:
            subprocess.run(
                [*get_pip_executable(), "install", "pip-tools"], 
                check=True
            )
            print("✓ pip-tools installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to install pip-tools: {e}")
            return False

def compile_requirements_file(input_file, output_file):
    """Compile a requirements.in file to a requirements.txt file using pip-compile."""
    input_path = Path(input_file)
    if not input_path.exists():
        print(f"✗ {input_path} not found")
        return False
    
    print(f"Compiling {input_file} to {output_file}...")
    try:
        # Use pip-compile to generate requirements.txt
        subprocess.run(
            [
                *get_python_executable(), 
                "-m", 
                "piptools", 
                "compile", 
                f"--output-file={output_file}", 
                "--resolver=backtracking",  # Use backtracking resolver for better conflict resolution
                "--allow-unsafe",  # Allow unsafe packages if needed
                "--generate-hashes",  # Add hashes for better security
                input_file
            ],
            check=True
        )
        print(f"✓ {output_file} generated successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to compile {input_file}: {e}")
        return False

def compile_requirements():
    """Compile requirements.in and dev-requirements.in to their respective .txt files."""
    success = True
    
    # Compile main requirements
    if not compile_requirements_file("requirements.in", "requirements.txt"):
        success = False
    
    # Compile development requirements if they exist
    if Path("dev-requirements.in").exists():
        if not compile_requirements_file("dev-requirements.in", "dev-requirements.txt"):
            success = False
    
    return success

def main():
    """Main function to run the script."""
    print("=== Requirements Compiler ===")
    
    if not install_pip_tools():
        return False
    
    if not compile_requirements():
        return False
    
    print("\nAll done! requirements.txt has been updated with pinned dependencies.")
    print("To install the dependencies, run:")
    if platform.system() == "Windows":
        print("  pip install -r requirements.txt")
    else:
        print("  pip install -r requirements.txt")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)