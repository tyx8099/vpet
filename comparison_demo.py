import pygame
import sys
import os
import random
from PIL import Image

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 960  # Double width for side-by-side comparison
SCREEN_HEIGHT = 320
BACKGROUND_COLOR = (135, 206, 235)  # Sky blue
DIGIMON_SPEED = 2

class DigimonGIF:
    """Original GIF-based Digimon class"""
    def __init__(self, sprite_path, speed=DIGIMON_SPEED, x_offset=0):
        self.frames = []
        self.current_frame = 0
        self.frame_timer = 0
        self.frame_delay = 5  # Change frame every 5 game ticks
        self.speed = speed
        self.x_offset = x_offset  # Offset for side-by-side display
        
        # Load the sprite (GIF)
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
                raise Exception("Not a GIF file")
                
        except Exception as e:
            print(f"Could not load GIF sprite: {e}")
            # Create a simple colored rectangle as fallback
            self.image = pygame.Surface((40, 40))
            self.image.fill((255, 0, 0))  # Red color for GIF fallback
            self.frames = [self.image]
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x_offset
        self.rect.y = SCREEN_HEIGHT - 30 - self.rect.height
        self.direction = 1
        self.flipped = False
        self.original_frames = self.frames.copy()
        self.direction_timer = 0
        self.next_direction_change = random.randint(60, 300)
        
        # Start facing right
        self.frames = [pygame.transform.flip(frame, True, False) for frame in self.frames]
        self.image = self.frames[self.current_frame]
        self.flipped = True
    
    def update(self):
        # Update animation frame
        if len(self.frames) > 1:
            self.frame_timer += 1
            if self.frame_timer >= self.frame_delay:
                self.frame_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.image = self.frames[self.current_frame]
        
        # Update direction timer
        self.direction_timer += 1
        
        # Random direction change
        if self.direction_timer >= self.next_direction_change:
            self.direction *= -1
            self.direction_timer = 0
            self.next_direction_change = random.randint(60, 300)
            
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
        
        # Move Digimon (constrained to left half of screen)
        self.rect.x += self.speed * self.direction
        
        # Check boundaries (left half only)
        if self.rect.right >= SCREEN_WIDTH // 2:
            self.rect.right = SCREEN_WIDTH // 2
            self.direction = -1
            self.direction_timer = 0
            self.next_direction_change = random.randint(30, 120)
            
            if self.flipped:
                self.frames = self.original_frames.copy()
                self.image = self.frames[self.current_frame]
                self.flipped = False
                
        elif self.rect.left <= self.x_offset:
            self.rect.left = self.x_offset
            self.direction = 1
            self.direction_timer = 0
            self.next_direction_change = random.randint(30, 120)
            
            if not self.flipped:
                self.frames = [pygame.transform.flip(frame, True, False) for frame in self.original_frames]
                self.image = self.frames[self.current_frame]
                self.flipped = True
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

class DigimonPNG:
    """New PNG-based Digimon class"""
    def __init__(self, sprite_folder, speed=DIGIMON_SPEED, x_offset=0):
        self.frames = []
        self.current_frame = 0
        self.frame_timer = 0
        self.frame_delay = 5  # Change frame every 5 game ticks (0.5 seconds at 10 FPS)
        self.speed = speed
        self.x_offset = x_offset  # Offset for side-by-side display
        
        # Load walking animation frames (0.png and 1.png)
        try:
            frame_0_path = os.path.join(sprite_folder, "0.png")
            frame_1_path = os.path.join(sprite_folder, "1.png")
            
            if os.path.exists(frame_0_path) and os.path.exists(frame_1_path):
                frame_0 = pygame.image.load(frame_0_path)
                frame_1 = pygame.image.load(frame_1_path)
                
                # Scale the frames
                if frame_0.get_width() > 60 or frame_0.get_height() > 60:
                    frame_0 = pygame.transform.scale(frame_0, (50, 50))
                if frame_1.get_width() > 60 or frame_1.get_height() > 60:
                    frame_1 = pygame.transform.scale(frame_1, (50, 50))
                
                self.frames = [frame_0, frame_1]
                self.image = self.frames[0]
            else:
                raise Exception(f"Walking frames not found: {frame_0_path} or {frame_1_path}")
                
        except Exception as e:
            print(f"Could not load PNG sprite: {e}")
            # Create a simple colored rectangle as fallback
            self.image = pygame.Surface((40, 40))
            self.image.fill((0, 255, 0))  # Green color for PNG fallback
            self.frames = [self.image]
        
        self.rect = self.image.get_rect()
        self.rect.x = self.x_offset + SCREEN_WIDTH // 2  # Start in right half
        self.rect.y = SCREEN_HEIGHT - 30 - self.rect.height
        self.direction = 1
        self.flipped = False
        self.original_frames = self.frames.copy()
        self.direction_timer = 0
        self.next_direction_change = random.randint(60, 300)
        
        # Start facing right
        self.frames = [pygame.transform.flip(frame, True, False) for frame in self.frames]
        self.image = self.frames[self.current_frame]
        self.flipped = True
    
    def update(self):
        # Update animation frame
        if len(self.frames) > 1:
            self.frame_timer += 1
            if self.frame_timer >= self.frame_delay:
                self.frame_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.frames)
                self.image = self.frames[self.current_frame]
        
        # Update direction timer
        self.direction_timer += 1
        
        # Random direction change
        if self.direction_timer >= self.next_direction_change:
            self.direction *= -1
            self.direction_timer = 0
            self.next_direction_change = random.randint(60, 300)
            
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
        
        # Move Digimon (constrained to right half of screen)
        self.rect.x += self.speed * self.direction
        
        # Check boundaries (right half only)
        if self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.direction = -1
            self.direction_timer = 0
            self.next_direction_change = random.randint(30, 120)
            
            if self.flipped:
                self.frames = self.original_frames.copy()
                self.image = self.frames[self.current_frame]
                self.flipped = False
                
        elif self.rect.left <= SCREEN_WIDTH // 2:
            self.rect.left = SCREEN_WIDTH // 2
            self.direction = 1
            self.direction_timer = 0
            self.next_direction_change = random.randint(30, 120)
            
            if not self.flipped:
                self.frames = [pygame.transform.flip(frame, True, False) for frame in self.original_frames]
                self.image = self.frames[self.current_frame]
                self.flipped = True
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

