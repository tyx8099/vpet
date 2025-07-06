#!/usr/bin/env python3
"""
Convert PNG images to LVGL C arrays for embedded use.
This script converts the Digimon sprites from PNG to C array format.
"""

import os
from PIL import Image
import sys

def png_to_c_array(image_path, array_name):
    """Convert a PNG image to LVGL C array format."""
    try:
        # Open and convert image to RGBA
        img = Image.open(image_path)
        img = img.convert('RGBA')
        
        width, height = img.size
        pixels = list(img.getdata())
        
        # Generate C array header
        c_array = f"""
/* {array_name} - {width}x{height} RGBA8888 */
static const uint32_t {array_name}_data[] = {{
"""
        
        # Convert pixels to hex values
        for i, (r, g, b, a) in enumerate(pixels):
            if i % 8 == 0:
                c_array += "\n    "
            
            # Convert RGBA to ARGB8888 format for LVGL
            argb = (a << 24) | (r << 16) | (g << 8) | b
            c_array += f"0x{argb:08X}"
            
            if i < len(pixels) - 1:
                c_array += ", "
        
        c_array += f"""
}};

static const lv_img_dsc_t {array_name} = {{
    .header.always_zero = 0,
    .header.w = {width},
    .header.h = {height},
    .data_size = {len(pixels) * 4},
    .header.cf = LV_IMG_CF_TRUE_COLOR_ALPHA,
    .data = (uint8_t*){array_name}_data,
}};
"""
        
        return c_array, width, height
        
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None, 0, 0

def convert_digimon_sprites():
    """Convert Agumon sprites to C arrays."""
    sprite_dir = r"c:\Users\yuxun\Desktop\code\vpet\assets\sprites\Agumon_dmc"
    output_file = r"c:\Users\yuxun\Desktop\code\vpet\LVGL_vpet_Demo\sprite_data.h"
    
    if not os.path.exists(sprite_dir):
        print(f"Sprite directory not found: {sprite_dir}")
        return False
    
    header = """#ifndef SPRITE_DATA_H
#define SPRITE_DATA_H

#include "lvgl/lvgl.h"

/* Agumon sprite frames - converted from PNG to LVGL format */
"""
    
    # Array to store sprite info
    sprite_info = []
    
    # Convert each sprite frame
    for i in range(15):  # 0-14 frames
        sprite_path = os.path.join(sprite_dir, f"{i}.png")
        if os.path.exists(sprite_path):
            array_name = f"agumon_frame_{i}"
            c_array, width, height = png_to_c_array(sprite_path, array_name)
            
            if c_array:
                header += c_array
                sprite_info.append((array_name, width, height))
                print(f"Converted {sprite_path} -> {array_name} ({width}x{height})")
            else:
                print(f"Failed to convert {sprite_path}")
        else:
            print(f"Sprite not found: {sprite_path}")
    
    # Generate sprite array
    header += f"""
/* Array of all Agumon frames */
static const lv_img_dsc_t* agumon_frames[] = {{
"""
    
    for array_name, _, _ in sprite_info:
        header += f"    &{array_name},\n"
    
    header += f"""
}};

#define AGUMON_FRAME_COUNT {len(sprite_info)}
#define AGUMON_WIDTH {sprite_info[0][1] if sprite_info else 0}
#define AGUMON_HEIGHT {sprite_info[0][2] if sprite_info else 0}

#endif /* SPRITE_DATA_H */
"""
    
    # Write to file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(header)
        print(f"Sprite data written to: {output_file}")
        print(f"Converted {len(sprite_info)} frames")
        return True
    except Exception as e:
        print(f"Error writing output file: {e}")
        return False

if __name__ == "__main__":
    print("Converting Digimon sprites to LVGL C arrays...")
    convert_digimon_sprites()
