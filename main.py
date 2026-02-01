import time
import webbrowser
import pyttsx3
import speech_recognition as sr
from datetime import datetime
import subprocess
import os
from google.genai import Client

api_key = os.getenv("GEMINI_API_KEY")  # Reads the env variable
client = Client(api_key=api_key)

def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def takecommand():
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source, duration=1)  # Added: Adjust for background noise
            audio = r.listen(source)

        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"User said: {query}")
        return query

    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
        say("Sorry, I couldn't understand that. Please try again.")
        return None  # Changed: Return None instead of string

    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        say("Network error. Please check your internet connection.")
        return None

    except Exception as e:
        print(f"Error: {e}")
        say("Can't recognize your voice. Please try again.")
        return None  # Changed: Return None instead of string

def ask_ai(prompt):
    """Send query to Gemini AI and get response"""
    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return "Sorry, I couldn't get a response from AI."


if __name__ == "__main__":
    say("Hello I am Jarvis AI")
    while True:
        query = takecommand()
        if query is None:
            continue
        query = query.lower()

        # Exit command
        if "exit" in query or "quit" in query:
            say("Goodbye")
            break

        # Sites Opening
        sites = [
            {"name": "Youtube", "link": "https://www.youtube.com"},
            {"name": "Google", "link": "https://www.google.com"},
            {"name": "Wikipedia", "link": "https://www.wikipedia.com"},
            {"name": "Spotify", "link": "https://open.spotify.com/"}
        ]

        site_opened = False
        for site in sites:
            if f"open {site['name'].lower()}" in query:
                say(f"Opening {site['name']}")
                webbrowser.open(site["link"])
                site_opened = True

                # Open Music
                if site['name'] == 'Spotify':
                    say("Play Chhaiya Chhaiya Song")
                    webbrowser.open("https://open.spotify.com/track/5H4rKylLnO8KrmdXTRhj5s")
                break

        if site_opened:
            continue

        # Current time
        if "current time" in query or "current time" in query:
            curr_time = datetime.now().strftime("%H:%M:%S")
            say(f"Current time is {curr_time}")
            print(curr_time)

        # Open camera
        elif "open camera" in query or "open my camera" in query:
            say("Opening camera")
            subprocess.run("start microsoft.windows.camera:", shell=True)

        # AI response for everything else
        else:
            say("Let me think...")
            answer = ask_ai(query)
            say(answer)
            print("Jarvis:", answer)