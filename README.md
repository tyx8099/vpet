# Virtual Pet Game

A simple virtual pet simulator featuring Agumon and Gabumon from the Digimon universe.

## Features

- **Dual Digimon**: Both Agumon and Gabumon walk around simultaneously
- **Animated Sprites**: Support for both GIF animations and static PNG images
- **Custom Background**: Uses bg1.jpg as the background image
- **Natural Movement**: Random direction changes for realistic pet behavior
- **Collision Detection**: Digimon bounce off each other when they meet
- **Retro Screen**: 480x320 pixel display for authentic virtual pet feel

## Requirements

- Python 3.7+
- pygame
- Pillow (PIL)

## Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Option 1: Using the launcher (recommended)
```bash
python run.py
```

### Option 2: Direct execution
```bash
python src/main.py
```

### Option 3: Windows batch file
Double-click `start_game.bat` on Windows systems

## Controls

- **ESC** - Exit game
- **Close Window** - Exit game

## Project Structure

```
vpet/
├── src/                    # Source code
│   └── main.py            # Main game file (can run directly)
├── assets/                # Game assets
│   ├── sprites/           # Digimon sprite files
│   └── bg1.jpg           # Background image
├── docs/                  # Documentation
├── scripts/               # Utility scripts
├── run.py                 # Launcher script (recommended)
├── start_game.bat         # Windows batch launcher
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Sprite Files

The game looks for these sprite files in `assets/sprites/`:

- **Agumon**: `agumon-walking.gif` or `The-REAL-Agumon-sprite.png`
- **Gabumon**: `Gabumon-walking.gif` or `Gabumon_1.png`

## Technical Details

- **Screen Resolution**: 480x320 pixels
- **Frame Rate**: 10 FPS
- **Sprite Scaling**: Auto-scaled to 50x50 pixels max
- **Animation**: Supports multi-frame GIF animations

## License

This project is for educational purposes. Digimon characters are property of their respective owners.
