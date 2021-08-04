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



def bot_listening ():
    dev_info = sd.query_devices(2)
    fs = int(dev_info['default_samplerate'])
    seconds = 5
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype = np.int32)
    sd.wait()
    write('out.WAV', fs,myrecording)
    r = sr.Recognizer()
    with sr.AudioFile('out.WAV') as source:
        
        audio_text = r.listen(source)
        try:
            
            text = r.recognize_google(audio_text)
            print('Converting audio transcripts into text ...')
            print(text)
            input_speach = text
            return input_speach
         
        except:
           return print('Sorry.. didn\'t hear you...')


def matching_scorer (x,y):
    ratio = fuzz.token_sort_ratio(x,y)
    return ratio



def Bot_speaking(response):
    engine = pyttsx3.init()
    newVoiceRate = 150
    engine.setProperty('rate',newVoiceRate)
    engine.setProperty('voice', 'com.apple.speech.synthesis.voice.samantha')
    engine.say(response)
    engine.runAndWait()



