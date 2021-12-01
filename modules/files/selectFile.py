import tkinter
from tkinter.filedialog import askopenfilename

def selectFile():       
    try:
        path = ""
        tkinter.Tk().wm_withdraw() 
        files = [('LOL Files', '*.lol'),('All Files', '*.*')]
        path = askopenfilename(
            title='Select a file.',
            initialdir='./',
            filetypes=files)
        return path
    except:
        return ""