import os

import pyttsx3
from datetime import datetime, timedelta
import requests
import speech_recognition as sr
import smtplib
from secrets import senderemail, epwd
import wikipedia
import webbrowser as wb
import pywhatkit
import pyautogui
from time import sleep
from newsapi import NewsApiClient
import clipboard
import pyjokes
from nltk.tokenize import word_tokenize


engine = pyttsx3.init()


def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    engine.setProperty('rate', 175)

def time():
    Time = datetime.now().strftime("%I:%M:%S")
    speak("the current time is:")
    print(Time)
    speak(Time)


# Get today's date
presentday = datetime.now()  # or presentday = datetime.today()

# Get Yesterday
yesterday = presentday - timedelta(1)

# Get Tomorrow
tomorrow = presentday + timedelta(1)


def date():
    year = int(presentday.year)
    month = int(datetime.now().month)
    date = int(datetime.now().day)
    speak("The current date is:")
    print(date, month, year)
    speak(date)
    speak(month)
    speak(year)


def tom():
    year = int(tomorrow.year)
    month = int(tomorrow.month)
    date = int(tomorrow.day)
    print(date,month,year)
    speak(date)
    speak(month)
    speak(year)


def yst():
    year = int(yesterday.year)
    month = int(yesterday.month)
    date = int(yesterday.day)
    print(date,month,year)
    # print(month)
    # print(year)
    speak(date)
    speak(month)
    speak(year)


def greeting():
    hour = datetime.now().hour
    if 6 <= hour < 12:
        speak("good morning sir!")
    elif 12 <= hour < 18:
        speak("good afternoon sir!")
    elif 18 <= hour < 24:
        speak("good evening sir!")
    else:
        speak("good night sir!")


def wishme():
    greeting()
    speak("I am your virtual assistant. How can i help you?")


def takeCommandCMD():
    query = input("")
    return query


def takeCommandMic():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in").lower()
        print(query)
    except Exception as e:
        print(e)
        return ""
    return query


def sendEmail(content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(senderemail, epwd)
    print("Enter the receiver's email address")
    speak("Enter the receiver's email address")
    to = takeCommandCMD()
    server.sendmail(senderemail, to, content)
    server.close()


def searchgoogle():
    search = takeCommandMic()

    exit()


def sendwhatapp(phone_no, message):
    # pywhatkit.sendwhatmsg(phone_no, message, 12, 20)
    wb.open('https://web.whatsapp.com/send?phone='+phone_no+'&text='+message)
    sleep(10)
    pyautogui.press('enter')


def news():
    newsapi = NewsApiClient(api_key='19e9399bb6354c62a53edb5656b6ceed')
    data = newsapi.get_top_headlines(language='en', country='in', page_size=2)

    newsdata = data['articles']
    speak("Here are some of the top headlines")
    for x, y in enumerate(newsdata):
        x += 1
        print(f'{x} {y["description"]}')
        speak(f'{y["description"]}')

    speak("Thank You")


def text2speech():
    text = clipboard.paste()
    print(text)
    speak(text)


def covid():
    r = requests.get('https://coronavirus-19-api.herokuapp.com/all')

    data = r.json()
    covid_data = f'Confirmed Cases : {data["cases"]} \n Deaths : {data["deaths"]} \n Recovered : {data["recovered"]} \n'
    print(covid_data)
    # speak(covid_data)


if __name__ == "__main__":
    # wishme()
    while True:
        query = takeCommandMic().lower()
        if 'time' in query:
            time()

        elif 'tomorrow' in query:
            tom()

        elif 'yesterday' in query:
            yst()

        elif 'date' in query:
            date()

        elif 'email' in query:
            try:
                print('Please say the subject')
                speak('Please say the subject')
                content = takeCommandMic()
                sendEmail(content)
                speak("Email has been sent")
            except Exception as e:
                print(e)
                speak("unable to send the email")

        elif 'message' in query:
            user_name = {
                'swetha': '+919686850387',
                'dekshitha': '+919743182263'
            }
            try:
                print("To whom do you want to send the message")
                speak("To whom do you want to send the message")
                name = takeCommandCMD()
                phone_no = user_name[name]
                # phone_no = user_name
                print("What is the message")
                speak("What is the message")
                message = takeCommandMic()
                # message = "Hello"
                sendwhatapp(phone_no, message)
                speak("Message has been sent")
            except Exception as e:
                print(e)
                speak("Message was not sent")

        elif 'weather' in query:
            print('Please say a city name')
            speak('Please say a city name')
            city = takeCommandMic()
            api = '77e58d8a245c67dea108ce128f056434'
            url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&appid=77e58d8a245c67dea108ce128f056434'
            # print(url)
            res = requests.get(url)
            data = res.json()
            weather = data['weather'][0]['main']
            temp = data['main']['temp']
            description = data['weather'][0]['description']
            temp = round((temp - 32) * 5/9)
            print(f'weather in {city} city')
            print('Temperature is {} degree celcius'.format(temp))
            print('weather is {}'.format(description))
            speak(f'weather in {city} city')
            speak('Temperature is {} degree celcius'.format(temp))
            speak('weather is {}'.format(description))

        elif 'search' in query:
            query = query.replace("search", "")
            wb.open('https://www.google.com/search?q='+query)
            # exit()

        elif 'what is' in query:
            query = query.replace("what", "")
            # print(query)
            result = wikipedia.summary(query, sentences=2)
            print(result)
            speak(result)

        elif 'play' in query:
            query = query.replace("play", "")
            # topic = takeCommandMic()
            pywhatkit.playonyt(query)
            # exit()

        elif 'news' in query:
            news()

        elif 'read' in query:
            text2speech()

        elif 'covid' in query:
            covid()

        elif 'ms word' in query:
            codepath = 'C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE'
            os.startfile(codepath)

        elif 'code' in query:
            codepath = 'C:\\Users\\Vinay\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe'
            os.startfile(codepath)

        elif 'browser' in query:
            codepath = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'
            os.startfile(codepath)

        elif 'open' in query:
            os.system('explorer C://{}'.format(query.replace('open', '')))

        elif 'joke' in query:
            joke = pyjokes.get_joke()
            print(joke)
            speak(joke)

        elif 'note' in query:
            speak("please say the subject")
            data = takeCommandMic()
            remember = open('data.txt', 'w')
            remember.write(data)
            remember.close()
            os.startfile('D:\\Vinay\\Projects\\python\\data.txt')

        elif 'stop' in query:
            quit()