class ComparisonDemo:
    def __init__(self):
        pygame.mouse.set_visible(True)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("GIF vs PNG Animation Comparison")
        self.clock = pygame.time.Clock()
        
        # Set up asset paths
        if os.path.basename(os.getcwd()) == 'src':
            assets_dir = os.path.join(os.path.dirname(os.getcwd()), "assets")
        else:
            assets_dir = os.path.join(os.path.dirname(__file__), "assets")
        
        sprites_dir = os.path.join(assets_dir, "sprites")
        
        # Load background
        bg_path = os.path.join(assets_dir, "bg1.jpg")
        try:
            self.background = pygame.image.load(bg_path)
            self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception as e:
            print(f"Could not load background: {e}")
            self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background.fill(BACKGROUND_COLOR)
        
        # Create GIF-based Digimon (left side)
        agumon_gif_path = os.path.join(sprites_dir, "Agumon-walking.gif")
        self.agumon_gif = DigimonGIF(agumon_gif_path, speed=2)
        
        gabumon_gif_path = os.path.join(sprites_dir, "Gabumon-walking.gif")
        self.gabumon_gif = DigimonGIF(gabumon_gif_path, speed=2)
        self.gabumon_gif.rect.x = 100
        self.gabumon_gif.direction = -1
        if self.gabumon_gif.flipped:
            self.gabumon_gif.frames = self.gabumon_gif.original_frames.copy()
            self.gabumon_gif.image = self.gabumon_gif.frames[self.gabumon_gif.current_frame]
            self.gabumon_gif.flipped = False
        
        # Create PNG-based Digimon (right side)
        agumon_folder = os.path.join(sprites_dir, "Agumon_dmc")
        self.agumon_png = DigimonPNG(agumon_folder, speed=2)
        
        gabumon_folder = os.path.join(sprites_dir, "Gabumon_dmc")
        self.gabumon_png = DigimonPNG(gabumon_folder, speed=2)
        self.gabumon_png.rect.x = SCREEN_WIDTH // 2 + 100
        self.gabumon_png.direction = -1
        if self.gabumon_png.flipped:
            self.gabumon_png.frames = self.gabumon_png.original_frames.copy()
            self.gabumon_png.image = self.gabumon_png.frames[self.gabumon_png.current_frame]
            self.gabumon_png.flipped = False
        
        # Create fonts for labels
        self.font = pygame.font.Font(None, 36)
        
        self.running = True
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def update(self):
        # Update GIF-based Digimon
        self.agumon_gif.update()
        self.gabumon_gif.update()
        
        # Update PNG-based Digimon
        self.agumon_png.update()
        self.gabumon_png.update()
    
    def draw(self):
        # Draw background
        self.screen.blit(self.background, (0, 0))
        
        # Draw dividing line
        pygame.draw.line(self.screen, (255, 255, 255), 
                        (SCREEN_WIDTH // 2, 0), 
                        (SCREEN_WIDTH // 2, SCREEN_HEIGHT), 3)
        
        # Draw labels
        gif_label = self.font.render("GIF Animation", True, (255, 255, 255))
        png_label = self.font.render("PNG Animation", True, (255, 255, 255))
        
        self.screen.blit(gif_label, (10, 10))
        self.screen.blit(png_label, (SCREEN_WIDTH // 2 + 10, 10))
        
        # Draw Digimon
        self.agumon_gif.draw(self.screen)
        self.gabumon_gif.draw(self.screen)
        self.agumon_png.draw(self.screen)
        self.gabumon_png.draw(self.screen)
        
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
    demo = ComparisonDemo()
    demo.run()

if __name__ == "__main__":
    main()
