# Advanced Scientific Solver & Handwriting Generator

This project has been upgraded to a "Scientist Level" solver with a professional GUI and handwriting generation.

## Features
- **Advanced Math Engine**: Solves integrals, derivatives, limits, and algebraic equations using symbolic mathematics (SymPy).
- **Handwriting Output**: Generates a "written on paper" image of the solution using a handwriting style font.
- **Modern GUI**: Built with CustomTkinter for a sleek, dark-mode scientific interface.

## How to Run
1. Ensure you have the required libraries:
   ```bash
   pip install sympy pillow customtkinter
   ```
   *(Note: These are pre-installed in this environment)*

2. Run the main application:
   ```bash
   python advanced_solver_gui.py
   ```

## Usage
- Enter your problem in natural syntax, e.g.:
  - `integrate x^2 * sin(x)`
  - `derive tan(x)`
  - `limit sin(x)/x as x -> 0`
  - `solve x^2 - 5*x + 6 = 0`
- Click **SOLVE PROBLEM**.
- View the step-by-step text on the left and the handwritten note on the right.

## Files
- `advanced_solver_gui.py`: The entry point and GUI.
- `scientific_core.py`: The backend logic for parsing and math.
- `handwriting_renderer.py`: The image generation logic.
