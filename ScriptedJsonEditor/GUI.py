# GUI for Scripted JSON Editor
# Python 3
import os
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from _tkToolTip import Tooltip
from ScriptedJsonEditor import get_jobs_hierarchy, \
                               get_all_job_definitions, \
                               get_all_job_files, \
                               read_jobs_in_jobs_file, \
                               TooltipStr, \
                               edit_job_file, \
                               execute_job_file

#########################
# The tab's public class:
#########################
class Tab:
  tkLabelframe_jobSettings = None
  jobDefinitionFrames = None
  def __init__(self, parentFrame, menu2tab, goCommand=False):
    """ Put this into the parent frame """

    self.parentFrame = parentFrame
    self.menu2tab = menu2tab
    menu2tab.setJobDefinitionsFolderRefresh(self.jobDefinitionsFolderRefresh)
    menu2tab.setJobsFolderRefresh(self.jobsFolderRefresh)
    menu2tab.setWriteJobFile(self.writeJobFile)

    # Create a Tkinter variable
    self.jobFileVar = tk.StringVar(parentFrame)
 
    tkLabelConditions = tk.Label(parentFrame, anchor='w', justify='l',
                                text='Displays the hierarchy of job definition files and jobs.\n\n\
Need to add\n\
* load job files if dir changed\n\
* detecting if changes are made\n\
* creating new configs\n\
')
    tkLabelConditions.grid(column=0, row=0, columnspan=2, sticky='w')

    # Add a grid
    self.jobFilesFrame = tk.LabelFrame(parentFrame, text='Job files')
    self.jobFilesFrame.grid(column=0,row=1, columnspan=5, sticky='w')
    self.jobFilesFrame.columnconfigure(0, weight=1)
    self.jobFilesFrame.rowconfigure(0, weight=1)
    self.jobFilesFrame.grid(pady=5, padx=5, ipadx=10)

    self.tkLabelframe_jobSettings = tk.LabelFrame(parentFrame, text='Job settings')
    self.tkLabelframe_jobSettings.grid(row=3, pady=5, padx=5, ipadx=10)

    self.jobDefinitionFrames = self.JobDefinitionFrames(self.tkLabelframe_jobSettings, self.menu2tab)

    self.fillJobDropdown(parentFrame)

    if goCommand:
      self.goButton = tk.Button(parentFrame, 
                                text='Execute job file',
                                height=5,
                                width=20,
                                command=self.goCommandPrepare)
      self.goButton.grid(column=1, row=0, padx=15, pady=20)
 
  def fillJobDropdown(self, parentFrame):
    # Dictionary with options
    choices = get_all_job_files(self.menu2tab.jobsFolder)
    
    if choices != {}:
      popupMenu = tk.OptionMenu(self.jobFilesFrame, self.jobFileVar, *choices)
      tk.Label(self.jobFilesFrame, text="Choose a job file").grid(row=1, column=0, sticky='w')
      popupMenu.grid(row=1, column=1, ipadx=10, sticky='w')
      self.jobFileVar.trace('w', self.change_dropdown)
      self.jobFileVar.set(next(iter(choices))) # set the default option to the "first" dict item
    else:
      messagebox.showinfo('No job files found',
                         'In %s' % self.menu2tab.jobsFolder)

  # on change dropdown value
  def change_dropdown(self, *args):
    self.jobDefinitionFrames.clear_checkbuttons()
    #self.initialJobDefinitions = {} # for detecting if anything has changed
    _jobsFile = os.path.join(self.menu2tab.jobsFolder, self.jobFileVar.get())
    self.menu2tab.jobFileName = _jobsFile
    try:
      _jobs = read_jobs_in_jobs_file(_jobsFile)
      for job in _jobs:
        for defnFile in job:
          for defn in job[defnFile]:
            self.jobDefinitionFrames.set_checkbutton(defnFile, defn, 1)
            #self.initialJobDefinitions[defnFile][defn] = 1
    except Exception as e:
      messagebox.showinfo('Error in job file %s' % _jobsFile,
                          getattr(e, 'message', repr(e)))

  def goCommandPrepare(self):
    _filepath = os.path.join(self.menu2tab.jobsFolder, self.jobFileVar.get())
    _result, _status = go(_filepath)
    if _result:
      messagebox.showerror('Job error',
                           '\n'.join(_status))
    elif len(_status):
      messagebox.askokcancel('Job completed, edits made',
                           '\n'.join(_status))
    else:
      messagebox.askokcancel('Job completed',
                          'No edits necessary')

  def getSettings(self):
    """ Return the settings for this tab """
    return ['Conditions']

  def setSettings(self, settings):
    """ Set the settings for this tab """
    pass
  
  def writeJobFile(self, filepath):
    _jobsFile = os.path.join(self.menu2tab.jobsFolder, self.jobFileVar.get())
    _edits = self.jobDefinitionFrames.get_checkbutton_edits()
    edit_job_file(_jobsFile, filepath, _edits)
    pass

  class JobDefinitionFrames:
    """ Show the job settings, allow them to be changed """
    def __init__(self, parentFrame, menu2tab):
      all_job_definitions = get_all_job_definitions(menu2tab.jobDefinitionsFolder)

      self.tkLabelframes = []
      tooltip_wraplength = 650
      # sort job_definition_files into order of number of jobs
      job_definition_file_names=[]
      total_jobs = 0  # and count the jobs
      if all_job_definitions:
        for job_definition_file_name,jobs in all_job_definitions.items():
          job_definition_file_names.append(
            [job_definition_file_name,
             jobs.json_dict['job definitions']])
          total_jobs += len(jobs.json_dict['job definitions']) +1 #for the frame
        job_definition_file_names.sort(key=self.__lenSecond, reverse=True)

      # Calculate the number of columns
      columns = total_jobs // 12
      if columns < 2: # at least 2 columns
        columns = 2
      left_right = 1
      _row = 2

      # Then display each job_definition_file in a frame in order of number of jobs
      self.checkbutton_IntVars = {}
      for job_definition_file_name, __ in job_definition_file_names:
        self.checkbutton_IntVars[job_definition_file_name] = []
        jobs = all_job_definitions[job_definition_file_name]
        _tkLabelframe = tk.LabelFrame(parentFrame, text=job_definition_file_name+'.json')
        self.checkbutton_IntVars[job_definition_file_name] = {}
        for job in jobs.json_dict['job definitions']:
          self.checkbutton_IntVars[job_definition_file_name][job] = tk.IntVar()
          _tkCheckbutton = tk.Checkbutton(
            _tkLabelframe, text=job, 
            variable=self.checkbutton_IntVars[job_definition_file_name][job])
          _tkCheckbutton.grid(sticky='w')
          # Extract a tooltip from the job's comments
          _tooltip = ''
          for line in jobs.json_dict['job definitions'][job]:
            if line.startswith(TooltipStr):
              _tooltip += line[len(TooltipStr):] + '\n'
          for __,section in jobs.json_dict['job definitions'][job]['edits'].items():
            for line in section:
              if line.startswith(TooltipStr):
                _tooltip += line[len(TooltipStr):] + '\n'
          if len(_tooltip):
            Tooltip(_tkCheckbutton, text=_tooltip[:-1], wraplength=tooltip_wraplength)

        _tkLabelframe.grid(column=left_right, row=_row, padx=5, pady=5, sticky='new')
      
        # Next column
        left_right += 1
        if left_right > columns:
          left_right = 1
          _row += 1
        self.tkLabelframes.append(_tkLabelframe)

    def set_checkbutton(self, job_definition_file_name, job_name, value):
      try:
        self.checkbutton_IntVars[job_definition_file_name][job_name].set(value)
      except:
        print('Could not set job definition file "%s" job "%s" to "%s"' % 
              (self.menu2tab.job_definition_file_name, job_name, value))
        raise

    def get_checkbutton(self, job_definition_file_name, job_name):
      try:
        value = self.checkbutton_IntVars[job_definition_file_name][job_name].get()
      except:
        print('Could not get job definition file "%s" job "%s"' % 
              (self.menu2tab.job_definition_file_name, job_name))
        value = 'ERROR'
        raise
      return value

    def clear_checkbuttons(self):
      for job_definition_file_name in self.checkbutton_IntVars:
        for job_name in self.checkbutton_IntVars[job_definition_file_name]:
          self.checkbutton_IntVars[job_definition_file_name][job_name].set(0)

    def get_checkbutton_edits(self):
      """
      Get a dict of jobs to edit into a jobs file by adding
      all the selected buttons
      """
      _jobs = {'jobs':[{}]}
      _job_definition_file_names = []
      for job_definition_file_name in self.checkbutton_IntVars:
        _jobs['jobs'][0][job_definition_file_name] = []
        for job_name in self.checkbutton_IntVars[job_definition_file_name]:
          if self.checkbutton_IntVars[job_definition_file_name][job_name].get():
            _jobs['jobs'][0][job_definition_file_name].append(job_name)
        if _jobs['jobs'][0][job_definition_file_name] == []:
          # No jobs for this job_definition_file_name
          del _jobs['jobs'][0][job_definition_file_name]
        else:
          _job_definition_file_names.append(r'job_definitions\%s.json' % job_definition_file_name)
      # Edit "job definition files" list too
      _jobs['job definition files'] = _job_definition_file_names
      return _jobs

    def __lenSecond(self, elem):  # for sorting job_definition_files by number of jobs
      return len(elem[1])

    def destroy(self):
      for r in self.tkLabelframes:
        r.destroy()

  def jobDefinitionsFolderRefresh(self):
    self.jobDefinitionFrames.destroy()
    self.jobDefinitionFrames = self.JobDefinitionFrames(self.tkLabelframe_jobSettings, self.menu2tab)

  def jobsFolderRefresh(self):
    self.fillJobDropdown(self.parentFrame)
    pass

