import pygame
import sys
import os
import random
import platform

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 320
BACKGROUND_COLOR = (135, 206, 235)  # Sky blue
DIGIMON_SPEED = 2

class Digimon:
    def __init__(self, sprite_folder, speed=DIGIMON_SPEED):
        self.frames = []
        self.current_frame = 0
        self.frame_timer = 0
        self.frame_delay = 5  # Change frame every 5 game ticks (0.5 seconds at 10 FPS)
        self.speed = speed  # Individual speed for each Digimon
        
        # Greeting animation state
        self.is_greeting = False
        self.greeting_timer = 0
        self.greeting_frame = 0
        self.greeting_cycles = 0
        self.greeting_frames = []  # Will store frames 2 and 0 for greeting
        self.post_greeting_direction = None  # Store direction to change to after greeting
        
        # Sleeping animation state
        self.is_sleeping = True  # Start sleeping
        self.sleeping_timer = 0
        self.sleeping_frame = 0
        self.sleeping_frames = []  # Will store frames 11 and 12 for sleeping
        
        # Jumping animation state
        self.is_jumping = False
        self.jump_velocity = 0
        self.ground_y = 0  # Will be set after rect is created
        self.gravity = 1
        self.jump_strength = -8  # Negative because pygame y-axis goes down
        
        # Load walking animation frames (0.png and 1.png), greeting frames (2.png), and sleeping frames (11.png and 12.png)
        try:
            # Load frame 0 and frame 1 for walking animation
            frame_0_path = os.path.join(sprite_folder, "0.png")
            frame_1_path = os.path.join(sprite_folder, "1.png")
            frame_2_path = os.path.join(sprite_folder, "2.png")
            frame_11_path = os.path.join(sprite_folder, "11.png")
            frame_12_path = os.path.join(sprite_folder, "12.png")
            
            if os.path.exists(frame_0_path) and os.path.exists(frame_1_path):
                # Load walking frames
                frame_0 = pygame.image.load(frame_0_path)
                frame_1 = pygame.image.load(frame_1_path)
                
                # Scale the frames for the smaller screen
                if frame_0.get_width() > 60 or frame_0.get_height() > 60:
                    frame_0 = pygame.transform.scale(frame_0, (50, 50))
                if frame_1.get_width() > 60 or frame_1.get_height() > 60:
                    frame_1 = pygame.transform.scale(frame_1, (50, 50))
                
                self.frames = [frame_0, frame_1]
                self.image = self.frames[0]
                
                # Load greeting frames (2 and 0)
                if os.path.exists(frame_2_path):
                    frame_2 = pygame.image.load(frame_2_path)
                    if frame_2.get_width() > 60 or frame_2.get_height() > 60:
                        frame_2 = pygame.transform.scale(frame_2, (50, 50))
                    self.greeting_frames = [frame_2, frame_0]  # 2 -> 0 -> 2 -> 0
                else:
                    # Fallback: use walking frames for greeting
                    self.greeting_frames = [frame_1, frame_0]
                
                # Load sleeping frames (11 and 12)
                if os.path.exists(frame_11_path) and os.path.exists(frame_12_path):
                    frame_11 = pygame.image.load(frame_11_path)
                    frame_12 = pygame.image.load(frame_12_path)
                    if frame_11.get_width() > 60 or frame_11.get_height() > 60:
                        frame_11 = pygame.transform.scale(frame_11, (50, 50))
                    if frame_12.get_width() > 60 or frame_12.get_height() > 60:
                        frame_12 = pygame.transform.scale(frame_12, (50, 50))
                    self.sleeping_frames = [frame_11, frame_12]  # 11 -> 12 -> 11 -> 12
                else:
                    # Fallback: use frame 0 for sleeping
                    self.sleeping_frames = [frame_0]
                    
            else:
                raise Exception(f"Walking frames not found: {frame_0_path} or {frame_1_path}")
                
        except Exception as e:
            print(f"Could not load sprite: {e}")
            # Create a simple colored rectangle as fallback
            self.image = pygame.Surface((40, 40))
            self.image.fill((255, 165, 0))  # Orange color
            self.frames = [self.image]
            self.greeting_frames = [self.image]  # Same fallback for greeting
            self.sleeping_frames = [self.image]  # Same fallback for sleeping
        
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = SCREEN_HEIGHT - 30 - self.rect.height  # Position on the invisible ground line
        self.ground_y = self.rect.y  # Store ground position for jumping
        self.direction = 1  # 1 for right, -1 for left
        self.flipped = False
        self.original_frames = self.frames.copy()  # Keep original frames for flipping
        self.original_greeting_frames = self.greeting_frames.copy()  # Keep original greeting frames
        self.original_sleeping_frames = self.sleeping_frames.copy()  # Keep original sleeping frames
        self.direction_timer = 0  # Timer for random direction changes
        self.next_direction_change = random.randint(60, 300)  # Random time between 1-5 seconds at 10fps
        
        # Start sleeping, so set image to first sleeping frame
        if self.sleeping_frames:
            self.image = self.sleeping_frames[0]
        
        # Ensure Digimon starts facing right by flipping if needed (but only when not sleeping)
        # Assume the original sprite faces left, so flip it to face right initially
        if not self.is_sleeping:
            self.frames = [pygame.transform.flip(frame, True, False) for frame in self.frames]
            self.greeting_frames = [pygame.transform.flip(frame, True, False) for frame in self.greeting_frames]
            self.sleeping_frames = [pygame.transform.flip(frame, True, False) for frame in self.sleeping_frames]
            self.image = self.frames[self.current_frame]
            self.flipped = True  # Mark as flipped since we're now facing right
    
    def start_greeting(self, face_direction=None, post_greeting_direction=None):
        """Start the greeting animation
        Args:
            face_direction: 1 for right, -1 for left (direction to face during greeting)
            post_greeting_direction: 1 for right, -1 for left (direction to move after greeting)
        """
        self.is_greeting = True
        self.greeting_timer = 0
        self.greeting_frame = 0
        self.greeting_cycles = 0
        # Stop moving while greeting
        self.speed_backup = self.speed
        self.speed = 0
        
        # Store the direction to change to after greeting
        self.post_greeting_direction = post_greeting_direction
        
        # Face the correct direction for greeting if specified
        if face_direction is not None:
            if face_direction == 1:  # Face right
                if not self.flipped:
                    self.frames = [pygame.transform.flip(frame, True, False) for frame in self.original_frames]
                    self.greeting_frames = [pygame.transform.flip(frame, True, False) for frame in self.original_greeting_frames]
                    self.sleeping_frames = [pygame.transform.flip(frame, True, False) for frame in self.original_sleeping_frames]
                    self.flipped = True
            else:  # Face left
                if self.flipped:
                    self.frames = self.original_frames.copy()
                    self.greeting_frames = self.original_greeting_frames.copy()
                    self.sleeping_frames = self.original_sleeping_frames.copy()
                    self.flipped = False
        
        # Immediately set to first greeting frame to avoid any walking animation
        self.image = self.greeting_frames[self.greeting_frame]
    
    def wake_up(self):
        """Wake up the Digimon from sleep"""
        if self.is_sleeping:
            self.is_sleeping = False
            self.sleeping_timer = 0
            self.sleeping_frame = 0
            
            # Switch back to walking animation
            self.current_frame = 0
            
            # Randomize direction when waking up
            self.direction = random.choice([-1, 1])
            
            # Set sprite orientation to match the direction
            if self.direction == 1:  # Moving right
                # Flip sprites to face right
                self.frames = [pygame.transform.flip(frame, True, False) for frame in self.original_frames]
                self.greeting_frames = [pygame.transform.flip(frame, True, False) for frame in self.original_greeting_frames]
                self.sleeping_frames = [pygame.transform.flip(frame, True, False) for frame in self.original_sleeping_frames]
                self.flipped = True
                print(f"Digimon woke up and will walk right!")
            else:  # Moving left
                # Use original sprites (facing left)
                self.frames = self.original_frames.copy()
                self.greeting_frames = self.original_greeting_frames.copy()
                self.sleeping_frames = self.original_sleeping_frames.copy()
                self.flipped = False
                print(f"Digimon woke up and will walk left!")
            
            self.image = self.frames[self.current_frame]
    
    def jump(self):
        """Make the Digimon jump (only if awake and not already jumping)"""
        if not self.is_sleeping and not self.is_jumping and not self.is_greeting:
            self.is_jumping = True
            self.jump_velocity = self.jump_strength
            print(f"Digimon jumped!")
    
    def update(self):
        # Handle sleeping animation
        if self.is_sleeping:
            self.sleeping_timer += 1
            
            # Animate sleeping frames
            if len(self.sleeping_frames) > 1 and self.sleeping_timer % self.frame_delay == 0:
                self.sleeping_frame = (self.sleeping_frame + 1) % len(self.sleeping_frames)
                self.image = self.sleeping_frames[self.sleeping_frame]
            
            return  # Don't do normal updates while sleeping
        
        # Handle jumping physics
        if self.is_jumping:
            self.jump_velocity += self.gravity
            self.rect.y += self.jump_velocity
            
            # Check if landed back on ground
            if self.rect.y >= self.ground_y:
                self.rect.y = self.ground_y
                self.is_jumping = False
                self.jump_velocity = 0
        
        # Handle greeting animation
        if self.is_greeting:
            self.greeting_timer += 1
            if self.greeting_timer >= self.frame_delay:
                self.greeting_timer = 0
                self.greeting_frame = (self.greeting_frame + 1) % len(self.greeting_frames)
                self.image = self.greeting_frames[self.greeting_frame]
                
                # Check if we completed a full cycle (2 -> 0)
                if self.greeting_frame == 0 and self.greeting_timer == 0:
                    self.greeting_cycles += 1
                    
                # After 2 cycles, stop greeting
                if self.greeting_cycles >= 2:
                    self.is_greeting = False
                    self.speed = self.speed_backup  # Restore movement
                    # Switch to walking animation
                    self.current_frame = 0
                    
                    # Apply post-greeting direction change if specified
                    if self.post_greeting_direction is not None:
                        self.direction = self.post_greeting_direction
                        self.post_greeting_direction = None  # Clear it
                    
                    # Update sprite direction to match movement direction after greeting
                    if self.direction == 1:  # Moving right
                        if not self.flipped:
                            self.frames = [pygame.transform.flip(frame, True, False) for frame in self.original_frames]
                            self.greeting_frames = [pygame.transform.flip(frame, True, False) for frame in self.original_greeting_frames]
                            self.sleeping_frames = [pygame.transform.flip(frame, True, False) for frame in self.original_sleeping_frames]
                            self.flipped = True
                    else:  # Moving left
                        if self.flipped:
                            self.frames = self.original_frames.copy()
                            self.greeting_frames = self.original_greeting_frames.copy()
                            self.sleeping_frames = self.original_sleeping_frames.copy()
                            self.flipped = False
                    
                    self.image = self.frames[self.current_frame]
            return  # Don't do normal updates while greeting
        
        # Update animation frame (normal walking)
        if len(self.frames) > 1:
            self.frame_timer += 1
            if self.frame_timer >= self.frame_delay:
                self.frame_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.image = self.frames[self.current_frame]
        
        # Update direction timer for random direction changes
        self.direction_timer += 1
        
        # Random direction change
        if self.direction_timer >= self.next_direction_change:
            self.direction *= -1  # Flip direction
            self.direction_timer = 0
            self.next_direction_change = random.randint(60, 300)  # Next change in 1-5 seconds
            
            # Flip sprite to match new direction
            if self.direction == 1:  # Moving right
                if not self.flipped:
                    self.frames = [pygame.transform.flip(frame, True, False) for frame in self.original_frames]
                    self.greeting_frames = [pygame.transform.flip(frame, True, False) for frame in self.original_greeting_frames]
                    self.sleeping_frames = [pygame.transform.flip(frame, True, False) for frame in self.original_sleeping_frames]
                    self.image = self.frames[self.current_frame]
                    self.flipped = True
            else:  # Moving left
                if self.flipped:
                    self.frames = self.original_frames.copy()
                    self.greeting_frames = self.original_greeting_frames.copy()
                    self.sleeping_frames = self.original_sleeping_frames.copy()
                    self.image = self.frames[self.current_frame]
                    self.flipped = False
        
        # Move Digimon
        self.rect.x += self.speed * self.direction
        
        # Check boundaries and bounce back (but don't flip sprite here)
        if self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.direction = -1
            # Reset timer for more natural movement after hitting boundary
            self.direction_timer = 0
            self.next_direction_change = random.randint(30, 120)
            
            # Flip sprite to match new direction
            if self.flipped:
                self.frames = self.original_frames.copy()
                self.greeting_frames = self.original_greeting_frames.copy()
                self.sleeping_frames = self.original_sleeping_frames.copy()
                self.image = self.frames[self.current_frame]
                self.flipped = False
                
        elif self.rect.left <= 0:
            self.rect.left = 0
            self.direction = 1
            # Reset timer for more natural movement after hitting boundary
            self.direction_timer = 0
            self.next_direction_change = random.randint(30, 120)
            
            # Flip sprite to match new direction
            if not self.flipped:
                self.frames = [pygame.transform.flip(frame, True, False) for frame in self.original_frames]
                self.greeting_frames = [pygame.transform.flip(frame, True, False) for frame in self.original_greeting_frames]
                self.sleeping_frames = [pygame.transform.flip(frame, True, False) for frame in self.original_sleeping_frames]
                self.image = self.frames[self.current_frame]
                self.flipped = True
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    def check_collision(self, other_digimon):
        """Check if this Digimon collides with another Digimon"""
        return self.rect.colliderect(other_digimon.rect)
    
    def handle_collision(self):
        """Handle collision by reversing direction"""
        self.direction *= -1
        # Reset timer for more natural movement after collision
        self.direction_timer = 0
        self.next_direction_change = random.randint(30, 120)
        
        # Flip sprite to match new direction
        if self.direction == 1:  # Moving right
            if not self.flipped:
                self.frames = [pygame.transform.flip(frame, True, False) for frame in self.original_frames]
                self.greeting_frames = [pygame.transform.flip(frame, True, False) for frame in self.original_greeting_frames]
                self.sleeping_frames = [pygame.transform.flip(frame, True, False) for frame in self.original_sleeping_frames]
                self.image = self.frames[self.current_frame]
                self.flipped = True
        else:  # Moving left
            if self.flipped:
                self.frames = self.original_frames.copy()
                self.greeting_frames = self.original_greeting_frames.copy()
                self.sleeping_frames = self.original_sleeping_frames.copy()
                self.image = self.frames[self.current_frame]
                self.flipped = False

