import tkinter as tk
import ctypes
import os
import sys
import pystray
from PIL import Image, ImageDraw
import pidfile
from pathlib import Path


SLEEP_ENABLED = True
SLEEP_STATUS = None
ROOT = None
ICON_ROOT = None
ICON_GREEN = None
ICON_RED = None

def sleep_off():
    global SLEEP_ENABLED, SLEEP_STATUS, ICON_ROOT
    
    ctypes.windll.kernel32.SetThreadExecutionState(0x80000002)
    SLEEP_ENABLED = False
    SLEEP_STATUS.set("Sleep mode is disabled")
    ICON_ROOT.title = SLEEP_STATUS.get()
    ICON_ROOT.icon = ICON_GREEN

def sleep_on():
    global SLEEP_ENABLED, SLEEP_STATUS, ICON_ROOT

    ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)
    SLEEP_ENABLED = True
    SLEEP_STATUS.set("Sleep mode is enabled")
    ICON_ROOT.title = SLEEP_STATUS.get()
    ICON_ROOT.icon = ICON_RED

def sleep_toggle():
    if SLEEP_ENABLED == True:
        sleep_off()
    else:
        sleep_on()

# window/icon show/hide
def quit_window(icon, item):
    global ROOT
    sleep_on()
    icon.stop()
    ROOT.destroy()
    sys.exit(0)

def quit():
    quit_window(ICON_ROOT, None)

def show_window(icon, item):
    global ROOT
    ROOT.after(0, ROOT.deiconify)

def withdraw_window():
    global ROOT
    ROOT.withdraw()   

def create_icon():
    # icon = Image.open("image.ico")
    global ICON_GREEN, ICON_RED
    ICON_GREEN = create_image("green")
    ICON_RED = create_image("red")
    
    menu = (pystray.MenuItem('Quit', quit_window), pystray.MenuItem('Show', show_window))
    return pystray.Icon("name", ICON_GREEN, "title", menu)

def create_image(colour):
    # Generate an image and draw a pattern
    width = 50
    height = 50
    colour1 = colour
    colour2 = None
    image = Image.new('RGB', (width, height), colour1)
    dc = ImageDraw.Draw(image)
    dc.rectangle(
        (width // 2, 0, width, height // 2), fill=colour2)
    dc.rectangle(
        (0, height // 2, width // 2, height), fill=colour2)

    return image

def create_root_gui():
    root = tk.Tk()
    root.geometry("200x60")
    root.title("Sleep Mode Toggler")
    root.grid_rowconfigure(1, weight=1)
    root.grid_columnconfigure(0, weight=1)
    frame = tk.Frame(root)
    frame.grid(row=0)
    btm_frame = tk.Frame(root)
    btm_frame.grid(row=1)

    button = tk.Button(frame,
                    text="Quit",
                    fg="red",
                    command=quit)
    button.pack(side=tk.LEFT)
    slogan = tk.Button(frame,
                    text="Toggle Sleep Mode",
                    command=sleep_toggle)
    slogan.pack(side=tk.LEFT)
    global SLEEP_STATUS
    SLEEP_STATUS = tk.StringVar()
    status = tk.Label(btm_frame,
                        textvariable=SLEEP_STATUS)
    status.place(relx=0.0, rely=1.0, anchor='sw')
    status.pack()

    root.protocol('WM_DELETE_WINDOW', withdraw_window)

    return root

def main():

    # determine if the application is a frozen `.exe` (e.g. pyinstaller --onefile) 
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    # or a script file (e.g. `.py` / `.pyw`)
    elif __file__:
        application_path = os.path.dirname(__file__)

    try:
        pid_file = "".join([str(application_path), r"\pidfile"])

        with pidfile.PIDFile(pid_file):
            global ICON_ROOT, ROOT
            ICON_ROOT = create_icon()
            ICON_ROOT.run_detached()
            ROOT = create_root_gui()

            sleep_off()

            # run program
            ROOT.mainloop()
    except pidfile.AlreadyRunningError:
        print("Already running, exiting.")
        return

if __name__ == "__main__":
    main()
