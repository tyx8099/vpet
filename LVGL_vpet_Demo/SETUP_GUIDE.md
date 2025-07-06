# LVGL VPet Demo - Complete Setup Guide

This guide will help you set up and run the LVGL VPet Demo, which showcases Digimon sprite animation using the LVGL graphics library.

## Prerequisites

### 1. Code::Blocks IDE with MinGW-w64
- Download from: [http://www.codeblocks.org/downloads](http://www.codeblocks.org/downloads)
- **Important**: Choose the version that includes MinGW-w64 compiler
- Alternative: `codeblocks-20.03mingw-setup.exe` (recommended)

### 2. SDL2 Development Libraries
For Windows with MinGW-w64:
- Download SDL2 development libraries from: [https://www.libsdl.org/download-2.0.php](https://www.libsdl.org/download-2.0.php)
- Get: `SDL2-devel-2.x.x-mingw.tar.gz`
- Extract to a folder (e.g., `C:\SDL2`)

### 3. LVGL PC Simulator
- Download from: [https://github.com/lvgl/lv_port_pc_eclipse](https://github.com/lvgl/lv_port_pc_eclipse)
- Click "Code" → "Download ZIP" or clone the repository
- Extract the contents to a folder named `lvgl` in this project directory

## Setup Instructions

### Step 1: Prepare LVGL
1. Download the LVGL PC simulator from the link above
2. Extract/copy all contents to a folder named `lvgl` in this directory
3. Your folder structure should look like:
   ```
   LVGL_vpet_Demo/
   ├── main.cpp
   ├── lvgl_demo.cpp
   ├── sprite_data.h
   ├── lvgl/              ← LVGL files go here
   │   ├── lvgl/
   │   ├── lv_drivers/
   │   ├── main.c
   │   └── ...
   └── ...
   ```

### Step 2: Configure SDL2 (if needed)
1. If SDL2 is not in your system PATH, you may need to:
   - Copy SDL2 DLLs to your project directory
   - Or add SDL2 lib/bin directories to your system PATH
   - Or update the Code::Blocks project to point to SDL2 location

### Step 3: Build and Run
1. Open `LVGL_vpet_Demo.cbp` in Code::Blocks
2. Select "Debug" or "Release" build target
3. Press **Ctrl+F9** to build
4. Press **Ctrl+F10** to run

### Alternative: Command Line Building
If you prefer command line:
```bash
# Using the provided Makefile
make all

# Or directly with g++
g++ main.cpp lvgl_demo.cpp -std=c++11 -ILVCL_CONF_INCLUDE_SIMPLE -I. -Ilvgl -lmingw32 -lSDL2main -lSDL2 -lgdi32 -luser32 -lwinmm -o LVGL_vpet_Demo.exe
```

### Alternative: Visual Studio Code
If you prefer VS Code (recommended for modern development):

1. **Install VS Code**: Download from [https://code.visualstudio.com/](https://code.visualstudio.com/)

2. **Install Required Extensions**:
   - **C/C++** (Microsoft) - IntelliSense, debugging, code browsing
   - **C/C++ Extension Pack** (Microsoft) - Complete C++ development
   - **CMake Tools** (optional) - For CMake support

3. **Open Project in VS Code**:
   ```bash
   cd "c:\Users\yuxun\Desktop\code\vpet\LVGL_vpet_Demo"
   code .
   ```

4. **Configure Compiler** (first time only):
   - Press **Ctrl+Shift+P** → Type "C/C++: Edit Configurations"
   - VS Code will create `.vscode/c_cpp_properties.json`
   - Or use the pre-configured files included in this project

5. **Build and Run**:
   - Press **Ctrl+Shift+P** → Type "Tasks: Run Task" → Select "Build LVGL Demo"
   - Or press **F5** to build and debug
   - Or use **Ctrl+Shift+`** to open terminal and run: `make all`

6. **VS Code Features**:
   - **IntelliSense**: Auto-completion for LVGL functions
   - **Debugging**: Set breakpoints, step through code
   - **Integrated Terminal**: Build and run without leaving editor
   - **Git Integration**: Version control built-in
   - **Extensions**: Python support for sprite conversion script

## Demo Features

Once running, the demo will display:

### Main Window
- **Title**: "LVGL VPet Demo - Agumon"
- **Animated Sprite**: 48x48 pixel Agumon walking animation
- **Info Panel**: Shows sprite dimensions, frame count, and format
- **FPS Counter**: Real-time frame rate display (top-right)
- **Frame Counter**: Current frame number (below sprite)

### Controls
- **Play/Pause Button**: Toggle animation playback
- **Reset Button**: Return to frame 1
- **Next Button**: Step through frames manually (pauses animation)

### Technical Details
- **Animation Speed**: 10 FPS (100ms per frame) - matches main VPet game
- **Sprite Format**: RGBA8888 (32-bit with alpha channel)
- **Frame Count**: 15 frames of Agumon walking cycle
- **Update Rate**: 60Hz UI updates with 10Hz sprite animation

## Troubleshooting

### Build Errors

**Error: "g++ is not recognized as the name of a cmdlet"**
This means you don't have MinGW-w64 installed or it's not in your PATH. Here are solutions:

**Solution 1: Install MSYS2 (Recommended)**
1. Download MSYS2 from: [https://www.msys2.org/](https://www.msys2.org/)
2. Install it (default location: `C:\msys64`)
3. Open "MSYS2 MSYS" from Start Menu
4. Run these commands:
   ```bash
   pacman -Syu                                    # Update package database
   pacman -S mingw-w64-x86_64-toolchain         # Install compiler
   pacman -S mingw-w64-x86_64-SDL2              # Install SDL2
   pacman -S mingw-w64-x86_64-SDL2_mixer        # Install SDL2_mixer
   ```
5. Add to Windows PATH: `C:\msys64\mingw64\bin`
6. Restart VS Code/Command Prompt

**Solution 2: Install MinGW-w64 Standalone**
1. Download from: [https://www.mingw-w64.org/downloads/](https://www.mingw-w64.org/downloads/)
2. Choose "MingW-W64-builds" installer
3. Install with these settings:
   - Version: Latest
   - Architecture: x86_64
   - Threads: posix
   - Exception: seh
   - Build revision: Latest
4. Add installation `bin` folder to Windows PATH

**Solution 3: Use Visual Studio Build Tools (Alternative)**
1. Download "Build Tools for Visual Studio" from Microsoft
2. Install "C++ build tools" workload
3. Update VS Code tasks to use `cl.exe` instead of `g++`

**Solution 4: Test Without Building (Quick Demo)**
The demo main.cpp can run as a simple console program:
```bash
# If you have Python installed, you can at least test sprite conversion
python convert_sprites.py
```

**How to Add to Windows PATH:**
1. Press `Win + R`, type `sysdm.cpl`, press Enter
2. Click "Environment Variables"
3. Under "System Variables", find and select "Path"
4. Click "Edit" → "New"
5. Add your MinGW bin path (e.g., `C:\msys64\mingw64\bin`)
6. Click "OK" and restart Command Prompt/VS Code

**Error: "lvgl/lvgl.h not found"**
- Ensure LVGL is extracted to the `lvgl/` folder
- Check that `lvgl/lvgl/lvgl.h` exists

**Error: "SDL2 not found"**
- Install SDL2 development libraries
- Add SDL2 to system PATH or project settings

**Error: "mingw32 not found"**
- Install Code::Blocks with MinGW-w64
- Or install MinGW-w64 separately and configure paths

### Runtime Errors

**Error: "SDL2.dll not found"**
- Copy SDL2.dll to the same folder as your executable
- Or add SDL2 bin directory to system PATH

**Window doesn't appear**
- Check if LVGL display driver is properly initialized
- Verify SDL2 is working correctly

### Performance Issues

**Choppy Animation**
- This is normal - the demo runs at 10 FPS intentionally
- The UI updates at 60Hz, but sprite frames change every 100ms

**High CPU Usage**
- Expected behavior for software rendering
- LVGL PC simulator uses CPU-based graphics

## File Structure

```
LVGL_vpet_Demo/
├── main.cpp              # Main application entry point
├── lvgl_demo.cpp         # Demo implementation
├── lvgl_demo.h           # Demo header
├── sprite_data.h         # Converted Agumon sprites (generated)
├── lv_conf.h            # LVGL configuration
├── convert_sprites.py    # Sprite conversion utility
├── build.bat            # Build script for Windows
├── Makefile             # Makefile for command-line building
├── README.md            # This file
├── LVGL_vpet_Demo.cbp   # Code::Blocks project file
└── lvgl/                # LVGL library (download separately)
    ├── lvgl/
    ├── lv_drivers/
    └── ...
```

## Converting Additional Sprites

To add more Digimon or modify sprites:

1. **Edit Sprite Paths**: Modify `convert_sprites.py` to point to different sprite folders
2. **Run Conversion**: `python convert_sprites.py`
3. **Update Code**: Modify `lvgl_demo.cpp` to use new sprite arrays
4. **Rebuild**: Compile the project again

## Platform Notes

### ESP32-S3 Port
This demo serves as a reference for porting to ESP32-S3:
- Sprite data can be used directly (may need ROM storage)
- Animation logic is portable
- UI scaling may need adjustment for 1.8" AMOLED (320x240)

### Raspberry Pi
- LVGL has Linux framebuffer support
- May need different display drivers
- Performance should be similar to PC simulator

## Next Steps

1. **Extend Animation**: Add more Digimon characters
2. **Add Interactions**: Implement feeding, playing, status changes
3. **Background Support**: Add animated backgrounds
4. **Sound Effects**: Integrate SDL2_mixer for audio
5. **Touch Input**: Add touch controls for mobile platforms

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all prerequisites are installed correctly
3. Test the basic Code::Blocks + MinGW setup with a simple "Hello World" program
4. Check LVGL documentation: [https://docs.lvgl.io/](https://docs.lvgl.io/)

## License

This demo uses:
- LVGL (MIT License)
- SDL2 (zlib License)
- Digimon sprites (for demonstration purposes)

Make sure to comply with all applicable licenses for your use case.
