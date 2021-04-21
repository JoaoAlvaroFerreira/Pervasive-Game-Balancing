import tkinter as tk
import os
from main import *

window = tk.Tk()

def analysisTest():
    analyse()

buttonSim = tk.Button(
    text="Sim",
    width=25,
    height=5,
    bg="white",
    fg="black",
)

buttonCreate = tk.Button(
    text="Create",
    width=25,
    height=5,
    bg="white",
    fg="black",
)

buttonAnalyse = tk.Button(
    text="Analyse",
    width=25,
    height=5,
    bg="white",
    fg="black",
    command=analysisTest
)

buttonSim.pack()
buttonCreate.pack()
buttonAnalyse.pack()


window.wm_title("Data Analysis Platform")
window.geometry("640x480")
window.mainloop()

