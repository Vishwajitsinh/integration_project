import customtkinter as ctk
from PIL import Image
import threading
import os
from scientific_core import ScientificSolver
from handwriting_renderer import HandwritingRenderer

ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class AdvancedSolverApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Theme & Color Configuration
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")
        
        # Professional Color Palette
        self.colors = {
            "bg_main": "#121212",       # Very dark background
            "bg_card": "#1E1E1E",       # Card surface
            "accent": "#3B8ED0",        # Professional Blue
            "text_main": "#E0E0E0",     # Light text
            "text_dim": "#A0A0A0"       # Dim text
        }

        # Window Setup
        self.title("Scientific Solver Pro")
        self.geometry("1100x800")
        self.configure(fg_color=self.colors["bg_main"])
        
        # Grid Configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1) # Output area expands

        self.solver = ScientificSolver()
        self.renderer = HandwritingRenderer()
        
        self.create_widgets()
        
    def create_widgets(self):
        # 1. Header Section (Minimalist)
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=30, pady=(30, 20))
        
        self.title_label = ctk.CTkLabel(self.header_frame, text="Integration Solver", 
                                      font=ctk.CTkFont(family="Roboto Medium", size=28, weight="bold"),
                                      text_color=self.colors["text_main"])
        self.title_label.pack(side="left")

        self.subtitle_label = ctk.CTkLabel(self.header_frame, text=" | Scientist Level Symbolic Engine", 
                                         font=ctk.CTkFont(family="Roboto", size=16),
                                         text_color=self.colors["text_dim"])
        self.subtitle_label.pack(side="left", padx=10, pady=(10, 0))

        # 2. Input Section (Floating Card)
        self.input_card = ctk.CTkFrame(self, fg_color=self.colors["bg_card"], corner_radius=15, border_width=1, border_color="#333333")
        self.input_card.grid(row=1, column=0, sticky="ew", padx=30, pady=(0, 20))
        self.input_card.grid_columnconfigure(0, weight=1)
        
        self.entry = ctk.CTkEntry(self.input_card, placeholder_text="Enter math problem (e.g. integrate x^2 * sin(x))",
                                height=50, border_width=0, fg_color="#2B2B2B",
                                font=ctk.CTkFont(family="Consolas", size=16), text_color="white")
        self.entry.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        self.entry.bind("<Return>", self.on_solve)
        
        self.solve_btn = ctk.CTkButton(self.input_card, text="SOLVE", command=self.on_solve,
                                     height=50, width=120, fg_color=self.colors["accent"], hover_color="#2C6FA0",
                                     font=ctk.CTkFont(size=14, weight="bold"))
        self.solve_btn.grid(row=0, column=1, padx=(0, 20), pady=20)

        # 3. Output Section (Split View)
        self.output_container = ctk.CTkFrame(self, fg_color="transparent")
        self.output_container.grid(row=2, column=0, sticky="nsew", padx=30, pady=(0, 30))
        self.output_container.grid_columnconfigure(0, weight=4) # Text side usually needs less width, but let's give it 40%
        self.output_container.grid_columnconfigure(1, weight=6) # Handwriting side gets 60%
        self.output_container.grid_rowconfigure(0, weight=1)

        # Left: Analysis Card
        self.analysis_card = ctk.CTkFrame(self.output_container, fg_color=self.colors["bg_card"], corner_radius=15, border_width=1, border_color="#333333")
        self.analysis_card.grid(row=0, column=0, sticky="nsew", padx=(0, 15), pady=0)
        
        ctk.CTkLabel(self.analysis_card, text="ANALYSIS", text_color=self.colors["text_dim"], 
                   font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=20, pady=(15, 10))
        
        self.text_output = ctk.CTkLabel(self.analysis_card, text="", justify="left", anchor="nw",
                                      font=ctk.CTkFont(family="Consolas", size=14), wraplength=350,
                                      text_color="#DDDDDD")
        self.text_output.pack(expand=True, fill="both", padx=20, pady=(0, 20))

        # Right: Handwriting Card
        self.handwriting_card = ctk.CTkFrame(self.output_container, fg_color="#FDFCF5", corner_radius=15) # Paper-like BG
        self.handwriting_card.grid(row=0, column=1, sticky="nsew", padx=(15, 0), pady=0)
        
        self.image_label = ctk.CTkLabel(self.handwriting_card, text="")
        self.image_label.pack(expand=True, fill="both", padx=10, pady=10)
        
    def on_solve(self, event=None):
        query = self.entry.get()
        if not query: return
        
        self.solve_btn.configure(state="disabled", text="Solving...")
        self.text_output.configure(text="Processing...")
        
        # Run in thread preventing UI freeze
        threading.Thread(target=self.process_math, args=(query,)).start()

    def process_math(self, query):
        try:
            # 1. Solve
            print(f"Solving: {query}")
            result = self.solver.process_query(query) # Now returns a DICT
            
            display_text = result['display']
            handwriting_text = result['handwriting']
            
            # 2. Render Handwritting
            print("Rendering handwriting...")
            output_image_path = os.path.join(os.getcwd(), "last_solution.png")
            self.renderer.render_text(handwriting_text, output_image_path)
            
            # 3. Update UI
            self.after(0, lambda: self.update_ui(display_text, output_image_path))
            
        except Exception as e:
            self.after(0, lambda: self.update_ui(f"Error: {str(e)}", None))

    def update_ui(self, text_result, image_path):
        self.solve_btn.configure(state="normal", text="SOLVE")
        self.text_output.configure(text=text_result)
        
        if image_path and os.path.exists(image_path):
            pil_img = Image.open(image_path)
            
            # Scale image to fit the frame
            # Force update via update_idletasks to get accurate dimensions if needed, 
            # though might flicker. Trust current geometry usually.
            frame_height = self.handwriting_card.winfo_height()
            frame_width = self.handwriting_card.winfo_width()
            
            # Safe defaults
            if frame_width < 100: frame_width = 500
            if frame_height < 100: frame_height = 500
            
            # Calculate scaling
            ratio = min((frame_width - 40) / pil_img.width, (frame_height - 40) / pil_img.height)
            ratio = min(ratio, 1.0) # Do not upscale too much
            
            new_size = (int(pil_img.width * ratio), int(pil_img.height * ratio))
            
            ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=new_size)
            self.image_label.configure(image=ctk_img, text="")
            self.image_label.image = ctk_img # keep reference
            
        else:
            self.image_label.configure(text="No visualization available.")

if __name__ == "__main__":
    app = AdvancedSolverApp()
    app.mainloop()
