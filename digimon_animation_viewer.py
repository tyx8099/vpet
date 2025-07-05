#!/usr/bin/env python3
"""
Digimon Animation Viewer
Shows all available animations for all Digimon in the collection
"""

import pygame
import sys
import os
import time
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
BACKGROUND_COLOR = (50, 50, 50)
TEXT_COLOR = (255, 255, 255)
HIGHLIGHT_COLOR = (255, 255, 0)
DIGIMON_SIZE = 80  # Larger size for better viewing
GRID_COLS = 6
GRID_ROWS = 4
CELL_WIDTH = SCREEN_WIDTH // GRID_COLS
CELL_HEIGHT = SCREEN_HEIGHT // GRID_ROWS
DIGIMON_PER_PAGE = GRID_COLS * GRID_ROWS  # 24 Digimon per page

# Animation types and their corresponding frame numbers
ANIMATION_TYPES = {
    "Walking": [0, 1],           # Frames 0 and 1
    "Greeting": [2, 0],          # Frame 2 and 0
    "Feeding": [5, 6],           # Frames 5 and 6
    "Sleeping": [11, 12],        # Frames 11 and 12
    "Special1": [3, 4],          # Frames 3 and 4 (if available)
    "Special2": [7, 8],          # Frames 7 and 8 (if available)
    "Special3": [9, 10],         # Frames 9 and 10 (if available)
    "Special4": [13, 14],        # Frames 13 and 14 (if available)
}

