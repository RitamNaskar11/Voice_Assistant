import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
from urllib.parse import quote_plus

engine = pyttsx3.init()
engine.setProperty("rate", 160)

recognizer = sr.Recognizer()


# Function to speak
def speak(text):
    print("Pyvoice:",text)
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

while True:
    query = listen()

    if not query:
        continue
    if "hello" in query or "hi" in query:
        speak("Hello! Nice to talk to you")

    elif query == "how are you":
        speak("I am doing great. Thank you for asking!")

    elif "your name" in query:
        speak("My name is Pyvoice")

    elif "time" in query:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        current_date = datetime.datetime.now().strftime("%d %B %Y")
        speak(f"The current time is {current_time}")
        speak(f"Today's date {current_date}")

    elif "day" in query:
        current_day = datetime.datetime.now().strftime("%A")
        speak(f"Today is {current_day}")

    elif "youtube" in query:
        speak("Opening Youtube")
        webbrowser.open("https://www.youtube.com")

    elif "search for" in query:
        search_query = query.replace("searc for", "",1).strip()
        if search_query:
            speak(f"Searching Google {search_query}")
            webbrowser.open("https://www.google.com/search?q=" + quote_plus(search_query))

        else:
            speak("What should I search for?")
    
    elif "stop" in query or "exit" in query or "goodbye" in query or "bye" in query:
        speak("Goodbye! See you again.")
        break



    else:
        speak("Sorry, I don't know that command yet.")
            



