#!/usr/bin/env python3

import os
import sys

# Add src directory to path
src_path = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, src_path)

# Test the animation
if __name__ == "__main__":
    try:
        from main import VPetGame
        print("Successfully imported VPetGame")
        print("PNG animation frames should be loaded from:")
        print("- assets/sprites/Agumon_dmc/0.png and 1.png")
        print("- assets/sprites/Gabumon_dmc/0.png and 1.png")
        print("Animation interval: 0.5 seconds (5 ticks at 10 FPS)")
        
        # Initialize and run the game
        game = VPetGame()
        print("Game initialized successfully with PNG frames!")
        print("Press ESC to exit the game")
        game.run()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
