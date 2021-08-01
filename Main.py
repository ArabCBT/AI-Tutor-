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


import Bot_Eng
import Student_Data_Modification
import DataBaseManagement
import QuestionDataControl
import Conversation_mini_scripts
#import GUI
from tkinter import *



conn = sqlite3.connect('ArabCbt_Education.db')
c = conn.cursor()




welcome = 'hi, my name is John, and I am here to help you with your artificial intelligence journy, so what is your name?, please enter it'
#GUI.respose_print(welcome)
Bot_Eng.Bot_speaking(welcome)

#GUI.button_enable()
Student_name = input('Please let me know your name: ')


Student_name_data = Student_Data_Modification.extraction(Student_name)

Name_existence = False
if len(Student_name_data)==0:
    Name_existence = False
else:
    Name_existence = True
    

Respond = f"Hey {Student_name}, and welcome to ArabCbt, is it you first time chatting with me?! "
#GUI.respose_print(Respond)

Bot_Eng.Bot_speaking(Respond)

try:
    answer = Bot_Eng.bot_listening()
except:
    Respond = "didn't hear you what was that again!"
    #GUI.respose_print(Respond)
    Bot_Eng.Bot_speaking(Respond)
    answer = Bot_Eng.bot_listening()




scores = list()
for i in Conversation_mini_scripts.First_time:
    Score = Bot_Eng.matching_scorer(answer,i)
    scores.append(Score)

answer =Conversation_mini_scripts.First_time[scores.index( max(scores))]

if answer == 'Yes':
    
    Student_Data_Modification.Add_New_Student(Student_name)
    c.execute('''select generated_id from Students''')
    last_ID = int(max(c.fetchall())[0])
    Respond = f'Okay {Student_name}, your student number {last_ID}'
    #GUI.respose_print(Respond)
    Bot_Eng.Bot_speaking(Respond)
    Student_no = last_ID

        
    
else:
    Respond = f'It is nice to have you back {Student_name}, So could you please give me your student number'
    #GUI.respose_print(Respond)
    Bot_Eng.Bot_speaking(Respond)
    try:
       # GUI.button_enable()

        Student_no = int(input('Please your student number: '))
    except:
        Respond = "didn't hear you what was that again!"
       #GUI.respose_print(Respond)
        Bot_Eng.Bot_speaking(Respond)
        #GUI.button_enable()

        Student_no = int(input('Please your student number: '))
        
        
    Student_data = Student_Data_Modification.extraction(Student_no)
    
    for i in list(range(5)):
        Student_number_existence = False
        Student_data = Student_Data_Modification.extraction(Student_no)
        if len(Student_data)==0:
            Student_number_existence = False
            Respond = f'{Student_name}, Iam not sure that, this is the correct number, could you please make sure of it and enter it again'
            #GUI.respose_print(Respond)
            Bot_Eng.Bot_speaking(Respond)
            #GUI.button_enable()

            Student_no = input('Please let me know your name: ')
                
            if i == 4:
                Respond = f"{Student_name}, Iam sure that you forgot your number, let's buld a new account for you"
                #GUI.respose_print(Respond)
                Bot_Eng.Bot_speaking(Respond)
                Student_Data_Modification.Add_New_Student(Student_name)
                c.execute('''select generated_id from Students''')
                last_ID = int(max(c.fetchall())[0])
                Respond = f'Okay {Student_name}, your student number {last_ID}'
                #GUI.respose_print(Respond)
                Bot_Eng.Bot_speaking(Respond)
                Student_no = last_ID
    
        else:
            Student_number_existence = True
            break


c.execute(f'''select * from Students where generated_id = {Student_no}''')
Student_Data = c.fetchall()

if Student_Data[0][2] > 0:
    Respond = f'Okay {Student_name}, I can see that we had {Student_Data[2]} conversations'
    #GUI.respose_print(Respond)
    Bot_Eng.Bot_speaking(Respond)
    Respond = f'And, as I can remember your last question was {Student_Data[0][6]}, so how can I help you today?'
    Student_Data_Modification.update_NumberOfVisits(conn,1,Student_no)
    #GUI.respose_print(Respond)
    Bot_Eng.Bot_speaking(Respond)
else:
    Respond = 'Please ask whatever you need to know about artificial intelligence'
    #GUI.respose_print(Respond)

    Bot_Eng.Bot_speaking(Respond)


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
            c.execute(f'''select Answer from QA where Question = {Question}''')
            Respond = c.fetchall()
            #GUI.respose_print(Respond)
            Bot_Eng.Bot_speaking(Respond)
        elif answer == 'I need a video':
            c.execute(f'''select VideoURL from QA where Question = {Question}''')
            VidURL = c.fetchall()
            Respond='Enjoy!!!'
            #GUI.respose_print(Respond)
            Bot_Eng.Bot_speaking(Respond)
    else:
        c.execute('''select Question from QA''')
        Qs = c.fetchall()[0]
        scores = list()
        for i in Qs:
            Score = Bot_Eng.matching_scorer(answer,i)
            scores.append(Score)
        Q =Qs[scores.index(max(scores))]
        c.execute(f'''select Answer from QA where Question = {Q}''')
        Respond = c.fetchall()
        Student_Data_Modification.update_lastQuestion(conn,Respond,Student_no)
        #GUI.respose_print(Respond)
        Bot_Eng.Bot_speaking(Respond)


