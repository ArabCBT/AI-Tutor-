# -*- coding: utf-8 -*-
"""
Created on Sun Aug  1 18:27:07 2021

@author: Ahmed Mohamed Abd Ellatief 
"""

import speech_recognition as sr
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
from fuzzywuzzy import fuzz,process
import pyttsx3
import sqlite3

from tkinter import *




def button_enable():
    Button["state"] = "enable"
    
def button_disable():
    Button["state"] = "disabled"
    

def respose_print (response):
    chatWindow.insert(INSERT, response)
    

def printValue ():
    global result
    result = messageWindow.get("1.0","end")
    messageWindow.delete("1.0","end")
    Button["state"] = "disabled"
    return result


root = Tk()
root.title("Arab Cbt ChatBot")
root.geometry("400x500")
root.resizable(width=FALSE, height=FALSE)
chatWindow = Text(root, bd=1, bg="black",  width="50", height="8", font=("Arial", 12), foreground="#00ffff")
chatWindow.place(x=6,y=6, height=385, width=370)
   
    
    
messageWindow = Text(root, bd=0, bg="black",width="30", height="4", font=("Arial", 12), foreground="#00ffff")
messageWindow.place(x=128, y=400, height=88, width=260)
    
    
    
Button= Button(root, text="Send",  width="12", height=5,
                        bd=0, bg="#0080ff", activebackground="#00bfff",foreground='#ffffff',font=("Arial", 12), command=printValue)
Button.place(x=6, y=400, height=88)
   
root.mainloop()
