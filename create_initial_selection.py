#!/usr/bin/env python3
"""
Create initial digimon_selection.json file
This script will create a default selection file with random Digimon
to prevent crashes when the game starts on a fresh system.
"""

import json
import os
import random

def create_initial_selection():
    """Create initial selection file with random Digimon"""
    
    # Find available Digimon
    assets_dir = os.path.join(os.path.dirname(__file__), "assets")
    sprites_dir = os.path.join(assets_dir, "sprites")
    
    available_digimon = []
    
    if os.path.exists(sprites_dir):
        for folder in os.listdir(sprites_dir):
            folder_path = os.path.join(sprites_dir, folder)
            if folder.endswith("_dmc") and os.path.isdir(folder_path):
                # Check if it has walking animation frames
                frame_0 = os.path.join(folder_path, "0.png")
                frame_1 = os.path.join(folder_path, "1.png")
                if os.path.exists(frame_0) and os.path.exists(frame_1):
                    available_digimon.append(folder)
    
    print(f"Found {len(available_digimon)} available Digimon: {available_digimon[:5]}...")
    
    if len(available_digimon) >= 2:
        # Select 2 random Digimon
        selected = random.sample(available_digimon, 2)
        print(f"Selected random Digimon: {[name.replace('_dmc', '') for name in selected]}")
    else:
        # Fallback defaults (will be handled by the game if they don't exist)
        selected = ["Agumon_dmc", "Gabumon_dmc"]
        print(f"Using fallback defaults: {[name.replace('_dmc', '') for name in selected]}")
    
    # Create selection data
    selection_data = {
        "selected_digimon": selected,
        "timestamp": 0
    }
    
    # Save to file
    selection_file = "digimon_selection.json"
    
    try:
        with open(selection_file, 'w') as f:
            json.dump(selection_data, f, indent=2)
        
        print(f"✅ Created {selection_file} successfully!")
        print(f"   Selected: {[name.replace('_dmc', '') for name in selected]}")
        return True
        
    except Exception as e:
        print(f"❌ Error creating selection file: {e}")
        return False

def main():
    """Main function to run the script"""
    print("=== Creating Initial Digimon Selection File ===")
    print()
    
    # Check if file already exists
    if os.path.exists("digimon_selection.json"):
        response = input("digimon_selection.json already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Cancelled.")
            return
    
    success = create_initial_selection()
    
    if success:
        print("\n🎮 The game should now start without issues!")
        print("   Run: python run.py")
    else:
        print("\n❌ Failed to create selection file.")
        print("   The game may still work with fallback Digimon.")

if __name__ == "__main__":
    main()
