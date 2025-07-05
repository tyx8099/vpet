#!/usr/bin/env python3
"""
Test script to verify Raspberry Pi compatibility
This script tests the key components that might fail on Raspberry Pi
"""

import os
import sys
import json

def test_selection_file_handling():
    """Test selection file loading and saving"""
    print("=== Testing Selection File Handling ===")
    
    # Test 1: Missing file
    test_file = "test_selection.json"
    if os.path.exists(test_file):
        os.remove(test_file)
    
    print("1. Testing missing file handling...")
    try:
        if os.path.exists(test_file):
            with open(test_file, 'r') as f:
                data = json.load(f)
            print("   ✅ File exists and loads correctly")
        else:
            print("   ✅ Missing file handled gracefully")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Create file
    print("2. Testing file creation...")
    try:
        test_data = {
            "selected_digimon": ["Agumon_dmc", "Gabumon_dmc"],
            "timestamp": 0
        }
        with open(test_file, 'w') as f:
            json.dump(test_data, f, indent=2)
        print("   ✅ File created successfully")
    except Exception as e:
        print(f"   ❌ Error creating file: {e}")
    
    # Test 3: Load created file
    print("3. Testing file loading...")
    try:
        with open(test_file, 'r') as f:
            loaded_data = json.load(f)
        print(f"   ✅ File loaded: {loaded_data['selected_digimon']}")
    except Exception as e:
        print(f"   ❌ Error loading file: {e}")
    
    # Cleanup
    if os.path.exists(test_file):
        os.remove(test_file)
    
    print()

def test_asset_paths():
    """Test asset path resolution"""
    print("=== Testing Asset Paths ===")
    
    # Test asset directories
    test_paths = [
        "assets",
        "assets/sprites", 
        "assets/background",
        "assets/food",
        "assets/others"
    ]
    
    for path in test_paths:
        if os.path.exists(path):
            count = len(os.listdir(path)) if os.path.isdir(path) else 0
            print(f"   ✅ {path}: {count} items")
        else:
            print(f"   ❌ {path}: NOT FOUND")
    
    print()

def test_sprite_folders():
    """Test Digimon sprite folders"""
    print("=== Testing Digimon Sprites ===")
    
    sprites_dir = "assets/sprites"
    if not os.path.exists(sprites_dir):
        print("   ❌ Sprites directory not found")
        return
    
    digimon_count = 0
    valid_digimon = 0
    
    for folder in os.listdir(sprites_dir):
        if folder.endswith("_dmc"):
            digimon_count += 1
            folder_path = os.path.join(sprites_dir, folder)
            
            # Check for required animation frames
            frame_0 = os.path.join(folder_path, "0.png")
            frame_1 = os.path.join(folder_path, "1.png")
            
            if os.path.exists(frame_0) and os.path.exists(frame_1):
                valid_digimon += 1
    
    print(f"   Found {digimon_count} Digimon folders")
    print(f"   Valid Digimon (with walking frames): {valid_digimon}")
    
    if valid_digimon >= 2:
        print("   ✅ Sufficient Digimon for game")
    else:
        print("   ⚠️  May need more Digimon sprites")
    
    print()

def test_pygame_import():
    """Test if pygame can be imported"""
    print("=== Testing Pygame Import ===")
    
    try:
        import pygame
        print("   ✅ Pygame imported successfully")
        print(f"   Version: {pygame.version.ver}")
    except ImportError as e:
        print(f"   ❌ Pygame import failed: {e}")
        print("   Install with: pip install pygame")
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
    
    print()

def main():
    """Run all tests"""
    print("🧪 VPet Raspberry Pi Compatibility Test")
    print("=" * 40)
    print()
    
    test_pygame_import()
    test_asset_paths()
    test_sprite_folders()
    test_selection_file_handling()
    
    print("=" * 40)
    print("🎯 Test completed!")
    print()
    print("To fix any issues:")
    print("1. Run: python create_initial_selection.py")
    print("2. Run: python run.py")

if __name__ == "__main__":
    main()
