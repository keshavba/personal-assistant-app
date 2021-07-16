import speech_recognition as sr
from gtts import gTTS
from datetime import datetime
import webbrowser
import time
import playsound
import os
from os import path
import random
import pickle
from dotenv import load_dotenv

from googleapiclient.discovery import build
from urllib import parse

load_dotenv()
recognizer = sr.Recognizer()
appName = "Kashish"

def terms_exist(terms):
    for term in terms:
        if term in voice_data:
            return True

class person:
    name = ''
    def set_name(self, name):
        self.name = name

def record_audio(ask = False, short_response = False):
    with sr.Microphone() as source:
        if(ask):
            assistant_speak(ask)
        
        if short_response:
            audio = recognizer.record(source, 5)
        else:
            audio = recognizer.listen(source)
        
        recognizer.adjust_for_ambient_noise(source)
        voice_data = ''
        try:
            voice_data = recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            assistant_speak('Apologies. I did not understand you.')
        except sr.RequestError:
            assistant_speak('Unfortunately, I am not working right now!')
        
        print(f">> {voice_data.lower()}")
        return voice_data.lower()

def assistant_speak(audio_string):
    tts = gTTS(text=audio_string, tld='co.in', lang="en")
    r = random.randint(1, 2000000000)
    audio_file = 'audio-' + str(r) + '.mp3'
    tts.save(audio_file)
    print(f">> {appName}: {audio_string}")
    playsound.playsound(audio_file)
    os.remove(audio_file)

def respond(voice_data):

    if terms_exist(['hey', 'hi', 'hello']):
        greetings = [f"hey, how can I help you, {user.name}?", f"hey, what's up, {user.name}?", f"I'm listening, {user.name}.", f"how can I help you, {user.name}?", f"hello {user.name}!"]
        greet = greetings[random.randint(0, len(greetings)-1)]
        assistant_speak(greet)
    
    if terms_exist(['what is your name', "what's your name", "tell me your name"]):
        assistant_speak(f'My name is {appName}!')
    
    if terms_exist(['how are you', 'how are you doing']):
        assistant_speak(f"I'm doing good, thanks for asking {user.name}")

    if terms_exist(['tell me my name']):
        assistant_speak(f"Your name should be {user.name}, unless I misspelled it!")
    
    if terms_exist(['change name']):
        data = record_audio(ask='Okay, please tell me your name', short_response=True)
        person_name = data

        response = record_audio(f"Is your name {person_name}?")
        if "no" in response:
            assistant_speak("Apologies. I misspell like Starbucks baristas!")
        else:
            assistant_speak(f"Great! Seems like I got lucky this time.")

        user.set_name(person_name)

        empty_list = []
        openfile = open(str(os.getenv('NAME')), 'wb')
        pickle.dump(empty_list, openfile)
        pickle.dump(user.name, openfile)
        openfile.close()

    if terms_exist(['what time is it', "what's the time", "tell me the time"]):
        currentTime = datetime.now()

        if currentTime.hour >= 13:
            hour = currentTime.hour - 12
            clockTime = "PM"
        elif currentTime.hour == 0:
            hour = 12
            clockTime = "AM"
        else:
            hour = currentTime.hour
            clockTime = "AM"

        time = f'{hour}:{currentTime.minute} {clockTime}'
        assistant_speak(time)

    if terms_exist(['search', 'search for']) and 'youtube' not in voice_data and 'weather' not in voice_data:
        if 'search for' in voice_data:
            search_phrase = voice_data.split("search for")[-1]
        else:
            search_phrase = voice_data.split("search")[-1]
        
        search_query(search_phrase)

    if terms_exist(['youtube']):
        if 'youtube for' in voice_data:
            search_phrase = voice_data.split("youtube for")[-1]
        else:
            search_phrase = voice_data.split("youtube")[-1]
        
        url = f"https://www.youtube.com/results?search_query={search_phrase}"
        webbrowser.get().open(url)
        assistant_speak('Here is what I found for' + search_phrase + ' on youtube')

    if terms_exist(['weather']):
        search_phrase = voice_data.split("search")[-1]
        url = "https://google.com/search?q=" + search_phrase
        webbrowser.get().open(url)
        assistant_speak("Here is the" + search_phrase + " on google")

    if terms_exist(['find location']):
        location = record_audio('What is the location?')
        url = 'https://www.google.com/maps/search/?api=1&query=' + location 
        webbrowser.get().open(url)
        assistant_speak('Here is the location of ' + location)
    
    if terms_exist(['show calendar', 'shoe calendar']):
        url = 'https://calendar.google.com'
        webbrowser.get().open(url)
        assistant_speak("Here's your calendar!")
    
    if terms_exist(['coronavirus update', 'covid update', 'covid 19 update']):
        google_url = "https://google.com/search?q=" + 'coronavirus+update'
        webbrowser.get().open(google_url)
        atlantic_url = "https://www.theatlantic.com/projects/our-essential-coronavirus-coverage/"
        webbrowser.get().open(atlantic_url)
        assistant_speak('Here is coronavirus updates on Google and the latest Atlantic articles related to the coronavirus!')
    
    if terms_exist(['rock-paper-scissors']):
        voice_data = record_audio("choose among rock, paper, or scissors")
        moves=["rock", "paper", "scissors"]
    
        comp_move = random.choice(moves)
        player_move = voice_data
        
        assistant_speak("The computer chose " + comp_move)
        assistant_speak("You chose " + player_move)
        
        if player_move == comp_move:
            assistant_speak("The match is a draw")
        elif player_move == "rock" and comp_move == "scissors":
            assistant_speak("Player wins")
        elif player_move == "rock" and comp_move == "paper":
            assistant_speak("Computer wins")
        elif player_move == "paper" and comp_move == "rock":
            assistant_speak("Player wins")
        elif player_move == "paper" and comp_move == "scissors":
            assistant_speak("Computer wins")
        elif player_move == "scissors" and comp_move == "paper":
            assistant_speak("Player wins")
        elif player_move == "scissors" and comp_move == "rock":
            assistant_speak("Computer wins")

    if terms_exist(['thank you']):
        assistant_speak("My pleasure!")

    if terms_exist(['exit', 'leave', 'quit', 'goodbye']):
        assistant_speak('Goodbye!')
        exit()

