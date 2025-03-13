import pyautogui
import time
import pyperclip

def copy_text():
    time.sleep(0.5)
    pyautogui.keyDown('ctrl')
    pyautogui.press('c')
    pyautogui.keyUp('ctrl')
    time.sleep(1)
    return pyperclip.paste()

def paste_text():
    time.sleep(0.5)
    pyautogui.keyDown('ctrl')
    pyautogui.press('v')
    pyautogui.keyUp('ctrl')

def click(x=None, y=None):
    time.sleep(0.5)
    pyautogui.click(x, y) if x is not None and y is not None else pyautogui.click()

def type_text(text):
    time.sleep(0.5)
    pyautogui.write(text + ' ')

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
    pyautogui.keyDown('ctrl')
    pyautogui.press('a')
    pyautogui.keyUp('ctrl')

def save():
    time.sleep(0.5)
    pyautogui.keyDown('ctrl')
    pyautogui.press('s')
    pyautogui.keyUp('ctrl')

def new_tab():
    time.sleep(0.5)
    pyautogui.keyDown('ctrl')
    pyautogui.press('t')
    pyautogui.keyUp('ctrl')

def close_tab():
    time.sleep(0.5)
    pyautogui.keyDown('ctrl')
    pyautogui.press('w')
    pyautogui.keyUp('ctrl')

def refresh():
    time.sleep(0.5)
    pyautogui.keyDown('ctrl')
    pyautogui.press('r')
    pyautogui.keyUp('ctrl')

def undo():
    time.sleep(0.5)
    pyautogui.keyDown('ctrl')
    pyautogui.press('z')
    pyautogui.keyUp('ctrl')

def redo():
    time.sleep(0.5)
    pyautogui.keyDown('ctrl')
    pyautogui.press('y')
    pyautogui.keyUp('ctrl')

def find():
    time.sleep(0.5)
    pyautogui.keyDown('ctrl')
    pyautogui.press('f')
    pyautogui.keyUp('ctrl')

def print_document():
    time.sleep(0.5)
    pyautogui.keyDown('ctrl')
    pyautogui.press('p')
    pyautogui.keyUp('ctrl')

def new():
    time.sleep(0.5)
    pyautogui.keyDown('ctrl')
    pyautogui.press('n')
    pyautogui.keyUp('ctrl')

def cut():
    time.sleep(0.5)
    pyautogui.keyDown('ctrl')
    pyautogui.press('x')
    pyautogui.keyUp('ctrl')

def perform_task_on_application(task, *args):
    print(f"Performing task '{task}'...")
    
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
        "cut": cut
    }
    
    if task in task_mapping:
        try:
            return task_mapping[task]()
        except Exception as e:
            print(f"Error executing task '{task}': {e}")
            return False
    else:
        print(f"Task '{task}' is not recognized.")
        return False