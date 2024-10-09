import speech_recognition as sr
import pyttsx3
import pyaudio
import wikipedia
import requests
from bs4 import BeautifulSoup
import webbrowser
import time
import re
import os
import pywhatkit
import random
import pyautogui
import datetime
import tkinter as tk
import tkinter.scrolledtext
from tkinter import *
import Apps
import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model

AppId = 'XVX5EP-7JGW8ULH2X'
your_name = 'sir'
welcomelist = [f'Welcome {your_name}..., how can I help you!',
               f'Nice..., you are here {your_name}..., What will we do today!', f"Hi {your_name}, how can I serve you."]
hilist = [f"oh!, good morning {your_name}...,I'm redy to serve you", f"Hi {your_name}..., how can I serve you!",
          f"hello {your_name} How are you?", f"hello!, Nice to hear your voice {your_name}...,give me your command!",
          f"Hi {your_name}, I hope you are doing well!..., can I help you!"]
byelist = [f"oh,ok Goodbye {your_name}...,be sure I'm ready to serve you any time...,bye ", f"bye.. bye {your_name}",
           f"bye {your_name}..., I'll miss you", f"bye!...,that was nice to hear your voice {your_name}"]

window = tk.Tk()
window.title("Leno")
window.configure(background="#48494B")
window.geometry("500x660")

icon=PhotoImage(file="Record.png")
window.iconphoto(False,icon)
Label(text="leno",font="arial 20",background="#48494B",fg="black").pack(side=TOP)

conversation = tk.Text(window, bg="#48494B", fg="white", font=("Courier", 12))
conversation.tag_configure("you", foreground="grey", spacing1=15, font="arial 20")
conversation.tag_configure("leno", foreground="white", spacing1=15, font="arial 20")
conversation.pack(expand=True, fill=tk.BOTH)

def send_message():
    tmp = input_label.get()
    input_label.delete(0, tk.END)  # Clear the input field
    return tmp

input_label = tk.Entry(window, width=50)
input_label.pack()


lemmatizer = WordNetLemmatizer()
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbotmodel.h5')

#يقوم الكود بتنظيف الجملة المدخلة
def clean_up_sentence(sentence):
    #تفكيك الجملة إلى كلمات منفردة
    sentence_words = nltk.word_tokenize(sentence)
    #تطبيق الاقتصاص على كل كلمة واعادت الكلمات الى جزرها
    sentence_words = [lemmatizer.lemmatize(word)  for word in sentence_words]
    #رجاع الجملة المنظفة كقائمة من الكلمات
    return sentence_words

#هذه الطريقة، يتم إنشاء قائمة باغ التي تحتوي على الترددات الحالية لجميع الكلمات في الجملة المدخلة
def bag_of_words(sentence):
    sentence_words= clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1

    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda  x:x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    global t
    t="sorry i didn't understand what are you saying!"
    if return_list != []:
        return return_list
    else:
        return t

def get_response(intents_list,intents_json):
    tag= intents_list[0]['intent']
    list_of_intents =intents_json['intents']
    result = ""
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    global t
    t = "sorry i didn't understand what are you saying!"
    if result != "":
        return result
    else:
        return t


# Initialize the speech recognizer and text-to-speech engine
r = sr.Recognizer()
engine = pyttsx3.init()

