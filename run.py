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
    print("Starting Virtual Pet Game...")
    
    # Get the path to main.py
    script_dir = os.path.dirname(os.path.abspath(__file__))
    main_py_path = os.path.join(script_dir, 'src', 'main.py')
    
    # Check if main.py exists
    if not os.path.exists(main_py_path):
        print(f"Error: Could not find {main_py_path}")
        print("Make sure you're running this script from the vpet project root directory.")
        input("Press Enter to exit...")
        sys.exit(1)
    
    # Check if assets directory exists
    assets_dir = os.path.join(script_dir, 'assets')
    if not os.path.exists(assets_dir):
        print(f"Warning: Assets directory not found at {assets_dir}")
        print("The game may not work properly without assets.")
    
    # Run main.py directly
    try:
        print("Launching game...")
        # Change to script directory to ensure relative paths work
        os.chdir(script_dir)
        subprocess.run([sys.executable, main_py_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running game: {e}")
        input("Press Enter to exit...")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nGame interrupted by user")
        sys.exit(0)
    except FileNotFoundError:
        print("Error: Python executable not found. Make sure Python is installed and in your PATH.")
        input("Press Enter to exit...")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()
