import tkinter as tk
from tkinter import messagebox
import math
import re

class Calculator:
    def __init__(self, master):
        self.master = master
        self.master.title('Scientific Calculator')
        self.master.geometry('500x650')
        self.master.resizable(False, False)
        
        # Configure style
        self.master.configure(bg='#f0f0f0')
        self.button_bg = '#e0e0e0'
        self.operator_bg = '#ff9800'
        self.function_bg = '#4caf50'
        self.clear_bg = '#f44336'
        self.equals_bg = '#2196f3'
        
        self.result_var = tk.StringVar()
        self.result_var.set('0')
        self.current_input = ''
        
        # Create display frame
        self.display_frame = tk.Frame(master, bg='#f0f0f0')
        self.display_frame.grid(row=0, column=0, columnspan=5, sticky='nsew')
        
        # Create input field
        self.input_field = tk.Entry(
            self.display_frame, 
            textvariable=self.result_var, 
            font=('Arial', 32), 
            bd=0,
            insertwidth=1, 
            width=14, 
            borderwidth=0,
            justify='right',
            readonlybackground='white',
            state='readonly'
        )
        self.input_field.pack(ipady=10, fill='both', expand=True)
        
        # Create buttons
        self.create_buttons()
        
        # Configure grid weights
        for i in range(1, 6):
            self.master.grid_rowconfigure(i, weight=1)
        for i in range(5):
            self.master.grid_columnconfigure(i, weight=1)
    
    def create_buttons(self):
        buttons = [
            ('C', self.clear_all, self.clear_bg), ('⌫', self.backspace, self.clear_bg), ('(', self.add_to_expression, self.operator_bg), (')', self.add_to_expression, self.operator_bg), ('/', self.add_operator, self.operator_bg),
            ('sin', self.add_trig_function, self.function_bg), ('7', self.add_digit, self.button_bg), ('8', self.add_digit, self.button_bg), ('9', self.add_digit, self.button_bg), ('*', self.add_operator, self.operator_bg),
            ('cos', self.add_trig_function, self.function_bg), ('4', self.add_digit, self.button_bg), ('5', self.add_digit, self.button_bg), ('6', self.add_digit, self.button_bg), ('-', self.add_operator, self.operator_bg),
            ('tan', self.add_trig_function, self.function_bg), ('1', self.add_digit, self.button_bg), ('2', self.add_digit, self.button_bg), ('3', self.add_digit, self.button_bg), ('+', self.add_operator, self.operator_bg),
            ('√', self.square_root, self.function_bg), ('^', self.add_operator, self.operator_bg), ('0', self.add_digit, self.button_bg), ('.', self.add_decimal, self.button_bg), ('=', self.calculate, self.equals_bg)
        ]
        
        row_val = 1
        col_val = 0
        
        for (text, command, bg) in buttons:
            action = lambda x=text, cmd=command: cmd(x)
            btn = tk.Button(
                self.master, 
                text=text, 
                padx=0, 
                pady=0, 
                font=('Arial', 18, 'bold'),
                command=action,
                bg=bg,
                fg='white' if bg in [self.operator_bg, self.function_bg, self.clear_bg, self.equals_bg] else 'black',
                activebackground='#bdbdbd',
                bd=0,
                highlightthickness=0,
                relief='ridge'
            )
            btn.grid(row=row_val, column=col_val, sticky='nsew', padx=1, pady=1)
            col_val += 1
            if col_val > 4:
                col_val = 0
                row_val += 1
    
    def update_display(self):
        """Update the display with current input"""
        display_text = self.current_input if self.current_input else '0'
        self.result_var.set(display_text)
    
    def add_digit(self, digit):
        """Add a digit to the current input"""
        if self.current_input == '0' and digit != '0':
            self.current_input = digit
        else:
            self.current_input += digit
        self.update_display()
    
    def add_decimal(self, decimal):
        """Add a decimal point to the current number"""
        if not self.current_input:
            self.current_input = '0.'
        elif '.' not in self.current_input.split()[-1]:
            self.current_input += '.'
        self.update_display()
    
    def add_operator(self, operator):
        """Add an operator to the expression"""
        if not self.current_input and operator == '-':
            self.current_input = '-'
        elif self.current_input:
            # Replace the last operator if there is one
            if self.current_input[-1] in '+-*/^':
                self.current_input = self.current_input[:-1] + operator
            else:
                self.current_input += operator
        self.update_display()
    
    def add_to_expression(self, char):
        """Add parentheses or other characters to the expression"""
        self.current_input += char
        self.update_display()
    
    def add_trig_function(self, func):
        """Add trigonometric function to the expression"""
        self.current_input += func + '('
        self.update_display()
    
    def clear_all(self, _):
        """Clear all input"""
        self.current_input = ''
        self.update_display()
    
    def backspace(self, _):
        """Remove the last character"""
        if self.current_input:
            self.current_input = self.current_input[:-1]
            if not self.current_input:
                self.current_input = '0'
        self.update_display()
    
    def square_root(self, _):
        """Calculate square root of current number"""
        try:
            value = float(self.current_input or '0')
            if value < 0:
                self.show_error("Cannot calculate square root of negative number")
                return
            result = math.sqrt(value)
            self.current_input = str(result)
            self.update_display()
        except ValueError:
            self.show_error("Invalid input for square root")
    
    def calculate(self, _):
        """Evaluate the expression including trigonometric functions"""
        if not self.current_input:
            return
        
        try:
            # Replace ^ with ** for exponentiation
            expression = self.current_input.replace('^', '**')
            
            # Process trigonometric functions
            expression = self.process_trig_functions(expression)
            
            # Evaluate the expression
            result = eval(expression, {'__builtins__': None}, {
                'sqrt': math.sqrt,
                'pi': math.pi,
                'e': math.e
            })
            
            # Format the result
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    # Limit to 10 decimal places to avoid floating point weirdness
                    result = round(result, 10)
            
            self.current_input = str(result)
            self.update_display()
            
        except ZeroDivisionError:
            self.show_error("Division by zero")
            self.current_input = ''
            self.update_display()
        except (ValueError, SyntaxError):
            self.show_error("Invalid expression")
        except Exception as e:
            self.show_error(f"Calculation error: {str(e)}")
    
    def process_trig_functions(self, expression):
        """Process trigonometric functions in the expression"""
        # Find all trigonometric functions in the expression
        trig_pattern = re.compile(r'(sin|cos|tan)\(([^)]*)\)')
        
        def trig_replacer(match):
            func = match.group(1)
            angle_expr = match.group(2)
            try:
                # Evaluate the angle expression first
                angle_value = eval(angle_expr, {'__builtins__': None}, {
                    'pi': math.pi,
                    'e': math.e,
                    'sqrt': math.sqrt
                })
                # Convert to radians and apply the trig function
                if func == 'sin':
                    return str(math.sin(math.radians(angle_value)))
                elif func == 'cos':
                    return str(math.cos(math.radians(angle_value)))
                elif func == 'tan':
                    tan_val = math.tan(math.radians(angle_value))
                    if abs(tan_val) > 1e10:  # Handle asymptotes
                        raise ValueError("Tangent undefined for this angle")
                    return str(tan_val)
            except Exception as e:
                raise ValueError(f"Invalid angle expression for {func} function: {str(e)}")
        
        # Replace all trig functions with their calculated values
        while True:
            new_expression = trig_pattern.sub(trig_replacer, expression)
            if new_expression == expression:
                break
            expression = new_expression
        
        return expression
    
    def show_error(self, message):
        """Show error message to user"""
        messagebox.showerror('Error', message)
        self.current_input = ''
        self.update_display()

if __name__ == '__main__':
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()