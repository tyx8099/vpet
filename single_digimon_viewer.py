#!/usr/bin/env python3
"""
Single Digimon Frame Viewer
Detailed frame-by-frame analysis of individual Digimon sprites
"""

import pygame
import sys
import os

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
BACKGROUND_COLOR = (30, 30, 30)
TEXT_COLOR = (255, 255, 255)
HIGHLIGHT_COLOR = (255, 255, 0)
SPRITE_SIZE = 200  # Large size for detailed viewing

class SingleDigimonViewer:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Single Digimon Frame Viewer")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.big_font = pygame.font.Font(None, 36)
        
        # State
        self.digimon_list = []
        self.current_digimon_index = 0
        self.current_frame = 0
        self.auto_animate = False
        self.animation_timer = 0
        self.animation_speed = 30  # Frames between animation updates
        
        self.load_all_digimon()
        
    def load_all_digimon(self):
        """Load all available Digimon"""
        assets_dir = os.path.join(os.path.dirname(__file__), "assets")
        sprites_dir = os.path.join(assets_dir, "sprites")
        
        if not os.path.exists(sprites_dir):
            print(f"Sprites directory not found: {sprites_dir}")
            return
        
        # Get all Digimon folders
        for folder in sorted(os.listdir(sprites_dir)):
            if folder.endswith("_dmc") and os.path.isdir(os.path.join(sprites_dir, folder)):
                digimon_path = os.path.join(sprites_dir, folder)
                digimon_data = self.load_digimon_frames(digimon_path, folder)
                if digimon_data:
                    self.digimon_list.append(digimon_data)
        
        print(f"Loaded {len(self.digimon_list)} Digimon")
    
    def load_digimon_frames(self, digimon_path, folder_name):
        """Load all frames for a single Digimon"""
        digimon_name = folder_name.replace("_dmc", "")
        frames = []
        frame_info = []
        
        # Load frames 0-14
        for frame_num in range(15):
            frame_path = os.path.join(digimon_path, f"{frame_num}.png")
            if os.path.exists(frame_path):
                try:
                    # Load original frame
                    original = pygame.image.load(frame_path)
                    original_size = original.get_size()
                    
                    # Create scaled version for display
                    scaled = pygame.transform.scale(original, (SPRITE_SIZE, SPRITE_SIZE))
                    
                    frames.append({
                        'original': original,
                        'scaled': scaled,
                        'number': frame_num,
                        'size': original_size,
                        'exists': True
                    })
                    
                    frame_info.append(f"Frame {frame_num}: {original_size[0]}x{original_size[1]}")
                    
                except Exception as e:
                    print(f"Error loading frame {frame_num} for {digimon_name}: {e}")
            else:
                # Add placeholder for missing frame
                frames.append({
                    'original': None,
                    'scaled': None,
                    'number': frame_num,
                    'size': (0, 0),
                    'exists': False
                })
        
        if not any(frame['exists'] for frame in frames):
            return None
            
        return {
            'name': digimon_name,
            'folder': folder_name,
            'frames': frames,
            'frame_info': frame_info
        }
    
    def get_current_digimon(self):
        """Get currently selected Digimon"""
        if self.digimon_list and 0 <= self.current_digimon_index < len(self.digimon_list):
            return self.digimon_list[self.current_digimon_index]
        return None
    
    def get_current_frame_data(self):
        """Get current frame data"""
        digimon = self.get_current_digimon()
        if digimon and 0 <= self.current_frame < len(digimon['frames']):
            return digimon['frames'][self.current_frame]
        return None
    
    def draw_sprite(self):
        """Draw the current sprite frame"""
        frame_data = self.get_current_frame_data()
        
        if frame_data and frame_data['exists'] and frame_data['scaled']:
            # Draw sprite in center-left area
            sprite_x = 150
            sprite_y = SCREEN_HEIGHT // 2 - SPRITE_SIZE // 2
            self.screen.blit(frame_data['scaled'], (sprite_x, sprite_y))
            
            # Draw border around sprite
            pygame.draw.rect(self.screen, (100, 100, 100), 
                           (sprite_x - 2, sprite_y - 2, SPRITE_SIZE + 4, SPRITE_SIZE + 4), 2)
        else:
            # Draw "missing frame" indicator
            sprite_x = 150
            sprite_y = SCREEN_HEIGHT // 2 - SPRITE_SIZE // 2
            pygame.draw.rect(self.screen, (50, 50, 50), 
                           (sprite_x, sprite_y, SPRITE_SIZE, SPRITE_SIZE))
            pygame.draw.rect(self.screen, (100, 100, 100), 
                           (sprite_x, sprite_y, SPRITE_SIZE, SPRITE_SIZE), 2)
            
            # Draw "X" for missing frame
            pygame.draw.line(self.screen, (150, 150, 150), 
                           (sprite_x, sprite_y), 
                           (sprite_x + SPRITE_SIZE, sprite_y + SPRITE_SIZE), 3)
            pygame.draw.line(self.screen, (150, 150, 150), 
                           (sprite_x + SPRITE_SIZE, sprite_y), 
                           (sprite_x, sprite_y + SPRITE_SIZE), 3)
            
            missing_text = self.font.render("MISSING", True, (150, 150, 150))
            text_rect = missing_text.get_rect()
            text_rect.center = (sprite_x + SPRITE_SIZE // 2, sprite_y + SPRITE_SIZE // 2 + 30)
            self.screen.blit(missing_text, text_rect)
    
    def draw_info_panel(self):
        """Draw information panel"""
        digimon = self.get_current_digimon()
        if not digimon:
            return
        
        info_x = 400
        info_y = 50
        
        # Digimon name
        name_surface = self.big_font.render(digimon['name'], True, HIGHLIGHT_COLOR)
        self.screen.blit(name_surface, (info_x, info_y))
        info_y += 50
        
        # Current frame info
        frame_data = self.get_current_frame_data()
        if frame_data:
            if frame_data['exists']:
                frame_text = f"Frame {frame_data['number']}: {frame_data['size'][0]}x{frame_data['size'][1]} pixels"
                color = TEXT_COLOR
            else:
                frame_text = f"Frame {frame_data['number']}: MISSING"
                color = (150, 150, 150)
            
            frame_surface = self.font.render(frame_text, True, color)
            self.screen.blit(frame_surface, (info_x, info_y))
            info_y += 30
        
        # Animation status
        anim_status = "ON" if self.auto_animate else "OFF"
        anim_color = HIGHLIGHT_COLOR if self.auto_animate else TEXT_COLOR
        anim_surface = self.font.render(f"Auto Animation: {anim_status}", True, anim_color)
        self.screen.blit(anim_surface, (info_x, info_y))
        info_y += 40
        
        # Available frames list
        available_text = self.font.render("Available Frames:", True, TEXT_COLOR)
        self.screen.blit(available_text, (info_x, info_y))
        info_y += 30
        
        # Show frame numbers in rows
        available_frames = [str(frame['number']) for frame in digimon['frames'] if frame['exists']]
        frames_per_row = 10
        
        for i in range(0, len(available_frames), frames_per_row):
            row_frames = available_frames[i:i+frames_per_row]
            row_text = ", ".join(row_frames)
            row_surface = self.font.render(row_text, True, (200, 200, 200))
            self.screen.blit(row_surface, (info_x + 20, info_y))
            info_y += 25
        
        # Usage info for frames
        info_y += 20
        usage_info = [
            "Frame Usage:",
            "0-1: Walking animation",
            "2: Greeting pose",
            "5-6: Feeding/eating",
            "11-12: Sleeping",
            "3-4, 7-10, 13-14: Special animations"
        ]
        
        for usage in usage_info:
            color = HIGHLIGHT_COLOR if usage.startswith("Frame Usage:") else (180, 180, 180)
            usage_surface = self.font.render(usage, True, color)
            self.screen.blit(usage_surface, (info_x, info_y))
            info_y += 22
    
    def draw_controls(self):
        """Draw control instructions"""
        controls = [
            "CONTROLS:",
            "LEFT/RIGHT: Previous/Next Digimon",
            "UP/DOWN: Previous/Next Frame",
            "A: Toggle auto animation",
            "SPACE: Play animation cycle",
            "R: Reset to frame 0",
            "S: Save current frame info",
            "ESC: Exit"
        ]
        
        y = SCREEN_HEIGHT - len(controls) * 22 - 10
        
        for control in controls:
            color = HIGHLIGHT_COLOR if control.startswith("CONTROLS:") else TEXT_COLOR
            control_surface = self.font.render(control, True, color)
            self.screen.blit(control_surface, (10, y))
            y += 22
    
    def draw_navigation(self):
        """Draw navigation info"""
        if not self.digimon_list:
            return
        
        nav_text = f"Digimon {self.current_digimon_index + 1}/{len(self.digimon_list)}"
        nav_surface = self.font.render(nav_text, True, HIGHLIGHT_COLOR)
        nav_rect = nav_surface.get_rect()
        nav_rect.topright = (SCREEN_WIDTH - 10, 10)
        self.screen.blit(nav_surface, nav_rect)
        
        # Frame navigation
        digimon = self.get_current_digimon()
        if digimon:
            available_count = sum(1 for frame in digimon['frames'] if frame['exists'])
            frame_nav_text = f"Frame {self.current_frame}/14 ({available_count} available)"
            frame_nav_surface = self.font.render(frame_nav_text, True, TEXT_COLOR)
            frame_nav_rect = frame_nav_surface.get_rect()
            frame_nav_rect.topright = (SCREEN_WIDTH - 10, 35)
            self.screen.blit(frame_nav_surface, frame_nav_rect)
    
    def save_frame_info(self):
        """Save information about current Digimon to a file"""
        digimon = self.get_current_digimon()
        if not digimon:
            return
        
        filename = f"{digimon['name']}_frame_info.txt"
        
        try:
            with open(filename, 'w') as f:
                f.write(f"Digimon: {digimon['name']}\n")
                f.write(f"Folder: {digimon['folder']}\n")
                f.write("=" * 40 + "\n\n")
                
                f.write("Available Frames:\n")
                for frame in digimon['frames']:
                    if frame['exists']:
                        f.write(f"Frame {frame['number']:2d}: {frame['size'][0]}x{frame['size'][1]} pixels\n")
                    else:
                        f.write(f"Frame {frame['number']:2d}: MISSING\n")
                
                f.write("\nFrame Usage Guide:\n")
                f.write("0-1: Walking animation\n")
                f.write("2: Greeting pose\n")
                f.write("5-6: Feeding/eating\n")
                f.write("11-12: Sleeping\n")
                f.write("3-4, 7-10, 13-14: Special animations\n")
            
            print(f"Frame info saved to {filename}")
        except Exception as e:
            print(f"Error saving frame info: {e}")
    
    def handle_events(self):
        """Handle user input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                
                elif event.key == pygame.K_LEFT:
                    # Previous Digimon
                    if self.digimon_list:
                        self.current_digimon_index = (self.current_digimon_index - 1) % len(self.digimon_list)
                        self.current_frame = 0
                
                elif event.key == pygame.K_RIGHT:
                    # Next Digimon
                    if self.digimon_list:
                        self.current_digimon_index = (self.current_digimon_index + 1) % len(self.digimon_list)
                        self.current_frame = 0
                
                elif event.key == pygame.K_UP:
                    # Previous frame
                    self.current_frame = (self.current_frame - 1) % 15
                
                elif event.key == pygame.K_DOWN:
                    # Next frame
                    self.current_frame = (self.current_frame + 1) % 15
                
                elif event.key == pygame.K_a:
                    # Toggle auto animation
                    self.auto_animate = not self.auto_animate
                
                elif event.key == pygame.K_r:
                    # Reset to frame 0
                    self.current_frame = 0
                
                elif event.key == pygame.K_s:
                    # Save frame info
                    self.save_frame_info()
                
                elif event.key == pygame.K_SPACE:
                    # Quick animation cycle through available frames
                    self.play_animation_cycle()
        
        return True
    
    def play_animation_cycle(self):
        """Play a quick cycle through all available frames"""
        digimon = self.get_current_digimon()
        if not digimon:
            return
        
        available_frames = [i for i, frame in enumerate(digimon['frames']) if frame['exists']]
        
        for frame_num in available_frames:
            self.current_frame = frame_num
            
            # Draw current state
            self.screen.fill(BACKGROUND_COLOR)
            self.draw_sprite()
            self.draw_info_panel()
            self.draw_controls()
            self.draw_navigation()
            pygame.display.flip()
            
            # Wait
            pygame.time.wait(300)  # 300ms per frame
    
    def update(self):
        """Update animation"""
        if self.auto_animate:
            self.animation_timer += 1
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                
                # Find next available frame
                digimon = self.get_current_digimon()
                if digimon:
                    available_frames = [i for i, frame in enumerate(digimon['frames']) if frame['exists']]
                    if available_frames:
                        current_index = available_frames.index(self.current_frame) if self.current_frame in available_frames else 0
                        next_index = (current_index + 1) % len(available_frames)
                        self.current_frame = available_frames[next_index]
    
    def run(self):
        """Main application loop"""
        if not self.digimon_list:
            print("No Digimon found! Make sure the assets/sprites directory exists.")
            return
        
        print(f"Single Digimon Viewer started with {len(self.digimon_list)} Digimon!")
        
        running = True
        while running:
            running = self.handle_events()
            self.update()
            
            # Draw everything
            self.screen.fill(BACKGROUND_COLOR)
            self.draw_sprite()
            self.draw_info_panel()
            self.draw_controls()
            self.draw_navigation()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

def main():
    """Run the Single Digimon Viewer"""
    try:
        viewer = SingleDigimonViewer()
        viewer.run()
    except Exception as e:
        print(f"Error running Single Digimon Viewer: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
