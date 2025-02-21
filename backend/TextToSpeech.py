import pygame # for handling audio playback
import random # for generating random choices
import asyncio # for asynchronous operations
import edge_tts # for text to speech functionality
import os
from dotenv import dotenv_values

# load environment variables from .env file
env_vars=dotenv_values(".env")
ASSISTANT_VOICE=env_vars.get("ASSISTANT_VOICE")

# asynchronous function to convert text to audio file
async def text_to_audio(text)->None:
    file_path=r"data/speech.mp3"
    if os.path.exists(file_path): # check if file already exists
        os.remove(file_path) # if it exists, remove it to avoid overwriting errors
    
    # create communicate object to generate speech
    communicate= edge_tts.Communicate(text,ASSISTANT_VOICE,pitch='+5Hz',rate='+13%')
    await communicate.save(r'data/speech.mp3') # save generated speech as audio

# function to manage text to speech functionality
def TTS(text, func=lambda r=None: True):
    while True:
        try:
            # convert text to audio file asynchronously
            asyncio.run(text_to_audio(text))

            # initialise pygame mixer for audio playback
            pygame.mixer.init()

            # load generated speech file into pygame mixer
            pygame.mixer.music.load(r'data/speech.mp3')
            pygame.mixer.music.play() # play audio

            # loop until the audio is done playing or the function stops
            while pygame.mixer.music.get_busy():
                if func()==False: # if external function returns false
                    break
                pygame.time.Clock().tick(10) # limit loop for 10 ticks per second

            return True # return True if audio played successfully
        
        except Exception as e: # handles any exception during the process
            print(f"Error in text to speech generation: {e}")

        finally:
            try:
                # call provided function with False to indicat the end of text to speech
                func(False)
                pygame.mixer.music.stop() # stop audio playback
                pygame.mixer.quit() # quit pygame
            
            except Exception as e: # handles any exception during the process
                print(f"Error in finally block: {e}")

# main exceution
if __name__=="__main__":
    while True:
        # prompt user for input and pass it to text to speech function
        TTS(input("Enter the text: "))

    