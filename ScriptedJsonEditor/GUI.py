# Python 3
import os
import sys
import tkinter as tk
from tkinter import ttk

from _tkToolTip import Tooltip
from ScriptedJsonEditor import get_jobs_hierarchy, get_all_job_definitions, get_all_job_files, TooltipStr
from GUImenu import Menu

o_tab = None

#########################
# The tab's public class:
#########################
class Tab:
  tkLabelframe_jobSettings = None
  jobFrames = None
  def __init__(self, parentFrame, jobDefinitionsFolder):
    """ Put this into the parent frame """

    # Allow this to be used from outside the current directory
    # os.chdir(cwd)

    self.jobDefinitionsFolder = jobDefinitionsFolder
    tkLabelConditions = tk.Label(parentFrame, anchor='w', justify='l',
                                text='Displays the hierarchy of job definition files and jobs.\n\n\
Need to add\n\
* load settings from job file\n\
* write settings back to job file\n\
* detecting if changes are made\n\
* creating new configs\n\
')
    tkLabelConditions.grid(column=0, row=0, columnspan=2, sticky='w')

    # Add a grid
    jobFilesFrame = tk.LabelFrame(parentFrame, text='Job files')
    jobFilesFrame.grid(column=0,row=1, columnspan=5, sticky='w')
    jobFilesFrame.columnconfigure(0, weight=1)
    jobFilesFrame.rowconfigure(0, weight=1)
    jobFilesFrame.grid(pady=5, padx=5, ipadx=10)
 
    # Create a Tkinter variable
    tkvar = tk.StringVar(parentFrame)
 
    self.o_menu = Menu(root, jobDefinitionsFolder=jobDefinitionsFolder, jobFolderRefresh=self.jobFolderRefresh)
    # Dictionary with options
    choices = get_all_job_files(self.o_menu.jobDefinitionsFolder)
    
    if choices != {}:
      tkvar.set(next(iter(choices))) # set the default option to the "first" dict item
 
      popupMenu = tk.OptionMenu(jobFilesFrame, tkvar, *choices)
      tk.Label(jobFilesFrame, text="Choose a job file").grid(row=1, column=0, sticky='w')
      popupMenu.grid(row=1, column=1, ipadx=10, sticky='w')
    else:
      print('No job files found in %s' % os.path.join(os.getcwd(), 'jobs'))
 
    self.tkLabelframe_jobSettings = tk.LabelFrame(parentFrame, text='Job settings')
    self.tkLabelframe_jobSettings.grid(row=3, pady=5, padx=5, ipadx=10)

    self.jobFrames = self.JobFrames(self.tkLabelframe_jobSettings, jobDefinitionsFolder=self.o_menu.jobDefinitionsFolder)

  # on change dropdown value
  def change_dropdown(*args):
      print( tkvar.get() )
    
  def getSettings(self):
    """ Return the settings for this tab """
    return ['Conditions']

  def setSettings(self, settings):
    """ Set the settings for this tab """
    pass
  

  class JobFrames:
    """ Show the job settings, allow them to be changed """
    def __init__(self, parentFrame, jobDefinitionsFolder):
      all_jobs = get_all_job_definitions(jobDefinitionsFolder)

      self.tkLabelframes = []
      tooltip_wraplength = 500
      # sort job_definition_files into order of number of jobs
      job_definition_file_names=[]
      total_jobs = 0  # and count the jobs
      for job_definition_file_name,jobs in all_jobs.items():
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
        jobs = all_jobs[job_definition_file_name]
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
              (job_definition_file_name, job_name, value))
        raise

    def get_checkbutton(self, job_definition_file_name, job_name):
      try:
        value = self.checkbutton_IntVars[job_definition_file_name][job_name].get()
      except:
        print('Could not get job definition file "%s" job "%s"' % 
              (job_definition_file_name, job_name))
        value = 'ERROR'
        raise
      return value

    def __lenSecond(self, elem):  # for sorting job_definition_files by number of jobs
      return len(elem[1])

    def destroy(self):
      for r in self.tkLabelframes:
        r.destroy()

  def jobFolderRefresh(self):
    self.jobFrames.destroy()
    self.jobFrames = self.JobFrames(self.tkLabelframe_jobSettings, self.o_menu.jobDefinitionsFolder)

if __name__ == '__main__':
  # To run this tab by itself for development
  root = tk.Tk()
  root.title('JSON file editor')
  jobFolder = os.path.join(os.getcwd(), 'jobs')
  jobDefinitionsFolder = os.path.join(os.getcwd(), 'job_definitions')

  tabConditions = ttk.Frame(root, width=1200, height=1200, 
                            relief='sunken', borderwidth=5)
  tabConditions.grid()
   
  o_tab = Tab(tabConditions, jobDefinitionsFolder)

  _test_frames = o_tab.jobFrames

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