class Menu2tab:
  """
  Interface between Menu and Tab classes
  """
  def __init__(self, jobDefinitionsFolder, jobsFolder):
    self.__jobDefinitionsFolder = jobDefinitionsFolder
    self.__jobsFolder = jobsFolder
    self.__jobFileName = None
    self.writeJobFile = None
  @property
  def jobDefinitionsFolder(self) :
    return self.__jobDefinitionsFolder
  @jobDefinitionsFolder.setter
  def jobDefinitionsFolder(self, jobDefinitionsFolder):
    self.__jobDefinitionsFolder = jobDefinitionsFolder

  @property
  def jobsFolder(self):
    return self.__jobsFolder
  @jobsFolder.setter
  def jobsFolder(self, jobsFolder):
    self.__jobsFolder = jobsFolder

  @property
  def jobFileName(self):
    return self.__jobFileName
  @jobFileName.setter
  def jobFileName(self, jobFileName):
    self.__jobFileName = jobFileName

  def setWriteJobFile(self, writeJobFile):
    self.writeJobFile = writeJobFile
  def writeJobFile(self, filepath):
    self.writeJobFile(filepath)

  def setJobsFolderRefresh(self, jobsFolderRefresh):
    self.jobsFolderRefresh = jobsFolderRefresh
  def jobsFolderRefresh(self):
    self.jobsFolderRefresh()

  def setJobDefinitionsFolderRefresh(self, jobDefinitionsFolderRefresh):
    self.jobDefinitionsFolderRefresh = jobDefinitionsFolderRefresh
  def jobDefinitionsFolderRefresh(self):
    self.jobDefinitionsFolderRefresh()