def search_query(query):
    query_plus = parse.quote_plus(query)
    custom_engine = os.environ.get('SEARCH_ENGINE')
    api_key = os.environ.get('API_KEY')
    resource = build("customsearch", 'v1', developerKey=api_key).cse()
    result = resource.list(q = query_plus, cx = custom_engine).execute()
    
    links = []
    titles = []

    for item in result['items']:
        titles.append(item['title'])
        links.append(item['link'])

    for title, link in zip(titles, links):
        print(f"{title}: {link}")

    url = 'https://google.com/search?q=' + query
    webbrowser.get().open(url)
    assistant_speak('These are the top 10 results from Google. Also, here is' + query + ' on google')

def set_user_name():

    person_name = record_audio()
    
    response = record_audio(f"Is your name {person_name}?")
    if "no" in response:
        assistant_speak("Apologies. I mispronounce like Starbucks baristas!")
    else:
        assistant_speak(f"Great! Seems like I got lucky this time.")

    user.set_name(person_name)
    pickle.dump(user.name, open(str(os.getenv('NAME')), 'wb'))

time.sleep(1)

user = person()

if path.exists(str(os.getenv('NAME'))):

    with (open(str(os.getenv('NAME')), "rb")) as openfile:
        while True:
            try:
                user.name = pickle.load(openfile)
            except EOFError:
                break
    
    assistant_speak("Hi! How can I help you?")
else:
    assistant_speak("Hi! First off, may I know your name?")
    set_user_name()

while path.exists(str(os.getenv('NAME'))):
    voice_data = record_audio()
    respond(voice_data)
