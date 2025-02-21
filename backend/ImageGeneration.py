import asyncio
from random import randint
from PIL import Image
import requests
from dotenv import get_key
import os
from time import sleep

# function to open and display images based on prompt
def open_images(prompt):
    folder_path=r"data" # folder where images are stored
    prompt = prompt.replace(" ","_") # replace spaces in prompt with underscore

    # generate file names for images
    files =[f"{prompt}{i}.jpg" for i in range(1,5)]

    for jpg_file in files:
        image_path=os.path.join(folder_path, jpg_file)

        try:
            # try to open and display image
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
            sleep(1) # pause for 1 second before showing next image

        except IOError:
            print(f"Unable to open {image_path}")

# api details fro hugging face stable diffusion
API_URL="https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers= {"Authorization": f"Bearer {get_key('.env','HUGGINGFACE_API_KEY')}"}

# async function to send query to hugging face api
async def query(payload):
    response= await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
    return response.content

# async function to generate images based on given prompt
async def generate_images(prompt: str):
    tasks=[]

    # create 4 image generation tasks
    for _ in range(4):
        payload= {
            "inputs" : f"{prompt}, quality=4K, sharpness=maximum, Ultra High details, high resolution, seed={randint(0,1000000)}",
        }
        task= asyncio.create_task(query(payload))
        tasks.append(task)
    
    # wait for all taasks to complete
    image_bytes_list= await asyncio.gather(*tasks)

    # save generated images to files
    for i, image_bytes in enumerate(image_bytes_list):
        with open(fr"data/{prompt.replace(' ','_')}{i+1}.jpg","wb") as f:
            f.write(image_bytes)

# wrapper unction to generate and open images
def image_generator(prompt: str):
    asyncio.run(generate_images(prompt))
    open_images(prompt)

# main loop for image generation requests
if __name__=="__main__":
    while True:
        try:
            with open(r"frontend/Files/ImageGeneration.data", "r") as f:
                Data : str= f.read()
            
            prompt, status = Data.split(",")
                                        
            # if the status indicates an image generation request
            if status== 'True':
                print("Generating images...")
                image_status= image_generator(prompt)

                # reset status in ile after generating images
                with open(r"frontend/Files/ImageGeneration.data","w") as f:
                    f.write("False,False")
                    break # exit loop after processing request

            else:
                sleep(1)
        except Exception as e:
            pass