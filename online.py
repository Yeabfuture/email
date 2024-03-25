import requests
from email.message import EmailMessage
import smtplib
import wikipedia
from decouple import config
import pywhatkit as kit

EMAIL = "yeabsiramersha58@gmail.com"
PASSWORD = "erpe dnyw bxfi xsza"


def search_on_wiki(query):
    result = wikipedia.summary(query, sentences=2)
    return result

def search_on_google(query):
    kit.search(query)

def youtube(video):
    kit.playonyt(video)

def send_email(receiver_add,subject,message):
    try:
        email = EmailMessage()
        email['To'] = receiver_add
        email['Subject'] = subject
        email['From'] = EMAIL

        email.set_content(message)
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        s.login(EMAIL,PASSWORD)
        s.send_message(email)
        s.close()
        return  True
    except Exception as e:
        print(e)
        return False