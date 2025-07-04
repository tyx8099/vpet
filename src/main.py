import pygame
import sys
import os
import random
import platform
import time
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 320
BACKGROUND_COLOR = (135, 206, 235)  # Sky blue
DIGIMON_SPEED = 2

# Heart emotion constants
HEART_DISPLAY_DURATION = 1000  # 1 second in milliseconds
HEART_FLOAT_SPEED = 1  # Pixels per frame heart floats upward

# Food constants
FOOD_FALL_SPEED = 3  # Pixels per frame food falls
FOOD_LIFETIME = 10000  # 10 seconds in milliseconds before food disappears
FOOD_SIZE = (30, 30)  # Size to scale meat to

class Food:
    def __init__(self, x, y, food_image):
        self.image = food_image
        # Use the actual image size instead of hardcoded FOOD_SIZE
        image_width = food_image.get_width()
        image_height = food_image.get_height()
        self.rect = pygame.Rect(x - image_width//2, y, image_width, image_height)
        self.fall_velocity = FOOD_FALL_SPEED
        self.creation_time = pygame.time.get_ticks()
        self.ground_y = SCREEN_HEIGHT - 30 - image_height  # Same ground level as Digimon
        self.on_ground = False
        self.consumed = False  # Flag to mark when food has been eaten
        self.claimed_by = None  # Which Digimon has claimed this food (None if unclaimed)
    
    def update(self):
        """Update food falling and lifetime"""
        current_time = pygame.time.get_ticks()
        
        # Check if food has been consumed
        if self.consumed:
            return False  # Food should be removed
        
        # Check if food should disappear (lifetime expired)
        if current_time - self.creation_time > FOOD_LIFETIME:
            return False  # Food should be removed
        
        # Fall down if not on ground
        if not self.on_ground:
            self.rect.y += self.fall_velocity
            
            # Check if hit the ground
            if self.rect.y >= self.ground_y:
                self.rect.y = self.ground_y
                self.on_ground = True
                print("Sushi landed on ground!")
        
        return True  # Food should stay
    
    def draw(self, screen):
        """Draw the food item"""
        screen.blit(self.image, self.rect)
    
    def check_collision_with_digimon(self, digimon):
        """Check if Digimon collides with this food"""
        return self.rect.colliderect(digimon.rect)

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
        
        # Heart emotion state
        self.heart_visible = False
        self.heart_start_time = 0
        self.heart_float_offset = 0
        self.heart_image = None
        
        # Feeding animation state
        self.is_feeding = False
        self.feeding_timer = 0
        self.feeding_frame = 0
        self.feeding_frames = []  # Will store frames 5 and 6 for feeding
        self.feeding_cycles = 0
        self.target_food = None  # Food item the Digimon is moving towards
        self.moving_to_food = False
        self.eating_position_reached = False
        
        # Hunger system
        self.hunger = 100  # Start with full hunger (0-100)
        self.hunger_decrease_rate = 0.05  # Hunger decreases by 0.05 per game tick
        self.hunger_timer = 0
        self.last_fed_time = 0
        
        # Load heart emotion from emotion folder
        emotion_dir = os.path.join(os.path.dirname(sprite_folder), "emotion")
        heart_path = os.path.join(emotion_dir, "heart.png")
        
        try:
            if os.path.exists(heart_path):
                self.heart_image = pygame.image.load(heart_path)
                # Scale heart to appropriate size (smaller than Digimon)
                if self.heart_image.get_width() > 30 or self.heart_image.get_height() > 30:
                    self.heart_image = pygame.transform.scale(self.heart_image, (25, 25))
                print(f"Loaded heart emotion: {heart_path}")
            else:
                print(f"Heart emotion not found: {heart_path}")
        except Exception as e:
            print(f"Could not load heart emotion: {e}")
            self.heart_image = None
        
        # Load walking animation frames (0.png and 1.png), greeting frames (2.png), sleeping frames (11.png and 12.png), and feeding frames (5.png and 6.png)
        try:
            # Load frame 0 and frame 1 for walking animation
            frame_0_path = os.path.join(sprite_folder, "0.png")
            frame_1_path = os.path.join(sprite_folder, "1.png")
            frame_2_path = os.path.join(sprite_folder, "2.png")
            frame_5_path = os.path.join(sprite_folder, "5.png")
            frame_6_path = os.path.join(sprite_folder, "6.png")
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
                
                # Load feeding frames (5 and 6)
                if os.path.exists(frame_5_path) and os.path.exists(frame_6_path):
                    frame_5 = pygame.image.load(frame_5_path)
                    frame_6 = pygame.image.load(frame_6_path)
                    if frame_5.get_width() > 60 or frame_5.get_height() > 60:
                        frame_5 = pygame.transform.scale(frame_5, (50, 50))
                    if frame_6.get_width() > 60 or frame_6.get_height() > 60:
                        frame_6 = pygame.transform.scale(frame_6, (50, 50))
                    self.feeding_frames = [frame_5, frame_6]  # 5 -> 6 -> 5 -> 6
                else:
                    # Fallback: use walking frames for feeding
                    self.feeding_frames = [frame_1, frame_0]
                    
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
        self.original_feeding_frames = self.feeding_frames.copy()  # Keep original feeding frames
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
            self.feeding_frames = [pygame.transform.flip(frame, True, False) for frame in self.feeding_frames]
            self.image = self.frames[self.current_frame]
            self.flipped = True  # Mark as flipped since we're now facing right
    
    def start_greeting(self, face_direction=None, post_greeting_direction=None):
        """Start the greeting animation
        Args:
            face_direction: 1 for right, -1 for left (direction to face during greeting)
            post_greeting_direction: 1 for right, -1 for left (direction to move after greeting)
        """
        # Don't start greeting if already engaged in other activities
        if self.is_feeding or self.moving_to_food or self.is_sleeping or self.is_greeting:
            return
            
        self.is_greeting = True
        self.greeting_timer = 0
        self.greeting_frame = 0
        self.greeting_cycles = 0
        # Stop moving while greeting
        # If the Digimon was feeding (has original_speed stored), use that instead of current speed
        if hasattr(self, 'original_speed') and self.speed == 0:
            self.speed_backup = self.original_speed
        else:
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
                    self.feeding_frames = [pygame.transform.flip(frame, True, False) for frame in self.original_feeding_frames]
                    self.flipped = True
            else:  # Face left
                if self.flipped:
                    self.frames = self.original_frames.copy()
                    self.greeting_frames = self.original_greeting_frames.copy()
                    self.sleeping_frames = self.original_sleeping_frames.copy()
                    self.feeding_frames = self.original_feeding_frames.copy()
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
                self.feeding_frames = [pygame.transform.flip(frame, True, False) for frame in self.original_feeding_frames]
                self.flipped = True
                print(f"Digimon woke up and will walk right!")
            else:  # Moving left
                # Use original sprites (facing left)
                self.frames = self.original_frames.copy()
                self.greeting_frames = self.original_greeting_frames.copy()
                self.sleeping_frames = self.original_sleeping_frames.copy()
                self.feeding_frames = self.original_feeding_frames.copy()
                self.flipped = False
                print(f"Digimon woke up and will walk left!")
            
            self.image = self.frames[self.current_frame]
            self.show_heart()  # Show heart when waking up
    
    def jump(self):
        """Make the Digimon jump (only if awake and not already jumping)"""
        if not self.is_sleeping and not self.is_jumping and not self.is_greeting and not self.is_feeding and not self.moving_to_food:
            self.is_jumping = True
            self.jump_velocity = self.jump_strength
            self.show_heart()  # Show heart when jumping
            print(f"Digimon jumped!")
    
    def show_heart(self):
        """Show heart emotion above Digimon's head"""
        if self.heart_image:
            self.heart_visible = True
            self.heart_start_time = pygame.time.get_ticks()
            self.heart_float_offset = 0
            print("💖 Digimon shows love!")
    
    def feed(self, food_value=20):
        """Feed the Digimon - increases hunger, shows heart, and plays feeding animation"""
        self.hunger = min(100, self.hunger + food_value)
        self.last_fed_time = pygame.time.get_ticks()
        self.show_heart()
        
        # Start feeding animation
        self.is_feeding = True
        self.feeding_timer = 0
        self.feeding_frame = 0
        self.feeding_cycles = 0
        
        print(f"Digimon fed! Hunger: {self.hunger}/100")
    
    def move_to_food(self, food_item):
        """Make the Digimon move towards a food item"""
        if not self.is_sleeping and not self.is_greeting and not self.is_feeding:
            # Check if food is already claimed by another Digimon
            if food_item.claimed_by is not None and food_item.claimed_by != self:
                print(f"Sushi already claimed by another Digimon!")
                return False  # Cannot claim this food
            
            # Claim the food for this Digimon
            food_item.claimed_by = self
            self.target_food = food_item
            self.moving_to_food = True
            self.eating_position_reached = False
            
            # Determine direction to face the food
            if food_item.rect.centerx > self.rect.centerx:
                self.direction = 1  # Move right towards food
            else:
                self.direction = -1  # Move left towards food
            
            # Update sprite direction immediately
            if self.direction == 1:  # Moving right
                if not self.flipped:
                    self.frames = [pygame.transform.flip(frame, True, False) for frame in self.original_frames]
                    self.greeting_frames = [pygame.transform.flip(frame, True, False) for frame in self.original_greeting_frames]
                    self.sleeping_frames = [pygame.transform.flip(frame, True, False) for frame in self.original_sleeping_frames]
                    self.feeding_frames = [pygame.transform.flip(frame, True, False) for frame in self.original_feeding_frames]
                    self.flipped = True
            else:  # Moving left
                if self.flipped:
                    self.frames = self.original_frames.copy()
                    self.greeting_frames = self.original_greeting_frames.copy()
                    self.sleeping_frames = self.original_sleeping_frames.copy()
                    self.feeding_frames = self.original_feeding_frames.copy()
                    self.flipped = False
            
            self.image = self.frames[self.current_frame]
            print(f"Digimon claimed and moving towards sushi at ({food_item.rect.centerx}, {food_item.rect.centery})")
            return True  # Successfully claimed the food
    
    def stop_moving_to_food(self):
        """Stop moving towards food and unclaim it"""
        if self.target_food and self.moving_to_food:
            # Unclaim the food so another Digimon can target it
            if self.target_food.claimed_by == self:
                self.target_food.claimed_by = None
                print(f"Digimon unclaimed sushi (stopped moving)")
        
        self.moving_to_food = False
        self.target_food = None
    
    def check_eating_position(self):
        """Check if Digimon is close enough to food to start eating"""
        if self.target_food and self.moving_to_food:
            distance = abs(self.rect.centerx - self.target_food.rect.centerx)
            if distance <= 35:  # Close enough to eat (food is 30px wide + 5px margin)
                self.eating_position_reached = True
                self.moving_to_food = False
                self.start_eating()
                return True
        return False
    
    def start_eating(self):
        """Start the eating animation for two chews (5→6→5→6→5)"""
        if not self.is_feeding:
            self.is_feeding = True
            self.feeding_timer = 0
            self.feeding_frame = 0  # Start with frame 0 (5.png)
            self.feeding_frame_count = 0  # Track total frame transitions
            
            # Store original speed and stop moving while eating
            self.original_speed = self.speed
            self.speed = 0
            
            print("Digimon started eating animation - will chew twice (56565 sequence)")
    
    def update(self):
        # Update hunger system
        self.hunger_timer += 1
        if self.hunger_timer >= 60:  # Every 6 seconds at 10 FPS
            self.hunger = max(0, self.hunger - self.hunger_decrease_rate * 60)
            self.hunger_timer = 0
            if self.hunger <= 0:
                print(f"Digimon is very hungry!")
        
        # Update heart emotion animation
        if self.heart_visible:
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - self.heart_start_time
            
            if elapsed_time >= HEART_DISPLAY_DURATION:
                # Heart animation finished
                self.heart_visible = False
                self.heart_float_offset = 0
            else:
                # Update heart floating animation
                self.heart_float_offset += HEART_FLOAT_SPEED
        
        # Handle feeding animation
        if self.is_feeding:
            self.feeding_timer += 1
            
            # Animate feeding frames for two complete chews (5→6→5→6→5)
            if len(self.feeding_frames) > 1 and self.feeding_timer % self.frame_delay == 0:
                # Initialize frame counter if not exists
                if not hasattr(self, 'feeding_frame_count'):
                    self.feeding_frame_count = 0
                
                self.feeding_frame_count += 1
                
                # Define the chewing sequence: 5→6→5→6→5 (2 complete chews)
                chew_sequence = [0, 1, 0, 1, 0]  # Frame indices (0=5.png, 1=6.png)
                
                if self.feeding_frame_count <= len(chew_sequence):
                    # Set the frame according to the sequence
                    self.feeding_frame = chew_sequence[self.feeding_frame_count - 1]
                    self.image = self.feeding_frames[self.feeding_frame]
                    print(f"Chew frame {self.feeding_frame_count}: {self.feeding_frame} ({'5.png' if self.feeding_frame == 0 else '6.png'})")                    # After completing the sequence (5 frames = 2 chews)
                if self.feeding_frame_count >= len(chew_sequence):
                    print(f"Feeding completed! Two chews finished (56565 sequence)")
                    self.is_feeding = False
                    self.feeding_timer = 0
                    self.feeding_frame = 0
                    self.feeding_frame_count = 0
                    self.eating_position_reached = False
                    
                    # Restore original movement speed
                    self.speed = self.original_speed
                    
                    # Increase hunger when eating finishes
                    self.hunger = min(100, self.hunger + 20)
                    self.show_heart()
                    
                    # Mark food for removal
                    if self.target_food:
                        self.target_food.consumed = True
                        self.target_food = None
                    
                    # Return to normal walking frame
                    self.current_frame = 0
                    self.image = self.frames[self.current_frame]
                    print("Eating completed! Sushi consumed. Resuming normal movement.")
            
            return  # Don't do normal updates while feeding
        
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
                            self.feeding_frames = [pygame.transform.flip(frame, True, False) for frame in self.original_feeding_frames]
                            self.flipped = True
                    else:  # Moving left
                        if self.flipped:
                            self.frames = self.original_frames.copy()
                            self.greeting_frames = self.original_greeting_frames.copy()
                            self.sleeping_frames = self.original_sleeping_frames.copy()
                            self.feeding_frames = self.original_feeding_frames.copy()
                            self.flipped = False
                    
                    self.image = self.frames[self.current_frame]
            return  # Don't do normal updates while greeting
        
        # Handle movement towards food
        if self.moving_to_food and self.target_food:
            # Check if we've reached eating position
            if self.check_eating_position():
                return  # Start eating, don't continue with normal movement
            
            # Continue moving towards food with boundary checking
            new_x = self.rect.x + self.speed * self.direction
            
            # Check boundaries before moving
            if new_x < 0:
                self.rect.x = 0
                # Stop moving towards food if we hit a boundary
                self.stop_moving_to_food()
                self.direction = 1  # Face right
            elif new_x + self.rect.width > SCREEN_WIDTH:
                self.rect.x = SCREEN_WIDTH - self.rect.width
                # Stop moving towards food if we hit a boundary
                self.stop_moving_to_food()
                self.direction = -1  # Face left
            else:
                self.rect.x = new_x
            
            # Update walking animation while moving to food
            if len(self.frames) > 1:
                self.frame_timer += 1
                if self.frame_timer >= self.frame_delay:
                    self.frame_timer = 0
                    self.current_frame = (self.current_frame + 1) % len(self.frames)
                    self.image = self.frames[self.current_frame]
            
            return  # Don't do normal updates while moving to food
        
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
                    self.feeding_frames = [pygame.transform.flip(frame, True, False) for frame in self.original_feeding_frames]
                    self.image = self.frames[self.current_frame]
                    self.flipped = True
            else:  # Moving left
                if self.flipped:
                    self.frames = self.original_frames.copy()
                    self.greeting_frames = self.original_greeting_frames.copy()
                    self.sleeping_frames = self.original_sleeping_frames.copy()
                    self.feeding_frames = self.original_feeding_frames.copy()
                    self.image = self.frames[self.current_frame]
                    self.flipped = False
        
        # Move Digimon
        self.rect.x += self.speed * self.direction
        
        # Check boundaries and bounce back with proper sprite flipping
        # Force direction change when hitting boundaries to prevent getting stuck
        if self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH - 1  # Clamp to boundary
            self.direction = -1  # Always force left direction
            # Reset timer for more natural movement after hitting boundary
            self.direction_timer = 0
            self.next_direction_change = random.randint(30, 120)
            
            # Always face left when hitting right boundary
            self.frames = self.original_frames.copy()
            self.greeting_frames = self.original_greeting_frames.copy()
            self.sleeping_frames = self.original_sleeping_frames.copy()
            self.feeding_frames = self.original_feeding_frames.copy()
            self.image = self.frames[self.current_frame]
            self.flipped = False
            print("Hit right boundary - forced direction left")
                
        elif self.rect.left <= 0:
            self.rect.left = 1  # Clamp to boundary
            self.direction = 1  # Always force right direction
            # Reset timer for more natural movement after hitting boundary
            self.direction_timer = 0
            self.next_direction_change = random.randint(30, 120)
            
            # Always face right when hitting left boundary
            self.frames = [pygame.transform.flip(frame, True, False) for frame in self.original_frames]
            self.greeting_frames = [pygame.transform.flip(frame, True, False) for frame in self.original_greeting_frames]
            self.sleeping_frames = [pygame.transform.flip(frame, True, False) for frame in self.original_sleeping_frames]
            self.feeding_frames = [pygame.transform.flip(frame, True, False) for frame in self.original_feeding_frames]
            self.image = self.frames[self.current_frame]
            self.flipped = True
            print("Hit left boundary - forced direction right")
    
    def draw(self, screen):
        # Safety check: Ensure Digimon is always within screen bounds
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - self.rect.height))
        
        screen.blit(self.image, self.rect)
        
        # Draw heart emotion if active
        if self.heart_visible and self.heart_image:
            # Position heart 10 pixels above Digimon's head
            heart_x = self.rect.centerx - self.heart_image.get_width() // 2
            heart_y = self.rect.top - 20 - self.heart_float_offset
            
            # Add gentle swaying animation
            sway_offset = int(2 * math.sin(pygame.time.get_ticks() * 0.005))
            heart_x += sway_offset
            
            # Draw heart with slight transparency fade effect
            elapsed_time = pygame.time.get_ticks() - self.heart_start_time
            if elapsed_time > HEART_DISPLAY_DURATION * 0.7:  # Start fading in last 30% of duration
                fade_progress = (elapsed_time - HEART_DISPLAY_DURATION * 0.7) / (HEART_DISPLAY_DURATION * 0.3)
                alpha = int(255 * (1 - fade_progress))
                heart_surface = self.heart_image.copy()
                heart_surface.set_alpha(alpha)
                screen.blit(heart_surface, (heart_x, heart_y))
            else:
                screen.blit(self.heart_image, (heart_x, heart_y))
    
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
                self.feeding_frames = [pygame.transform.flip(frame, True, False) for frame in self.original_feeding_frames]
                self.image = self.frames[self.current_frame]
                self.flipped = True
        else:  # Moving left
            if self.flipped:
                self.frames = self.original_frames.copy()
                self.greeting_frames = self.original_greeting_frames.copy()
                self.sleeping_frames = self.original_sleeping_frames.copy()
                self.feeding_frames = self.original_feeding_frames.copy()
                self.image = self.frames[self.current_frame]
                self.flipped = False

