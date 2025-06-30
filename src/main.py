import pygame
import sys
import os
import random
from PIL import Image

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 320
BACKGROUND_COLOR = (135, 206, 235)  # Sky blue
DIGIMON_SPEED = 2

class Digimon:
    def __init__(self, sprite_path, speed=DIGIMON_SPEED):
        self.frames = []
        self.current_frame = 0
        self.frame_timer = 0
        self.frame_delay = 5  # Change frame every 5 game ticks
        self.speed = speed  # Individual speed for each Digimon
        
        # Load the sprite (try GIF first, then static image)
        try:
            if sprite_path.lower().endswith('.gif'):
                # Load animated GIF
                pil_image = Image.open(sprite_path)
                
                # Extract all frames from the GIF
                for frame_num in range(pil_image.n_frames):
                    pil_image.seek(frame_num)
                    frame = pil_image.copy().convert('RGBA')
                    
                    # Convert PIL image to pygame surface
                    mode = frame.mode
                    size = frame.size
                    data = frame.tobytes()
                    
                    pygame_surface = pygame.image.fromstring(data, size, mode)
                    
                    # Scale the frame for the smaller screen
                    if pygame_surface.get_width() > 60 or pygame_surface.get_height() > 60:
                        pygame_surface = pygame.transform.scale(pygame_surface, (50, 50))
                    
                    self.frames.append(pygame_surface)
                
                if not self.frames:
                    raise Exception("No frames found in GIF")
                    
                self.image = self.frames[0]
            else:
                # Load static image
                self.image = pygame.image.load(sprite_path)
                # Scale the sprite for the smaller screen
                sprite_rect = self.image.get_rect()
                if sprite_rect.width > 60 or sprite_rect.height > 60:
                    self.image = pygame.transform.scale(self.image, (50, 50))
                self.frames = [self.image]
                
        except Exception as e:
            print(f"Could not load sprite: {e}")
            # Create a simple colored rectangle as fallback
            self.image = pygame.Surface((40, 40))
            self.image.fill((255, 165, 0))  # Orange color
            self.frames = [self.image]
        
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = SCREEN_HEIGHT - 30 - self.rect.height  # Position on the invisible ground line
        self.direction = 1  # 1 for right, -1 for left
        self.flipped = False
        self.original_frames = self.frames.copy()  # Keep original frames for flipping
        self.direction_timer = 0  # Timer for random direction changes
        self.next_direction_change = random.randint(60, 300)  # Random time between 1-5 seconds at 10fps
        
        # Ensure Digimon starts facing right by flipping if needed
        # Assume the original sprite faces left, so flip it to face right initially
        self.frames = [pygame.transform.flip(frame, True, False) for frame in self.frames]
        self.image = self.frames[self.current_frame]
        self.flipped = True  # Mark as flipped since we're now facing right
    
    def update(self):
        # Update animation frame
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
                    self.image = self.frames[self.current_frame]
                    self.flipped = True
            else:  # Moving left
                if self.flipped:
                    self.frames = self.original_frames.copy()
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
                self.image = self.frames[self.current_frame]
                self.flipped = True
        else:  # Moving left
            if self.flipped:
                self.frames = self.original_frames.copy()
                self.image = self.frames[self.current_frame]
                self.flipped = False

class VPetGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Virtual Pet - Agumon & Gabumon")
        self.clock = pygame.time.Clock()
        
        # Set up asset paths - handle both direct execution and launcher
        if os.path.basename(os.getcwd()) == 'src':
            # Running directly from src directory
            assets_dir = os.path.join(os.path.dirname(os.getcwd()), "assets")
        else:
            # Running from project root (via launcher)
            assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
        
        sprites_dir = os.path.join(assets_dir, "sprites")
        
        # Load background image
        bg_path = os.path.join(assets_dir, "bg1.jpg")
        try:
            self.background = pygame.image.load(bg_path)
            # Scale background to fit screen
            self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
            print(f"Loaded background: {bg_path}")
        except Exception as e:
            print(f"Could not load background {bg_path}: {e}")
            # Create fallback colored background
            self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background.fill(BACKGROUND_COLOR)
        
        # Create Agumon
        agumon_gif_path = os.path.join(sprites_dir, "agumon-walking.gif")
        agumon_png_path = os.path.join(sprites_dir, "The-REAL-Agumon-sprite.png")
        
        if os.path.exists(agumon_gif_path):
            agumon_sprite_path = agumon_gif_path
        elif os.path.exists(agumon_png_path):
            agumon_sprite_path = agumon_png_path
        else:
            agumon_sprite_path = agumon_gif_path  # Will trigger fallback
            print(f"Warning: Could not find Agumon sprites in {sprites_dir}")
        
        self.agumon = Digimon(agumon_sprite_path, speed=2)
        
        # Create Gabumon
        gabumon_gif_path = os.path.join(sprites_dir, "Gabumon-walking.gif")
        gabumon_png_path = os.path.join(sprites_dir, "Gabumon_1.png")
        
        if os.path.exists(gabumon_gif_path):
            gabumon_sprite_path = gabumon_gif_path
        elif os.path.exists(gabumon_png_path):
            gabumon_sprite_path = gabumon_png_path
        else:
            gabumon_sprite_path = gabumon_gif_path  # Will trigger fallback
            print(f"Warning: Could not find Gabumon sprites in {sprites_dir}")
        
        self.gabumon = Digimon(gabumon_sprite_path, speed=2)  # Same speed as Agumon
        
        # Position them differently so they don't overlap
        self.agumon.rect.x = 50  # Start Agumon a bit to the right
        self.gabumon.rect.x = 200  # Start Gabumon further right
        
        # Give them different initial directions for variety
        self.gabumon.direction = -1  # Start Gabumon moving left
        if self.gabumon.flipped:
            self.gabumon.frames = self.gabumon.original_frames.copy()
            self.gabumon.image = self.gabumon.frames[self.gabumon.current_frame]
            self.gabumon.flipped = False
        
        self.running = True
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def update(self):
        # Store previous positions
        prev_agumon_x = self.agumon.rect.x
        prev_gabumon_x = self.gabumon.rect.x
        
        # Update both Digimon
        self.agumon.update()
        self.gabumon.update()
        
        # Check for collision between the two Digimon
        if self.agumon.check_collision(self.gabumon):
            # Move them back to prevent overlap
            self.agumon.rect.x = prev_agumon_x
            self.gabumon.rect.x = prev_gabumon_x
            
            # Both change direction
            self.agumon.handle_collision()
            self.gabumon.handle_collision()
            
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