class VPetGame:
    def __init__(self):
        # Check if running on Raspberry Pi
        is_raspberry_pi = self.is_raspberry_pi()
        
        # Hide mouse cursor on Raspberry Pi (touchscreen), show on desktop for development
        if is_raspberry_pi:
            pygame.mouse.set_visible(False)  # Hide cursor on Pi (touchscreen)
            print("Mouse cursor hidden for touchscreen use")
        else:
            pygame.mouse.set_visible(True)   # Show cursor on desktop for development
            print("Mouse cursor visible for desktop development")
        
        if is_raspberry_pi:
            # Force fullscreen mode on Raspberry Pi
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.NOFRAME)
            print("Running on Raspberry Pi - using fullscreen mode")
        else:
            # Set up a windowed mode for desktop testing
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            print("Running on desktop - using windowed mode")
            
        pygame.display.set_caption("Vpet")
        self.clock = pygame.time.Clock()
        
        # Set up asset paths - handle both direct execution and launcher
        if os.path.basename(os.getcwd()) == 'src':
            # Running directly from src directory
            assets_dir = os.path.join(os.path.dirname(os.getcwd()), "assets")
        else:
            # Running from project root (via launcher)
            assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
        
        sprites_dir = os.path.join(assets_dir, "sprites")
        self.background_dir = os.path.join(assets_dir, "background")
        
        # Load all background images and set up cycling
        self.background_files = []
        self.current_background_index = 0
        self.backgrounds = []
        self.load_all_backgrounds()
        
        # Set initial background
        if self.backgrounds:
            self.background = self.backgrounds[0]
        else:
            # Fallback to solid color background
            self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background.fill(BACKGROUND_COLOR)
        
        # Double-tap detection for background changing
        self.last_tap_time = 0
        self.double_tap_delay = 500  # 500ms for double-tap detection
        
        # Create Agumon
        agumon_folder = os.path.join(sprites_dir, "Agumon_dmc")
        self.agumon = Digimon(agumon_folder, speed=2)
        
        # Create Gabumon
        gabumon_folder = os.path.join(sprites_dir, "Gabumon_dmc")
        self.gabumon = Digimon(gabumon_folder, speed=2)  # Same speed as Agumon
        
        # Randomize starting positions ensuring they don't start side by side
        min_distance = 100  # Minimum distance between them
        max_attempts = 10  # Prevent infinite loop
        
        for attempt in range(max_attempts):
            # Random positions within screen bounds (accounting for sprite size)
            agumon_x = random.randint(0, SCREEN_WIDTH - 60)
            gabumon_x = random.randint(0, SCREEN_WIDTH - 60)
            
            # Check if they're far enough apart
            if abs(agumon_x - gabumon_x) >= min_distance:
                break
            
            # If this is the last attempt, force them apart
            if attempt == max_attempts - 1:
                agumon_x = random.randint(0, SCREEN_WIDTH // 2 - 60)
                gabumon_x = random.randint(SCREEN_WIDTH // 2 + min_distance, SCREEN_WIDTH - 60)
        
        # Set the randomized positions
        self.agumon.rect.x = agumon_x
        self.gabumon.rect.x = gabumon_x
        
        # Randomize initial directions
        self.agumon.direction = random.choice([-1, 1])
        self.gabumon.direction = random.choice([-1, 1])
        
        # Set proper sprite directions to match movement
        # Agumon sprite direction
        if self.agumon.direction == -1:  # Moving left
            if self.agumon.flipped:
                self.agumon.frames = self.agumon.original_frames.copy()
                self.agumon.greeting_frames = self.agumon.original_greeting_frames.copy()
                self.agumon.image = self.agumon.frames[self.agumon.current_frame]
                self.agumon.flipped = False
        
        # Gabumon sprite direction  
        if self.gabumon.direction == -1:  # Moving left
            if self.gabumon.flipped:
                self.gabumon.frames = self.gabumon.original_frames.copy()
                self.gabumon.greeting_frames = self.gabumon.original_greeting_frames.copy()
                self.gabumon.image = self.gabumon.frames[self.gabumon.current_frame]
                self.gabumon.flipped = False
        
        self.running = True
    
    def is_raspberry_pi(self):
        """
        Detect if the code is running on a Raspberry Pi.
        Returns True if running on Raspberry Pi, False otherwise.
        """
        try:
            # Check if we're on Linux with ARM architecture
            if platform.system() == 'Linux' and platform.machine().startswith('arm'):
                return True
            
            # Additional check: look for Raspberry Pi specific files
            if os.path.exists('/proc/device-tree/model'):
                with open('/proc/device-tree/model', 'r') as f:
                    model = f.read().lower()
                    if 'raspberry pi' in model:
                        return True
            
            # Check for Raspberry Pi in /proc/cpuinfo (fallback)
            if os.path.exists('/proc/cpuinfo'):
                with open('/proc/cpuinfo', 'r') as f:
                    cpuinfo = f.read().lower()
                    if 'raspberry pi' in cpuinfo or 'bcm' in cpuinfo:
                        return True
                        
        except Exception as e:
            print(f"Error detecting Raspberry Pi: {e}")
            
        return False
    
    def load_all_backgrounds(self):
        """
        Load all background images from the background directory.
        """
        try:
            # Get list of background files
            if os.path.exists(self.background_dir):
                self.background_files = [f for f in os.listdir(self.background_dir) 
                                      if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
                
                # Sort the files for consistent order
                self.background_files.sort()
                
                if self.background_files:
                    # Load all backgrounds
                    for bg_file in self.background_files:
                        bg_path = os.path.join(self.background_dir, bg_file)
                        
                        try:
                            # Load and scale the background
                            background = pygame.image.load(bg_path)
                            background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
                            self.backgrounds.append(background)
                            print(f"Loaded background: {bg_file}")
                        except Exception as e:
                            print(f"Error loading background {bg_file}: {e}")
                    
                    print(f"Loaded {len(self.backgrounds)} backgrounds total")
                else:
                    print("No background images found in background directory")
            else:
                print(f"Background directory not found: {self.background_dir}")
                
        except Exception as e:
            print(f"Error loading backgrounds: {e}")
    
    def load_random_background(self, background_dir):
        """
        Load a random background image from the background directory.
        Returns a pygame Surface with the background.
        """
        try:
            # Get list of background files
            if os.path.exists(background_dir):
                background_files = [f for f in os.listdir(background_dir) 
                                  if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
                
                if background_files:
                    # Randomly select a background
                    selected_bg = random.choice(background_files)
                    bg_path = os.path.join(background_dir, selected_bg)
                    
                    # Load and scale the background
                    background = pygame.image.load(bg_path)
                    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
                    print(f"Loaded random background: {selected_bg}")
                    return background
                else:
                    print("No background images found in background directory")
            else:
                print(f"Background directory not found: {background_dir}")
                
        except Exception as e:
            print(f"Error loading random background: {e}")
        
        # Fallback to solid color background
        print("Using fallback colored background")
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        background.fill(BACKGROUND_COLOR)
        return background
    
    def change_background(self):
        """
        Cycle to the next background image.
        """
        if self.backgrounds:
            # Move to next background (cycle back to 0 if at end)
            self.current_background_index = (self.current_background_index + 1) % len(self.backgrounds)
            self.background = self.backgrounds[self.current_background_index]
            
            # Get the filename for display
            if self.current_background_index < len(self.background_files):
                current_bg_name = self.background_files[self.current_background_index]
                print(f"Background changed to: {current_bg_name} ({self.current_background_index + 1}/{len(self.backgrounds)})")
            else:
                print(f"Background changed to: {self.current_background_index + 1}/{len(self.backgrounds)}")
        else:
            print("No backgrounds available to cycle through")
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_pos = pygame.mouse.get_pos()
                    current_time = pygame.time.get_ticks()
                    
                    # Check if tapped on upper half of screen for background change
                    if mouse_pos[1] < SCREEN_HEIGHT // 2:  # Upper half of screen
                        # Check for double-tap
                        if current_time - self.last_tap_time < self.double_tap_delay:
                            self.change_background()
                            self.last_tap_time = 0  # Reset to prevent triple-tap
                        else:
                            self.last_tap_time = current_time
                    else:
                        # Lower half - check for Digimon interaction
                        # Check if clicked on Agumon
                        if self.agumon.rect.collidepoint(mouse_pos):
                            if self.agumon.is_sleeping:
                                self.agumon.wake_up()
                                print("Clicked on Agumon - waking up!")
                            else:
                                self.agumon.jump()
                                print("Clicked on Agumon - jumping!")
                        # Check if clicked on Gabumon  
                        elif self.gabumon.rect.collidepoint(mouse_pos):
                            if self.gabumon.is_sleeping:
                                self.gabumon.wake_up()
                                print("Clicked on Gabumon - waking up!")
                            else:
                                self.gabumon.jump()
                                print("Clicked on Gabumon - jumping!")
    
    def update(self):
        # Store previous positions
        prev_agumon_x = self.agumon.rect.x
        prev_gabumon_x = self.gabumon.rect.x
        
        # Update both Digimon
        self.agumon.update()
        self.gabumon.update()
        
        # Check for collision between the two Digimon (only if neither is greeting or sleeping)
        if (self.agumon.check_collision(self.gabumon) and 
            not self.agumon.is_greeting and not self.gabumon.is_greeting and
            not self.agumon.is_sleeping and not self.gabumon.is_sleeping):
            
            # Move them back to prevent overlap
            self.agumon.rect.x = prev_agumon_x
            self.gabumon.rect.x = prev_gabumon_x
            
            # Determine which direction each should face to look at each other
            # and which direction they should move after greeting
            if self.agumon.rect.centerx < self.gabumon.rect.centerx:
                # Agumon is on the left, Gabumon on the right
                agumon_face_direction = 1  # Agumon faces right
                gabumon_face_direction = -1  # Gabumon faces left
                # After greeting, they should move away from each other
                agumon_post_direction = -1  # Agumon moves left (away)
                gabumon_post_direction = 1  # Gabumon moves right (away)
            else:
                # Agumon is on the right, Gabumon on the left
                agumon_face_direction = -1  # Agumon faces left
                gabumon_face_direction = 1  # Gabumon faces right
                # After greeting, they should move away from each other
                agumon_post_direction = 1  # Agumon moves right (away)
                gabumon_post_direction = -1  # Gabumon moves left (away)
            
            # Start greeting animation with proper facing directions and post-greeting directions
            self.agumon.start_greeting(agumon_face_direction, agumon_post_direction)
            self.gabumon.start_greeting(gabumon_face_direction, gabumon_post_direction)
            
            # Reset timers for more natural movement after greeting
            self.agumon.direction_timer = 0
            self.gabumon.direction_timer = 0
            self.agumon.next_direction_change = random.randint(30, 120)
            self.gabumon.next_direction_change = random.randint(30, 120)
            
            # Move them slightly apart to prevent getting stuck
            if self.agumon.rect.centerx < self.gabumon.rect.centerx:
                self.agumon.rect.x -= 5
                self.gabumon.rect.x += 5
            else:
                self.agumon.rect.x += 5
                self.gabumon.rect.x -= 5
    
    def draw(self):
        # Draw background image instead of solid color
        self.screen.blit(self.background, (0, 0))
        self.agumon.draw(self.screen)
        self.gabumon.draw(self.screen)
        
        # Ground line exists but is invisible (no drawing)
        # pygame.draw.line(self.screen, (34, 139, 34), 
        #                 (0, SCREEN_HEIGHT - 30), 
        #                 (SCREEN_WIDTH, SCREEN_HEIGHT - 30), 2)
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(10)  # 10 FPS
        
        pygame.quit()
        sys.exit()

def main():
    game = VPetGame()
    game.run()

if __name__ == "__main__":
    main()