class VPetGame:
    def __init__(self):
        # Check if running on Raspberry Pi
        self.is_raspberry_pi_device = self.is_raspberry_pi()
        
        # Always show mouse cursor initially on all platforms
        pygame.mouse.set_visible(True)
        print("Mouse cursor visible - will auto-hide after 2 seconds of inactivity")
        
        if self.is_raspberry_pi_device:
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
        food_dir = os.path.join(assets_dir, "food")
        
        # Load food assets
        self.sushi_image = None
        sushi_path = os.path.join(food_dir, "sushi.png")
        try:
            if os.path.exists(sushi_path):
                self.sushi_image = pygame.image.load(sushi_path)
                print(f"Loaded sushi image: {sushi_path}")
            else:
                print(f"Sushi image not found: {sushi_path}")
        except Exception as e:
            print(f"Could not load sushi image: {e}")
        
        # Food management
        self.food_items = []  # List to store dropped food items
        
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
        
        # Auto-hide mouse cursor after inactivity
        self.last_mouse_move_time = pygame.time.get_ticks()
        self.mouse_hide_delay = 1000  # 1s in milliseconds
        self.cursor_visible = True  # Always start with cursor visible on all platforms
        self.last_mouse_pos = pygame.mouse.get_pos()
        
        # Get list of available Digimon
        available_digimon = []
        if os.path.exists(sprites_dir):
            for folder in os.listdir(sprites_dir):
                if folder.endswith("_dmc") and os.path.isdir(os.path.join(sprites_dir, folder)):
                    available_digimon.append(folder)
        
        if len(available_digimon) < 2:
            # Fallback to original if not enough Digimon found
            available_digimon = ["Agumon_dmc", "Gabumon_dmc"]
        
        # Randomly select 2 different Digimon
        selected_digimon = random.sample(available_digimon, 2)
        
        # Create first Digimon
        digimon1_folder = os.path.join(sprites_dir, selected_digimon[0])
        self.digimon1 = Digimon(digimon1_folder, speed=2)
        self.digimon1_name = selected_digimon[0].replace("_dmc", "")
        
        # Create second Digimon
        digimon2_folder = os.path.join(sprites_dir, selected_digimon[1])
        self.digimon2 = Digimon(digimon2_folder, speed=2)
        self.digimon2_name = selected_digimon[1].replace("_dmc", "")
        
        print(f"Game started with {self.digimon1_name} and {self.digimon2_name}!")
        
        # Randomize starting positions ensuring they don't start side by side
        min_distance = 100  # Minimum distance between them
        max_attempts = 10  # Prevent infinite loop
        
        for attempt in range(max_attempts):
            # Random positions within screen bounds (accounting for sprite size)
            digimon1_x = random.randint(0, SCREEN_WIDTH - 60)
            digimon2_x = random.randint(0, SCREEN_WIDTH - 60)
            
            # Check if they're far enough apart
            if abs(digimon1_x - digimon2_x) >= min_distance:
                break
            
            # If this is the last attempt, force them apart
            if attempt == max_attempts - 1:
                digimon1_x = random.randint(0, SCREEN_WIDTH // 2 - 60)
                digimon2_x = random.randint(SCREEN_WIDTH // 2 + min_distance, SCREEN_WIDTH - 60)
        
        # Set the randomized positions
        self.digimon1.rect.x = digimon1_x
        self.digimon2.rect.x = digimon2_x
        
        # Randomize initial directions
        self.digimon1.direction = random.choice([-1, 1])
        self.digimon2.direction = random.choice([-1, 1])
        
        # Set proper sprite directions to match movement
        # Digimon1 sprite direction
        if self.digimon1.direction == -1:  # Moving left
            if self.digimon1.flipped:
                self.digimon1.frames = self.digimon1.original_frames.copy()
                self.digimon1.greeting_frames = self.digimon1.original_greeting_frames.copy()
                self.digimon1.image = self.digimon1.frames[self.digimon1.current_frame]
                self.digimon1.flipped = False
        
        # Digimon2 sprite direction  
        if self.digimon2.direction == -1:  # Moving left
            if self.digimon2.flipped:
                self.digimon2.frames = self.digimon2.original_frames.copy()
                self.digimon2.greeting_frames = self.digimon2.original_greeting_frames.copy()
                self.digimon2.image = self.digimon2.frames[self.digimon2.current_frame]
                self.digimon2.flipped = False
        
        # Load sushi food image  
        food_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "food")
        sushi_path = os.path.join(food_dir, "sushi.png")
        
        try:
            if os.path.exists(sushi_path):
                self.food_image = pygame.image.load(sushi_path)
                print(f"Loaded sushi image: {sushi_path}")
            else:
                print(f"Sushi image not found: {sushi_path}")
        except Exception as e:
            print(f"Could not load sushi image: {e}")
            self.food_image = None
        
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
    
    def drop_food(self, x, y):
        """Drop a piece of sushi at the specified coordinates"""
        if self.sushi_image:
            food = Food(x, y, self.sushi_image)
            self.food_items.append(food)
            print(f"Dropped sushi at ({x}, {y})")
        else:
            print("No sushi image available to drop!")
    
    def handle_events(self):
        current_time = pygame.time.get_ticks()
        current_mouse_pos = pygame.mouse.get_pos()
        
        # Check for mouse movement to show/hide cursor
        if current_mouse_pos != self.last_mouse_pos:
            self.last_mouse_pos = current_mouse_pos
            self.last_mouse_move_time = current_time
            
            # Show cursor when mouse moves
            if not self.cursor_visible:
                pygame.mouse.set_visible(True)
                self.cursor_visible = True
        
        # Auto-hide cursor after inactivity on all platforms
        if self.cursor_visible:
            if current_time - self.last_mouse_move_time > self.mouse_hide_delay:
                pygame.mouse.set_visible(False)
                self.cursor_visible = False
        
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
                        # Lower half - check for Digimon interaction or food dropping
                        digimon_clicked = False
                        
                        # Check if clicked on first Digimon
                        if self.digimon1.rect.collidepoint(mouse_pos):
                            digimon_clicked = True
                            if self.digimon1.is_sleeping:
                                self.digimon1.wake_up()
                                print(f"Clicked on {self.digimon1_name} - waking up!")
                            else:
                                self.digimon1.jump()
                                print(f"Clicked on {self.digimon1_name} - jumping!")
                        # Check if clicked on second Digimon  
                        elif self.digimon2.rect.collidepoint(mouse_pos):
                            digimon_clicked = True
                            if self.digimon2.is_sleeping:
                                self.digimon2.wake_up()
                                print(f"Clicked on {self.digimon2_name} - waking up!")
                            else:
                                self.digimon2.jump()
                                print(f"Clicked on {self.digimon2_name} - jumping!")
                        
                        # If didn't click on Digimon, drop food
                        if not digimon_clicked and self.sushi_image:
                            self.drop_food(mouse_pos[0], mouse_pos[1])
    
    def update(self):
        # Store previous positions
        prev_digimon1_x = self.digimon1.rect.x
        prev_digimon2_x = self.digimon2.rect.x
        
        # Update both Digimon
        self.digimon1.update()
        self.digimon2.update()
        
        # Update food items and handle Digimon interactions
        active_food = []
        for food in self.food_items:
            if food.update():  # Food returns True if it should stay
                # Check if food is on ground and if any Digimon should move towards it
                if food.on_ground and not food.consumed and food.claimed_by is None:
                    # Check if either Digimon is available to move towards food
                    digimon1_available = (not self.digimon1.is_sleeping and not self.digimon1.is_greeting 
                                        and not self.digimon1.is_feeding and not self.digimon1.moving_to_food)
                    digimon2_available = (not self.digimon2.is_sleeping and not self.digimon2.is_greeting 
                                        and not self.digimon2.is_feeding and not self.digimon2.moving_to_food)
                    
                    # Find which Digimon is closer to the food
                    if digimon1_available or digimon2_available:
                        dist1 = abs(self.digimon1.rect.centerx - food.rect.centerx) if digimon1_available else float('inf')
                        dist2 = abs(self.digimon2.rect.centerx - food.rect.centerx) if digimon2_available else float('inf')
                        
                        # Make the closer available Digimon move towards food
                        if dist1 <= dist2 and digimon1_available and dist1 <= 150:  # Only if within reasonable distance
                            self.digimon1.move_to_food(food)
                        elif digimon2_available and dist2 <= 150:  # Only if within reasonable distance
                            self.digimon2.move_to_food(food)
                
                active_food.append(food)  # Keep this food
            # If food.update() returns False, food is removed (lifetime expired or consumed)
        
        self.food_items = active_food
        
        # Check for collision between the two Digimon (only if neither is greeting, sleeping, feeding, or moving to food)
        if (self.digimon1.check_collision(self.digimon2) and 
            not self.digimon1.is_greeting and not self.digimon2.is_greeting and
            not self.digimon1.is_sleeping and not self.digimon2.is_sleeping and
            not self.digimon1.is_feeding and not self.digimon2.is_feeding and
            not self.digimon1.moving_to_food and not self.digimon2.moving_to_food):
            
            # Move them back to prevent overlap
            self.digimon1.rect.x = prev_digimon1_x
            self.digimon2.rect.x = prev_digimon2_x
            
            # Determine which direction each should face to look at each other
            # and which direction they should move after greeting
            if self.digimon1.rect.centerx < self.digimon2.rect.centerx:
                # Digimon1 is on the left, Digimon2 on the right
                digimon1_face_direction = 1  # Digimon1 faces right
                digimon2_face_direction = -1  # Digimon2 faces left
                # After greeting, they should move away from each other
                digimon1_post_direction = -1  # Digimon1 moves left (away)
                digimon2_post_direction = 1  # Digimon2 moves right (away)
            else:
                # Digimon1 is on the right, Digimon2 on the left
                digimon1_face_direction = -1  # Digimon1 faces left
                digimon2_face_direction = 1  # Digimon2 faces right
                # After greeting, they should move away from each other
                digimon1_post_direction = 1  # Digimon1 moves right (away)
                digimon2_post_direction = -1  # Digimon2 moves left (away)
            
            # Start greeting animation with proper facing directions and post-greeting directions
            self.digimon1.start_greeting(digimon1_face_direction, digimon1_post_direction)
            self.digimon2.start_greeting(digimon2_face_direction, digimon2_post_direction)
            
            # Reset timers for more natural movement after greeting
            self.digimon1.direction_timer = 0
            self.digimon2.direction_timer = 0
            self.digimon1.next_direction_change = random.randint(30, 120)
            self.digimon2.next_direction_change = random.randint(30, 120)
            
            # Move them slightly apart to prevent getting stuck
            if self.digimon1.rect.centerx < self.digimon2.rect.centerx:
                self.digimon1.rect.x -= 5
                self.digimon2.rect.x += 5
            else:
                self.digimon1.rect.x += 5
                self.digimon2.rect.x -= 5
    
    def draw(self):
        # Draw background image instead of solid color
        self.screen.blit(self.background, (0, 0))
        self.digimon1.draw(self.screen)
        self.digimon2.draw(self.screen)
        
        # Draw all active food items
        for food in self.food_items:
            food.draw(self.screen)
        
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
