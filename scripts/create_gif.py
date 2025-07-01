#!/usr/bin/env python3
"""
GIF Creator Script
Creates walking animations from individual frame images
"""

from PIL import Image
import os
import sys

def create_walking_gif(frame1_path, frame2_path, output_path, duration=500):
    """
    Create a walking GIF animation from two frame images
    
    Args:
        frame1_path (str): Path to first frame image
        frame2_path (str): Path to second frame image
        output_path (str): Path for output GIF file
        duration (int): Duration per frame in milliseconds
    """
    
    if not os.path.exists(frame1_path):
        print(f"Error: {frame1_path} not found!")
        return False
    
    if not os.path.exists(frame2_path):
        print(f"Error: {frame2_path} not found!")
        return False
    
    try:
        # Load the two frames
        frame1 = Image.open(frame1_path).convert('RGBA')
        frame2 = Image.open(frame2_path).convert('RGBA')
        
        print(f"Frame 1 size: {frame1.size}")
        print(f"Frame 2 size: {frame2.size}")
        
        # Create the walking animation sequence
        frames = [frame1, frame2]
        
        # Save as animated GIF
        frame1.save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            duration=duration,
            loop=0,  # Loop forever
            disposal=2  # Clear frame before next one to reduce ghosting
        )
        
        print(f"Successfully created {output_path}")
        print(f"Animation has {len(frames)} frames with {duration}ms duration each")
        return True
        
    except Exception as e:
        print(f"Error creating GIF: {e}")
        return False

def main():
    """Main function for command line usage"""
    if len(sys.argv) != 4:
        print("Usage: python create_gif.py <frame1.png> <frame2.png> <output.gif>")
        print("Example: python create_gif.py Gabumon_1.png Gabumon_2.png Gabumon-walking.gif")
        sys.exit(1)
    
    frame1_path = sys.argv[1]
    frame2_path = sys.argv[2]
    output_path = sys.argv[3]
    
    success = create_walking_gif(frame1_path, frame2_path, output_path)
    
    if success:
        print("GIF creation completed successfully!")
    else:
        print("GIF creation failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
