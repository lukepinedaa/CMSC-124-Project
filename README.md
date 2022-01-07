
  

#  CMSC 124 - FINAL PROJECT (AY 2021-2022)

  

This is the final project for CMSC 124. This is an interpreter for LOL code.

  

*<insert  more  description\>*

  

  

##  AUTHORS

  

1. HIZON, Rafael Red Angelo M.

  

2. LEE, Serena Mae CS.

  

3. PINEDA, Luke Adrian

  
  

##  PROGRAMMING LANGUAGE

  

This project uses **Python**  _(Python 3.9.7)_ To compare or check your version of Python, simply enter this to the terminal: `python --version`.

  

##  MODULES

  

###  Files

  

`selectFile()` - For selecting a file. This returns the path of the file.

  

`saveFile(code)` - Accepts string as a parameter. For saving the user's code to a specific directory. This returns the filename if there were no problems while saving. It returns `False` if a problem occurred or if the file was not saved.

###  Lexical Analyzer

  

`lexer(code)` - Accepts string as parameter. For converting the string to sequence of tokens. This returns the symbol table which is a 2D list (a list of lists of dictionaries) or a list containing error information: `[False, lineNumber, ErrorMessage]`.

  

###  Syntax Analyzer

  

`parser(lexer_result)` - Accepts the symbol table made using the Lexical Analyzer. For checking the grammar of the code using the tokens made by the Lexical Analyzer. This returns the line number of error and a short description of the error.

  
  

###  Semantic Analyzer

  

`interpret(list)` - Accepts a list (code representation) to be interpreted. Returns the symbol table after executing the interpreted code.

  

##  OTHER DEPENDENCIES / LIBRARIES USED

  

1.  `pathlib` - For paths for the GUI assets.

2.  `tkinter` - For the GUI window and widgets.

3.  `os` - For file handling.

4.  `intertools` - For turning nested lists into a single list (flat).

5.  `re` - For using regular expressions.

6.  `math` - For truncating decimals.

  

*These modules are built into the Python's standard library. To install python, visit this [link](https://www.python.org/downloads/).*