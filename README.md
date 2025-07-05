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
- **Right Click & Drag Food**: Feed your Digimon (drag food items to pets)
- **Swipe Right**: Open Digimon selection UI (click and drag left to right)
- **Double-tap Upper Screen**: Change background
- **ESC**: Exit game

## 🎪 Game Mechanics

### Pet Behaviors
- **Sleeping**: Pets start sleeping with gentle animation
- **Walking**: Random movement with direction changes
- **Jumping**: Half-height jumps when tapped
- **Greeting**: Face each other and animate when colliding
- **Feeding**: Drag food items to pets to increase their hunger levels

### Visual Effects
- **Heart Emotions**: 💖 Appear 10 pixels above pet's head for 1 second
- **Sprite Animations**: Smooth PNG frame cycling
- **Background Rotation**: Multiple scenic backgrounds
- **Auto-hiding Cursor**: Disappears after 2 seconds of inactivity

### Digimon Selection
- **Swipe Right**: Opens a selection UI with all available Digimon
- **Grid Layout**: Browse through Digimon in an organized grid
- **Live Preview**: Each Digimon shows their walking animation
- **Max 2 Selection**: Choose up to 2 Digimon for the main game

## 📁 Project Structure

```
vpet/
├── src/
│   └── main.py          # Main game engine
├── assets/
│   ├── sprites/         # Digimon sprite folders
│   │   ├── Agumon_dmc/  # Individual Digimon sprites
│   │   └── ...
│   ├── others/          # Heart emotion and other assets
│   ├── food/            # Food items
│   └── background/      # Background images
├── run.py              # Game launcher
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── DIGIMON_SELECTION.md # Digimon selection UI documentation
└── RASPBERRY_PI_FIXES.md # Raspberry Pi compatibility guide
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

## 📚 Documentation

- **[DIGIMON_SELECTION.md](DIGIMON_SELECTION.md)** - Complete guide to the Digimon selection UI
- **[RASPBERRY_PI_FIXES.md](RASPBERRY_PI_FIXES.md)** - Raspberry Pi compatibility and troubleshooting

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

## 📄 License

This project is for educational purposes. Digimon characters are property of their respective owners.
