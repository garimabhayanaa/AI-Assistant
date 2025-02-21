from frontend.GUI import (
    graphical_user_interface,
    set_assistant_status,
    show_text_to_screen,
    temp_directory_path,
    set_microphone_status,
    answer_modifier,
    query_modifier,
    get_microphone_status,
    get_assistant_status
)
from backend.Model import first_layer_dmm
from backend.RealtimeSearchEngine import realtime_search_engine
from backend.Automation import automation
from backend.SpeechToText import speech_recognition
from backend.Chatbot import chatbot
from backend.TextToSpeech import TTS
from backend.AppControl import perform_task_on_application  
from dotenv import dotenv_values
from asyncio import run
from time import sleep
import subprocess
import threading
import json
import os
import sys

env_vars=dotenv_values(".env")
USERNAME= env_vars.get("USERNAME")
ASSISTANT_NAME= env_vars.get("ASSISTANT")

DEFAULT_MESSAGE=f'''
{USERNAME} : Hello {ASSISTANT_NAME}, How are you?
{ASSISTANT_NAME} : Welcome {USERNAME}. I am doing well. How may I help you?
'''
subprocesses=[]
functions =["open", "close", "play", "system", "content", "google search", "youtube search"]

# Global variable to track unanswered input
unanswered_input = None

def has_unanswered_input():
    return unanswered_input is not None

def answer_unanswered_input():
    global unanswered_input
    if unanswered_input:
        # Process the unanswered input
        query_final = unanswered_input
        answer = chatbot(query_modifier(query_final))
        show_text_to_screen(f"{ASSISTANT_NAME} : {answer}")
        set_assistant_status("Answering...")
        TTS(answer)
        unanswered_input = None  # Reset the unanswered input after processing

def show_default_chats():
    file= open(r'data/ChatLog.json',"r", encoding='utf-8')
    if len(file.read())<5:
        with open(temp_directory_path('Database.data'),'w',encoding='utf-8') as file:
            file.write("")

        with open(temp_directory_path('Responses.data'),'w',encoding='utf-8') as file:
            file.write(DEFAULT_MESSAGE)

def read_chatlog_json():
    with open(r'data/ChatLog.json','r',encoding='utf-8') as file:
        chatlog_data=json.load(file)
    return chatlog_data

def chatlog_integration():
    json_data= read_chatlog_json()
    formatted_chatlog=""
    for entry in json_data:
        if entry["role"] =="user":
            formatted_chatlog += f"User: {entry['content']}\n"
        elif entry["role"] == "assistant":
            formatted_chatlog += f"Assistant: {entry['content']}\n"
    formatted_chatlog=formatted_chatlog.replace("User", USERNAME+" ")
    formatted_chatlog = formatted_chatlog.replace("Assistant",ASSISTANT_NAME+" ")

    with open(temp_directory_path('Database.data'),'w', encoding='utf-8') as file:
        file.write(answer_modifier(formatted_chatlog))

def show_chats_on_gui():
    file= open(temp_directory_path('Database.data'),'r', encoding='utf-8')
    data=file.read()
    if len(str(data))>0:
        lines= data.split('\n')
        result= '\n'.join(lines)
        file.close()
        file= open(temp_directory_path('Responses.data'),'w',encoding='utf-8')
        file.write(result)
        file.close()

def initial_execution():
    set_microphone_status("False")
    show_text_to_screen("")
    show_default_chats()
    chatlog_integration()
    show_chats_on_gui()

initial_execution()



def main_execution():
    global unanswered_input  # Declare the global variable to modify it
    task_execution = False
    image_execution = False
    image_generation_query = ""

    set_assistant_status("Listening...")
    query = speech_recognition()
    
    if query:  # Check if there is a valid query
        show_text_to_screen(f"{USERNAME}: {query}")
        unanswered_input = None  # Reset unanswered input if there's a valid query
    else:
        unanswered_input = query  # Store the query if it's empty (indicating no input)

    set_assistant_status("Thinking...")
    try: 
        decision = first_layer_dmm(query)

        print("")
        print(f"Decision: {decision}")
        print("")

        G = any([i for i in decision if i.startswith("general")])
        R = any([i for i in decision if i.startswith("realtime")])

        merged_query = " and ".join(
            [" ".join(i.split()[1:]) for i in decision if i.startswith("general") or i.startswith("realtime")]
        )

        for queries in decision:
            if task_execution==False:
                if any(queries.startswith(func) for func in functions):
                    run(automation(list(decision)))
                    task_execution=True
        
        if image_execution==True:

            with open(r"frontend/Files/ImageGeneration.data","w") as file:
                file.write(f"{image_generation_query},True")

            try:
                p1= subprocess.Popen(['python', r'backend/ImageGeneration.py'],
                                    stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                                    stdin=subprocess.PIPE, shell=False)
                subprocesses.append(p1)

            except Exception as e:
                print(f"Error starting ImageGeneration.py: {e}")
        
        if G and R or R:
            set_assistant_status("Searching...")
            answer= realtime_search_engine(query_modifier(merged_query))
            show_text_to_screen(f"{ASSISTANT_NAME} : {answer}")
            set_assistant_status("Answering...")
            TTS(answer)
            return True
        
        else:
            for queries in decision:

                if "perform " in queries:  # Check for the new command
                    query_final=queries.replace("perform ","")
                    _, app_name, task, *args = query_final.split()  # Split the command into parts
                    perform_task_on_application(app_name,task, *args)  # Call the function
                    return True

                elif "general" in queries:
                    set_assistant_status("Thinking...")
                    query_final= queries.replace("general ","")
                    answer= chatbot(query_modifier(query_final))
                    show_text_to_screen(f"{ASSISTANT_NAME} : {answer}")
                    set_assistant_status("Answering...")
                    TTS(answer)
                
                elif "realtime" in queries:
                    set_assistant_status("Searching...")
                    query_final=queries.replace("realtime ","")
                    answer= realtime_search_engine(query_modifier(query_final))
                    show_text_to_screen(f"{ASSISTANT_NAME} : {answer}")
                    set_assistant_status("Answering...")
                    TTS(answer)
                    return True
                
                elif "exit" in queries:
                    query_final = "Okay, Bye!"
                    answer = chatbot(query_modifier(query_final))
                    show_text_to_screen(f"{ASSISTANT_NAME} : {answer}")
                    set_assistant_status("Answering...")
                    TTS(answer)
                    sys.exit(0)
                    return
    except Exception as e:
        print(f"An error occurred: {e}")  
        set_assistant_status("Listening...") 

def first_thread():
    while True:
        current_status = get_microphone_status()

        if current_status == "True":
            set_assistant_status("Listening...")
            main_execution()
        else:
            AI_status = get_assistant_status()

            if "Available..." in AI_status:
                sleep(0.1)
            else:
                # Check if there was any unanswered input
                if has_unanswered_input():  # You need to implement this function
                    answer_unanswered_input()  # You need to implement this function
                else:
                    set_assistant_status("Available...")

def second_thread():
    graphical_user_interface()

if __name__=="__main__":
    thread2=threading.Thread(target=first_thread, daemon=True)
    thread2.start()
    second_thread()