from webbrowser import open as webopen # import web browser functionality 
from pywhatkit import playonyt,search # functions for google search and youtube playback
from googlesearch import search as search_g
from dotenv import dotenv_values # to manage environment variables
from bs4 import BeautifulSoup # to parse html content
from rich import print # for styled console output
from groq import Groq # for AI chat functionalities
import webbrowser # for opening urls
import subprocess # for interacting with the system
import requests # for making https requests
import os # for operating system functionalities
import asyncio # for asynchronous programming
import keyboard # for keyboard related actions
import psutil  # Make sure to import psutil at the top of your file
import time

# load environment variables
env_vars=dotenv_values(".env")
GROQ_API_KEY=env_vars.get("GROQ_API_KEY")

# define css classes for parsing specific elements in html
classes=["zCubwf", "hgKElc", "LTKOO sY7ric", "Z0LcW", "gsrt vk_bk FzvWSb YwPhnf", "pclqee", "tw-Data-text tw-text-small tw-ta", 
        "IZ6rdc", "O5uR6d LTKOO", "vlzY6d", "webanswers-webanswers_table__webanswers-table", "dDoNo ikb4Bb gsrt", "sXLaOe", 
        "LWkfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"]

# define user agent for making web requests
user_agent= 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

# initialise client with api
client= Groq(api_key=GROQ_API_KEY)

# predefined professional responses for user interaction
professional_responses=[
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or support you may need. Please do not hesitate to ask."
]

# list to store chatbot messages
messages=[]

# system message to provide context to chatbot
system_chatbot= [{"role": "system", "content": f"Hello, I am {env_vars.get("USERNAME")}. You are a content writer. You have to write content like letters, codes, applications, essays, notes, songs, poems etc."}]

# function to perform google search
def google_search(Topic):
    search(Topic) # use pywhatkit's search function to perform google search
    return True # indicate success

# function to generate content using AI
def content(Topic):

    # nested function to open a file in text editor
    def open_notepad(file):
        if os.name == 'posix':  # Check if running on Unix-like system (Mac/Linux)
            default_text_editor = 'open'  # 'open' command on Mac will use default text editor (TextEdit)
        else:
            default_text_editor = 'notepad.exe'  # Windows default
        subprocess.Popen([default_text_editor, file])  # open file in text editor

    # nested function to generate content using AI chatbot
    def content_writer(prompt):
        messages.append({"role": "user", "content": f"{prompt}"}) # add user's prompt to messages

        completion= client.chat.completions.create(
            model= "mixtral-8x7b-32768",
            messages= system_chatbot+messages,
            max_tokens= 2048,
            temperature=0.7,
            top_p=1,
            stream= True,
            stop=None
        )

        answer=""

        # process streamed response chunks
        for chunk in completion:
            if chunk.choices[0].delta.content: # chck or content in current chunk
                answer += chunk.choices[0].delta.content # append content to answer
        
        answer = answer.replace("</s>", " ") # remove unwanted tokens from response
        messages.append({"role": "assistant", "content": answer}) # add ai's response tp messages
        return answer
    
    Topic: str= Topic.replace("Content ","") # remove "Content" from the topic
    content_by_ai= content_writer(Topic) # generate content using ai

    # save generated content to text file
    with open(rf"data/{Topic.lower().replace(' ','')}.txt", "w", encoding="utf-8") as file:
        file.write(content_by_ai) # write content to file
        file.close()

    open_notepad(rf"data/{Topic.lower().replace(' ','')}.txt") # open file in text editor
    return True # indicate success

# function to search for a topic on YouTube
def youtube_search(topic):
    try:
        # Construct the search URL
        search_url = f"https://www.youtube.com/results?search_query={topic}"
        print(f"Opening YouTube search for: {topic}")  # Debugging output
        webbrowser.open(search_url)  # Open the search URL in the default web browser
        return True  # indicate success
    except Exception as e:
        print(f"Error opening searching youtube: {e}")  # print the error message
        return False  # indicate failure

# function to play video on youtube
def play_youtube(query):
    playonyt(query) # use pywhatkit's playonyt function to play the video
    return True # indicate success

