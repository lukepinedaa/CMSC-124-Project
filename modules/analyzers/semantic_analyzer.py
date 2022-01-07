# This is the program for semantic analysis
# Accepts the result of the lexer as a parameter
from tkinter import *
import math
code = "" # global variable that will hold the code to be interpreted
isDeclaring = False
isMultipleLineRequired = False
isPrinting = False
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

def evaluate(expr):
    # base case
    if len(expr) == 1:
        return str(eval(expr[0]))
    
    # recursive calls
    else:
        if expr[0] == "SUM OF":
            #SUM OF SUM OF A AN B AN SUM OF 2 AN 3
            if expr[1] in ("SUM OF", "DIFF OF", "PRODUKT OF", "QUOSHUNT OF", "MOD OF", "BIGGR OF", "SMALLR OF", "BOTH SAEM", "DIFFRINT", "BOTH OF", "EITHER OF"):
                leftOp = []
                rightOp = []
                # loop here to separate left and right expression/operand
                return evaluate(leftOp)+"+"+evaluate(rightOp)
                
            # SUM OF A AN DIFF OF C AN D => [A,DIFF OF C,D] => [A] [DIFF OF C,D]
        pass
    # I HAS A num ITZ SUM OF 1 AN 1 => "num =" + evaluate(["SUM OF", "1", "AN", "1"])

# for truncating decimals (reference: https://stackoverflow.com/questions/29246455/python-setting-decimal-place-range-without-rounding)
def truncate(f, n):
    return math.floor(f * 10 ** n) / 10 ** n

