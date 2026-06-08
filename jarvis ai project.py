from os import mkdir

import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import random

import openai
from config import apikey

def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for prompt {prompt} \n **********\n\n"

    response = openai.Completion.create(
        model="gpt-3.5-turbo",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256
    )

    print(response["choices"][0]["text"])
    text += response["choices"][0]["text"]
    if not os.path.exists("../openai"):
        os.mkdir("../openai")

    with open(f"openai/prompt- {random.randint(1, 324932749733534)}","w") as f:
        f.write(text)


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")

    elif hour>=18 and hour<20:
        speak("Good Evening!")
    else:
        speak("Good Night!")

    speak("I am Jarvis Sir. Please tell me how can I help you")

def takeCommand():
    #It take microphone input from user and return string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1.5
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"User said: {query}\n")

    except Exception as e:
        #print(e)
        print("Say that again please...")
        return "None"
    return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login('youremail@gmail.com', 'your_password')
    server.sendmail('youremail@gmail.com',to,content)
    server.close()

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()
        #Logic for executing tasks based on query

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif ' open Google' in query:
            webbrowser.open("google.com")

        elif 'Play music' in query:
            music_dir = "D:\\songs"
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir , the time is {strTime}")

        elif 'open code' in query:
            codePath = "C:\\Users\\Shubham Anil Birari\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)

        elif 'email to harry' in query:
            try:
                speak("What you should i say?")
                content = takeCommand()
                to = "shubhambirari698@gmail.com"
                sendEmail(to, content)
                speak("Email has been send")
            except Exception as e:
                print(e)
                speak("sorry my friend shubham. I am not able to send this email")

        elif "using open AI".lower() in query.lower():
            ai(prompt=query)



