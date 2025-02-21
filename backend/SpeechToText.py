from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import os
import mtranslate as mt

# load environment variables from .env file
env_vars=dotenv_values(".env")
# get input language setting from environment variables
INPUT_LANGUAGE=env_vars.get("INPUT_LANGUAGE")

# define html code for speech recognition interface
html_code="""
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {
            recognition = new webkitSpeechRecognition() || new SpeechRecognition();
            recognition.lang = '';
            recognition.continuous = true;

            recognition.onresult = function(event) {
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript;
            };

            recognition.onend = function() {
                recognition.start();
            };
            recognition.start();
        }

        function stopRecognition() {
            recognition.stop();
            output.innerHTML = "";
        }
    </script>
</body>
</html>
"""

# replace language setting in html code with input language from environment variables
html_code= str(html_code).replace("recognition.lang= '';",f"recognition.lang= '{INPUT_LANGUAGE}';")

# write modified html code to file
with open(r"data/Voice.html","w") as f:
    f.write(html_code)

# get current directory
current_dir= os.getcwd()
# generate file path for html file
link = f"{current_dir}/data/Voice.html"

# set chrome options for webdriver
chrome_options= Options()
user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36"
chrome_options.add_argument(f'user_agent={user_agent}')
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-stream")
chrome_options.add_argument("--headless=new")
# initialise Chrome web driver using ChromeDriverManager
service= Service(ChromeDriverManager().install())
driver= webdriver.Chrome(service=service, options=chrome_options)

# define path for temporary files
temp_dir_path=rf"{current_dir}/frontend/Files"

# function to set assistant's status by writing it to a file
def set_assistant_status(status):
    with open(rf'{temp_dir_path}/status.data',"w", encoding='utf-8') as file:
        file.write(status)

# function to modify a query to ensure proper punctuation and formatting
def query_modifier(query):
    new_query=query.lower().strip()
    query_words=new_query.split()
    question_words=["how","what","who","when","where","why","which", "whose","whom","can you","what's","where's","how's","who's"]

    # check if query is a question and add question mark if necessary
    if any(word+ " " in new_query for word in question_words):
        if query_words[-1][-1] in ['.','?','!']:
            new_query=new_query[:-1]+"?"
        else:
            new_query += "?"
    else:
        # add period if query is not a question
        if query_words[-1][-1] in ['.','?','!']:
            new_query=new_query[:-1]+"."
        else:
            new_query += "."
    
    return new_query.capitalize()

# function to translate text into english using mtranslate
def universal_translator(text):
    english_translation=mt.translate(text,"en","auto")
    return english_translation.capitalize()

# function to perform speech recognition using webdriver
def speech_recognition():
    # open html file in browser
    driver.get("file:///"+link)
    # start speech recognition by clicking start button
    driver.find_element(by=By.ID, value="start").click()
    while True:
        try:
            # get recognised text from html outpt element
            text= driver.find_element(by=By.ID, value="output").text
            if text:
                # stop recognition by clicking stop button
                driver.find_element(by=By.ID, value="end").click()
                # if input language is english return modified query
                if INPUT_LANGUAGE.lower()=="en" or "en" in INPUT_LANGUAGE.lower():
                    return query_modifier(text)
                else:
                    # if input language is not english, translate text and return it
                    set_assistant_status("Translating...")
                    return query_modifier(text)
        except Exception as e:
            pass

if __name__=="__main__":
    while True:
        # continuously perform speech recognition and print recognised text
        text=speech_recognition()
        print(text)

