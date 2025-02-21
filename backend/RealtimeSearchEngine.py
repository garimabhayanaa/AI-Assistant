from googlesearch import search 
from groq import Groq  # to use Groq API
from json import load,dump # functions to read and write json files
import datetime  # for real-time date and time information
from dotenv import dotenv_values # to load environment variables from .env

# load environment variables from .env
env_vars= dotenv_values(".env")
# retrieve environment variables for chatbot configuration
USERNAME=env_vars.get("USERNAME")
ASSISTANT=env_vars.get("ASSISTANT")
GROQ_API_KEY= env_vars.get("GROQ_API_KEY")

# initialise client using API key
client= Groq(api_key=GROQ_API_KEY)

# system instructions for chatbot
System= f"""Hello, I am {USERNAME}, You are a very accurate and advanced AI chatbot named {ASSISTANT} which has real-time up-to-date information from the internet.
*** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***
*** Just answer the question from the provided data in a professional way. ***"""

# try to load chat log from a json file or create an empty one if it doesn't exist
try:
    with open(r"data/ChatLog.json","r") as f:
        messages=load(f)
except:
    with open(r"data/ChatLog.json","w") as f:
        dump([],f)

# function to perform google search and format its result
def google_search(query):
    results= list(search(query,advanced=True,num_results=5))
    answer=f"The search results for '{query}' are:\n[start]\n"
    for i in results:
        answer+= f"Title: {i.title}\nDescription: {i.description}\n\n"
    answer+= "[end]"
    return answer

# function to clean answer by removing empty lines
def answer_modified(answer):
    lines=answer.split('\n')
    non_empty_lines= [line for line in lines if line.strip()]
    modified_answer='\n'.join(non_empty_lines)
    return modified_answer

# predefined chatbot conversation system message and an initial user message
system_chatbot=[
    {"role": "system", "content": System},
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello, how can I help you ?"}
]

# function to get real-time information like current date and time
def information():
    data= ""
    current_datetime= datetime.datetime.now() # current date and time
    day= current_datetime.strftime("%A") # day of the week
    date= current_datetime.strftime("%d") # day of the month
    month= current_datetime.strftime("%B") # month name
    year= current_datetime.strftime("%Y") # year
    hour= current_datetime.strftime("%H") # hour in 24-hour format
    minute= current_datetime.strftime("%M") # minute
    second= current_datetime.strftime("%S") # second
    data += f"Use this real time information if needed:\n"
    data += f"Day: {day}\n"
    data += f"Date: {date}\n"
    data += f"Month: {month}\n"
    data += f"Year: {year}\n"
    data += f"Time: {hour} hours, {minute} minutes, {second} seconds.\n"
    return data

# function to handle real-time search and response generation
def realtime_search_engine(prompt):
    global system_chatbot, messages

    # load chatlog from json file
    with open(r"data/ChatLog.json","r") as f:
        messages=load(f)
    messages.append({"role": "user", "content": f"{prompt}"})

    # generate response using groq client
    completion= client.chat.completions.create(
        model="llama3-70b-8192",
        messages= [{"role": "system", "content": google_search(prompt)}] + messages,  # Only include the search results here
        temperature=0.7,
        max_tokens=2048,
        top_p=1,
        stream=True,
        stop=None
    )

    answer=""

    # concatenate response chunks from streaming output
    for chunk in completion:
        if chunk.choices[0].delta.content:
            answer += chunk.choices[0].delta.content
    
    # clean up the response
    answer = answer.strip().replace("</s>", " ")
    messages.append({"role": "assistant", "content": answer})

    # save updated chatlog back to json file
    with open(r"data/ChatLog.json","w") as f:
        dump(messages,f,indent=4)

    return answer_modified(answer=answer)

if __name__=="__main__":
    while True:
        prompt=input("Enter your query: ")
        print(realtime_search_engine(prompt=prompt))