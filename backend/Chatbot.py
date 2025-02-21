from groq import Groq # to use Groq API
from json import load, dump # functions to read and write json files
import datetime # for real-time date and time information
from dotenv import dotenv_values # to load environment variables from .env

# load environment variables from .env
env_vars= dotenv_values(".env")
# retrieve user-specific variables
USERNAME=env_vars.get("USERNAME")
ASSISTANT=env_vars.get("ASSISTANT")
GROQ_API_KEY= env_vars.get("GROQ_API_KEY")

# initialise client using API key
client= Groq(api_key=GROQ_API_KEY)

# empty list to store messages
messages=[]

# system message that provides context to AI model about its role and behaviour
System = f"""Hello, I am {USERNAME}, You are a very accurate and advanced AI chatbot named {ASSISTANT} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in same language in which the user is talking.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

# list of system instructions for chatbot
SystemChatBot= [
    {"role":"system", "content": System}
]

# attempt to load chatlog from json file
try:
    with open(r"data/ChatLog.json","r") as f:
        messages=load(f)
except FileNotFoundError:
    with open(r"data/ChatLog.json","w") as f:
        dump([],f)

# function to get real-time date-time information
def realtime_information():
    current_datetime= datetime.datetime.now() # current date and time
    day= current_datetime.strftime("%A") # day of the week
    date= current_datetime.strftime("%d") # day of the month
    month= current_datetime.strftime("%B") # month name
    year= current_datetime.strftime("%Y") # year
    hour= current_datetime.strftime("%H") # hour in 24-hour format
    minute= current_datetime.strftime("%M") # minute
    second= current_datetime.strftime("%S") # second
    # format information
    data=f"Please use this real-time information if needed,\n"
    data += f"Day: {day}\nDate: {date}\nMonth: {month}\nYear: {year}"
    data += f"Time: {hour} hours {minute} minues {second} seconds"
    return data

# function to modify chatbot's response for better formatting
def answer_modified(answer):
    lines= answer.split('\n') # split response into lines
    non_empty_lines= [line for line in lines if line.strip()] # remove empty lines
    modified_answer='\n'.join(non_empty_lines) # join cleaned lines back together
    return modified_answer

# main chatbot to handle user queries
def chatbot(query):
    """This function sends user's query to chatbot and returns AI's response."""
    try:
        with open(r"data/ChatLog.json","r") as f:
            messages=load(f)
        # append query to messages list
        messages.append({"role": "user", "content": f"{query}"})
        # make request to groq API for response
        completion=client.chat.completions.create(
            model="llama3-70b-8192", # specify model
            messages= SystemChatBot+[{"role": "system", "content": realtime_information()}]+messages, # include system instructions, real time info and chat history
            max_tokens=1024, # maximum tokens in response
            temperature=0.7, # esponse randomness
            top_p=1, # nucleus sampling to control diversity
            stream=True, # enable streaming response
            stop=None # allow model to decide when to stop
        )
        # empty string to store ai's response
        answer="" 
        # process streamed response chunks
        for chunk in completion:
            if chunk.choices[0].delta.content: # check for content in current chunk
                answer+=chunk.choices[0].delta.content # append content to answer
        
        answer=answer.replace("</s>", " ") # remove unwanted tokens from answer
        # append chatbot's response to messages list
        messages.append({"role": "assistant", "content": answer})
        with open(r"data/ChatLog.json","w") as f:
            dump(messages,f,indent=4)
        return answer_modified(answer)

    except Exception as e:
        # handle exceptions by printing rror and clearing chatlog
        print(f"Error: {e}")
        with open(r"data/ChatLog.json","w") as f:
            dump([],f,indent=4)
        return chatbot(query)
if __name__=="__main__":
    while True:
        user_input=input("Enter your question: ")
        print(chatbot(user_input))