# function to open an application or relevant webpage
def open_app(app, sess=requests.Session()):  # Create a Session object
    try:
        if os.name == 'posix':  # Check if running on macOS
            subprocess.Popen(['open', '-a', app])  # Use 'open' command to open the app
        else:  # Assume Windows
            subprocess.Popen(['start', app], shell=True)  # Use 'start' command to open the app
        
        # Check if the application is running
        time.sleep(3)
        if not is_app_running(app):
            print(f"{app} did not start. Proceeding to search online...")
            search_and_open(app, sess)  # Call the search function
            return False  # indicate failure to open app

        return True  # indicate success

    except Exception as e:
        print(f"Error opening app: {e}")  # print the error message
        search_and_open(app, sess)  # Call the search function
        return False  # indicate failure to open app

def is_app_running(app_name):
    """Check if there is any running process that contains the given app_name."""
    for process in psutil.process_iter(['name']):
        if app_name.lower() in process.info['name'].lower():
            return True
    return False

def search_and_open(app, sess):
    try:
        print(f"Searching for: {app}")
        search_results = list(search_g(app, num_results=1))  # Get first result

        if search_results:
            first_link = search_results[0]
            print(f"Opening: {first_link}")
            webbrowser.open(first_link)  # Open the first link
            return True
        else:
            print("No valid search results found.")
            return False
    except Exception as e:
        print(f"Error occurred: {e}")
        return False

# function to close an application
def close_app(app):

    if "chrome" in app:
        pass
    else:
        try:
            if is_app_running(app):
                if os.name == 'posix':  # macOS/Linux
                    subprocess.run(['pkill', '-i', app], check=True)  # Case-insensitive kill
                else:  # Windows
                    subprocess.run(['taskkill', '/F', '/IM', f"{app}.exe"], shell=True, check=True)
                print(f"{app} has been closed.")
                return True
            else:
                print(f"{app} is not running.")
                return False
        except Exception as e:
            print(f"Error closing app: {e}")
            return False

def system_commands(command):
    if command == "mute":
        subprocess.run(["osascript", "-e", "set volume output muted true"])
    elif command == "unmute":
        subprocess.run(["osascript", "-e", "set volume output muted false"])
    elif command == "volume up":
        subprocess.run(["osascript", "-e", "set volume output volume (output volume of (get volume settings) + 5)"])
    elif command == "volume down":
        subprocess.run(["osascript", "-e", "set volume output volume (output volume of (get volume settings) - 5)"])


# asynchronous function to translate and execute user commands
async def translate_and_execute(commands: list[str]):
    funcs=[] # list to store asynchronous tasks

    for command in commands:
        if command.startswith("open "): # handle open commands
            if "open it" in command:
                pass
            if "open file" in command:
                pass
            else:
                fun= asyncio.to_thread(open_app,command.removeprefix("open ")) # schedule app opening
                funcs.append(fun)

        elif command.startswith("general "):  # placeholder for general commands
            pass
        elif command.startswith("realtime "):
            pass
        elif command.startswith("close "):
            fun= asyncio.to_thread(close_app, command.removeprefix("close ")) # schedule app closing
            funcs.append(fun)

        elif command.startswith("play "):
            fun= asyncio.to_thread(play_youtube, command.removeprefix("play "))
            funcs.append(fun)

        elif command.startswith("content "):
            fun= asyncio.to_thread(content,command.removeprefix("content "))
            funcs.append(fun)
        
        elif command.startswith("google search "):
            fun=asyncio.to_thread(google_search,command.removeprefix("google search "))
            funcs.append(fun)

        elif command.startswith("youtube search "):
            fun=asyncio.to_thread(youtube_search, command.removeprefix("youtube search "))
            funcs.append(fun)

        elif command.startswith("system "):
            fun=asyncio.to_thread(system_commands,command.removeprefix("system "))
            funcs.append(fun)

        else:
            print(f"No function found for {command}")

    results= await asyncio.gather(*funcs) # execute all tasks concurrently

    for result in results: # process results
        if isinstance(result,str):
            yield result
        else:
            yield result

async def automation(commands: list[str]):

    async for result in translate_and_execute(commands):
        pass
    return True # indicate success

if __name__=="__main__":
    asyncio.run(automation([]))