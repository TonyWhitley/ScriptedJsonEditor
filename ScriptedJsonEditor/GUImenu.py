# Python 3
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from os.path import join, normpath, split
import pyperclip

from ScriptedJsonEditor import versionStr, versionDate
from backups import Backups
from GUI import Menu2tab

def about():
  messagebox.askokcancel(
            'About Scripted JSON Editor',
            '%s  %s\nby Tony Whitley' % (versionStr, versionDate)
        )

def faq():
  _backupDir = Backups().get_tempdir()
  messagebox.askokcancel(
            'Scripted JSON Editor FAQ',
            'Scripted JSON editor is a program to make changes for example '
            'to rFactor 2 player.json'
            '\n'
            'Rather than a list of instructions to "edit player.json setting '
            '\'blah\' to 15" and so on, instead a JSON file is provided and '
            'ScriptedJsonEditor will edit it for you.'
            '\n'
            'The GUI allows you to select a job file that executes a number '
            'of such "jobs".  You can then change which jobs are selected '
            'and save as a new job file.\n\n'
            'Whenever a file is edited a timestamped backup is placed in %s\n'
            '(which has been pasted in the clipboard)'
            % _backupDir
        )
  pyperclip.copy(_backupDir)


class Menu:
  jobDefinitionsFolder = '.'
  jobsFolder = '.'
  def __init__(self, 
               menubar, 
               menu2tab):

    self.parentFrame = menubar.master
    self.menu2tab = menu2tab

    # create a pulldown menu, and add it to the menu bar
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Open job definitions folder", command=self.openJobDefinitionsFolder)
    filemenu.add_command(label="Open jobs folder", command=self.openJobsFolder)
    filemenu.add_command(label="Save job file", command=self.save)
    # The shortcut operates when rFactory Saves scenario too
    # so don't use it.
    # , accelerator='Ctrl+S')
    # menubar.master.bind_all("<Control-s>", self.save)

    filemenu.add_command(label="Save job file as...", command=self.saveAs)
    filemenu.add_separator()
    filemenu.add_command(label="Change rFactor player folder", command=self.changeRF2player)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=menubar.master.quit)
    menubar.add_cascade(label="File", menu=filemenu)

    helpmenu = tk.Menu(menubar, tearoff=0)
    helpmenu.add_command(label="FAQ", command=faq)
    helpmenu.add_command(label="About", command=about)
    menubar.add_cascade(label="Help", menu=helpmenu)

  def controlS(self):
    """ Add the Ctrl/S accelerator """
    menubar.master.bind_all("<Control-s>", self.save)

  def openJobDefinitionsFolder(self):
    _folder = filedialog.askdirectory(parent=self.parentFrame,
                                     initialdir=self.menu2tab.jobDefinitionsFolder,
                                     title="Please select a folder containing job definition files")
    if _folder:
      self.menu2tab.jobDefinitionsFolder = _folder
      self.menu2tab.jobDefinitionsFolderRefresh()

  def openJobsFolder(self):
    _folder = filedialog.askdirectory(parent=self.parentFrame,
                                     initialdir=self.menu2tab.jobsFolder,
                                     title="Please select a folder containing job files")
    if _folder:
      self.menu2tab.jobsFolder = _folder
      self.menu2tab.jobsFolderRefresh()

  def saveAs(self):
    _filepath = filedialog.asksaveasfilename(
                                 title='Save job file as...', 
                                 initialdir=self.menu2tab.jobsFolder, 
                                 initialfile=self.menu2tab.jobFileName,
                                 defaultextension='.JSON',
                                 filetypes=[('Job files', 'JSON')])
    if _filepath:
      self.menu2tab.jobFileName = os.path.basename(_filepath)
      self.menu2tab.writeJobFile(_filepath)
      self.menu2tab.jobsFolderRefresh()

  def save(self, *kw):
    self.menu2tab.writeJobFile(join(self.menu2tab.jobsFolder, self.menu2tab.jobFileName))

  def changeRF2player(self):
    """
    Change the player ID that is being edited
    """
    _player = join(self.menu2tab.rF2root, 'UserData')
    _folder = filedialog.askdirectory(parent=self.parentFrame,
                                     initialdir=_player,
                                     title="Please select the player folder")
    if _folder:
      _folder = normpath(_folder)
      self.menu2tab.rF2root, self.menu2tab.playerID = split(_folder)
      # Now get rid of /UserData/
      self.menu2tab.rF2root, __ = split(self.menu2tab.rF2root)
      # GUI.py reads self.menu2tab.playerID/rF2root

if __name__ == '__main__':
  # To run this tab by itself for development
  def nullFn(*args):
    return nullFolder
  def quit():
    pass
  nullFolder = 'c:/temp'
  root = tk.Tk()
  root.title('JSON file editor menu testing')

  menu2tab = Menu2tab(jobDefinitionsFolder=nullFolder,
                    jobsFolder=nullFolder)
  menu2tab.setJobDefinitionsFolderRefresh(nullFn)
  menu2tab.setJobsFolderRefresh(nullFn)
  menu2tab.setWriteJobFile(nullFn)
  menu2tab.jobFileName = nullFolder

  tabGraphics = ttk.Frame(root, width=800, height=800, 
                            relief='sunken', borderwidth=5)
  tabGraphics.grid()

  menubar = tk.Menu(root)

  filemenu = tk.Menu(menubar, tearoff=0)
  menubar.add_cascade(label="JSON Editor", menu=filemenu)

  filemenu2 = tk.Menu(menubar, tearoff=0)
  menubar.add_cascade(label="Another tab", menu=filemenu2)

  # display the menu
  root.config(menu=menubar)


  o_menu = Menu(menubar=filemenu, 
                menu2tab=menu2tab)
  o_menu.controlS() # Add the Ctrl/S accelerator

  root.mainloop()
