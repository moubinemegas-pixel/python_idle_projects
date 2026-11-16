# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 20:16:28 2024

@author: Moubine Mamadou
"""
import custom_tkinter
root=custom_tkinter.Tk()
I=0
while I<=12:
    I=I+1
    if I%2==0:
        continue
custom_tkinter.Label("4 *",I,"=",4*I)
root.mainloop()