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

        # Window Setup
        self.title("Advanced Scientific Solver - Version 2.0")
        self.geometry("1000x800")
        
        # Grid Configuration
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Core Modules
        self.solver = ScientificSolver()
        self.renderer = HandwritingRenderer() # Defaults to handwriting font
        
        self.create_widgets()
        
    def create_widgets(self):
        # Header
        self.header_frame = ctk.CTkFrame(self, corner_radius=0)
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        
        self.header_label = ctk.CTkLabel(self.header_frame, text="SCIENTIFIC INTEGRATION SOLVER", 
                                       font=ctk.CTkFont(size=24, weight="bold"))
        self.header_label.pack(pady=15, padx=20)
        
        # Input Section
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=20, pady=20)
        
        self.input_label = ctk.CTkLabel(self.input_frame, text="Enter Problem (e.g., 'Integrate x^2 + sin(x)'):", 
                                      font=ctk.CTkFont(size=14))
        self.input_label.pack(anchor="w", padx=15, pady=(10, 0))
        
        self.entry = ctk.CTkEntry(self.input_frame, placeholder_text="Type your math query here...", 
                                height=40, font=ctk.CTkFont(size=16))
        self.entry.pack(fill="x", padx=15, pady=10)
        self.entry.bind("<Return>", self.on_solve)
        
        self.solve_btn = ctk.CTkButton(self.input_frame, text="SOLVE PROBLEM", command=self.on_solve, 
                                     font=ctk.CTkFont(size=15, weight="bold"), height=40)
        self.solve_btn.pack(pady=(0, 15))

        # Output Section
        # Split into Left (Raw Text) and Right (Handwritten Paper)
        self.output_container = ctk.CTkFrame(self)
        self.output_container.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=20, pady=(0, 20))
        
        self.output_container.grid_columnconfigure(0, weight=1)
        self.output_container.grid_columnconfigure(1, weight=1)
        self.output_container.grid_rowconfigure(0, weight=1)

        # Left: Raw Output
        self.raw_frame = ctk.CTkScrollableFrame(self.output_container, label_text="Step-by-Step Analysis")
        self.raw_frame.grid(row=0, column=0, sticky="nsew", padx=(5, 5), pady=5)
        
        self.text_output = ctk.CTkLabel(self.raw_frame, text="Waiting for input...", justify="left", 
                                      font=ctk.CTkFont(family="Consolas", size=14), wraplength=400)
        self.text_output.pack(anchor="nw", ipadx=10, ipady=10)

        # Right: Handwriting View
        self.handwriting_frame = ctk.CTkFrame(self.output_container)
        self.handwriting_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 5), pady=5)
        
        self.image_label = ctk.CTkLabel(self.handwriting_frame, text="[Handwritten Output Will Appear Here]")
        self.image_label.pack(expand=True, fill="both")
        
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
            result_text = self.solver.process_query(query)
            
            # 2. Render Handwritting
            print("Rendering handwriting...")
            # Generate a cleaned filename
            output_image_path = os.path.join(os.getcwd(), "last_solution.png")
            self.renderer.render_text(result_text, output_image_path)
            
            # 3. Update UI
            self.after(0, lambda: self.update_ui(result_text, output_image_path))
            
        except Exception as e:
            self.after(0, lambda: self.update_ui(f"Error: {str(e)}", None))

    def update_ui(self, text_result, image_path):
        self.solve_btn.configure(state="normal", text="SOLVE PROBLEM")
        self.text_output.configure(text=text_result)
        
        if image_path and os.path.exists(image_path):
            pil_img = Image.open(image_path)
            
            # Scale image to fit the frame
            frame_height = self.handwriting_frame.winfo_height()
            frame_width = self.handwriting_frame.winfo_width()
            
            # Maintain aspect ratio
            # Use 400 as a safe default if window causes 1
            if frame_width < 100: frame_width = 400 
            
            ratio = min(frame_width / pil_img.width, frame_height / pil_img.height) if frame_height > 100 else 0.5
            new_size = (int(pil_img.width * ratio * 0.9), int(pil_img.height * ratio * 0.9))
            
            ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=new_size)
            self.image_label.configure(image=ctk_img, text="")
            self.image_label.image = ctk_img # keep reference
            
        else:
            self.image_label.configure(text="Could not render image.")

if __name__ == "__main__":
    app = AdvancedSolverApp()
    app.mainloop()