def go(filepath):
  """ Execute the job file """
  return execute_job_file(filepath)

def setMenu2tab(basedir):
  jobsFolder = os.path.join(basedir, 'jobs')
  jobDefinitionsFolder = os.path.join(basedir, 'job_definitions')

  menu2tab = Menu2tab(jobDefinitionsFolder=jobDefinitionsFolder,
                      jobsFolder=jobsFolder)
  return menu2tab

def Main(playerID='player', 
         rF2root=r'"c:\Program Files (x86)\Steam\steamapps\common\rFactor 2"', 
         test=False,
         goCommand=False):
  from GUImenu import Menu
  root = tk.Tk()
  root.title('JSON file editor')

  tabGraphics = ttk.Frame(root, width=1200, height=1200, 
                            relief='sunken', borderwidth=5)
  tabGraphics.grid()
   
  menu2tab = setMenu2tab(os.getcwd())
  o_tab = Tab(tabGraphics, menu2tab, goCommand=goCommand)

  menubar = tk.Menu(root)
  # display the menu
  root.config(menu=menubar)

  o_menu = Menu(menubar=menubar, 
                menu2tab=menu2tab)


  if not test:
    root.mainloop()
  else:
    return o_tab,root  # For testing

if __name__ == '__main__':
  # To run this tab by itself for development
  o_tab, root = Main(True, goCommand=True)

  _test_frames = o_tab.jobDefinitionFrames

  _test_frames.set_checkbutton('G25_jobs', 'Monitor', 1)
  assert _test_frames.get_checkbutton('G25_jobs', 'Monitor') == 1

  _test_frames.set_checkbutton('VR_jobs', 'universal', 1)
  assert _test_frames.get_checkbutton('VR_jobs', 'universal') == 1

  _test_frames.set_checkbutton('Game_jobs', 'Flags off', 1)
  _test_frames.set_checkbutton('Game_jobs', 'Flags off', 0)
  assert _test_frames.get_checkbutton('Game_jobs', 'Flags off') == 0

  # Error cases
  try:
    _test_frames.set_checkbutton('OOPS!', 'Monitor', 1)
    print('Should have raised an error')
    raise
  except: # error raised as expected
    pass

  try:
    assert _test_frames.get_checkbutton('OOPS!', 'Monitor') == 'ERROR'
    print('Should have raised an error')
    raise
  except: # error raised as expected
    pass

  root.mainloop()



