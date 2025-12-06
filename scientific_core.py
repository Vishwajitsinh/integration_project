import sympy
from sympy import symbols, integrate, diff, solve, limit, oo, simplify, Matrix, latex, pretty
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

class ScientificSolver:
    def __init__(self):
        self.x, self.y, self.z, self.t = symbols('x y z t')
        self.transformations = (standard_transformations + (implicit_multiplication_application,))

    def parse_input(self, expression_str):
        """Attempts to cleaner parse variable expression."""
        try:
            # Handle common replacements for natural language feel
            expression_str = expression_str.replace('^', '**')
            
            # Create a context with all sympy functions
            local_dict = {
                'x': self.x, 'y': self.y, 'z': self.z, 't': self.t,
                'sin': sympy.sin, 'cos': sympy.cos, 'tan': sympy.tan,
                'exp': sympy.exp, 'log': sympy.log, 'ln': sympy.log,
                'sqrt': sympy.sqrt, 'pi': sympy.pi, 'e': sympy.E,
                'inf': oo
            }
            
            return parse_expr(expression_str, local_dict=local_dict, transformations=self.transformations)
        except Exception as e:
            # Try a second pass assuming implied multiplication is the issue or unknown symbol
            try:
                # Fallback: let sympy auto-create symbols for unknown vars
                return parse_expr(expression_str, transformations=self.transformations)
            except:
                print(f"DEBUG: Parse error on '{expression_str}': {e}")
                return None

    def process_query(self, query):
        """
        Identify the intent of the query and solve it.
        Supported keywords: integra, deriv, diff, solve, limit, simplif, matrix, factor
        """
        query = query.lower()
        
        try:
            if "integ" in query: # integrate, integration
                return self.handle_integration(query)
            elif "deriv" in query or "diff" in query:
                return self.handle_differentiation(query)
            elif "lim" in query:
                return self.handle_limit(query)
            elif "solv" in query or "=" in query:
                return self.handle_solve(query)
            elif "simp" in query:
                return self.handle_simplify(query)
            else:
                # Default to simplify/evaluate
                return self.handle_simplify(query)
        except Exception as e:
            return f"Error processing query: {str(e)}\nPlease try standard math notation."

    def extract_func(self, query, keywords):
        # Naive extraction: remove keywords and whitespace, assume rest is math
        clean = query
        for k in keywords:
            clean = clean.replace(k, "")
        
        # Remove common prepositions like "of", "the"
        for word in [" of ", " the ", " for ", " with ", " respect ", " to "]:
            clean = clean.replace(word, " ")
            
        return clean.strip()

    def handle_integration(self, query):
        func_str = self.extract_func(query, ["integration", "integrate", "integral"])
        
        # Check for definite integral syntax "from a to b"
        expr = None
        limits = None
        
        if "from" in func_str and "to" in func_str:
            parts = func_str.split("from")
            expr_part = parts[0]
            limit_parts = parts[1].split("to")
            try:
                a = float(limit_parts[0])
                b = float(limit_parts[1])
                limits = (self.x, a, b)
                func_str = expr_part
            except:
                pass 
                
        expr = self.parse_input(func_str)
        if not expr: return "Could not understand the function."
        
        if limits:
            result = integrate(expr, limits)
            return f"Definite Integral of {pretty(expr)}\nfrom {limits[1]} to {limits[2]}:\n\n= {pretty(result)}\n\n(Approx: {result.evalf()})"
        else:
            result = integrate(expr, self.x)
            return f"Indefinite Integral of {pretty(expr)} dx:\n\n= {pretty(result)} + C"

    def handle_differentiation(self, query):
        func_str = self.extract_func(query, ["differentiate", "derivative", "derive", "diff"])
        expr = self.parse_input(func_str)
        if not expr: return "Could not understand the function."
        
        result = diff(expr, self.x)
        return f"Derivative of {pretty(expr)} with respect to x:\n\n= {pretty(result)}"

    def handle_limit(self, query):
        # Format: limit of f(x) as x -> a
        # Simplified parser
        if "->" in query:
            parts = query.split("->")
            val_str = parts[1].strip().split()[0] # take first word/number
        elif "approach" in query:
            parts = query.split("approach")
            val_str = parts[1].strip().split(" ")[-1]
        else:
            val_str = "0" # default
            
        target_val = oo if "inf" in val_str else float(val_str) if val_str.replace('.','',1).isdigit() else 0
        
        func_str = self.extract_func(query, ["limit", "approaches", "as", "x", "->", val_str])
        expr = self.parse_input(func_str)
        
        res = limit(expr, self.x, target_val)
        return f"Limit of {pretty(expr)} as x -> {target_val}:\n\n= {pretty(res)}"

    def handle_solve(self, query):
        # solves for x = 0 by default if no = sign
        # But if there is an =, we split
        if "=" in query:
            sides = query.split("=")
            lhs = self.parse_input(sides[0])
            rhs = self.parse_input(sides[1])
            expr = lhs - rhs
        else:
            clean = self.extract_func(query, ["solve", "equation", "for", "x", "zeros", "roots"])
            expr = self.parse_input(clean)
            
        if not expr: return "Could not parse equation."
        
        solution = solve(expr, self.x)
        return f"Solution for {pretty(expr)} = 0:\n\n{pretty(solution)}"

    def handle_simplify(self, query):
        clean = self.extract_func(query, ["simplify", "evaluate", "calc"])
        expr = self.parse_input(clean)
        
        if not expr:
            # Maybe it's a matrix? "[[1,2],[3,4]]"
            try:
                mat = Matrix(eval(clean)) # risky eval but local usage
                return f"Matrix:\n{pretty(mat)}\n\nDeterminant: {mat.det()}\nInverse:\n{pretty(mat.inv() if mat.det() != 0 else 'Singular')}"
            except:
                return "Could not understand expression."
        
        res = simplify(expr)
        return f"Simplified form of {pretty(expr)}:\n\n= {pretty(res)}"

if __name__ == "__main__":
    solver = ScientificSolver()
    print(solver.process_query("integrate x^2 + sin(x)"))
    print(solver.process_query("solve x^2 - 4 = 0"))
