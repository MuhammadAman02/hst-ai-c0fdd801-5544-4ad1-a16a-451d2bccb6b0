import os
import sys
import subprocess
import platform
import importlib.util
from pathlib import Path

# Minimum Python version required
MIN_PYTHON_VERSION = (3, 8)

# Critical dependencies to verify
CRITICAL_DEPENDENCIES = [
    "uvicorn",
    "fastapi",
    "nicegui",
    "pydantic"
]

# Known dependency compatibility requirements
DEPENDENCY_COMPATIBILITY = {
    "nicegui": {
        "version_range": "1.4.21-1.4.24",
        "requires": {
            "fastapi": ">=0.109.1,<0.110.0"
        }
    }
}

def check_python_version():
    """Check if the current Python version meets the minimum requirement."""
    current_version = sys.version_info[:2]
    if current_version < MIN_PYTHON_VERSION:
        print(f"Error: Python {MIN_PYTHON_VERSION[0]}.{MIN_PYTHON_VERSION[1]} or higher is required.")
        print(f"Current version: {current_version[0]}.{current_version[1]}")
        return False
    return True

def create_venv():
    """Create a virtual environment if it doesn't exist."""
    venv_path = Path("venv")
    if venv_path.exists():
        print("Virtual environment already exists.")
        return True
    
    print("Creating virtual environment...")
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("Virtual environment created successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error creating virtual environment: {e}")
        return False

def install_pip_tools():
    """Install pip-tools in the virtual environment."""
    print("Installing pip-tools...")
    
    # Determine the path to the pip executable in the virtual environment
    if platform.system() == "Windows":
        pip_path = Path("venv") / "Scripts" / "pip"
    else:
        pip_path = Path("venv") / "bin" / "pip"
    
    try:
        subprocess.run([str(pip_path), "install", "pip-tools"], check=True)
        print("pip-tools installed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing pip-tools: {e}")
        return False

def compile_requirements_file(input_file, output_file):
    """Compile a requirements.in file to a requirements.txt file using pip-compile."""
    print(f"Compiling {input_file} to {output_file}...")
    
    # Check if input file exists
    if not Path(input_file).exists():
        print(f"Error: {input_file} not found.")
        return False
    
    # Determine the path to the Python executable in the virtual environment
    if platform.system() == "Windows":
        python_path = Path("venv") / "Scripts" / "python"
    else:
        python_path = Path("venv") / "bin" / "python"
    
    try:
        # Use pip-compile to generate requirements.txt with pinned versions
        subprocess.run(
            [
                str(python_path), 
                "-m", 
                "piptools", 
                "compile", 
                f"--output-file={output_file}", 
                "--resolver=backtracking",  # Better conflict resolution
                "--allow-unsafe",  # Allow unsafe packages if needed
                input_file
            ],
            check=True
        )
        print(f"{output_file} generated successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error compiling {input_file}: {e}")
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

def install_dependencies():
    """Install dependencies from requirements.txt."""
    print("Installing dependencies...")
    
    # Determine the path to the pip executable in the virtual environment
    if platform.system() == "Windows":
        pip_path = Path("venv") / "Scripts" / "pip"
    else:
        pip_path = Path("venv") / "bin" / "pip"
    
    try:
        subprocess.run([str(pip_path), "install", "-r", "requirements.txt"], check=True)
        print("Dependencies installed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False

def verify_critical_dependencies():
    """Verify that critical dependencies are installed."""
    print("Verifying critical dependencies...")
    
    # Determine the path to the Python executable in the virtual environment
    if platform.system() == "Windows":
        python_path = Path("venv") / "Scripts" / "python"
    else:
        python_path = Path("venv") / "bin" / "python"
    
    missing_deps = []
    installed_versions = {}
    
    for dep in CRITICAL_DEPENDENCIES:
        try:
            # Use the virtual environment's Python to check for the dependency and its version
            result = subprocess.run(
                [str(python_path), "-c", f"import {dep}; print('{dep}:' + getattr({dep}, '__version__', 'unknown'))"],
                capture_output=True,
                text=True,
                check=True
            )
            version_output = result.stdout.strip()
            if ':' in version_output:
                dep_name, version = version_output.split(':', 1)
                installed_versions[dep_name] = version
                print(f"✓ {dep} is installed (version {version})")
            else:
                print(f"✓ {dep} is installed (version unknown)")
        except subprocess.CalledProcessError:
            missing_deps.append(dep)
            print(f"✗ {dep} is missing")
    
    if missing_deps:
        print("\nWarning: Some critical dependencies are missing:")
        for dep in missing_deps:
            print(f"  - {dep}")
        print("\nPlease install them manually or try running the setup again.")
        return False
    
    # Check for dependency compatibility issues
    compatibility_issues = check_dependency_compatibility(installed_versions)
    if compatibility_issues:
        print("\nWarning: Dependency compatibility issues detected:")
        for issue in compatibility_issues:
            print(f"  - {issue}")
        print("\nThe application may not function correctly due to these compatibility issues.")
        print("Please refer to the README.md for more information on dependency compatibility.")
        return False
    
    print("All critical dependencies are installed and compatible.")
    return True

def check_dependency_compatibility(installed_versions):
    """Check for known dependency compatibility issues."""
    issues = []
    
    # Check NiceGUI and FastAPI compatibility
    if 'nicegui' in installed_versions and 'fastapi' in installed_versions:
        nicegui_version = installed_versions['nicegui']
        fastapi_version = installed_versions['fastapi']
        
        # NiceGUI 1.4.21-1.4.24 requires FastAPI <0.110.0, >=0.109.1
        if nicegui_version.startswith('1.4.2'):
            from packaging import version
            if version.parse(fastapi_version) >= version.parse('0.110.0'):
                issues.append(f"NiceGUI {nicegui_version} requires FastAPI <0.110.0, but {fastapi_version} is installed")
    
    return issues

def print_activation_instructions():
    """Print instructions for activating the virtual environment."""
    print("\nTo activate the virtual environment:")
    
    if platform.system() == "Windows":
        print("  venv\\Scripts\\activate")
    else:
        print("  source venv/bin/activate")
    
    print("\nAfter activation, you can run the application with:")
    print("  python main.py")

def main():
    """Main setup function."""
    print("=== Project Setup ===")
    
    if not check_python_version():
        return False
    
    if not create_venv():
        return False
    
    # Install pip-tools for dependency management
    if not install_pip_tools():
        print("Warning: Failed to install pip-tools. Will use existing requirements.txt.")
    else:
        # Compile requirements.in to requirements.txt if requirements.in exists
        if Path("requirements.in").exists():
            if not compile_requirements():
                print("Warning: Failed to compile requirements. Will use existing requirements.txt.")
    
    if not install_dependencies():
        return False
    
    if not verify_critical_dependencies():
        print("Setup completed with warnings.")
    else:
        print("\nSetup completed successfully!")
    
    print_activation_instructions()
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)