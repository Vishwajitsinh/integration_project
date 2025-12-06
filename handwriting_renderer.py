from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
import random

class HandwritingRenderer:
    def __init__(self, font_path=r"C:\Windows\Fonts\Inkfree.ttf", font_size=20):
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
        Renders the given text onto a "handwritten" image with support for superscripts (e.g. x^2).
        """
        margin_left = self.font_size * 4
        margin_top = self.font_size * 2
        line_height = int(self.font_size * 2.5) # More space for math
        
        # Calculate image size
        max_width = 900
        
        # Simple wrapping
        chars_per_line = int((max_width - margin_left - 50) / (self.font_size * 0.6))
        
        lines = []
        for raw_line in text.split('\n'):
            # Pre-processing: Ensure spacing around operators for better wrap, but keep exponents tight
            # We don't want to wrap inside x^2
            wrapped = textwrap.wrap(raw_line, width=chars_per_line)
            if not wrapped:
                lines.append("")
            else:
                lines.extend(wrapped)
        
        total_height = max(600, margin_top + len(lines) * line_height + 100)
        
        img = self.create_paper_background(max_width, total_height)
        draw = ImageDraw.Draw(img)
        
        current_y = margin_top
        
        # Prepare fonts
        font_regular = self.font
        # Attempt to load a smaller version for superscripts
        try:
            font_small = ImageFont.truetype(self.font_path, int(self.font_size * 0.6))
        except:
            font_small = font_regular
            
        for line in lines:
            self.draw_math_line(draw, line, margin_left, current_y, font_regular, font_small)
            current_y += line_height
            
        img.save(output_file)
        return output_file

    def draw_math_line(self, draw, line_text, start_x, start_y, font_reg, font_sup):
        """
        Draws a line of text, handling basic math superscripts denoted by '^'.
        """
        cursor_x = start_x
        # Add random line wobble
        base_y = start_y + random.randint(-1, 2)
        
        i = 0
        while i < len(line_text):
            char = line_text[i]
            
            # Check for Superscript Trigger
            if char == '^':
                i += 1
                if i < len(line_text):
                    # Draw next char/sequence as superscript
                    # We assume superscript is the next immediate number or variable
                    # or a block in parens (simple handling for now: just next alphanumeric chunk)
                    sup_text = ""
                    while i < len(line_text) and (line_text[i].isalnum() or line_text[i] in "+-"):
                        sup_text += line_text[i]
                        i += 1
                    
                    # Draw Superscript
                    draw.text((cursor_x, base_y - self.font_size * 0.4), sup_text, font=font_sup, fill=(20, 20, 60))
                    cursor_x += font_sup.getlength(sup_text)
                    continue
                else:
                    # Trailing ^, just draw it
                    draw.text((cursor_x, base_y), char, font=font_reg, fill=(20, 20, 60))
                    cursor_x += font_reg.getlength(char)
                    i += 1
            else:
                # Operator Handling for Clarity
                if char in "+-=*/":
                    # Add extra spacing before operator
                    cursor_x += 5
                    
                    if char == '-':
                        # Draw a manual line for the minus sign to ensure visibility
                        # Calculate center line for the character height
                        line_y = base_y + self.font_size // 2
                        line_width = int(self.font_size * 0.6)
                        start_line_x = int(cursor_x)
                        end_line_x = start_line_x + line_width
                        
                        # Draw thick line
                        draw.line([(start_line_x, line_y), (end_line_x, line_y)], fill=(20, 20, 60), width=3)
                        
                        # Advance cursor manually since we didn't use draw.text
                        cursor_x += line_width
                    else:
                        draw.text((cursor_x, base_y), char, font=font_reg, fill=(20, 20, 60))
                        cursor_x += font_reg.getlength(char)
                    
                    # Add extra spacing after operator
                    cursor_x += 5
                    i += 1
                else:
                    # Regular Text
                    draw.text((cursor_x, base_y), char, font=font_reg, fill=(20, 20, 60))
                    cursor_x += font_reg.getlength(char)
                    i += 1

if __name__ == "__main__":
    renderer = HandwritingRenderer()
    renderer.render_text("Scientific Solver Output:\n\nIntegral of x^2 is x^3/3 + C\n\nThis looks like handwriting!")
