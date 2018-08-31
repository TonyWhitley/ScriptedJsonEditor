# Python 3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from ScriptedJsonEditor import versionStr

def hello():
    print("hello!")

def about():
  messagebox.showinfo(
            'About Scripted JSON Editor',
            versionStr+'\nby Tony Whitley'
        )
  
class Menu:
  def __init__(self, parentFrame):
    menubar = tk.Menu(parentFrame)

    # create a pulldown menu, and add it to the menu bar
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Open", command=hello)
    filemenu.add_command(label="Save", command=hello)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=parentFrame.quit)
    menubar.add_cascade(label="File", menu=filemenu)

    """
    # create more pulldown menus
    editmenu = tk.Menu(menubar, tearoff=0)
    editmenu.add_command(label="Cut", command=hello)
    editmenu.add_command(label="Copy", command=hello)
    editmenu.add_command(label="Paste", command=hello)
    menubar.add_cascade(label="Edit", menu=editmenu)
    """

    helpmenu = tk.Menu(menubar, tearoff=0)
    helpmenu.add_command(label="About", command=about)
    menubar.add_cascade(label="Help", menu=helpmenu)

    # display the menu
    parentFrame.config(menu=menubar)
    #print(parentFrame.config())
