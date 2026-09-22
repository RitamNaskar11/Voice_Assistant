import pyttsx3
import speech_recognition as sr
import datetime
# import webbrowser
from urllib.parse import quote_plus
import subprocess
import requests
import psutil


engine = pyttsx3.init()
engine.setProperty("rate", 140)

recognizer = sr.Recognizer()


# Function to speak
def speak(text):
    print("Emo:",text)
    engine.say(text)
    engine.runAndWait()
    

speak("Hello! I am Emo, your virtual assistant.")


# with sr.Microphone() as source:
#     print("Something Speak")
#     audio = recognizer.listen(source)

def listen():
    try:
        with sr.Microphone() as source:
            print("\nListening")

            recognizer.adjust_for_ambient_noise(source, duration=0.5)

            audio = recognizer.listen(source,timeout=5 , phrase_time_limit=5)

        print("Recognizing")

        query = recognizer.recognize_google(audio , language = "en-IN")

        print("You", query)
        return query.lower()

    except sr.WaitTimeoutError:
            print("No speech detected.")
            return ""
    
    except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
            return ""
    
    except sr.RequestError:
            speak("Please check your internet connection.")
            return ""
# function of telling joke
def tell_joke():
    try:
        url = "https://official-joke-api.appspot.com/random_joke"

        response = requests.get(url, timeout = 10)
        response.raise_for_status()

        joke_data = response.json()

        setup = joke_data["setup"]
        punchline = joke_data["punchline"]

        speak(setup)
        speak(punchline)

    except requests.exceptions.RequestException:
        speak("Sorry, I cannot fetch a joke right now.")

# function of check weather
def get_weather(city):
    try:
        speak(f"Checking weather in {city}")

        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url, timeout = 10)
        response.raise_for_status()

        weather_data = response.json()

        current = weather_data ["current_condition"][0]

        temperature = current["temp_C"]
        condition = current["weatherDesc"][0]["value"] 
        humidity = current["humidity"]

        speak(f"The temperature in {city} is {temperature} degree Celsius")
        speak(f"Weather condition is {condition}")
        speak(f"Humadity is {humidity} percent")

    except requests.exceptions.RequestException:
        speak("Sorry, I could not fetch weather information.")
    except (KeyError , IndexError, ValueError):
        speak("Sorry, I could not understand the weather data.")

# function of checking bettery

def bettery_check():
    battery = psutil.sensors_battery()

    if battery is None:
        speak("Sorry, battery information is not available.")
        return
    percentage = battery.percent

    if battery.power_plugged:
        status = "Your device is charging"
    else:
        status = "Your device is not charging"
    speak(f"Your battery is at {percentage} percent")
    speak(status)

while True:
    query = listen()

    if not query:
        continue

    elif query.strip() in ["hi","hello" ,"hey"]:
        speak("Hello! Nice to talk to you")

    elif query == "how are you":
        speak("I am doing great. Thank you for asking!")

    elif "your name" in query:
        speak("My name is Emo")
# joke command
    elif "joke" in query:
        speak("Here is joke for you")
        tell_joke()

# weather command
    elif "weather in " in query:
        city = query.split("weather in ", 1)[1].strip()
        if city:

            speak(f"Did you say {city}? Please say yes or no")
            confirmation = listen()
            if "yes" in confirmation:
                get_weather(city)
            elif "no" in confirmation:
                speak("Sorry, please tell me the city name again.")
            else:
                speak("I could not confirm the city. Please try again.")

        else:
            speak("Please tell me the city name")

# bettery check command
    elif "battery" in query:
        bettery_check()

# time and date command
    elif "time" in query:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        current_date = datetime.datetime.now().strftime("%d %B %Y")
        speak(f"The current time is {current_time}")
        speak(f"Today's date {current_date}")

    elif "day" in query:
        current_day = datetime.datetime.now().strftime("%A")
        speak(f"Today is {current_day}")

# searching command
    elif "search for" in query:
        search_query = query.replace("search for", "",1).strip()
        if search_query:
            speak(f"Searching Google for {search_query}")
            subprocess.Popen(["cmd","/c","start","chrome","https://www.google.com/search?q=" + quote_plus(search_query)])
        else:
            speak("What should I search for?")

# open application and play command
    elif "open youtube" in query:
        speak("Opening YouTube")    
        subprocess.Popen(["cmd", "/c", "start", "chrome","https://www.youtube.com"])

    elif "play" in query:
        song = query.replace("play","",1).strip()

        if song.endswith(" song"):
            song = song[:-5].strip()
            

        if song:
            speak(f"Searching Youtube for {song}")   
            subprocess.Popen(["cmd", "/c", "start","chrome","https://www.youtube.com/results?search_query=" + quote_plus(song)])
        else:
            speak("What should I play for?")

# open notepad command
    elif "notepad" in query:
        speak("Opening Notepad")
        subprocess.Popen(["notepad"])

# open calculator command
    elif "calculator" in query:
        speak("Opening calculator")
        subprocess.Popen(["calc"])

# calculate the calculation command
    elif "calculate" in query:
        speak("Lets the calculate")
        expression = query.replace("calculate", "", 1).strip()

        expression = expression.replace("+", " plus ")
        expression = expression.replace("-", " minus ")
        # expression = expression.replace("*", " multiply ")
        expression = expression.replace("/", " divide ")
        expression = expression.replace(" x ", " multiply ")
    

        try:
            if "plus" in expression:
                numbers = expression.split("plus")
                result = float(numbers[0])+ float(numbers[1])
            elif "minus" in expression:
                numbers = expression.split("minus")
                result = float(numbers[0])- float(numbers[1])
            elif "multiply" in expression:
                numbers = expression.split("multiply")
                result = float(numbers[0])* float(numbers[1])
            elif "divide" in expression:
                numbers = expression.split("divide")
                result = float(numbers[0])/ float(numbers[1])

            else:
                speak("Sorry I don't calculation this")
                continue
            if result == int(result):
                result = int(result)
            speak(f"The answer is {result}")

        except (ValueError,IndexError,ZeroDivisionError):
            speak("Sorry, I could not calculate that.")


    
    elif "stop" in query or "exit" in query or "goodbye" in query or "bye" in query:
        speak("Goodbye! See you again.")
        break



    else:
        speak("Sorry, I don't know that command yet.")
            



