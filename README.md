# Virtual Pet Game

A charming virtual pet simulator featuring random Digimon selection, interactive gameplay, and heart emotions.

## 🎮 Features

- **Random Digimon Selection**: Game randomly picks 2 different Digimon from 20+ available types
- **Interactive Gameplay**: Tap to wake up sleeping pets or make them jump
- **Heart Emotions**: Adorable heart animations appear when interacting with pets
- **Background Cycling**: Double-tap to cycle through beautiful backgrounds
- **Collision Greetings**: Pets greet each other when they meet
- **Sleep/Wake Cycles**: Pets start sleeping and wake up when tapped

## 🎯 Quick Start

```bash
# Install dependencies
pip install pygame

# Run the game
python run.py
```

## 🎨 Available Digimon

The game includes 20+ Digimon types:
- Agumon, Gabumon, Greymon, Garurumon
- Patamon, Betamon, Elecmon, Gizamon
- Koromon, Botamon, Mamemon, Meramon
- Kabuterimon, Airdramon, Devimon
- And many more!

## 🎵 Controls

- **Left Click on Pet**: Wake up (if sleeping) or Jump (if awake)
- **Double-tap Upper Screen**: Change background
- **ESC**: Exit game

## 🎪 Game Mechanics

### Pet Behaviors
- **Sleeping**: Pets start sleeping with gentle animation
- **Walking**: Random movement with direction changes
- **Jumping**: Half-height jumps when tapped
- **Greeting**: Face each other and animate when colliding

### Visual Effects
- **Heart Emotions**: 💖 Appear 10 pixels above pet's head for 1 second
- **Sprite Animations**: Smooth PNG frame cycling
- **Background Rotation**: Multiple scenic backgrounds
- **Auto-hiding Cursor**: Disappears after 2 seconds of inactivity

## 📁 Project Structure

```
vpet/
├── src/
│   └── main.py          # Main game engine
├── assets/
│   ├── sprites/         # Digimon sprite folders
│   │   ├── emotion/     # Heart and other emotions
│   │   ├── Agumon_dmc/  # Individual Digimon sprites
│   │   └── ...
│   └── background/      # Background images
├── run.py              # Game launcher
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🚀 Deployment

### Desktop/Laptop
```bash
python run.py
```

### Raspberry Pi
```bash
cd /path/to/vpet
git pull origin main
python run.py
```

## 🛠 Development

### Adding New Digimon
1. Create new folder: `assets/sprites/NewDigimon_dmc/`
2. Add sprite files: `0.png`, `1.png`, `2.png`, `11.png`, `12.png`
3. Game will automatically detect and include it

### Adding New Backgrounds
1. Add image to `assets/background/`
2. Supported formats: PNG, JPG, JPEG, BMP
3. Will be automatically loaded and cycled

## 📊 System Requirements

- **Python 3.6+**
- **Pygame library**
- **~5-8 MB disk space**
- **Minimal RAM usage** (<100MB)

## 🎯 Perfect For

- **Raspberry Pi projects**
- **Desktop entertainment**
- **Learning game development**
- **Nostalgic virtual pet experience**

## 💖 Special Thanks

Built with love for Digimon fans and virtual pet enthusiasts!

---
*Enjoy your virtual pet adventure!* 🎮✨
- Pillow (PIL) - only needed for comparison tools

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

### Analysis Tools
```bash
# Compare GIF vs PNG animations side by side
python comparison_demo.py

# Analyze differences between image files
python analyze_images.py

# Visual image comparison tool
python image_comparison.py
```

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