# for checking if string is a number
def is_num(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

# interprets the code
def interpret(lexer_result,terminal,root):
    global code, isDeclaring, symbol_table, isMultipleLineRequired, currInput
    
    var_iden = ""

    # reset global entities
    code = "" # global variable that will hold the code to be interpreted
    isDeclaring = False
    isMultipleLineRequired = False
    isPrinting = False
    currInput = "" # input of user from pop-up menu
    symbol_table = {"IT": None}

    isDeclaring = isInputting = isPrinting = False
    toBePrinted = ""

    line_counter = 0 # line counter
    for line in lexer_result:
        line_counter += 1
        isDest = True
        if line == []: # if line is empty, we skip it
            continue

        for token in line: # if line is NOT empty...
            _type = token["type"]
            # checks if BTW has been detected
            # the comment itself has already been removed by the lexer
            if _type == "Comment Delimiter": 
                continue
            
            #if HAI or KTHXBYE, continue loop
            elif _type == "Code Delimiter":
                continue
            
            #if VISIBLE, update isPrinting to True
            elif _type == "Output Keyword":
                isPrinting = True

            #if VISIBLE, update isDeclaring to True
            elif _type == "Variable Declaration":
                isDeclaring = True

            elif _type == "Variable Identifier":
                #if current line has "R"
                if checkInLine(line, "R"):
                    #current variable is the destination variable
                    if isDest:
                        #variable is still not in symbol table, error occured
                        if token["lexeme"] not in symbol_table:
                            printToConsole("ERROR: Variable "+token["lexeme"]+" at Line "+str(line_counter)+" does not exist.",terminal) #error "variable does not exist: token["lexeme"]"
                            return symbol_table
                        #update var_iden to current variable identifier, set isDest to False
                        var_iden = token["lexeme"]
                        isDest = False
                    #if source variable
                    else:
                        #assign source variable's value to dest variable
                        if token["lexeme"] in symbol_table:
                            symbol_table[var_iden] = symbol_table[token["lexeme"]]
                            # isDest = True
                        else: #variable not int symbol table, error occured
                            printToConsole("ERROR: Variable "+token["lexeme"]+" at Line "+str(line_counter)+" does not exist.",terminal) #error "variable does not exist: token["lexeme"]"
                            return symbol_table

                #Recast operator, set var_ident to current var identifier
                elif checkInLine(line, "IS NOW A"):
                    #variable is still not in symbol table, error occured
                    if token["lexeme"] not in symbol_table:
                        printToConsole("ERROR: Variable "+token["lexeme"]+" at Line "+str(line_counter)+" does not exist.",terminal) #error "variable does not exist: token["lexeme"]"
                        return symbol_table
                    var_iden = token["lexeme"]

                #current line is declaring a variable
                elif isDeclaring == True:
                    #if will initialize value
                    if checkInLine(line, "ITZ"):
                        code = code + token["lexeme"]
                        #current variable is the destination variable
                        if isDest == True:
                            #variable is not yet in symbol table, add to symbol table, set var_iden to curren varaiable, and update isDest to False
                            if token["lexeme"] not in symbol_table:
                                symbol_table[token["lexeme"]] = None
                                var_iden = token["lexeme"]
                                isDest = False
                            #variable is already in symbol table, error occured
                            else:
                                printToConsole("ERROR: Redeclaration of variable "+token["lexeme"]+" at Line "+str(line_counter),terminal) #error "variable does not exist: token["lexeme"]"
                                return symbol_table
                        #current variable is the source variable
                        else:
                            #assign source variable's value to dest variable
                            if token["lexeme"] in symbol_table:
                                symbol_table[var_iden] = symbol_table[token["lexeme"]]
                                # isDest = True
                            #variable is not yet in symbol table, error occured
                            else:
                                printToConsole("ERROR: Variable "+token["lexeme"]+" at Line "+str(line_counter)+" does not exist.",terminal) #error "variable does not exist: token["lexeme"]"
                                return symbol_table
                    #uninitialized variable, add to symbol table with None as value
                    else:
                        symbol_table[token["lexeme"]] = None
                        code = code + token["lexeme"] + "=None"
                
                #current line is printing
                elif isPrinting:
                    #variable not yet in symbol table, error occured
                    if token["lexeme"] not in symbol_table:
                        printToConsole("ERROR: Variable "+token["lexeme"]+" at Line "+str(line_counter)+" does not exist.",terminal) #error "Cannot implicitly cast nil"
                        return symbol_table
                    #convert to string and concatenate with toBePrinted
                    else: 
                        if type(symbol_table[token["lexeme"]]) == float:
                            toBePrinted = toBePrinted + str(truncate(float(symbol_table[token["lexeme"]]), 2)) 
                        else:
                            toBePrinted = toBePrinted + str(symbol_table[token["lexeme"]])
                    # code = code + token["lexeme"] + ")"
                    # printToConsole(symbol_table[token["lexeme"]],terminal)

                #get input from user
                elif isInputting: 
                    getInput(root, token["lexeme"]) 
                
                #if variable exists in symbol table, set var_iden to current variable, else error occured
                elif isTypecasting:
                    if token["lexeme"] not in symbol_table:
                        printToConsole("ERROR: Cannot explicitly typecast nil at Line "+str(line_counter),terminal) #error "Cannot implicitly cast nil"
                        return symbol_table
                    else:
                        var_iden = token["lexeme"]

            #if current lexeme is R
            elif _type == "Variable Assignment":
                continue
            
            #if current lexeme is a literal
            elif _type == "Integer Literal" or _type == "Float Literal" or _type == "String Literal" or _type == "Boolean Literal":
                #if line with assignment operator
                if checkInLine(line, "R"):
                    #convert lexeme to int and assign to variable in symbol table
                    if (_type == "Integer Literal"):
                        symbol_table[var_iden] = int(token["lexeme"])
                    #convert lexeme to float and assign to variable in symbol table
                    elif (_type == "Float Literal"):
                        symbol_table[var_iden] = float(token["lexeme"])
                    #remove wuotes from string then assign to variable in symbol table
                    elif (_type == "String Literal"):
                        symbol_table[var_iden] = token["lexeme"].replace('"', "")
                    #convert lexeme to corresponding boolean value and assign to variable in symbol table
                    else:
                        if token["lexeme"] == "WIN":
                            symbol_table[var_iden] = True
                        else:
                            symbol_table[var_iden] = False
                #concatenate literal to toBePrinted
                elif isPrinting:
                    #truncate to 2 decimal places before concatenating
                    if _type == "Float Literal":
                        toBePrinted = toBePrinted + str(truncate(float(token["lexeme"]), 2))
                    #remove quotes before concatenating
                    else:
                        toBePrinted = toBePrinted + str(token["lexeme"]).replace('"', "")
                #assign literal to variable (var_iden)
                elif isDeclaring:
                    #convert to int before assigning value
                    if (_type == "Integer Literal"):
                        symbol_table[var_iden] = int(token["lexeme"])
                    #convert to float before assigning value
                    elif (_type == "Float Literal"):
                        symbol_table[var_iden] = float(token["lexeme"])
                    #remove quotes before assigning value
                    elif (_type == "String Literal"):
                        symbol_table[var_iden] = token["lexeme"].replace('"', "")
                    #convert to corresponding boolean value before assigning value
                    else:
                        if token["lexeme"] == "WIN":
                            symbol_table[var_iden] = True
                        else:
                            symbol_table[var_iden] = False
                        
                    code = code + token["lexeme"]
            
            #current lexeme is GIMMEH
            elif _type == "Input Keyword":
                isInputting = True
            
            #current lexeme is MAEK 
            elif _type == "Typecast Operator":
                isTypecasting = True

            #current lexeme is IS NOW A
            elif _type == "Recast Operator":
                isTypecasting = True

            #current lexeme is A
            elif _type == "Separator":
                continue
            
            #
            elif _type == "Type Literal":
                if isTypecasting:
                    if checkInLine(line, "R") or checkInLine(line, "IS NOW A"):
                        dest = var_iden
                    else:
                        dest = "IT"
                    if token["lexeme"] == "TROOF": # boolean
                        if symbol_table[var_iden] == "" or symbol_table[var_iden] == 0:
                            symbol_table[dest] = False
                        else:
                            symbol_table[dest] = True
                    elif token["lexeme"] == "NOOB":
                         printToConsole("ERROR: Cannot typecast "+var_iden+" into NOOB at Line "+str(line_counter),terminal) # error
                    elif token["lexeme"] == "NUMBR": # float
                        if symbol_table[var_iden] != None:
                            if (type(symbol_table[var_iden]) == str) and is_num(symbol_table[var_iden]):
                                symbol_table[dest] = float(symbol_table[var_iden].replace('"', ""))
                            elif is_num(symbol_table[var_iden]) == False:
                                printToConsole("ERROR: Cannot typecast at Line "+str(line_counter),terminal)
                                return symbol_table
                            else:
                                symbol_table[dest] = float(symbol_table[var_iden])
                        else:
                            symbol_table[dest] = 0.00
                    elif token["lexeme"] == "NUMBAR":
                        if symbol_table[var_iden] != None:
                            if (type(symbol_table[var_iden]) == str) and is_num(symbol_table[var_iden]):
                                symbol_table[dest] = int(symbol_table[var_iden].replace('"', ""))
                            elif is_num(symbol_table[var_iden]) == False:
                                printToConsole("ERROR: Cannot typecast at Line "+str(line_counter),terminal)
                                return symbol_table
                            else:
                                symbol_table[dest] = int(symbol_table[var_iden])
                        else:
                            symbol_table[dest] = 0
                    elif token["lexeme"] == "YARN":
                        if symbol_table[var_iden] != None:
                            if type(symbol_table[var_iden]) == int:
                                symbol_table[dest] = str(symbol_table[var_iden])
                            elif type(symbol_table[var_iden]) == float:
                                symbol_table[dest] = str(truncate(symbol_table[var_iden],2))
                        else:
                            symbol_table[dest] = ''
        if isPrinting == True:
            printToConsole(toBePrinted,terminal)
            toBePrinted = ""
        code = code + "\n"
        isDeclaring = isPrinting = isInputting = isTypecasting = False
    
    # execute()
    return symbol_table