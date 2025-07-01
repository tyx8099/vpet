#!/usr/bin/env python3

import os
from PIL import Image

def analyze_images():
    # Set up paths
    if os.path.basename(os.getcwd()) == 'src':
        assets_dir = os.path.join(os.path.dirname(os.getcwd()), "assets")
    else:
        assets_dir = os.path.join(os.path.dirname(__file__), "assets")
    
    sprites_dir = os.path.join(assets_dir, "sprites")
    
    gabumon_1_path = os.path.join(sprites_dir, "Gabumon_1.png")
    gabumon_dmc_0_path = os.path.join(sprites_dir, "Gabumon_dmc", "0.png")
    
    print("="*60)
    print("GABUMON PNG COMPARISON ANALYSIS")
    print("="*60)
    
    try:
        # Load first image
        img1 = Image.open(gabumon_1_path)
        print(f"✓ Loaded: {os.path.basename(gabumon_1_path)}")
        print(f"  - Path: {gabumon_1_path}")
        print(f"  - Size: {img1.size[0]}x{img1.size[1]} pixels")
        print(f"  - Mode: {img1.mode}")
        print(f"  - Format: {img1.format}")
        
        # Get file size
        file_size1 = os.path.getsize(gabumon_1_path)
        print(f"  - File Size: {file_size1:,} bytes ({file_size1/1024:.1f} KB)")
        
    except Exception as e:
        print(f"✗ Could not load {gabumon_1_path}: {e}")
        return
    
    print()
    
    try:
        # Load second image
        img2 = Image.open(gabumon_dmc_0_path)
        print(f"✓ Loaded: {os.path.basename(gabumon_dmc_0_path)}")
        print(f"  - Path: {gabumon_dmc_0_path}")
        print(f"  - Size: {img2.size[0]}x{img2.size[1]} pixels")
        print(f"  - Mode: {img2.mode}")
        print(f"  - Format: {img2.format}")
        
        # Get file size
        file_size2 = os.path.getsize(gabumon_dmc_0_path)
        print(f"  - File Size: {file_size2:,} bytes ({file_size2/1024:.1f} KB)")
        
    except Exception as e:
        print(f"✗ Could not load {gabumon_dmc_0_path}: {e}")
        return
    
    print("\n" + "-"*40)
    print("COMPARISON RESULTS:")
    print("-"*40)
    
    # Compare dimensions
    if img1.size == img2.size:
        print("✓ DIMENSIONS: Both images have the same size")
    else:
        print("✗ DIMENSIONS: Images have different sizes")
        print(f"  - Gabumon_1.png: {img1.size[0]}x{img1.size[1]}")
        print(f"  - 0.png: {img2.size[0]}x{img2.size[1]}")
    
    # Compare file sizes
    size_diff = abs(file_size1 - file_size2)
    size_diff_percent = (size_diff / max(file_size1, file_size2)) * 100
    print(f"\n📁 FILE SIZE DIFFERENCE: {size_diff:,} bytes ({size_diff_percent:.1f}%)")
    
    # Compare modes
    if img1.mode == img2.mode:
        print(f"✓ COLOR MODE: Both images use {img1.mode} mode")
    else:
        print(f"✗ COLOR MODE: Different modes - {img1.mode} vs {img2.mode}")
    
    # If same size, do pixel comparison
    if img1.size == img2.size:
        try:
            # Convert to same mode for comparison
            if img1.mode != img2.mode:
                if img1.mode == 'RGBA':
                    img2 = img2.convert('RGBA')
                elif img2.mode == 'RGBA':
                    img1 = img1.convert('RGBA')
                else:
                    img1 = img1.convert('RGB')
                    img2 = img2.convert('RGB')
            
            # Simple pixel comparison using PIL
            # Convert to list of pixels
            pixels1 = list(img1.getdata())
            pixels2 = list(img2.getdata())
            
            total_pixels = len(pixels1)
            different_pixels = sum(1 for p1, p2 in zip(pixels1, pixels2) if p1 != p2)
            similarity = ((total_pixels - different_pixels) / total_pixels) * 100
            
            print(f"\n🔍 PIXEL ANALYSIS:")
            print(f"  - Total pixels: {total_pixels:,}")
            print(f"  - Different pixels: {different_pixels:,}")
            print(f"  - Similarity: {similarity:.2f}%")
            
            # Detailed difference analysis
            print(f"\n🔬 DETAILED DIFFERENCE ANALYSIS:")
            
            # Analyze types of differences
            color_changes = 0
            transparency_changes = 0
            major_changes = 0  # Completely different pixels
            minor_changes = 0  # Small color variations
            
            # Sample some different pixels for analysis
            sample_differences = []
            sample_count = 0
            max_samples = 10
            
            for i, (p1, p2) in enumerate(zip(pixels1, pixels2)):
                if p1 != p2:
                    # Analyze the type of difference
                    if len(p1) == 4 and len(p2) == 4:  # RGBA
                        r1, g1, b1, a1 = p1
                        r2, g2, b2, a2 = p2
                        
                        # Check if only transparency changed
                        if (r1, g1, b1) == (r2, g2, b2) and a1 != a2:
                            transparency_changes += 1
                        # Check if colors changed but transparency same
                        elif (r1, g1, b1) != (r2, g2, b2) and a1 == a2:
                            color_changes += 1
                            # Calculate color difference magnitude
                            color_diff = abs(r1-r2) + abs(g1-g2) + abs(b1-b2)
                            if color_diff > 100:  # Arbitrary threshold
                                major_changes += 1
                            else:
                                minor_changes += 1
                        else:
                            # Both color and transparency changed
                            major_changes += 1
                        
                        # Collect samples for display
                        if sample_count < max_samples:
                            row = i // img1.size[0]
                            col = i % img1.size[0]
                            sample_differences.append({
                                'position': (col, row),
                                'pixel1': p1,
                                'pixel2': p2,
                                'type': 'transparency' if (r1, g1, b1) == (r2, g2, b2) else 'color'
                            })
                            sample_count += 1
                    
                    elif len(p1) == 3 and len(p2) == 3:  # RGB
                        r1, g1, b1 = p1
                        r2, g2, b2 = p2
                        color_changes += 1
                        color_diff = abs(r1-r2) + abs(g1-g2) + abs(b1-b2)
                        if color_diff > 100:
                            major_changes += 1
                        else:
                            minor_changes += 1
                        
                        if sample_count < max_samples:
                            row = i // img1.size[0]
                            col = i % img1.size[0]
                            sample_differences.append({
                                'position': (col, row),
                                'pixel1': p1,
                                'pixel2': p2,
                                'type': 'color'
                            })
                            sample_count += 1
            
            print(f"  - Pure transparency changes: {transparency_changes}")
            print(f"  - Pure color changes: {color_changes}")
            print(f"  - Major changes (big color diff): {major_changes}")
            print(f"  - Minor changes (small color diff): {minor_changes}")
            
            # Show sample differences
            if sample_differences:
                print(f"\n📋 SAMPLE PIXEL DIFFERENCES (first {len(sample_differences)}):")
                for i, diff in enumerate(sample_differences):
                    pos = diff['position']
                    p1 = diff['pixel1']
                    p2 = diff['pixel2']
                    diff_type = diff['type']
                    
                    print(f"  {i+1}. Position ({pos[0]}, {pos[1]}) - {diff_type} change")
                    print(f"     Gabumon_1.png: {p1}")
                    print(f"     Gabumon_dmc/0.png: {p2}")
            
            # Analyze distribution of differences
            print(f"\n📊 DIFFERENCE DISTRIBUTION:")
            width, height = img1.size
            
            # Check if differences are clustered in certain areas
            diff_positions = []
            for i, (p1, p2) in enumerate(zip(pixels1, pixels2)):
                if p1 != p2:
                    row = i // width
                    col = i % width
                    diff_positions.append((col, row))
            
            if diff_positions:
                # Find bounding box of differences
                min_x = min(pos[0] for pos in diff_positions)
                max_x = max(pos[0] for pos in diff_positions)
                min_y = min(pos[1] for pos in diff_positions)
                max_y = max(pos[1] for pos in diff_positions)
                
                print(f"  - Differences span from ({min_x}, {min_y}) to ({max_x}, {max_y})")
                print(f"  - Difference area: {max_x - min_x + 1} x {max_y - min_y + 1} pixels")
                
                # Check if differences are concentrated in center vs edges
                center_x, center_y = width // 2, height // 2
                center_diffs = sum(1 for x, y in diff_positions 
                                 if abs(x - center_x) < width // 4 and abs(y - center_y) < height // 4)
                edge_diffs = different_pixels - center_diffs
                
                print(f"  - Center region differences: {center_diffs} ({center_diffs/different_pixels*100:.1f}%)")
                print(f"  - Edge region differences: {edge_diffs} ({edge_diffs/different_pixels*100:.1f}%)")
            
            # Conclusion about difference types
            print(f"\n💡 DIFFERENCE ANALYSIS CONCLUSION:")
            if transparency_changes > different_pixels * 0.5:
                print("  🎭 Most differences are transparency changes - likely due to")
                print("     different compression or anti-aliasing techniques")
            elif minor_changes > major_changes:
                print("  🎨 Most differences are minor color variations - likely due to")
                print("     different compression levels or slight pose differences")
            elif major_changes > different_pixels * 0.3:
                print("  🔄 Many major color changes - these represent actual")
                print("     animation frame differences (pose, position changes)")
            else:
                print("  📸 Mixed types of differences - combination of compression")
                print("     artifacts and actual animation frame changes")
            
            if different_pixels == 0:
                print("✓ RESULT: Images are pixel-perfect identical!")
            elif similarity > 99:
                print("⚠ RESULT: Images are nearly identical (>99% similar)")
            elif similarity > 90:
                print("⚠ RESULT: Images are very similar (>90% similar)")
            elif similarity > 50:
                print("⚠ RESULT: Images are somewhat similar (>50% similar)")
            else:
                print("✗ RESULT: Images are significantly different")
                
        except Exception as e:
            print(f"Could not perform pixel comparison: {e}")
    
    print("\n" + "="*60)
    print("SUMMARY:")
    print("="*60)
    
    if img1.size == img2.size and 'similarity' in locals() and similarity > 95:
        print("🎯 These images are very similar and likely represent the same")
        print("   character pose/frame. Good candidates for animation comparison!")
    elif img1.size != img2.size:
        print("📏 These images have different dimensions, which may affect")
        print("   how they appear in your animation.")
    else:
        print("🔄 These images show different poses/states of Gabumon,")
        print("   which is expected for animation frames.")

if __name__ == "__main__":
    analyze_images()
