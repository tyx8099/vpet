# LVGL VPet Demo

This is a demonstration of the VPet game using LVGL for cross-platform compatibility.

## Setup Instructions

### For Windows (Code::Blocks + MinGW-w64):

1. Install Code::Blocks with MinGW-w64
2. Download LVGL PC simulator from: https://github.com/lvgl/lv_port_pc_eclipse
3. Extract LVGL files to `lvgl/` directory in this project
4. Open `LVGL_vpet_Demo.cbp` in Code::Blocks
5. Build and run

### Project Structure:
```
LVGL_vpet_Demo/
├── main.cpp                 # Main application entry point
├── lvgl_demo.cpp           # LVGL demo implementation
├── sprite_data.h           # Converted Digimon sprites
├── lvgl_config.h           # LVGL configuration
├── LVGL_vpet_Demo.cbp      # Code::Blocks project file
├── lvgl/                   # LVGL library (download separately)
└── assets/                 # Converted sprite assets
```

## Features Demonstrated:
- Digimon walking animation (15 frames)
- Basic UI elements (background, status indicators)
- Frame-based animation system
- Cross-platform sprite rendering

## Sprite Conversion:
The demo includes converted Agumon sprites. To add more Digimon:
1. Use the sprite conversion script in the main project
2. Add new sprite arrays to `sprite_data.h`
3. Update the animation code in `lvgl_demo.cpp`
