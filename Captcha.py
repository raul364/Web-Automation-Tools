# DATE DEVELOPED: 2020/11/10
# Version 1
# WRITTEN BY: James Hills(Joh5)
# Date Tested: 2020/12/08
# Description: Audio Captcha Obtaining and cracking system utilising speech to text libraries.
#



##### please install ffmpeg for pydub
import speech_recognition as sr
import requests
import os
from pydub import AudioSegment

##############################################################################
#downloads audio file from given link     file is mp3 not html
def get_captcha(file_link):
    remove_file() # cleans last file if there is one
    headers = {'user-agent':'uni-password-test'}
    r = requests.get(file_link)
    with open('cap.mp3','wb')as audio_file:
        audio_file.write(r.content)
    convert_file()

##############################################################################
#convert file from mp3 to wav
def convert_file():
    file = AudioSegment.from_mp3("cap.mp3")
    file.export("cap.wav",format="wav")

##############################################################################
#get string from file and return
def get_voice():
    
    speech_recognizer = sr.Recognizer()
    file = sr.AudioFile('cap.wav')
    with file as source:
        speech_recognizer.adjust_for_ambient_noise(source)
        audio = speech_recognizer.record(source)
        result = speech_recognizer.recognize_google(audio,language='en')
    return(result)

#once file is processed and speech is returned remove file to save space
def remove_file():
    try:
        os.remove('cap.wav')
    except:
        print("no file to remove")
    try:
        os.remove("cap.mp3")
    except:
        print("no file found")

def main(link):
    get_captcha(link)
    #trim_file()
    string = get_voice()
    return string
