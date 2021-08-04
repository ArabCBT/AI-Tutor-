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




conn = sqlite3.connect('ArabCbt_Education.db')
c = conn.cursor()



#c.execute('''CREATE TABLE Students ([generated_id] INTEGER PRIMARY KEY,[Name] text, 
#          [NumberOfVisits] int, [interests] text, [progress] int, [lastLesson] text, [lastQuestion] text)''')


#c.execute('''CREATE TABLE QA ([generated_id] INTEGER PRIMARY KEY,[Question] text, 
#          [Answer] text, [Recommendation] text, [VideoURL] text)''')

'''
c.execute("DROP TABLE QA")
conn.commit()
'''

