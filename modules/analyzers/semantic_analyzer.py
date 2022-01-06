# This is the program for semantic analysis
# Accepts the result of the lexer as a parameter
from tkinter import *
code = "" # global variable that will hold the code to be interpreted
isDeclaring = False
isMultipleLineRequired = False
isPrinting = False
printMe = ""
currInput = "" # input of user from pop-up menu
inputWindowIsClosed = True

# for the symbol table
symbol_table = {"IT": "None"} # symbol table (list of dictionaries)

# for getting input of user (when GIMMEH is input)
def inputBtnClick(i,lexeme,button_pressed):
    global currInput, code
    button_pressed.set(1)
    currInput = i
    symbol_table[lexeme] = currInput
    code = code + lexeme + "=" + currInput
    print(code)

def on_menu_closing(button_pressed):
    global currInput
    button_pressed.set(1)
    currInput = ""
    
def getInput(root,lexeme):
    global currInput
    menu = Toplevel(root)
    menu.resizable(False, False)
    menu.title("GIMMEH")

    # sets the menu at the center
    x = root.winfo_x()
    y = root.winfo_y()
    g = "340x200+"+str(x+500)+"+"+str(y+200)
    menu.geometry(g)
    
    # label
    Label(menu, text="Enter Input", font=('Helvetica 17 bold')).pack(pady=30)

    # Texbox
    input_entry = Entry(menu)
    input_entry.pack()

    # button
    button_pressed = IntVar()    
    go = Button(menu, text="Enter", font=('Helvetica',8), height=1, width=7, bg='SystemButtonFace', command=lambda: inputBtnClick(input_entry.get(),lexeme,button_pressed))
    go.pack(pady=5)

    menu.protocol("WM_DELETE_WINDOW", lambda: on_menu_closing(button_pressed))
    
    go.wait_variable(button_pressed)

    menu.destroy()    

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

def checkInLine(line, lexeme):
    for token in line:
        if token["lexeme"] == lexeme:
            return True
    return False

# interprets the code
def interpret(lexer_result,terminal,root):
    global code, isDeclaring, var_iden, var_val
    isDeclaring = isInputting = isPrinting = False
    toBePrinted = ""
    line_counter = 0 # line counter
    for line in lexer_result:
        line_counter += 1
        isDest = True
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
                # code = code + "print("

            elif type == "Variable Declaration":
                isDeclaring = True
                continue 

            elif type == "Variable Identifier":
                if checkInLine(line, "R"):
                    if isDest:
                        if token["lexeme"] not in symbol_table:
                            printToConsole("ERROR: Variable "+token["lexeme"]+" at Line "+str(line_counter)+" does not exist.",terminal) #error "variable does not exist: token["lexeme"]"
                            return
                        var_iden = token["lexeme"]
                        isDest = False
                    else:
                        if token["lexeme"] in symbol_table:
                            symbol_table[var_iden] = symbol_table[token["lexeme"]]
                            isDest = True
                        else:
                            printToConsole("ERROR: Variable "+token["lexeme"]+" at Line "+str(line_counter)+" does not exist.",terminal) #error "variable does not exist: token["lexeme"]"
                            return

                elif isDeclaring == True:
                    if checkInLine(line, "ITZ"):
                        code = code + token["lexeme"]
                        if isDest == True:
                            if token["lexeme"] not in symbol_table:
                                symbol_table[token["lexeme"]] = None
                                var_iden = token["lexeme"]
                                isDest = False
                            else:
                                printToConsole("ERROR: Redeclaration of variable "+token["lexeme"]+" at Line "+str(line_counter),terminal) #error "variable does not exist: token["lexeme"]"
                                return
                        else:
                            if token["lexeme"] in symbol_table:
                                print(token["lexeme"], symbol_table)
                                symbol_table[var_iden] = symbol_table[token["lexeme"]]
                                isDest = True
                            else:
                                printToConsole("ERROR: Variable "+token["lexeme"]+" at Line "+str(line_counter)+" does not exist.",terminal) #error "variable does not exist: token["lexeme"]"
                                return

                    else:
                        symbol_table[token["lexeme"]] = None
                        code = code + token["lexeme"] + "=None"
                elif isPrinting:
                    if token["lexeme"] not in symbol_table:
                        printToConsole("ERROR: Cannot implicitly cast nil"+" at Line "+str(line_counter),terminal) #error "Cannot implicitly cast nil"
                        return
                    else: toBePrinted = toBePrinted + symbol_table[token["lexeme"]] 
                    # code = code + token["lexeme"] + ")"
                    # printToConsole(symbol_table[token["lexeme"]],terminal)
                elif isInputting: 
                    getInput(root, token["lexeme"]) 

            elif type == "Variable Assignment":
                code = code + "="
                
            elif type == "Integer Literal" or type == "Float Literal" or type == "String Literal" or type == "Boolean Literal":
                if checkInLine(line, "R"):
                    symbol_table[var_iden] = token["lexeme"]
                elif isPrinting:
                    toBePrinted = toBePrinted + token["lexeme"].replace('"', "")
                    # code = code + token["lexeme"] + ")"
                    # printToConsole(token["lexeme"].replace('"', ""),terminal)
                elif isDeclaring:
                    if (type == "Integer Literal"):
                        symbol_table[var_iden] = (token["lexeme"])
                    elif (type == "Float Literal"):
                        symbol_table[var_iden] = (token["lexeme"])
                    elif (type == "String Literal"):
                        symbol_table[var_iden] = token["lexeme"].replace('"', "")
                    else:
                        symbol_table[var_iden] = (token["lexeme"])
                    code = code + token["lexeme"]
            
            elif type == "Input Keyword":
                isInputting = True
        if isPrinting == True:
            printToConsole(toBePrinted,terminal)
            toBePrinted = ""
        code = code + "\n"
        isDeclaring = isPrinting = isInputting = False
    # print(code)
    execute()      