class DigimonAnimationViewer:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Digimon Animation Viewer")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        
        # Load all Digimon
        self.digimon_list = []
        self.current_animation = "Walking"
        self.animation_frame = 0
        self.frame_timer = 0
        self.frame_delay = 30  # Slower animation for viewing
        
        # UI state
        self.show_instructions = True
        self.selected_digimon = 0
        self.current_page = 0  # For pagination
        
        self.load_all_digimon()
        
    def load_all_digimon(self):
        """Load all available Digimon sprites"""
        assets_dir = os.path.join(os.path.dirname(__file__), "assets")
        sprites_dir = os.path.join(assets_dir, "sprites")
        
        if not os.path.exists(sprites_dir):
            print(f"Sprites directory not found: {sprites_dir}")
            return
        
        # Get all Digimon folders
        digimon_folders = []
        for folder in os.listdir(sprites_dir):
            if folder.endswith("_dmc") and os.path.isdir(os.path.join(sprites_dir, folder)):
                digimon_folders.append(folder)
        
        digimon_folders.sort()  # Sort alphabetically
        
        for folder in digimon_folders:
            digimon_path = os.path.join(sprites_dir, folder)
            digimon_data = self.load_digimon_sprites(digimon_path, folder)
            if digimon_data:
                self.digimon_list.append(digimon_data)
        
        print(f"Loaded {len(self.digimon_list)} Digimon with animations")
    
    def load_digimon_sprites(self, digimon_path, folder_name):
        """Load all sprite frames for a single Digimon"""
        digimon_name = folder_name.replace("_dmc", "")
        
        # Load all available frames (0-14)
        frames = {}
        animations = {}
        
        for frame_num in range(15):  # 0-14
            frame_path = os.path.join(digimon_path, f"{frame_num}.png")
            if os.path.exists(frame_path):
                try:
                    frame = pygame.image.load(frame_path)
                    # Scale to consistent size
                    frame = pygame.transform.scale(frame, (DIGIMON_SIZE, DIGIMON_SIZE))
                    frames[frame_num] = frame
                except Exception as e:
                    print(f"Error loading frame {frame_num} for {digimon_name}: {e}")
        
        if not frames:
            print(f"No frames found for {digimon_name}")
            return None
        
        # Build animations based on available frames
        for anim_name, frame_list in ANIMATION_TYPES.items():
            if all(frame_num in frames for frame_num in frame_list):
                animations[anim_name] = [frames[frame_num] for frame_num in frame_list]
        
        # Ensure at least one animation exists
        if not animations and frames:
            # Create a basic animation from available frames
            available_frames = sorted(frames.keys())
            if len(available_frames) >= 2:
                animations["Basic"] = [frames[available_frames[0]], frames[available_frames[1]]]
            else:
                animations["Static"] = [frames[available_frames[0]]]
        
        return {
            "name": digimon_name,
            "folder": folder_name,
            "frames": frames,
            "animations": animations,
            "current_frame": 0
        }
    
    def get_current_page_digimon(self):
        """Get the Digimon to display on the current page"""
        start_index = self.current_page * DIGIMON_PER_PAGE
        end_index = start_index + DIGIMON_PER_PAGE
        return self.digimon_list[start_index:end_index]
    
    def get_total_pages(self):
        """Get the total number of pages needed"""
        if not self.digimon_list:
            return 0
        return (len(self.digimon_list) - 1) // DIGIMON_PER_PAGE + 1
    
    def get_animation_info(self, digimon):
        """Get information about current animation"""
        if self.current_animation in digimon["animations"]:
            return digimon["animations"][self.current_animation]
        elif digimon["animations"]:
            # Return first available animation
            first_anim = list(digimon["animations"].keys())[0]
            return digimon["animations"][first_anim]
        else:
            return []
    
    def update_animations(self):
        """Update animation frames for all Digimon"""
        self.frame_timer += 1
        
        if self.frame_timer >= self.frame_delay:
            self.frame_timer = 0
            
            # Only update animations for currently visible Digimon
            current_digimon = self.get_current_page_digimon()
            for digimon in current_digimon:
                anim_frames = self.get_animation_info(digimon)
                if anim_frames:
                    digimon["current_frame"] = (digimon["current_frame"] + 1) % len(anim_frames)
    
    def draw_digimon_grid(self):
        """Draw all Digimon in a grid layout"""
        current_digimon = self.get_current_page_digimon()
        
        for i, digimon in enumerate(current_digimon):
            # Calculate grid position
            col = i % GRID_COLS
            row = i // GRID_COLS
            x = col * CELL_WIDTH + CELL_WIDTH // 2 - DIGIMON_SIZE // 2
            y = row * CELL_HEIGHT + CELL_HEIGHT // 2 - DIGIMON_SIZE // 2
            
            # Calculate actual digimon index for selection highlight
            actual_index = self.current_page * DIGIMON_PER_PAGE + i
            
            # Highlight selected Digimon
            if actual_index == self.selected_digimon:
                pygame.draw.rect(self.screen, HIGHLIGHT_COLOR, 
                               (col * CELL_WIDTH + 5, row * CELL_HEIGHT + 5, 
                                CELL_WIDTH - 10, CELL_HEIGHT - 10), 3)
            
            # Draw cell border
            pygame.draw.rect(self.screen, (100, 100, 100), 
                           (col * CELL_WIDTH, row * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT), 1)
            
            # Get current animation frame
            anim_frames = self.get_animation_info(digimon)
            if anim_frames:
                current_sprite = anim_frames[digimon["current_frame"]]
                self.screen.blit(current_sprite, (x, y))
            
            # Draw Digimon name
            name_surface = self.small_font.render(digimon["name"], True, TEXT_COLOR)
            name_rect = name_surface.get_rect()
            name_rect.centerx = col * CELL_WIDTH + CELL_WIDTH // 2
            name_rect.y = row * CELL_HEIGHT + CELL_HEIGHT - 40
            self.screen.blit(name_surface, name_rect)
            
            # Draw current animation name
            anim_name = self.current_animation if self.current_animation in digimon["animations"] else "N/A"
            anim_surface = self.small_font.render(anim_name, True, (200, 200, 200))
            anim_rect = anim_surface.get_rect()
            anim_rect.centerx = col * CELL_WIDTH + CELL_WIDTH // 2
            anim_rect.y = row * CELL_HEIGHT + CELL_HEIGHT - 20
            self.screen.blit(anim_surface, anim_rect)
    
    def draw_ui(self):
        """Draw user interface elements"""
        # Current animation type
        anim_text = f"Current Animation: {self.current_animation}"
        anim_surface = self.font.render(anim_text, True, HIGHLIGHT_COLOR)
        self.screen.blit(anim_surface, (10, 10))
        
        # Animation list
        y_offset = 40
        for i, anim_name in enumerate(ANIMATION_TYPES.keys()):
            color = HIGHLIGHT_COLOR if anim_name == self.current_animation else TEXT_COLOR
            anim_surface = self.small_font.render(f"{i+1}. {anim_name}", True, color)
            self.screen.blit(anim_surface, (10, y_offset))
            y_offset += 20
        
        # Instructions
        if self.show_instructions:
            instructions = [
                "CONTROLS:",
                "1-8: Switch animation type",
                "SPACE: Cycle through animations",
                "ARROW KEYS: Navigate selection",
                "PAGE UP/DOWN: Navigate pages",
                "ENTER: Focus on selected Digimon",
                "F: Toggle fullscreen mode",
                "H: Toggle this help",
                "ESC: Exit",
                "",
                f"Showing {len(self.digimon_list)} Digimon total",
                f"Page {self.current_page + 1}/{self.get_total_pages()}",
                f"Selected: {self.digimon_list[self.selected_digimon]['name'] if self.digimon_list else 'None'}"
            ]
            
            # Draw instructions background
            inst_width = 300
            inst_height = len(instructions) * 20 + 20
            pygame.draw.rect(self.screen, (0, 0, 0, 128), 
                           (SCREEN_WIDTH - inst_width - 10, 10, inst_width, inst_height))
            pygame.draw.rect(self.screen, TEXT_COLOR, 
                           (SCREEN_WIDTH - inst_width - 10, 10, inst_width, inst_height), 1)
            
            for i, instruction in enumerate(instructions):
                color = HIGHLIGHT_COLOR if instruction.startswith("CONTROLS") else TEXT_COLOR
                inst_surface = self.small_font.render(instruction, True, color)
                self.screen.blit(inst_surface, (SCREEN_WIDTH - inst_width, 20 + i * 20))
        
        # Draw page indicator at bottom
        if self.get_total_pages() > 1:
            page_text = f"Page {self.current_page + 1} of {self.get_total_pages()} | Total: {len(self.digimon_list)} Digimon"
            page_surface = self.font.render(page_text, True, HIGHLIGHT_COLOR)
            page_rect = page_surface.get_rect()
            page_rect.centerx = SCREEN_WIDTH // 2
            page_rect.y = SCREEN_HEIGHT - 30
            
            # Draw background for page indicator
            bg_rect = page_rect.copy()
            bg_rect.inflate_ip(20, 10)
            pygame.draw.rect(self.screen, (0, 0, 0, 180), bg_rect)
            pygame.draw.rect(self.screen, HIGHLIGHT_COLOR, bg_rect, 1)
            
            self.screen.blit(page_surface, page_rect)
    
    def draw_detailed_view(self):
        """Draw detailed view of selected Digimon"""
        if not self.digimon_list or self.selected_digimon >= len(self.digimon_list):
            return
        
        digimon = self.digimon_list[self.selected_digimon]
        
        # Clear screen for detailed view
        self.screen.fill(BACKGROUND_COLOR)
        
        # Large Digimon sprite in center
        anim_frames = self.get_animation_info(digimon)
        if anim_frames:
            large_sprite = pygame.transform.scale(anim_frames[digimon["current_frame"]], (200, 200))
            sprite_rect = large_sprite.get_rect()
            sprite_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            self.screen.blit(large_sprite, sprite_rect)
        
        # Digimon name
        name_surface = pygame.font.Font(None, 48).render(digimon["name"], True, HIGHLIGHT_COLOR)
        name_rect = name_surface.get_rect()
        name_rect.centerx = SCREEN_WIDTH // 2
        name_rect.y = 50
        self.screen.blit(name_surface, name_rect)
        
        # Available animations
        anim_list_title = self.font.render("Available Animations:", True, TEXT_COLOR)
        self.screen.blit(anim_list_title, (50, 150))
        
        y_offset = 180
        for anim_name in digimon["animations"].keys():
            color = HIGHLIGHT_COLOR if anim_name == self.current_animation else TEXT_COLOR
            anim_surface = self.font.render(f"• {anim_name}", True, color)
            self.screen.blit(anim_surface, (70, y_offset))
            y_offset += 30
        
        # Frame information
        frame_info = self.font.render(f"Animation: {self.current_animation}", True, TEXT_COLOR)
        self.screen.blit(frame_info, (50, SCREEN_HEIGHT - 100))
        
        if anim_frames:
            frame_count_info = self.font.render(f"Frames: {len(anim_frames)}", True, TEXT_COLOR)
            self.screen.blit(frame_count_info, (50, SCREEN_HEIGHT - 70))
            
            current_frame_info = self.font.render(f"Current Frame: {digimon['current_frame'] + 1}/{len(anim_frames)}", True, TEXT_COLOR)
            self.screen.blit(current_frame_info, (50, SCREEN_HEIGHT - 40))
        
        # Back instruction
        back_text = self.small_font.render("Press ESCAPE to return to grid view", True, (150, 150, 150))
        back_rect = back_text.get_rect()
        back_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20)
        self.screen.blit(back_text, back_rect)
    
    def handle_events(self):
        """Handle user input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                
                elif event.key == pygame.K_h:
                    self.show_instructions = not self.show_instructions
                
                elif event.key == pygame.K_SPACE:
                    # Cycle through animations
                    anim_list = list(ANIMATION_TYPES.keys())
                    current_index = anim_list.index(self.current_animation) if self.current_animation in anim_list else 0
                    self.current_animation = anim_list[(current_index + 1) % len(anim_list)]
                
                elif event.key == pygame.K_f:
                    # Toggle fullscreen
                    pygame.display.toggle_fullscreen()
                
                elif event.key >= pygame.K_1 and event.key <= pygame.K_8:
                    # Switch animation by number
                    anim_index = event.key - pygame.K_1
                    anim_list = list(ANIMATION_TYPES.keys())
                    if anim_index < len(anim_list):
                        self.current_animation = anim_list[anim_index]
                
                elif event.key == pygame.K_LEFT:
                    if self.digimon_list:
                        self.selected_digimon = (self.selected_digimon - 1) % len(self.digimon_list)
                        # Update page if selection moved to different page
                        self.current_page = self.selected_digimon // DIGIMON_PER_PAGE
                
                elif event.key == pygame.K_RIGHT:
                    if self.digimon_list:
                        self.selected_digimon = (self.selected_digimon + 1) % len(self.digimon_list)
                        # Update page if selection moved to different page
                        self.current_page = self.selected_digimon // DIGIMON_PER_PAGE
                
                elif event.key == pygame.K_UP:
                    if self.digimon_list:
                        self.selected_digimon = (self.selected_digimon - GRID_COLS) % len(self.digimon_list)
                        # Update page if selection moved to different page
                        self.current_page = self.selected_digimon // DIGIMON_PER_PAGE
                
                elif event.key == pygame.K_DOWN:
                    if self.digimon_list:
                        self.selected_digimon = (self.selected_digimon + GRID_COLS) % len(self.digimon_list)
                        # Update page if selection moved to different page
                        self.current_page = self.selected_digimon // DIGIMON_PER_PAGE
                
                elif event.key == pygame.K_PAGEUP:
                    # Previous page
                    if self.current_page > 0:
                        self.current_page -= 1
                        # Move selection to corresponding position on new page
                        page_position = self.selected_digimon % DIGIMON_PER_PAGE
                        self.selected_digimon = self.current_page * DIGIMON_PER_PAGE + page_position
                        # Ensure selection is within bounds
                        if self.selected_digimon >= len(self.digimon_list):
                            self.selected_digimon = len(self.digimon_list) - 1
                
                elif event.key == pygame.K_PAGEDOWN:
                    # Next page
                    if self.current_page < self.get_total_pages() - 1:
                        self.current_page += 1
                        # Move selection to corresponding position on new page
                        page_position = self.selected_digimon % DIGIMON_PER_PAGE
                        self.selected_digimon = self.current_page * DIGIMON_PER_PAGE + page_position
                        # Ensure selection is within bounds
                        if self.selected_digimon >= len(self.digimon_list):
                            self.selected_digimon = len(self.digimon_list) - 1
        
        return True
    
    def run(self):
        """Main application loop"""
        if not self.digimon_list:
            print("No Digimon found! Make sure the assets/sprites directory exists with Digimon folders.")
            return
        
        print(f"Digimon Animation Viewer started!")
        print(f"Loaded {len(self.digimon_list)} Digimon:")
        for digimon in self.digimon_list:
            anim_count = len(digimon["animations"])
            print(f"  - {digimon['name']}: {anim_count} animations")
        
        running = True
        while running:
            running = self.handle_events()
            
            # Update animations
            self.update_animations()
            
            # Clear screen
            self.screen.fill(BACKGROUND_COLOR)
            
            # Draw content
            self.draw_digimon_grid()
            self.draw_ui()
            
            # Update display
            pygame.display.flip()
            self.clock.tick(60)  # 60 FPS
        
        pygame.quit()
        sys.exit()

def main():
    """Run the Digimon Animation Viewer"""
    try:
        viewer = DigimonAnimationViewer()
        viewer.run()
    except Exception as e:
        print(f"Error running Digimon Animation Viewer: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
