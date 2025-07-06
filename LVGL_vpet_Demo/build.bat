@echo off
echo LVGL VPet Demo Build Script
echo ===========================

echo Checking for LVGL directory...
if not exist "lvgl" (
    echo ERROR: LVGL directory not found!
    echo.
    echo Please download LVGL PC simulator from:
    echo https://github.com/lvgl/lv_port_pc_eclipse
    echo.
    echo Extract the contents to a folder named "lvgl" in this directory.
    echo.
    pause
    exit /b 1
)

echo LVGL directory found.

echo Checking for Code::Blocks installation...
where /q codeblocks.exe
if errorlevel 1 (
    echo WARNING: Code::Blocks not found in PATH
    echo You may need to open the project manually from Code::Blocks IDE
) else (
    echo Code::Blocks found.
)

echo.
echo Build options:
echo 1. Open project in Code::Blocks
echo 2. Build using MinGW directly (advanced)
echo 3. Show setup instructions
echo 4. Test sprite conversion
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo Opening project in Code::Blocks...
    start "" "LVGL_vpet_Demo.cbp"
) else if "%choice%"=="2" (
    echo Building with MinGW...
    echo NOTE: This requires proper MinGW setup and SDL2 libraries
    mingw32-make -f Makefile
) else if "%choice%"=="3" (
    goto :instructions
) else if "%choice%"=="4" (
    echo Testing sprite conversion...
    python convert_sprites.py
    echo.
    echo Check sprite_data.h for converted sprites.
) else (
    echo Invalid choice.
)

goto :end

:instructions
echo.
echo Setup Instructions:
echo ==================
echo.
echo 1. Install Code::Blocks with MinGW-w64:
echo    - Download from: http://www.codeblocks.org/downloads
echo    - Choose the version that includes MinGW-w64
echo.
echo 2. Download LVGL PC simulator:
echo    - Go to: https://github.com/lvgl/lv_port_pc_eclipse
echo    - Download as ZIP or clone the repository
echo    - Extract/copy the contents to a "lvgl" folder in this directory
echo.
echo 3. Install SDL2 development libraries:
echo    - Download SDL2 development libraries from: https://www.libsdl.org/
echo    - Extract to a location accessible by MinGW
echo    - Or use package manager: pacman -S mingw-w64-x86_64-SDL2
echo.
echo 4. Open LVGL_vpet_Demo.cbp in Code::Blocks:
echo    - File -^> Open -^> LVGL_vpet_Demo.cbp
echo    - Build -^> Build (Ctrl+F9)
echo    - Run -^> Run (Ctrl+F10)
echo.
echo 5. The demo will show:
echo    - Agumon walking animation
echo    - Animation controls (Play/Pause/Reset/Next)
echo    - Frame counter and FPS display
echo    - Sprite information panel
echo.

:end
echo.
pause
