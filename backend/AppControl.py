import pyautogui
import time
import subprocess
import pyperclip
import os
import applescript

def copy_text():
    time.sleep(0.5)
    pyautogui.keyDown('command')
    pyautogui.press('c')
    pyautogui.keyUp('command')
    time.sleep(1)
    return pyperclip.paste()

def paste_text():
    time.sleep(0.5)
    pyautogui.keyDown('command')
    pyautogui.press('v')
    pyautogui.keyUp('command')

def click(x=None, y=None):
    time.sleep(0.5)
    if x is not None and y is not None:
        pyautogui.click(x, y)
    else:
        pyautogui.click()

def type_text(text):
    time.sleep(0.5)
    for word in text.split():
        pyautogui.typewrite(word + ' ')

def press_hotkey(*keys):
    time.sleep(0.5)
    pyautogui.hotkey(*keys)

def scroll(amount):
    time.sleep(0.5)
    pyautogui.scroll(amount)

def move_mouse(x, y):
    time.sleep(0.5)
    pyautogui.moveTo(x, y)

def press_key(key):
    time.sleep(0.5)
    pyautogui.press(key)

def select_all():
    time.sleep(0.5)
    pyautogui.keyDown('command')
    pyautogui.press('a')
    pyautogui.keyUp('command')

def save():
    time.sleep(0.5)
    pyautogui.keyDown('command')
    pyautogui.press('s')
    pyautogui.keyUp('command')

def new_tab():
    time.sleep(0.5)
    pyautogui.keyDown('command')
    pyautogui.press('t')
    pyautogui.keyUp('command')

def close_tab():
    time.sleep(0.5)
    pyautogui.keyDown('command')
    pyautogui.press('w')
    pyautogui.keyUp('command')

def refresh():
    time.sleep(0.5)
    pyautogui.keyDown('command')
    pyautogui.press('r')
    pyautogui.keyUp('command')

def undo():
    time.sleep(0.5)
    pyautogui.keyDown('command')
    pyautogui.press('z')
    pyautogui.keyUp('command')

def redo():
    time.sleep(0.5)
    pyautogui.keyDown('command')
    pyautogui.keyDown('shift')
    pyautogui.press('z')
    pyautogui.keyUp('shift')
    pyautogui.keyUp('command')

def find():
    time.sleep(0.5)
    pyautogui.keyDown('command')
    pyautogui.press('f')
    pyautogui.keyUp('command')

def print_document():
    time.sleep(0.5)
    pyautogui.keyDown('command')
    pyautogui.press('p')
    pyautogui.keyUp('command')

def new():
    time.sleep(0.5)
    pyautogui.keyDown('command')
    pyautogui.press('n')
    pyautogui.keyUp('command')

def cut():
    time.sleep(0.5)
    pyautogui.keyDown('command')
    pyautogui.press('x')
    pyautogui.keyUp('command')


def perform_task_on_application(app, task, *args):
    print(f"Performing task '{task}' on {app}...")
    
    task_mapping = {
        "click": lambda: click(*args) if args else click(),
        "type": lambda: type_text(' '.join(args)) if args else print("No text provided."),
        "hotkey": lambda: press_hotkey(*args),
        "copy": copy_text,
        "paste": paste_text,
        "scroll": lambda: scroll(args[0]) if args else print("No scroll value provided."),
        "move": lambda: move_mouse(args[0], args[1]) if len(args) == 2 else print("Invalid mouse coordinates."),
        "press": lambda: press_key(args[0]) if args else print("No key provided."),
        "select": select_all,
        "save": save,
        "tab": new_tab,
        "close": close_tab,
        "refresh": refresh,
        "undo": undo,
        "redo": redo,
        "find": find,
        "print": print_document,
        "new": new,
        "cut":cut
    }
    
    if task in task_mapping:
        try:
            task_mapping[task]()
            return True
        except Exception as e:
            print(f"Error executing task '{task}': {e}")
            return False
    else:
        print(f"Task '{task}' is not recognized.")
        return False
