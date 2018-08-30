# Python 3
import tkinter as tk
from tkinter import ttk

from _tkToolTip import Tooltip
from ScriptedJsonEditor import get_jobs_hierarchy, get_all_jobs



#########################
# The tab's public class:
#########################
class Tab:
  def __init__(self, parentFrame):
    """ Put this into the parent frame """
    pass
    tkLabelConditions = tk.Label(parentFrame, 
                                text='This could be used to display the hierarchy of jobs and job definitions')
    tkLabelConditions.grid(column=1, row=1, columnspan=2)

    all_jobs = get_all_jobs()

    tkLabelframes = []
    left_right = 1  # put frames in alternating columns
    _row = 2
    wraplength = 500
    # sort jobfiles into order of number of jobs
    jobfile_names=[]
    for jobfile_name,jobs in all_jobs.items():
      jobfile_names.append([jobfile_name,jobs.json_dict['job definitions']])
    jobfile_names.sort(key=self.__lenSecond, reverse=True)

    # Then display each jobfile in a frame in order of number of jobs
    for jobfile_name, __ in jobfile_names:
      jobs = all_jobs[jobfile_name]
      _tkLabelframe = tk.LabelFrame(parentFrame, text=jobfile_name)
      tkCheckbuttons = []
      for job in jobs.json_dict['job definitions']:
        _tkCheckbutton = tk.Checkbutton(_tkLabelframe, text=job)
        _tkCheckbutton.grid(sticky='w')
        tkCheckbuttons.append(_tkCheckbutton)
        _tooltip = ''
        for line in jobs.json_dict['job definitions'][job]:
          if line.startswith('# '):
            _tooltip += line[2:] + '\n'
        for __,section in jobs.json_dict['job definitions'][job]['edits'].items():
          for line in section:
            if line.startswith('# '):
              _tooltip += line[2:] + '\n'
        if len(_tooltip):
          Tooltip(_tkCheckbutton, text=_tooltip[:-1], wraplength=wraplength)
      _tkLabelframe.grid(column=left_right, row=_row, padx=5, pady=5, sticky='new')
      if left_right == 1:
        left_right = 2
      else:
        left_right = 1
        _row += 1
      tkLabelframes.append(_tkLabelframe)
  def __lenSecond(self, elem):  # for sorting jobfiles by number of jobs
    return len(elem[1])

  def getSettings(self):
    """ Return the settings for this tab """
    return ['Conditions']

  def setSettings(self, settings):
    """ Set the settings for this tab """
    pass
  
if __name__ == '__main__':
  # To run this tab by itself for development
  root = tk.Tk()
  tabConditions = ttk.Frame(root, width=1200, height=1200, relief='sunken', borderwidth=5)
  tabConditions.grid()
   
  o_tab = Tab(tabConditions)
  root.mainloop()



