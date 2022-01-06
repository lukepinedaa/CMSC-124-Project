# User-defined modules
import sys
sys.path.append("./modules/analyzers/") 
sys.path.append("./modules/files/") 
from lexical_analyzer import lexer
from saveFile import saveFile
from selectFile import selectFile
from syntax_analyzer import parser
from semantic_analyzer import interpret

# Import statements for the GUI
from pathlib import Path
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./gui_assets")

# Other Import statements
import os
from itertools import chain

# For the GUI Assets
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# For printing the  lexemes
def displayLexemes(flatTokenList):
    lexeme_table.delete(*lexeme_table.get_children()) # clear the current content of the table
    count = 0 # a unique identifier for each content of the table
    for token in flatTokenList:
        lexeme_table.insert(parent="", index="end", iid=count, text="", values=(token["lexeme"], token["type"])) # insert current element to table
        count = count+1 # update count

# For printing error on the console
def printError(err):
    if err[0] == "lexical_err":
        print("lexical error")
    elif err[0] == "parser_err":
        print("parser error")

# execute Function
def execute():
    code = text_editor.get("1.0","end-1c") # user's code

    if code == "": # no code 
        return

    lexer_result = lexer(code) # result of lexer
    try:
        flatTokenList = list(chain.from_iterable(lexer_result)) # flattens the 2D list (reference: https://www.geeksforgeeks.org/python-ways-to-flatten-a-2d-list/)
        displayLexemes(flatTokenList) # display the result on the table

        if lexer_result[0] != False: # no error from lexer
            parser_result = parser(lexer_result) # pass lexer result to parser

            if parser_result[0] != 0: # parser detected an error
                printError(["parser_err",parser_result]) # print error message to console
            else:
                interpret(lexer_result,terminal) # invoke semantic analyzer
                

        else: # lexer detected an error
            printError(["lexical_err",lexer_result]) # print error message to console

    except Exception as e:
        # print("Something went wrong")
        print("\n=====================\n",e)

# For saving the file (Save As)
def save():
    code = text_editor.get("1.0","end-1c") # user's code
    try:
        fname = saveFile(code)
        window.title(os.path.basename(fname)) # set the title to the filename of the saved file
    except:
        return

# For selecting a file
def openFile():
    code = selectFile()
    if code != "": # user selected a file
        text_editor.delete("1.0",END)
        window.title(os.path.basename(code)) # set the title to the filename of the opened file
        f = open(code,"r")
        text_editor.insert(END, f.read())
        f.close()
    else:
        return

################### GUI ########################
# INITIALIZATIONS
window = Tk()
window.geometry("1152x700") 
window.title("Unsaved File")
window.resizable(False, False)
style = ttk.Style()
################################################

################################################
canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 700,
    width = 1152,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

# RECTANGLE
canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    0.0,
    0.0,
    1152.0,
    61.0,
    fill="#2E3F46",
    outline="")
################################################

################################################
# TEXT EDITOR

# frame
textEditorFrame = Frame(window, bg="#27363E")

# bg
text_editor_image = PhotoImage(
    file=relative_to_assets("entry_1.png"))
text_editor_bg_1 = canvas.create_image(
    576.0,
    308.0,
    image=text_editor_image
)

# scrollbar
text_editor_scroll = Scrollbar(textEditorFrame)
text_editor_scroll.pack(side=RIGHT, fill=Y)

# textbox
text_editor = Text(
    textEditorFrame,
    bd=0,
    bg="#27363E",
    highlightthickness=0,
    font=("Monaco", 12),
    width=170,
    height=35,
    selectbackground="#009687",
    selectforeground="black",
    foreground="white",
    undo=True,
    yscrollcommand=text_editor_scroll.set

)
text_editor.pack(padx=15, pady=15)

# configure scrollbar
text_editor_scroll.config(command=text_editor.yview)

# place frame
textEditorFrame.place(
    x=0.0,
    y=61.0,
    width=900.0,
    height=492.0
)

################################################
# TERMINAL
terminal_image = PhotoImage(
    file=relative_to_assets("entry_2.png"))
terminal_bg_2 = canvas.create_image(
    576.0,
    638.0,
    image=terminal_image
)
terminal = Text(
    bd=0,
    bg="#1E292F",
    highlightthickness=0,
    selectbackground="#009687",
    selectforeground="black",
    foreground="white",
    state=DISABLED
)
terminal.place(
    x=13.0,
    y=576.0,
    width=1125.0,
    height=122.0
)
################################################

################################################
# LEXEME TREEVIEW

