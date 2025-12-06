import sympy
from sympy import symbols, integrate, pretty

def solve_integration():
    print("--- Professional Integration Solver ---")
    x = symbols('x')
    
    print("Enter your function to integrate (e.g., 'x**2 + sin(x)'):")
    # In a real GUI app we would take this from args, but for CLI:
    expr_str = input("f(x) = ").strip()
    
    try:
        # Parse expression
        expr = sympy.sympify(expr_str)
        
        # Calculate Indefinite Integral
        indefinite = integrate(expr, x)
        
        print("\n--- Result ---")
        print(f"Indefinite Integral ∫ ({expr_str}) dx =")
        print(pretty(indefinite))
        
        # Check if user wants definite integral
        print("\nCalculate definite integral? (y/n)")
        if input().lower() == 'y':
            a = float(input("Lower limit (a): "))
            b = float(input("Upper limit (b): "))
            definite = integrate(expr, (x, a, b))
            print(f"\nDefinite Integral from {a} to {b} = {definite}")
            print(f"Approx Value: {definite.evalf()}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    solve_integration()
