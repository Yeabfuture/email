import pyttsx3
import speech_recognition as sr
import os
import subprocess as sp
from decouple import config
from datetime import datetime
from online import search_on_google, search_on_wiki, youtube, send_email

# Initialize Text-to-Speech Engine
engine = pyttsx3.init('sapi5')
engine.setProperty('volume', 2.5)
engine.setProperty('rate', 190)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Load Configuration
USER = config('USER')
HOSTNAME = config('BOT')

# Function to Speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to Recognize Speech
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        print("Recognizing....")
        query = r.recognize_google(audio, language='en-in')
        print("You said:", query)
        if 'stop' in query or 'exit' in query:
            hour = datetime.now().hour
            if 21 <= hour < 6:
                speak(f"It's time to sleep {USER}. Have a good night")
            else:
                speak(f"Good day {USER}")
            exit()
        else:
            return query.lower()
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that. Please try again.")
        return 'None'
    except sr.RequestError as e:
        print("Sorry, I am unable to process your request at the moment. Please try again later.")
        print(f"Recognition request failed: {e}")
        return 'None'
    except Exception as e:
        print("Sorry, an unexpected error occurred. Please try again.")
        print(f"Error: {e}")
        return 'None'

# Function to Greet User
def greet_me():
    hour = datetime.now().hour
    if 6 <= hour < 12:
        speak(f"Good Morning {USER}")
    elif 12 <= hour < 16:
        speak(f"Good afternoon {USER}")
    elif 16 <= hour < 20:
        speak(f"Good evening {USER}")
    else:
        speak(f"Hello {USER}, it's late. How may I assist you?")

# Main Function
if __name__ == '__main__':
    greet_me()
    listening = False
    speak("Waiting for wake word...")
    while True:
        if not listening:
            query = take_command()
            if "wake" in query:
                listening = True
                speak("How can I help you?")
        else:
            query = take_command()
            if "wake" in query:
                listening = False
                speak("Waiting for wake word...")
            elif "how are you" in query:
                speak("I'm doing great! How about you?")
            elif "open command prompt" in query:
                speak("Opening command prompt")
                os.system('start cmd')
            elif "open camera" in query:
                speak("Opening camera")
                sp.run('start microsoft.windows.camera', shell=True)
            elif "open figma" in query:
                speak("Opening figma")
                figma_path = r"C:\Users\hp\AppData\Local\Figma\figma.exe"
                os.startfile(figma_path)
            elif "open internet" in query:
                speak("Opening Internet")
                chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
                os.startfile(chrome_path)
            elif "wikipedia" in query:
                speak("What do you want to search on Wikipedia?")
                search = take_command()
                result = search_on_wiki(search)
                speak(f"According to Wikipedia, {result}")
            elif "youtube" in query:
                speak("What do you want to watch on YouTube?")
                video = take_command()
                youtube(video)
            elif "open google" in query:
                speak("What do you want to search in Google?")
                search_on_google(query)
            elif "send email" in query:
                speak("To whom? Please provide the email address.")
                receiver_add = input("To: Email address: ")
                speak("What is the subject of the email?")
                subject = take_command().capitalize()
                speak("What should be the content of the email? I'm listening...")
                message = take_command().capitalize()
                if send_email(receiver_add, subject, message):
                    speak(f"Email successfully sent to {receiver_add}")
                else:
                    speak("Sending email failed!")
