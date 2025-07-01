#!/usr/bin/env python3
"""
Virtual Pet Game - Launcher
A simple launcher for the virtual pet simulator
"""

import subprocess
import sys
import os

def main():
    """Launch the virtual pet game"""
    # Get the path to main.py
    main_py_path = os.path.join(os.path.dirname(__file__), 'src', 'main.py')
    
    # Check if main.py exists
    if not os.path.exists(main_py_path):
        print(f"Error: Could not find {main_py_path}")
        sys.exit(1)
    
    # Run main.py directly
    try:
        subprocess.run([sys.executable, main_py_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running game: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nGame interrupted by user")
        sys.exit(0)

if __name__ == "__main__":
    main()
