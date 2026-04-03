# import lib, python -m pip install pyautogui mouse customtkinter
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import pyautogui as pg
import mouse
import time as t
import threading
import keyboard

# Func to compare input is digit
def validate_input(P):
    # P is Entry input if isdigit allow to show
    if P == "" or P.isdigit():
        return True
    return False

# Create Tkinter window
root = tk.Tk()
root.title("PY-AutoClicker")
root.geometry("720x480")
root.resizable(False, False)

# Validate Command Register
vcmd = (root.register(validate_input), '%P')

# Set Var/System stuffs
run_status_var = tk.BooleanVar()
set_mouse_position = tk.BooleanVar()
x_pos, y_pos = tk.StringVar(value=f"X : {0}"), tk.StringVar(value=f"Y : {0}")
x, y = tk.IntVar(value=0), tk.IntVar(value=0)
click_time_var = tk.IntVar(value=100)

# Text Label for click mode
option_label = tk.Label(root, text="Click Option", font=("Arial", 10, 'normal'))
option_label.place(x=15, y=10)

# dropdownlist to select click option
clicks_mode_option = ['left', 'right', 'middle']
clicks_mode_listbox = ttk.Combobox(root, values=clicks_mode_option, state="readonly")
clicks_mode_listbox.set(clicks_mode_option[0])
clicks_mode_listbox.place(x=120, y=10)

# Text Label for click frequenze
ClickTimeSet = tk.Label(root, text="Time", font=("Arial", 10, 'normal'))
ClickTimeSet.place(x=340, y=10)
ClickTimeSet = tk.Label(root, text="ms", font=("Arial", 10, 'normal'))
ClickTimeSet.place(x=500, y=10)

# Time Entry Box
click_time_ms = ttk.Entry(root, justify='right', width=12, validate='key', validatecommand=vcmd)
click_time_ms.insert(0, "100")
click_time_ms.place(x=390,  y=10)

# Create Widget
check_box_mouse_pos = tk.Checkbutton(root, text="Set Position Mode",  variable=set_mouse_position, font=("Arial", 10,  'normal'))

set_mouse_pos_frame = tk.Frame(root, width=700, height=50, bg="lightgray") # Set Position Option Frame
set_text_frame = tk.Frame(set_mouse_pos_frame, width=500, height=27, bg='lightgray') # X, Y Text Frame
# Show X, Y Position
x_label = tk.Label(set_text_frame, textvariable=x_pos, bg='gray', width=10, fg='white', font=("Arial", 8, 'bold'))
y_label = tk.Label(set_text_frame, textvariable=y_pos, bg='gray', width=10, fg='white', font=("Arial", 8, 'bold'))

def setmousepos(): # For SetPosition Button Command
    print(f"Read Position loop running . . .")
    while True:
        if mouse.is_pressed('left'):
            x_raw, y_raw = pg.position()
            x_pos.set(f"X : {x_raw}")
            y_pos.set(f"Y : {y_raw}")
            x.set(x_raw)
            y.set(y_raw)
            break
    print("Read Mouse Position.")
    print(f"Position dump = X:{x_raw} | Y:{y_raw}")

# Create SetPosition Button
set_pos_btn = tk.Button(set_mouse_pos_frame, text="Set Position", command=setmousepos)
set_pos_btn.configure(font=('Arial', 8, 'bold'), width='10', height='1')

def read_check_box(): # Show Set Positon config when status is true and hide if false
    print(f"Set Position Mode is:{set_mouse_position.get()}")
    if set_mouse_position.get():
        set_mouse_pos_frame.place(x=10, y=90)
        set_pos_btn.place(x=20, y=12)
        set_text_frame.place(x=130, y=12)
        x_label.place(x=0, y=0)
        y_label.place(x=100, y=0)
    else:
        set_mouse_pos_frame.place_forget()

# Deploy Check box Button
check_box_mouse_pos.configure(command=read_check_box)
check_box_mouse_pos.place(x=20, y=50)

# Start Button
RunBtn = tk.Button(root, text="Run Auto Click", width=20, height=1, font=("Arial", 14, 'bold'), bg='gray', fg='white')

def excute():
    while run_status_var.get():
        try:
            interval = int(click_time_ms.get()) / 1000
        except:
            interval = 0.1
            
        if set_mouse_position.get():
            # คลิกตามตำแหน่งที่ตั้งไว้
            pg.moveTo(x=x.get(), y=y.get())
            mouse.click(button=clicks_mode_listbox.get())
        else:
            # คลิกตรงที่เมาส์วางอยู่
            mouse.click(button=clicks_mode_listbox.get())
        
        if keyboard.is_pressed('ctrl'): stop()
        t.sleep(interval)

def stop():
    run_status_var.set(False)
    RunBtn.configure(text='Run Auto Click', bg='gray')

def run():
    RunBtn.configure(text='Kill Auto Click', bg='red')
    if not run_status_var.get():
        run_status_var.set(True)
        threading.Thread(target=excute, daemon=True).start()
    else:
        stop()
    
    t.sleep(0.5)

RunBtn.configure(command=run)
RunBtn.place(x=15, y=400)

root.attributes('-topmost', True)
root.mainloop()