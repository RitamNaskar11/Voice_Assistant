import pyttsx3
import speech_recognition as sr
import datetime
# import webbrowser
from urllib.parse import quote_plus
import subprocess
import requests
import psutil
import pygetwindow as gw


engine = pyttsx3.init()
engine.setProperty("rate", 140)

recognizer = sr.Recognizer()


# Function to speak
def speak(text):
    print("Emo:",text)
    engine.say(text)
    engine.runAndWait()
    

speak("Hello!")


# with sr.Microphone() as source:
#     print("Something Speak")
#     audio = recognizer.listen(source)


# ollama model 
def ask_ai(query):
    prompt = f"""You are Emo, a fast voice assistant. Answer in simple, clear English. Keep answers short, around 2-4 sentences.
    Avoid unnecessary explanations. Answer the user's question directly. User: {query} Emo:"""

    try:
        url = "http://127.0.0.1:11434/api/generate"
        data = {
            "model":"llama3.2:3b",
            "prompt":prompt,
            "stream":False,
            "options": {
                "num_predict": 120
            }
        }
        
        session = requests.Session()
        session.trust_env = False

        response = session.post(
            url,
            json=data,
            timeout=120
        )

        response.raise_for_status()

        # AI ka response JSON format mein lena
        result = response.json()

        return result ["response"].strip()
    
    except requests.exceptions.RequestException as e:
        print("AI Error",e)
        return "Sorry, I cannot connect to my AI brain right now."
    except (KeyError,ValueError)as e:
        print("AI Response error")
        return "Sorry, I could not process the AI response."


# speak and listening function   
def listen():
    try:
        with sr.Microphone() as source:
            print("\nListening")

            recognizer.adjust_for_ambient_noise(source, duration=0.8)

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


# Close any running application

def close_app(app_name):
    app_name = app_name.lower().strip()
    # Remove common voice command words
    for word in ["emo", "you", "please", "close"]:
        app_name = app_name.replace(word, "").strip()

    

# Fix speech recognition mistakes
    app_aliases = {
        "age":"edge",
        "this":"edge",
        "microsoft age":"edge"
    }
    app_name = app_aliases.get(app_name,app_name)

    windows = gw.getAllWindows()
    
    matched = [
        window for window in windows
        if app_name in window.title.lower()
        and window.title.strip() != ""
    ]

    if not matched:
        speak(f"I could not find {app_name} open.")
        return

    closed = False

    for window in matched:
        try:
            window.close()
            closed = True
        except Exception:
            continue

    if closed:
        speak(f"Closing {app_name}")
    else:
        speak(f"Could not close {app_name}")




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
    elif "weather" in query:
        city = ""
        patterns = [
                    "checking weather in ",
        "checking weather at ",
        "checking weather for ",
        "checking weather ",
        "check the weather in ",
        "check the weather at ",
        "check the weather for ",
        "check the weather ",
        "check weather in ",
        "check weather at ",
        "check weather for ",
        "check weather ",
        "weather in ",
        "weather at ",
        "weather for "
        ]

        for pattern in patterns:
            if pattern in query:
                city = query.split(pattern, 1)[1].strip()
                break
        city = city.strip(".,?!")

        if city :
            get_weather(city)

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

    elif "open google" in query:
        speak("Opening google")    
        subprocess.Popen(["cmd", "/c", "start", "chrome","https://www.google.com"])

    elif "play" in query:
        song = query.replace("play","",1).strip()

        if song.endswith(" song"):
            song = song[:-5].strip()
            
        if song:
            speak(f"Searching Youtube for {song}")   
            subprocess.Popen(["cmd", "/c", "start","chrome","https://www.youtube.com/results?search_query="+quote_plus(song)])
        else:
            speak("What should I play for?")

# open notepad command (must be checked BEFORE the generic "open" command)
    elif "open" in query.lower() and "notepad" in query.lower():
        speak("Opening Notepad")
        subprocess.Popen(["notepad"])

# open calculator command (must be checked BEFORE the generic "open" command)
    elif "open" in query.lower() and "calculator" in query.lower():
        speak("Opening calculator")
        subprocess.Popen(["calc"])

    elif "open" in query.lower():
        app_name = query.lower().replace("open","",1).strip()

        apps={
            "word": "winword",
            "microsoft word": "winword",
            "excel": "excel",
            "microsoft excel": "excel",
            "paint": "mspaint",
            "edge": "msedge",
            "microsoft edge": "msedge",
            "whatsapp": "WhatsApp",
            "code": "vscode"
        }
        if app_name in apps:
            try:
                subprocess.Popen(["cmd" , "/c","start", "", apps[app_name]])
                speak(f"Open{app_name}")
            except Exception:
                speak(f"Could not open{app_name}")

        else:
            speak(f"Sorry I didn't find it{app_name}")


# calculate the calculation command
    elif "calculate" in query:
        speak("Lets the calculate")
        expression = query.replace("calculate", "", 1).strip()
        expression = expression.replace("+", " plus ")
        expression = expression.replace("-", " minus ")
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




    elif "close" in query.lower():
        app_name = query.lower()

        for word in ["emo", "you", "please", "close"]:
            app_name = app_name.replace(word, "").strip()

        if app_name:
            close_app(app_name)

        else:
            speak("Please tell me which application to close.")

    
    elif "stop" in query or "exit" in query or "goodbye" in query or "bye" in query:
        speak("Goodbye! See you again.")
        break


    

    else:
        answer = ask_ai(query)
        speak(answer)
            



