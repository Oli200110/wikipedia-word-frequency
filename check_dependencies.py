"""
Script to check if all required dependencies are installed.
"""

import importlib
import sys


def check_dependency(module_name):
    """Check if a module is installed."""
    try:
        importlib.import_module(module_name)
        print(f"✓ {module_name} is installed")
        return True
    except ImportError:
        print(f"✗ {module_name} is NOT installed")
        return False


def main():
    """Check all required dependencies."""
    print("Checking required dependencies...\n")

    dependencies = [
        "fastapi",
        "uvicorn",
        "requests",
        "bs4",  # BeautifulSoup
        "numpy",
        "pytest",
        "httpx",
        "numpy",
    ]

    all_installed = True

    for dep in dependencies:
        if not check_dependency(dep):
            all_installed = False

    print("\nSummary:")
    if all_installed:
        print("All required dependencies are installed.")
    else:
        print("Some dependencies are missing. Please install them using:")
        print("pip install -e .")

    return 0 if all_installed else 1


if __name__ == "__main__":
    sys.exit(main())
