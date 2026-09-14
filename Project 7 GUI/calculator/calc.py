import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import math
import os

## TODO
#
# - Try out the program and figure out how the code works
#    - How is text added to the top white field when buttons are pressed?
#    - How is text added to the top white field when buttons are pressed?
#    - What does sticky="EW" do?
# - Make the buttons [2] and [3] work
# - Add buttons the numbers 4-9 and 0
# - Add subtraction, multiplication and division to the program
# - Add a [C] button to clear everything
# - Add a [CE] button to clear the last en (Clear Entry)

operand1 = ""
operand2 = "" 
operator = "" 
result = "" 
expression = ""
c = ""
ce = ""
def set_operand(x):
    global operand1, operand2
    if not operator:
        operand1 += x
    else:
        operand2 += x

    update_expression()


def set_operator(op):
    global operator
    if operand1:
        operator = op
    elif result:
        set_operand(result)
        operator = op
    else:
        tk.messagebox.showerror(title="Error", message="You can not input an operator without first inputting an operand!")

    update_expression()

def set_deletion(op):
    global operand1, operand2, operator, result
    c,ce=op
    if c:
        operand1 = ""
        operand2 = ""
        operator = ""
        result = ""

        
    if ce: 
        if operand1 and operator:
            operand2 = ""
        if operand1 and not operator:
            operand1 = ""
            operand2 = ""
            operator = ""
        if operand2:
            operand2 = ""

    update_expression()

def eval_expr():
    global operand1, operand2, operator, result
    op1 = float(operand1)
    op2 = float(operand2)
    if operator == "+":
        result = op1 + op2
    if operator == "-":
        result = op1 - op2
    if operator == "x":
        result = op1 * op2
    if operator == "/":
        result = op1 / op2
    if operator == "sqrt()":
        op2 = 0
        result = math.sqrt(op1)+op2
    if operator == "^":
        result = op1 ** op2

    if notation == "Mathematical":
        result = str(result)
    if notation == "Scientific":
        result = str(f"{result:.2e}")
    if notation == "Chemical":
        suicide = True

    operand1 = ""
    operand2 = ""
    operator = ""

    update_expression()


def update_expression():
    expression = ""
    if operand1:
        expression += operand1
    if operator:
        expression += operator 
    if operand2:
        expression += operand2
    if not expression and result:
        expression = result

    expression_label.config(text=expression) 

def mode_selection():
    selected_value = notation.get()
    label.config(text=f"Selected: {selected_value}")


root = tk.Tk()
root.title("Calculator")
root.geometry("600x600")
# logo = tk.PhotoImage(file=os.path.abspath('logo.png'))
# root.iconphoto(False, logo)
# root.wm_iconphoto(False, logo) 
# Create a variable to hold the selected value
# Frame for mode selection

# Frame for calculator buttons
frame = ttk.Frame(root, padding=10, relief="solid", borderwidth=1)
frame.grid(column=0, row=1, sticky="EW")

notation = tk.StringVar(value="Mathematical")

expression_label = ttk.Label(frame, text=expression, background="#FFFFFF")
expression_label.grid(column=0, row=0, columnspan=4, sticky="NEW")

but1 = ttk.Button(frame, text="1", command=lambda: set_operand("1"))
but1.grid(column=0, row=1)

butc = ttk.Button(frame, text="CE", command=lambda: set_deletion("ce"))
butc.grid(column=4, row=2)

butca = ttk.Button(frame, text="C", command=lambda: set_deletion("c"))
butca.grid(column=4, row=1)

but2 = ttk.Button(frame, text="2", command=lambda: set_operand("2"))
but2.grid(column=1, row=1)

but3 = ttk.Button(frame, text="3", command=lambda: set_operand("3"))
but3.grid(column=2, row=1)

butplus = ttk.Button(frame, text="+", command=lambda: set_operator("+"))
butplus.grid(column=3, row=1)

butmin = ttk.Button(frame, text="-", command=lambda: set_operator("-"))
butmin.grid(column=3, row=2)

butcalc = ttk.Button(frame, text="=", command=eval_expr)
butcalc.grid(column=3, row=5)

but4 = ttk.Button(frame, text="4", command=lambda: set_operand("4"))
but4.grid(column=0, row=2)

but5 = ttk.Button(frame, text="5", command=lambda: set_operand("5"))
but5.grid(column=1, row=2)

but6 = ttk.Button(frame, text="6", command=lambda: set_operand("6"))
but6.grid(column=2, row=2)

but7 = ttk.Button(frame, text="7", command=lambda: set_operand("7"))
but7.grid(column=0, row=3)

but8 = ttk.Button(frame, text="8", command=lambda: set_operand("8"))
but8.grid(column=1, row=3)

but9 = ttk.Button(frame, text="9", command=lambda: set_operand("9"))
but9.grid(column=2, row=3)

but0 = ttk.Button(frame, text="0", command=lambda: set_operand("0"))
but0.grid(column=1, row=4)

butsqrt = ttk.Button(frame, text="sqrt()", command=lambda: set_operator("sqrt()"))
butsqrt.grid(column=2, row=4)

butdivide = ttk.Button(frame, text="/", command=lambda: set_operator("/"))
butdivide.grid(column=3, row=4)

butmult = ttk.Button(frame, text="x", command=lambda: set_operator("x"))
butmult.grid(column=3, row=3)

butlift = ttk.Button(frame, text="^", command=lambda: set_operator("^"))
butlift.grid(column=4, row=3)

# Create radio buttons
radio1 = tk.Radiobutton(frame, text="Scientific", variable=notation, value="Scientific", command=mode_selection)
radio2 = tk.Radiobutton(frame, text="Mathematical", variable=notation, value="Mathematical", command=mode_selection)
radio3 = tk.Radiobutton(frame, text="Chemical", variable=notation, value="Chemical", command=mode_selection)

# Place radio buttons in the grid
radio1.grid(row=1, column=7, padx=10, pady=5)
radio2.grid(row=2, column=7, padx=10, pady=5)
radio3.grid(row=3, column=7, padx=10, pady=5)

# Label to display the selected option
label = tk.Label(frame, text="Selected: Standard (Math)")
label.grid(row=4, column=7, padx=10, pady=10)
#label to display notation options
label2 = tk.Label(frame, text="Notation form")
label2.grid(row=0, column=7, padx=10, pady=10)

root.mainloop()
