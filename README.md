# Advanced Scientific Solver & Handwriting Generator
> A symbolic mathematics engine capable of solving calculus problems and rendering the output as realistic, human-like handwriting.

![Math](https://img.shields.io/badge/Engine-SymPy-orange)
![Render](https://img.shields.io/badge/Render-Handwriting%20Synthesis-white)
![GUI](https://img.shields.io/badge/Interface-CustomTkinter-blue)

## 📐 Overview
This project combines symbolic computation with procedural image generation. It serves as a comprehensive tool for students and researchers to not only solve complex equations but to generate "proof-of-work" style solution papers that look like they were written by hand.

### Core Modules
1.  **Symbolic Math Engine (`scientific_core.py`)**:
    *   Powered by `SymPy`.
    *   Solves Integrals (Definite/Indefinite), Derivatives, Limits, and Differential Equations.
    *   Supports step-by-step logic.

2.  **Handwriting Synthesizer (`handwriting_renderer.py`)**:
    *   Takes LaTeX/Text output and maps it to randomized human handwriting fonts.
    *   Adds subtle noise, rotation, and ink-bleed effects for realism.

3.  **Modern GUI (`advanced_solver_gui.py`)**:
    *   A sleek, dark-themed interface built with `CustomTkinter`.
    *   Real-time split-pane view: Input/Logic on the left, Rendered "Paper" on the right.

## 🚀 Usage

1.  **Install Requirements**
    ```bash
    pip install sympy pillow customtkinter
    ```

2.  **Launch the Solver**
    ```bash
    python advanced_solver_gui.py
    ```

3.  **Input Commands**:
    *   `integrate x^2 * sin(x)`
    *   `derive tan(x)`
    *   `solve x^2 - 5*x + 6 = 0`

4.  **Export**: Click the save button to export your handwritten solution as a `.png`.

---
*From digital logic to analog aesthetics.*
