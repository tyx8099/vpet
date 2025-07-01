import pygame
import sys
import os

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (64, 64, 64)  # Dark gray for better contrast

class ImageComparison:
    def __init__(self):
        pygame.mouse.set_visible(True)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("PNG Image Comparison: Gabumon_1.png vs Gabumon_dmc/0.png")
        self.clock = pygame.time.Clock()
        
        # Set up asset paths
        if os.path.basename(os.getcwd()) == 'src':
            assets_dir = os.path.join(os.path.dirname(os.getcwd()), "assets")
        else:
            assets_dir = os.path.join(os.path.dirname(__file__), "assets")
        
        sprites_dir = os.path.join(assets_dir, "sprites")
        
        # Load the two images to compare
        gabumon_1_path = os.path.join(sprites_dir, "Gabumon_1.png")
        gabumon_dmc_0_path = os.path.join(sprites_dir, "Gabumon_dmc", "0.png")
        
        try:
            self.image1 = pygame.image.load(gabumon_1_path)
            self.image1_name = "Gabumon_1.png"
            print(f"Loaded: {gabumon_1_path}")
            print(f"Size: {self.image1.get_size()}")
        except Exception as e:
            print(f"Could not load {gabumon_1_path}: {e}")
            self.image1 = self.create_error_surface("ERROR: Gabumon_1.png")
            self.image1_name = "Gabumon_1.png (ERROR)"
        
        try:
            self.image2 = pygame.image.load(gabumon_dmc_0_path)
            self.image2_name = "Gabumon_dmc/0.png"
            print(f"Loaded: {gabumon_dmc_0_path}")
            print(f"Size: {self.image2.get_size()}")
        except Exception as e:
            print(f"Could not load {gabumon_dmc_0_path}: {e}")
            self.image2 = self.create_error_surface("ERROR: 0.png")
            self.image2_name = "Gabumon_dmc/0.png (ERROR)"
        
        # Scale images for better viewing (maintain aspect ratio)
        self.scaled_image1 = self.scale_image_for_display(self.image1)
        self.scaled_image2 = self.scale_image_for_display(self.image2)
        
        # Create fonts for labels
        self.font_large = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        self.running = True
        
        # Print analysis
        self.analyze_differences()
    
    def create_error_surface(self, text):
        """Create an error surface when image can't be loaded"""
        surface = pygame.Surface((200, 200))
        surface.fill((255, 0, 0))
        font = pygame.font.Font(None, 24)
        text_surf = font.render(text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(100, 100))
        surface.blit(text_surf, text_rect)
        return surface
    
    def scale_image_for_display(self, image):
        """Scale image to fit nicely in the display while maintaining aspect ratio"""
        max_width = 350
        max_height = 400
        
        original_width, original_height = image.get_size()
        
        # Calculate scaling factor
        scale_x = max_width / original_width
        scale_y = max_height / original_height
        scale = min(scale_x, scale_y, 4.0)  # Max 4x zoom
        
        new_width = int(original_width * scale)
        new_height = int(original_height * scale)
        
        return pygame.transform.scale(image, (new_width, new_height))
    
    def analyze_differences(self):
        """Analyze and print differences between the two images"""
        print("\n" + "="*50)
        print("IMAGE COMPARISON ANALYSIS")
        print("="*50)
        
        # Size comparison
        size1 = self.image1.get_size()
        size2 = self.image2.get_size()
        
        print(f"Image 1 ({self.image1_name}):")
        print(f"  - Size: {size1[0]}x{size1[1]} pixels")
        
        print(f"Image 2 ({self.image2_name}):")
        print(f"  - Size: {size2[0]}x{size2[1]} pixels")
        
        if size1 == size2:
            print("✓ Both images have the same dimensions")
        else:
            print("✗ Images have different dimensions")
        
        # Try to analyze pixel differences (if same size)
        if size1 == size2:
            try:
                # Convert to pixel arrays for comparison
                pixels1 = pygame.surfarray.array3d(self.image1)
                pixels2 = pygame.surfarray.array3d(self.image2)
                
                # Count different pixels
                diff_pixels = (pixels1 != pixels2).any(axis=2).sum()
                total_pixels = pixels1.shape[0] * pixels1.shape[1]
                
                print(f"\nPixel Analysis:")
                print(f"  - Total pixels: {total_pixels}")
                print(f"  - Different pixels: {diff_pixels}")
                print(f"  - Similarity: {((total_pixels - diff_pixels) / total_pixels * 100):.1f}%")
                
                if diff_pixels == 0:
                    print("✓ Images are identical!")
                elif diff_pixels < total_pixels * 0.01:
                    print("⚠ Images are very similar (< 1% difference)")
                elif diff_pixels < total_pixels * 0.1:
                    print("⚠ Images are similar (< 10% difference)")
                else:
                    print("✗ Images are significantly different")
                    
            except Exception as e:
                print(f"Could not perform pixel analysis: {e}")
        
        print("="*50)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def draw(self):
        # Clear screen
        self.screen.fill(BACKGROUND_COLOR)
        
        # Draw title
        title = self.font_large.render("Image Comparison", True, (255, 255, 255))
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 30))
        self.screen.blit(title, title_rect)
        
        # Draw dividing line
        pygame.draw.line(self.screen, (255, 255, 255), 
                        (SCREEN_WIDTH // 2, 60), 
                        (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60), 2)
        
        # Position images
        left_x = SCREEN_WIDTH // 4 - self.scaled_image1.get_width() // 2
        right_x = 3 * SCREEN_WIDTH // 4 - self.scaled_image2.get_width() // 2
        image_y = SCREEN_HEIGHT // 2 - max(self.scaled_image1.get_height(), self.scaled_image2.get_height()) // 2
        
        # Draw images
        self.screen.blit(self.scaled_image1, (left_x, image_y))
        self.screen.blit(self.scaled_image2, (right_x, image_y))
        
        # Draw labels
        label1 = self.font_small.render(self.image1_name, True, (255, 255, 255))
        label2 = self.font_small.render(self.image2_name, True, (255, 255, 255))
        
        label1_rect = label1.get_rect(center=(SCREEN_WIDTH // 4, image_y - 30))
        label2_rect = label2.get_rect(center=(3 * SCREEN_WIDTH // 4, image_y - 30))
        
        self.screen.blit(label1, label1_rect)
        self.screen.blit(label2, label2_rect)
        
        # Draw size info
        size1_text = f"Size: {self.image1.get_size()[0]}x{self.image1.get_size()[1]}"
        size2_text = f"Size: {self.image2.get_size()[0]}x{self.image2.get_size()[1]}"
        
        size1_surf = self.font_small.render(size1_text, True, (200, 200, 200))
        size2_surf = self.font_small.render(size2_text, True, (200, 200, 200))
        
        size1_rect = size1_surf.get_rect(center=(SCREEN_WIDTH // 4, image_y + self.scaled_image1.get_height() + 20))
        size2_rect = size2_surf.get_rect(center=(3 * SCREEN_WIDTH // 4, image_y + self.scaled_image2.get_height() + 20))
        
        self.screen.blit(size1_surf, size1_rect)
        self.screen.blit(size2_surf, size2_rect)
        
        # Instructions
        instructions = self.font_small.render("Press ESC to exit", True, (150, 150, 150))
        instr_rect = instructions.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        self.screen.blit(instructions, instr_rect)
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(60)  # 60 FPS for smooth display
        
        pygame.quit()
        sys.exit()

def main():
    comparison = ImageComparison()
    comparison.run()

if __name__ == "__main__":
    main()
