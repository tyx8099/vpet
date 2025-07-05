# Digimon Selection UI - Feature Documentation

## Overview
The main game now includes a swipe right gesture that opens a Digimon selection UI, allowing users to choose which 2 Digimon appear in the main game.

## How to Use

### Opening the Selection UI
1. **Swipe Right Gesture**: In the main game, click and drag from left to right across the screen
   - Minimum swipe distance: 50 pixels
   - Maximum time limit: 500 milliseconds
   - Must be primarily horizontal movement

### Using the Selection UI
1. **Digimon Grid**: Browse through available Digimon in a 4x3 grid layout
2. **Walking Animation**: Each Digimon shows their walking animation (frames 0 and 1)
3. **Selection**: Click on a Digimon to select/deselect it
   - Maximum 2 Digimon can be selected
   - Selected Digimon have a green background
4. **Navigation**: 
   - Use "Previous" and "Next" buttons to change pages
   - Page indicator shows current page and total pages
5. **Confirmation**: 
   - "Confirm" button appears when exactly 2 Digimon are selected
   - Click "Confirm" to apply the selection and return to the main game
6. **Closing**: Click the "X" button in the top-right to close without changing selection

### Persistent Selection
- The selected Digimon are saved to `digimon_selection.json`
- When the game starts, it automatically loads the last saved selection
- If no saved selection exists, 2 random Digimon are chosen

## Technical Details

### Files Modified
- `src/main.py`: Main game logic with selection UI integration

### Key Features Added
1. **DigimonSelectionUI Class**: Complete UI for Digimon selection
2. **Swipe Gesture Detection**: Mouse/touch gesture recognition
3. **Persistent Storage**: JSON file for saving/loading selections
4. **Game Integration**: Selection UI blocks normal game input when active

### Constants Added
```python
SWIPE_THRESHOLD = 50  # Minimum swipe distance
SWIPE_TIME_LIMIT = 500  # Maximum swipe time in milliseconds
SELECTION_GRID_COLS = 4  # Grid columns
SELECTION_GRID_ROWS = 3  # Grid rows
SELECTION_CELL_SIZE = 100  # Size of each Digimon cell
```

### Key Methods Added
- `get_available_digimon()`: Scans sprites directory for available Digimon
- `load_selection()`: Loads saved Digimon selection from JSON file
- `save_selection()`: Saves current selection to JSON file
- `initialize_digimon()`: Creates Digimon instances based on selection

## Testing
Run the test script to verify functionality:
```bash
python test_selection.py
```

The test verifies:
- Successful import of all classes
- VPetGame initialization
- Available Digimon detection
- Selection save/load functionality

## Usage Examples

### Manual Testing
1. Run the main game: `python src/main.py`
2. Try swiping right to open the selection UI
3. Select 2 different Digimon and confirm
4. The main game should now show your selected Digimon
5. Restart the game - it should remember your selection

### Programmatic Usage
```python
from main import VPetGame

# Create game instance
game = VPetGame()

# Check current selection
print(f"Current Digimon: {game.digimon1_name}, {game.digimon2_name}")

# Save a specific selection
game.save_selection(['Agumon_dmc', 'Gabumon_dmc'])

# Initialize with specific Digimon
game.initialize_digimon(['Greymon_dmc', 'Garurumon_dmc'])
```

## Notes
- The selection UI only shows walking animation (frames 0 and 1) for preview
- All available Digimon folders ending with "_dmc" are automatically detected
- The UI is responsive and handles pagination for large numbers of Digimon
- Game state is properly preserved when switching between UI and main game
