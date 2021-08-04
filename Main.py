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
import pandas as pd
import Bot_Eng
import Student_Data_Modification
import DataBaseManagement
import QuestionDataControl
import Conversation_mini_scripts
from tkinter import *



def begining():
    global c
    global conn
    conn = sqlite3.connect('ArabCbt_Education.db')
    c = conn.cursor()
    
    global answer
    global Student_name
    global Student_name_data
    global Name_existence
    global Respond
    
    welcome = 'hi, my name is John, and I am here to help you with your artificial intelligence journy, so what is your name?, please enter it'
    Bot_Eng.Bot_speaking(welcome)
    
    Student_name = input('Please let me know your name: ')
    
    
    Student_name_data = Student_Data_Modification.extraction(Student_name)
    
    Name_existence = False
    if len(Student_name_data)==0:
        Name_existence = False
    else:
        Name_existence = True
        
    
    Respond = f"Hey {Student_name}, and welcome to ArabCbt, is it you first time chatting with me?! "
    
    Bot_Eng.Bot_speaking(Respond)
    
    try:
        answer = Bot_Eng.bot_listening()
    except:
        Respond = "didn't hear you what was that again!"
        Bot_Eng.Bot_speaking(Respond)
        answer = Bot_Eng.bot_listening()
    
    scores = list()
    for i in Conversation_mini_scripts.First_time:
        Score = Bot_Eng.matching_scorer(answer,i)
        scores.append(Score)
    
    answer =Conversation_mini_scripts.First_time[scores.index( max(scores))]
    return answer

def registration_checking (answer):
    global Student_no
    global Student_Data
    if answer == 'Yes':
        
        Student_Data_Modification.Add_New_Student(Student_name)
        c.execute('''select generated_id from Students''')
        last_ID = int(max(c.fetchall())[0])
        Respond = f'Okay {Student_name}, your student number {last_ID}'
        Bot_Eng.Bot_speaking(Respond)
        Student_no = last_ID
    
            
        
    else:
        Respond = f'It is nice to have you back {Student_name}, So could you please give me your student number'
        Bot_Eng.Bot_speaking(Respond)
        try:
    
            Student_no = int(input('Please your student number: '))
        except:
            Respond = "didn't hear you what was that again!"
            Bot_Eng.Bot_speaking(Respond)
    
            Student_no = int(input('Please your student number: '))
            
            
        Student_data = Student_Data_Modification.extraction(Student_no)
        
        for i in list(range(5)):
            Student_number_existence = False
            Student_data = Student_Data_Modification.extraction(Student_no)
            if len(Student_data)==0:
                Student_number_existence = False
                Respond = f'{Student_name}, Iam not sure that, this is the correct number, could you please make sure of it and enter it again'
                Bot_Eng.Bot_speaking(Respond)
    
                Student_no = input('Please let me know your name: ')
                    
                if i == 4:
                    Respond = f"{Student_name}, Iam sure that you forgot your number, let's buld a new account for you"
                    Bot_Eng.Bot_speaking(Respond)
                    Student_Data_Modification.Add_New_Student(Student_name)
                    c.execute('''select generated_id from Students''')
                    last_ID = int(max(c.fetchall())[0])
                    Respond = f'Okay {Student_name}, your student number {last_ID}'
                    Bot_Eng.Bot_speaking(Respond)
                    Student_no = last_ID
        
            else:
                Student_number_existence = True
                break
    
    
    c.execute(f'''select * from Students where generated_id = {Student_no}''')
    Student_Data = c.fetchall()
    return Student_Data, Student_no


def revision (Student_Data):
    Student_Data = Student_Data
    if Student_Data[0][2] > 0:
        Respond = f'Okay {Student_name}, I can see that we had {Student_Data[2]} conversations'
        Bot_Eng.Bot_speaking(Respond)
        Respond = f'And, as I can remember your last question was {Student_Data[0][6]}, so how can I help you today?'
        Student_Data_Modification.update_NumberOfVisits(conn,1,Student_no)
        Bot_Eng.Bot_speaking(Respond)
    else:
        Respond = 'Please ask whatever you need to know about artificial intelligence'
    
        Bot_Eng.Bot_speaking(Respond)
        
        
        
        
        
  
begining()
registration_checking(answer)
revision(Student_Data)


c.execute(f'select * from QA ')
Qs_Data = c.fetchall()
Qs_Data = list(Qs_Data)
Qs_data_2 = list()
for i in Qs_Data:
    i = list(i)
    Qs_data_2.append(i)
Qs_Data = pd.DataFrame(Qs_data_2,columns = ['ind','Q','A','R','URL'])


def question_extractor(question):
    ind = int(Qs_Data.index[Qs_Data['Q'] == question][0])
    return ind


def conv():
    Cancel = False
    while Cancel == False:
        try:
            answer = Bot_Eng.bot_listening()
        except:
            Respond = "didn't hear you what was that again!"
            #GUI.respose_print(Respond)
            Bot_Eng.Bot_speaking(Respond)
            answer = Bot_Eng.bot_listening()
        
        
        scores = list()
        for i in Conversation_mini_scripts.asking_for_a_repeat:
            Score = Bot_Eng.matching_scorer(answer,i)
            scores.append(Score)
        
        max_score =  max(scores)
        if Score > 60:
            answer =Conversation_mini_scripts.asking_for_a_repeat[scores.index( max(scores))]
            if answer == 'again':
                Question= Student_Data[0][6]
                Respond = Qs_Data.iloc[question_extractor(str(Question)),2]
                #GUI.respose_print(Respond)
                Bot_Eng.Bot_speaking(Respond)
            elif answer == 'I need a video':
                
                VidURL = Qs_Data.iloc[question_extractor(str(Question)),4]
                Respond='Enjoy!!!'
                #GUI.respose_print(Respond)
                Bot_Eng.Bot_speaking(Respond)
        else:
            Qs = Qs_Data['Q']
            scores = list()
            for i in Qs:
                Score = Bot_Eng.matching_scorer(answer,i)
                scores.append(Score)
            Question =Qs[scores.index(max(scores))]
            Respond = Qs_Data.iloc[question_extractor(str(Question)),2]
            Student_Data_Modification.update_lastQuestion(conn,Respond,Student_no)
            #GUI.respose_print(Respond)
            Bot_Eng.Bot_speaking(Respond)
    
    
        
      
conv()
        
        
        
        
     