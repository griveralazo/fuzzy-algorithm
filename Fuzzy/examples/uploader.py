# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 13:03:54 2019

@author: jgonz
"""

from Tkinter import Tk
from tkinter.filedialog import askopenfilename

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
print(filename)