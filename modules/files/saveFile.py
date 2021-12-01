import tkinter
from tkinter.filedialog import asksaveasfile

def saveFile(code):
    try:
        tkinter.Tk().wm_withdraw() 
        files = [('LOL Files', '*.lol'),('All Files', '*.*')]
        file = asksaveasfile(filetypes = files, defaultextension = files) # returns a file object (reference: https://docs.python.org/3/library/dialog.html)
        fname = file.name # filename of the code
        # reference for file descriptors: https://www.w3schools.com/python/python_file_handling.asp
        f = open(fname, "w") # opens the file
        f.write(code) # writes the code to the file
        f.close() # closes the file
        return True
    except:
        return False