# frame
lexemeFrame = Frame(window)

# scrollbar
lexeme_scroll = Scrollbar(lexemeFrame)
lexeme_scroll.pack(side=RIGHT, fill=Y)

# treeview
lexeme_table= ttk.Treeview(lexemeFrame,  yscrollcommand=lexeme_scroll.set)

# columns
lexeme_table["columns"] = ("Lexeme", "Classification")
lexeme_table.column("#0", width=0, stretch=NO)
lexeme_table.column("Lexeme", anchor=CENTER, width=100)
lexeme_table.column("Classification", anchor=CENTER, width=100)

# heading
lexeme_table.heading("#0", text="")
lexeme_table.heading("Lexeme", text="LEXEME", anchor=CENTER)
lexeme_table.heading("Classification", text="CLASSIFICATION", anchor=CENTER)

# configure scrollbar
lexeme_scroll.config(command=lexeme_table.yview)

# style
style.theme_use("default")
style.configure(
    "Treeview",
     foreground = "white",
     background = "#1E292F",     
     fieldbackground = "#1E292F"
    )
style.map(
    "Treeview",
     background = [("selected", "#009687")],
     foreground = [("!selected", "#009687")]
)

# pack 
lexeme_table.pack()

# place frame
lexemeTableYpos = 80.0
lexemeFrame.place(
    x=915.0,
    y= lexemeTableYpos,
    width=220,
    height=200.0
)
################################################

################################################
# SYMBOL TABLE TREEVIEW

# frame
symbolTableFrame = Frame(window)

# scrollbar
sybolTable_scroll = Scrollbar(symbolTableFrame)
sybolTable_scroll.pack(side=RIGHT, fill=Y)

# treeview
symbol_table= ttk.Treeview(symbolTableFrame,  yscrollcommand=sybolTable_scroll.set)

# columns
symbol_table["columns"] = ("Identifier", "Value")
symbol_table.column("#0", width=0, stretch=NO)
symbol_table.column("Identifier", anchor=CENTER, width=100)
symbol_table.column("Value", anchor=CENTER, width=100)

# heading
symbol_table.heading("#0", text="")
symbol_table.heading("Identifier", text="IDENTIFIER", anchor=CENTER)
symbol_table.heading("Value", text="VALUE", anchor=CENTER)

# configure scrollbar
sybolTable_scroll.config(command=symbol_table.yview)

# style
style.theme_use("default")
style.configure(
    "Treeview",
     foreground = "white",
     background = "#1E292F",     
     fieldbackground = "#1E292F"
    )
style.map(
    "Treeview",
     background = [("selected", "#009687")],
     foreground = [("!selected", "#009687")]
)

# pack 
symbol_table.pack()

# place frame
symbolTableFrame.place(
    x=915.0,
    y=lexemeTableYpos+220,
    width=220,
    height=200.0
)
################################################

################################################
# RECTANGLE
canvas.create_rectangle(
    0.0,
    555.0,
    1152.0,
    700.0,
    fill="#1B282E",
    outline="")
canvas.create_text(
    14.0,
    559.0,
    anchor="nw",
    text="Console",
    fill="#009687",
    font=("Archivo Bold", 12 * -1)
)
################################################

################################################
# Buttons
saveBtn_image = PhotoImage(
    file=relative_to_assets("button_1.png"))
saveBtn = Button(
    image=saveBtn_image,
    borderwidth=0,
    highlightthickness=0,
    command=save,
    relief="flat"
)
saveBtn.place(
    x=158.0,
    y=12.0,
    width=41.0,
    height=37.0
)

openBtn_image = PhotoImage(
    file=relative_to_assets("button_2.png"))
openBtn = Button(
    image=openBtn_image,
    borderwidth=0,
    highlightthickness=0,
    command=openFile,
    relief="flat"
)
openBtn.place(
    x=110.0,
    y=12.0,
    width=41.0,
    height=37.0
)

stopBtn_image = PhotoImage(
    file=relative_to_assets("button_3.png"))
stopBtn = Button(
    image=stopBtn_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("STOP button clicked"),
    relief="flat"
)
stopBtn.place(
    x=62.0,
    y=12.0,
    width=41.0,
    height=37.0
)

runBtn_image = PhotoImage(
    file=relative_to_assets("button_4.png"))
runBtn = Button(
    image=runBtn_image,
    borderwidth=0,
    highlightthickness=0,
    command=execute,
    relief="flat"
)
runBtn.place(
    x=14.0,
    y=12.0,
    width=41.0,
    height=37.0
)
################################################

# Loop
window.mainloop()