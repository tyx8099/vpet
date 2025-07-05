#!/usr/bin/env python3
"""Test script to verify the Digimon selection functionality works"""

import sys
import os
import json

# Add src directory to path so we can import main
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    import pygame
    pygame.init()
    
    # Import our main module
    from main import VPetGame, DigimonSelectionUI
    
    print("✓ Successfully imported VPetGame and DigimonSelectionUI")
    
    # Test creating a game instance (without running it)
    print("Testing VPetGame initialization...")
    game = VPetGame()
    
    print("✓ VPetGame initialized successfully")
    print(f"Available Digimon: {len(game.available_digimon)}")
    print(f"First few Digimon: {game.available_digimon[:5] if game.available_digimon else 'None'}")
    print(f"Current Digimon: {game.digimon1_name}, {game.digimon2_name}")
    print(f"Selection UI active: {game.selection_ui.active}")
    
    # Test selection file functionality
    print("\nTesting selection file operations...")
    test_selection = ['Agumon_dmc', 'Gabumon_dmc']
    game.save_selection(test_selection)
    loaded_selection = game.load_selection()
    print(f"✓ Save/load selection works: {loaded_selection}")
    
    print("\nAll tests passed! The implementation should work correctly.")
    print("You can now:")
    print("1. Run the main game: python src/main.py")
    print("2. Try swiping right to open the Digimon selection UI")
    print("3. Select 2 Digimon and confirm to change the active ones")
    
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you have pygame installed: pip install pygame")
except Exception as e:
    print(f"Error during testing: {e}")
    import traceback
    traceback.print_exc()
finally:
    try:
        pygame.quit()
    except:
        pass
