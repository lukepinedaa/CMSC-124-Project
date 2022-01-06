# This is the program for semantic analysis
# Accepts the result of the lexer as a parameter
from tkinter import *
code = "" # global variable that will hold the code to be interpreted
isDeclaring = False
isMultipleLineRequired = False
isPrinting = False
printMe = ""

# for the symbol table
symbol_table = {} # symbol table (list of dictionaries)

# executes the code 
def execute():
    global code, isDeclaring, isMultipleLineRequired
    exec(code)
    isDeclaring = False
    isMultipleLineRequired = False

# for printing to console
def printToConsole(s,terminal):
    s = str(s)
    terminal.config(state=NORMAL)
    terminal.insert(END,s+"\n")
    terminal.config(state=DISABLED)

# interprets the code
def interpret(lexer_result,terminal):
    global code, isDeclaring, var_iden, var_val
    line_counter = 0 # line counter
    for line in lexer_result:
        line_counter += 1
        if line == []: # if line is empty, we skip it
            continue

        for token in line: # if line is NOT empty...
            type = token["type"]
            # checks if BTW has been detected
            # the comment itself has already been removed by the lexer
            if type == "Comment Delimiter": 
                continue

            elif type == "Code Delimiter":
                continue

            elif type == "Output Keyword":
                isPrinting = True
                code = code + "print("                

            elif type == "Variable Declaration":
                isDeclaring = True
                continue 

            elif type == "Variable Identifier":
                if isDeclaring == True:
                    symbol_table[token["lexeme"]] = None
                    # if "ITZ" in line (meaning that it an initialized variable)
                    code = code + token["lexeme"]  
                elif isPrinting:
                    code = code + token["lexeme"] + ")"
                    printToConsole(symbol_table[token["lexeme"]],terminal)
                    

            elif type == "Variable Assignment":
                code = code + "="
                
            elif type == "Integer Literal" or type == "Float Literal" or type == "String Literal" or type == "Boolean Literal":
                code = code + token["lexeme"]
        code = code + "\n"
        isDeclaring = isPrinting = False
    # print(code)
    execute()
            
