from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import soundfile
import speech_recognition as sr
import os
import random
import urllib
import pandas as pd
import certifi
import math
from multiprocessing import Process, freeze_support
from tkinter import *
from tkinter import messagebox
from datetime import datetime, timedelta
import ssl 
ssl._create_default_https_context = ssl._create_unverified_context

class Window(Frame):
    
    def __init__(self, master=None):
        Frame.__init__(self, master)        
        self.master = master
        self.pack(fill=BOTH, expand=1)

        start_button = Button(self, text="開始", command=self.clickStartButton)
        start_button.place(x=20, y=20, width=80)
        close_button = Button(self, text="完了", command=self.clickExitButton)
        close_button.place(x=130, y=20, width=80)
        
        self.text6 = Label(self, text="")
        self.text6.place(x=20,y=50,width=190)
    
    def activation(self):
        if self.var1.get() == 1:
            self.start_time.config(state="disabled")
            self.end_time.config(state="disabled")
        else:
            self.start_time.config(state="normal")
            self.end_time.config(state="normal")
    
    def setStatus(self, text):
        statusbar.config(text=text)
        # self.text6.config(text=text)
    
    def clickStartButton(self):
        self.setStatus("started")
        app.update()
        time.sleep(5)
        

    def clickExitButton(self):
        exit()

freeze_support()
root = Tk()
app = Window(root)
statusbar = Label(app, text="on the way…", bd=1, relief=SUNKEN, anchor=W)
statusbar.pack(side=BOTTOM, fill=X)
root.wm_title("gameclub.jp")
root.geometry("230x80+1100+400")
root.resizable(False, False)
root.mainloop()