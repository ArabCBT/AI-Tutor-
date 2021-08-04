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

def Add_New_Q(Q,A,Recommendaation,VidURL):
    c.execute('''select generated_id from QA''')
    last_ID = int(max(c.fetchall())[0])+1
    SQL = ("""INSERT INTO QA (generated_id,Question,Answer,Recommendation,VideoURL) VALUES (?,?,?,?,?)""")
    Vals = [last_ID,Q,A,Recommendaation,VidURL]
    c.execute(SQL,Vals)
    conn.commit()



def Answering(Question):
    answer = c.execute('select Answer from QA where Question = ?', (Question,))
    Vid = c.execute('select VideoURL from QA where Question = ?', (Question,))
    Recommendation = c.execute('select Recommendation from QA where Question = ?', (Question,))
    return c.fetchall()


def update_Answer(conn, modification,ID):
    sql = ''' UPDATE QA
              SET Answer = ? WHERE generated_id = ?'''
    c.execute(sql, (modification,ID,))
    conn.commit()


def update_Recommendation(conn, modification,ID):
    sql = ''' UPDATE QA
              SET Recommendation = ? WHERE generated_id = ?'''
    c.execute(sql, (modification,ID,))
    conn.commit()
    

def update_VideoURL(conn, modification,ID):
    sql = ''' UPDATE QA
              SET VideoURL = ? WHERE generated_id = ?'''
    c.execute(sql, (modification,ID,))
    conn.commit()




'''
What is the sector of artificial intelligence?

'''


