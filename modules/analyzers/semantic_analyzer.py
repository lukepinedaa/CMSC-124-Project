# This is the program for semantic analysis
# Accepts the result of the lexer as a parameter
from tkinter import *
import math

isMultipleLineRequired = False
currInput = "" # input of user from pop-up menu
inputWindowIsClosed = True

# for the symbol table
symbol_table = {"IT": "None"} # symbol table (list of dictionaries)

# for getting input of user (when GIMMEH is input)
def inputBtnClick(i,lexeme,button_pressed):
    global currInput
    button_pressed.set(1)
    currInput = i
    symbol_table[lexeme] = currInput

def on_menu_closing(button_pressed):
    global currInput
    button_pressed.set(1)
    currInput = ""

#gets the input from user
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

# for printing to console
def printToConsole(s,terminal):
    s = str(s)
    terminal.config(state=NORMAL)
    terminal.insert(END,s+"\n")
    terminal.config(state=DISABLED)

#checks if elexeme is in current line
def checkInLine(line, lexeme):
    for token in line:
        if token["lexeme"] == lexeme:
            return True
    return False

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
    global symbol_table, isMultipleLineRequired, currInput
    
    var_iden = ""

    # reset global entities
    isMultipleLineRequired = False
    isPrinting = False
    currInput = "" # input of user from pop-up menu
    symbol_table = {"IT": None}

    isDeclaring = isInputting = isPrinting = isTypecasting = False
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
            
            #current lexeme is a type literal
            elif _type == "Type Literal":
                if isTypecasting:
                    #assign proper dest value
                    if checkInLine(line, "R") or checkInLine(line, "IS NOW A"):
                        dest = var_iden
                    else:
                        dest = "IT"
                    #typecast to corresponding boolean value
                    if token["lexeme"] == "TROOF":
                        if symbol_table[var_iden] == "" or symbol_table[var_iden] == 0:
                            symbol_table[dest] = False
                        else:
                            symbol_table[dest] = True
                    #typecast to corresponding boolean value
                    elif token["lexeme"] == "NOOB":
                         printToConsole("ERROR: Cannot typecast "+var_iden+" into NOOB at Line "+str(line_counter),terminal) # error
                    #typecast to corresponding float value
                    elif token["lexeme"] == "NUMBR":
                        #initialized variable
                        if symbol_table[var_iden] != None:
                            if (type(symbol_table[var_iden]) == str) and is_num(symbol_table[var_iden]):
                                symbol_table[dest] = float(symbol_table[var_iden].replace('"', ""))
                            #cannot be converted to float, error occurred
                            elif is_num(symbol_table[var_iden]) == False:
                                printToConsole("ERROR: Cannot typecast at Line "+str(line_counter),terminal)
                                return symbol_table
                            else:
                                symbol_table[dest] = float(symbol_table[var_iden])
                        #uninitialized variable
                        else:
                            symbol_table[dest] = 0.00
                    #typecast to corresponding int value
                    elif token["lexeme"] == "NUMBAR":
                        #initialized variable
                        if symbol_table[var_iden] != None:
                            if (type(symbol_table[var_iden]) == str) and is_num(symbol_table[var_iden]):
                                symbol_table[dest] = int(float(symbol_table[var_iden].replace('"', "")))
                            #cannot be converted to int, error occurred
                            elif is_num(symbol_table[var_iden]) == False:
                                printToConsole("ERROR: Cannot typecast at Line "+str(line_counter),terminal)
                                return symbol_table
                            else:
                                symbol_table[dest] = int(symbol_table[var_iden])
                        #uninitialized variable
                        else:
                            symbol_table[dest] = 0
                    #typecast to corresponding string value
                    elif token["lexeme"] == "YARN":
                        #initialized variable
                        if symbol_table[var_iden] != None:
                            if type(symbol_table[var_iden]) == int:
                                symbol_table[dest] = str(symbol_table[var_iden])
                            elif type(symbol_table[var_iden]) == float:
                                symbol_table[dest] = str(truncate(symbol_table[var_iden],2))
                        #uninitialized variable
                        else:
                            symbol_table[dest] = ''
                            
        #Prints toBePrinted to GUI terminal
        if isPrinting == True:
            printToConsole(toBePrinted,terminal)
            toBePrinted = ""
        isDeclaring = isPrinting = isInputting = isTypecasting = False
    
    return symbol_table