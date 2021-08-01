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


def Add_New_Student(Name):
    c.execute('''select generated_id from Students''')
    last_ID = int(max(c.fetchall())[0])+1
    SQL = ("""INSERT INTO Students (generated_id, Name,NuberOfVisits,interests, progress,lastLesson ,lastQuestion) VALUES (?,?,?,?,?,?,?)""")
    Vals = [last_ID, Name, 0,'None', 0, 'None', 'None']
    c.execute(SQL,Vals)
    conn.commit()
    
def update_progress(conn, modification,ID):
    sql = ''' UPDATE Students
              SET progress = ? WHERE generated_id = ?'''
    c.execute(sql, (modification,ID,))
    conn.commit()

def update_NumberOfVisits(conn, modification,ID):
    query = 'select NumberOfVisits  from Students where generated_id = ? '
    c.execute(query, (ID,))
    current_value = c.fetchall()
    new_value = int(current_value) + modification
    sql = ''' UPDATE Students
              SET NumberOfVisits = ? WHERE generated_id = ?'''
    c.execute(sql, (new_value,ID,))
    conn.commit()

def update_interests(conn, modification,ID):
    sql = ''' UPDATE Students
              SET interests = ? WHERE generated_id = ?'''
    c.execute(sql, (modification,ID,))
    conn.commit()

def update_lastLesson(conn, modification,ID):
    sql = ''' UPDATE Students
              SET lastLesson = ? WHERE generated_id = ?'''
    c.execute(sql, (modification,ID,))
    conn.commit()

def update_lastQuestion(conn, modification,ID):
    sql = ''' UPDATE Students
              SET lastQuestion = ? WHERE generated_id = ?'''
    c.execute(sql, (modification,ID,))
    conn.commit()

def extraction(Student_Id):
    c.execute('select * from Students where generated_id = ?', (Student_Id,))
    return c.fetchall()