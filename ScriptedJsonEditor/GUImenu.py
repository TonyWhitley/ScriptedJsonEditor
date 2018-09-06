# Python 3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

from ScriptedJsonEditor import versionStr

def hello():
    print("hello!")

def about():
  messagebox.showinfo(
            'About Scripted JSON Editor',
            versionStr+'\nby Tony Whitley'
        )


  
class Menu:
  jobDefinitionsFolder = '.'
  jobsFolder = '.'
  def __init__(self, parentFrame, 
               jobDefinitionsFolder, 
               jobsFolder, 
               jobDefinitionsFolderRefresh,
               jobsFolderRefresh):
    self.jobDefinitionsFolder = jobDefinitionsFolder
    self.jobsFolder = jobsFolder
    self.jobDefinitionsFolderRefresh = jobDefinitionsFolderRefresh
    self.jobsFolderRefresh = jobsFolderRefresh
    menubar = tk.Menu(parentFrame)
    self.parentFrame = parentFrame

    # create a pulldown menu, and add it to the menu bar
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Open job definitions folder", command=self.openJobDefinitionsFolder)
    filemenu.add_command(label="Open jobs folder", command=self.openJobsFolder)
    filemenu.add_command(label="Save job file", command=hello)
    filemenu.add_command(label="Save job file as...", command=hello)
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

  def openJobDefinitionsFolder(self):
    self.jobDefinitionsFolder = filedialog.askdirectory(parent=self.parentFrame,
                                     initialdir=self.jobDefinitionsFolder,
                                     title="Please select a folder containing job definition files")
    self.jobDefinitionsFolderRefresh()

  def openJobsFolder(self):
    self.jobsFolder = filedialog.askdirectory(parent=self.parentFrame,
                                     initialdir=self.jobsFolder,
                                     title="Please select a folder containing job files")
    self.jobsFolderRefresh()
