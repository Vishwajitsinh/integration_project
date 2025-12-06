from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
import random

class HandwritingRenderer:
    def __init__(self, font_path=r"C:\Windows\Fonts\LHANDW.TTF", font_size=20):
        self.font_path = font_path
        self.font_size = font_size
        try:
            self.font = ImageFont.truetype(font_path, font_size)
        except IOError:
            # Fallback to default if custom font fails
            self.font = ImageFont.load_default()
            print(f"Warning: Could not load font at {font_path}. Using default.")

    def create_paper_background(self, width, height):
        # Create a slightly off-white background
        img = Image.new('RGB', (width, height), color=(253, 252, 245))
        draw = ImageDraw.Draw(img)
        
        # Draw blue lines like notebook paper
        line_spacing = self.font_size * 2
        for y in range(line_spacing, height, line_spacing):
            draw.line([(0, y), (width, y)], fill=(200, 220, 255), width=1)
            
        # Draw red margin line
        draw.line([(self.font_size * 3, 0), (self.font_size * 3, height)], fill=(255, 200, 200), width=1)
        
        return img

    def render_text(self, text, output_file="output_handwriting.png"):
        """
        Renders the given text onto a "handwritten" image.
        """
        margin_left = self.font_size * 4
        margin_top = self.font_size * 2
        line_height = self.font_size * 2
        
        # Calculate image size based on text
        # (A naive estimation, usually we'd wrap text first to measure height)
        max_width = 800
        wrapped_lines = []
        
        # Wrap text to fit
        chars_per_line = int((max_width - margin_left - 20) / (self.font_size * 0.6)) # rough estimate of char width
        
        original_lines = text.split('\n')
        for line in original_lines:
            wrapped = textwrap.wrap(line, width=chars_per_line)
            if not wrapped:
                wrapped_lines.append("")
            else:
                wrapped_lines.extend(wrapped)
                
        # Calculate total height
        total_height = max(600, margin_top + len(wrapped_lines) * line_height + 100)
        
        img = self.create_paper_background(max_width, total_height)
        draw = ImageDraw.Draw(img)
        
        current_y = margin_top
        
        for line in wrapped_lines:
            # Add slight random offset for "human" touch
            x_offset = random.randint(-1, 2)
            y_offset = random.randint(-1, 2)
            
            draw.text((margin_left + x_offset, current_y + y_offset), line, font=self.font, fill=(20, 20, 60)) # Dark blue ink
            current_y += line_height
            
        img.save(output_file)
        return output_file

if __name__ == "__main__":
    renderer = HandwritingRenderer()
    renderer.render_text("Scientific Solver Output:\n\nIntegral of x^2 is x^3/3 + C\n\nThis looks like handwriting!")