# define word with dectionary
def define_word(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        meanings = data[0]["meanings"]
        tmp = "the meaning of " + word +" are: "
        speak(tmp)
        for meaning in meanings:
            part_of_speech = meaning["partOfSpeech"]
            definitions = meaning["definitions"]
            for definition in definitions:
                tmp = f"{part_of_speech}: {definition['definition']}"
                leno_said(tmp)
                speak(tmp)
    else:
        tmp = f"Sorry, {word} is not found."
        leno_said(tmp)
        speak(tmp)
# Define the function to search on wikihow
def search_wikihow(text=''):
    query = text
    wikihow_url = f'https://www.wikihow.com/wikiHowTo?search={query}'
    tmp = "here is some results from wikihow..."
    leno_said(tmp)
    speak(tmp)
    webbrowser.open(wikihow_url)
# Define the function to search on wikipedia
def search_wikipedia(text=''):
    searchResults = wikipedia.search(text)
    if not searchResults:
        tmp = 'No wikipedia result'
        leno_said(tmp)
        speak(tmp)
        return 'No result received'
    try:
        wikiPage = wikipedia.page(searchResults[0])
    except wikipedia.DisambiguationError as error:
        wikiPage = wikipedia.page(error.options[0])
    print(wikiPage.title)
    wikiSummary = str(wikiPage.summary)
    return wikiSummary
# Define the function to set timer
def set_timer(timer):
    time.sleep(timer)
    tmp = "Time's up"
    leno_said(tmp)
    speak(tmp)
# Define the function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()
# Define the function to listen to the user's voice
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            return text
        except:
            return ""

def you_said(tmp):
    tmp = "YOU: "+ tmp + "\n"
    conversation.insert(tk.END, tmp, "you")

def leno_said(tmp):
    tmp = "LENO: " + tmp + "\n"
    conversation.insert(tk.END, tmp, "leno")

global sspeak
sspeak = 0
def Speak1():
    global sspeak
    sspeak = 1
    main()
    sspeak = 0


def main():
        if( sspeak==1 ):
            text = listen().lower()
            you_said(text)
        else:
            text = send_message()
            you_said(text)


        if "hello" in text:
            tmp = random.choice(hilist)
            leno_said(tmp)
            speak(tmp)
        elif "what is your name" in text:
            tmp = "My name is Leno."
            leno_said(tmp)
            speak(tmp)
        elif "goodbye" in text:
            tmp = random.choice(byelist)
            leno_said(tmp)
            speak(tmp)
        elif "who is" in text:
            text = text[7:]
            tmp = search_wikipedia(text)
            leno_said(tmp)
            speak(tmp)
        elif "how to" in text:
            tmp = search_wikihow(text)
        elif "set timer for " in text:
            timr = re.findall('\d+', text)
            timer = int(timr[0])
            if "minute" in text:
                timer *= 60
            set_timer(timer)
        elif "what is " in text:
            query = text
            google_url = f'https://www.google.com/search?q={query}&rlz=1C1GCEA_enSY978SY978&oq={query}&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIJCAEQABgKGIAEMgkIAhAAGAoYgAQyCQgDEAAYChiABDIJCAQQABgKGIAEMgkIBRAAGAoYgAQyCQgGEAAYChiABDIJCAcQABgKGIAEMgkICBAAGAoYgAQyBwgJEAAYgATSAQgyNzAwajBqN6gCALACAA&sourceid=chrome&ie=UTF-8'
            tmp = "here is some results from google..."
            leno_said(tmp)
            speak(tmp)
            webbrowser.open( google_url)
        elif "can " in text:
            query = text
            wikihow_url = f'https://www.google.com/search?q={query}&rlz=1C1GCEA_enSY978SY978&oq={query}&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIJCAEQABgKGIAEMgkIAhAAGAoYgAQyCQgDEAAYChiABDIJCAQQABgKGIAEMgkIBRAAGAoYgAQyCQgGEAAYChiABDIJCAcQABgKGIAEMgkICBAAGAoYgAQyBwgJEAAYgATSAQgyNzAwajBqN6gCALACAA&sourceid=chrome&ie=UTF-8'
            tmp ="here is some results from google..."
            leno_said(tmp)
            speak(tmp)
            webbrowser.open(wikihow_url)
        elif "play" in text:
            song_name = text[4:]
            tmp = "playing" + song_name + "..."
            leno_said(tmp)
            speak(tmp)
            pywhatkit.playonyt(song_name)
        elif "open" in text:
            query = text[5:]
            tmp = "opening " + query + " ..."
            leno_said(tmp)
            speak(tmp)
            Apps.openApp(query)
        elif "take screenshot" in text:
            tmp = "taking screenshot"
            leno_said(tmp)
            speak(tmp)
            screenshot = pyautogui.screenshot()
            screenshot.save('C:/Users/96399/Desktop/screenshot.png')

        elif "define" in text:
            word = text[6:]
            tmp = "defining..."
            speak(tmp)
            define_word(word)

        else:
            ints = predict_class(text)
            res = get_response(ints, intents)
            leno_said(res)
            speak(res)

write_button = tk.Button(window, text="send", command=main, bg='#777B7E',activebackground="#4a4a4f",font="arial 20")
write_button.pack(side=tk.LEFT, padx=10, pady=10)
voice_button = tk.Button(window, text="speak", command=Speak1, bg='#777B7E',activebackground="#4a4a4f",font="arial 20")
voice_button.pack(side=tk.RIGHT, padx=10, pady=10)

window.mainloop()