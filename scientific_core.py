import sympy
from sympy import symbols, integrate, diff, solve, limit, oo, simplify, Matrix, latex, pretty
from sympy.integrals.manualintegrate import integral_steps, manualintegrate
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

    def format_steps(self, rule):
        """Recursively formatting the rule tree into strings."""
        steps = []
        name = rule.__class__.__name__.replace("Rule", "")
        
        # Simple formatting logic
        if name == "Power":
            steps.append(f"Apply Power Rule on {rule.integrand}")
        elif name == "Add":
            steps.append(f"Split integration (Sum Rule)")
            for sub in rule.substeps:
                steps.extend(self.format_steps(sub))
        elif name == "ConstantTimes":
            steps.append(f"Factor out constant: {rule.constant}")
            steps.extend(self.format_steps(rule.substep))
        elif name == "Parts":
            steps.append(f"Integration by Parts: u={rule.u}, dv={rule.dv}")
            steps.extend(self.format_steps(rule.substep)) # recursive part
        elif name == "U":
            steps.append(f"U-Substitution: u={rule.u_func}")
            steps.extend(self.format_steps(rule.substep))
        else:
            steps.append(f"Apply {name} Rule on {rule.integrand}")
            
        return steps

    def sanitize_output(self, text):
        """Helper to make output 'human' readable (e.g. ^ instead of **)."""
        if not text: return ""
        return text.replace("**", "^")

    def process_query(self, query):
        """
        Identify the intent of the query and solve it.
        Returns a DICTIONARY: {'display': str, 'handwriting': str}
        """
        query = query.lower()
        result = {}
        
        try:
            if "integ" in query: 
                result = self.handle_integration(query)
            elif "deriv" in query or "diff" in query:
                result = self.handle_differentiation(query)
            elif "lim" in query:
                result = self.handle_limit(query)
            elif "solv" in query or "=" in query:
                result = self.handle_solve(query)
            elif "simp" in query:
                result = self.handle_simplify(query)
            else:
                result = self.handle_simplify(query)
                
            return result
        except Exception as e:
            err_msg = f"Error processing query: {str(e)}\nPlease try standard math notation."
            return {'display': err_msg, 'handwriting': "Error in calculation."}

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
        if not expr: return {'display': "Could not understand the function.", 'handwriting': "Parse Error"}
        
        # Step-by-step for indefinite integration
        steps_text = ""
        try:
            steps = integral_steps(expr, self.x)
            step_list = self.format_steps(steps)
            steps_text = "\n\nSteps:\n" + "\n".join([f"{i+1}. {s}" for i, s in enumerate(step_list)])
        except:
            steps_text = "\n(Detailed steps not available for this integral)"

        if limits:
            result = integrate(expr, limits)
            # Use str() instead of pretty() to keep it on one line for the GUI text
            display = self.sanitize_output(f"Definite Integral of {expr}\nfrom {limits[1]} to {limits[2]}:\n\n= {result}\n\n(Approx: {result.evalf()}){steps_text}")
            
            # Simple ASCII for handwriting
            handwriting = f"Integral of {expr} from {limits[1]} to {limits[2]}:\n\n{steps_text}\n\n= {result}"
            handwriting = self.sanitize_output(handwriting) # Normalize for renderer
            
            return {'display': display, 'handwriting': handwriting}
        else:
            result = integrate(expr, self.x)
            # Use str() instead of pretty() to keep it on one line for the GUI text
            display = self.sanitize_output(f"Indefinite Integral of {expr} dx:\n\n= {result} + C{steps_text}")
            
            # Simple ASCII for handwriting
            handwriting = f"Integral of {expr} dx:\n\n{steps_text}\n\n= {result} + C"
            handwriting = self.sanitize_output(handwriting) # Normalize for renderer
            
            return {'display': display, 'handwriting': handwriting}

    def handle_differentiation(self, query):
        func_str = self.extract_func(query, ["differentiate", "derivative", "derive", "diff"])
        expr = self.parse_input(func_str)
        if not expr: return {'display': "Could not understand the function.", 'handwriting': "Parse Error"}
        
        result = diff(expr, self.x)
        display = self.sanitize_output(f"Derivative of {expr} with respect to x:\n\n= {result}")
        handwriting = f"Derivative of {expr}:\n\n= {result}"
        handwriting = self.sanitize_output(handwriting)
        return {'display': display, 'handwriting': handwriting}

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
        
        if not expr: return {'display': "Could not parse function for limit.", 'handwriting': "Parse Error"}
        
        res = limit(expr, self.x, target_val)
        display = self.sanitize_output(f"Limit of {expr} as x -> {target_val}:\n\n= {res}")
        handwriting = f"Limit of {expr} as x -> {target_val}:\n\n= {res}"
        handwriting = self.sanitize_output(handwriting)
        return {'display': display, 'handwriting': handwriting}

    def handle_solve(self, query):
        # solves for x = 0 by default if no = sign
        # But if there is an =, we split
        if "=" in query:
            sides = query.split("=")
            # clean the "solve" keyword from lhs if present
            clean_lhs = self.extract_func(sides[0], ["solve", "equation", "for", "find"])
            lhs = self.parse_input(clean_lhs)
            rhs = self.parse_input(sides[1])
            if lhs is None or rhs is None: return {'display': "Could not parse equation sides.", 'handwriting': "Parse Error"}
            expr = lhs - rhs
        else:
            clean = self.extract_func(query, ["solve", "equation", "for", "x", "zeros", "roots"])
            expr = self.parse_input(clean)
            
        if expr is None: return {'display': "Could not parse equation.", 'handwriting': "Parse Error"}
        
        solution = solve(expr, self.x)
        display = self.sanitize_output(f"Solution for {expr} = 0:\n\n{solution}")
        handwriting = f"Solution for {expr} = 0:\n\n{solution}"
        handwriting = self.sanitize_output(handwriting)
        return {'display': display, 'handwriting': handwriting}

    def handle_simplify(self, query):
        clean = self.extract_func(query, ["simplify", "evaluate", "calc"])
        expr = self.parse_input(clean)
        
        if not expr:
            # Maybe it's a matrix? "[[1,2],[3,4]]"
            try:
                mat = Matrix(eval(clean)) # risky eval but local usage
                display = f"Matrix:\n{pretty(mat)}\n\nDeterminant: {mat.det()}\nInverse:\n{pretty(mat.inv() if mat.det() != 0 else 'Singular')}"
                handwriting = f"Matrix Analysis:\nDet: {mat.det()}"
                return {'display': display, 'handwriting': handwriting}
            except:
                return {'display': "Could not understand expression.", 'handwriting': "Error"}
        
        res = simplify(expr)
        display = self.sanitize_output(f"Simplified form of {expr}:\n\n= {res}")
        handwriting = f"Simplified {expr}:\n\n= {res}"
        handwriting = self.sanitize_output(handwriting)
        return {'display': display, 'handwriting': handwriting}

if __name__ == "__main__":
    solver = ScientificSolver()
    print(solver.process_query("integrate x^2 + sin(x)"))
    print(solver.process_query("solve x^2 - 4 = 0"))
