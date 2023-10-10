import cv2
import os
from concurrent.futures import ThreadPoolExecutor
import tkinter as tk
from tkinter import ttk, filedialog
import threading
import ctypes
import time

import customtkinter

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

def select_video():
    video_path.set(filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mkv;*.mov")]))

def select_folder():
    folder_path.set(filedialog.askdirectory())

def generate_thumbnails(video, progress_callback):
    filename, ext = os.path.splitext(video)
    vidcap = cv2.VideoCapture(video)
    vid_length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    interval = vid_length // 10
    scale_percent = size_scale.get()

    for i in range(1, 11):
        vidcap.set(cv2.CAP_PROP_POS_FRAMES, i * interval)
        success, image = vidcap.read()
        if success:
            width = int(image.shape[1] * scale_percent / 100)
            height = int(image.shape[0] * scale_percent / 100)
            dim = (width, height)
            resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
            cv2.imwrite(f"{filename}_thumbnail_{i}.jpg", resized)
        progress_callback()
    vidcap.release()

def update_progress():
    progress['value'] += 10
    root.update_idletasks()

def process_files_thread():
    video_files = []
    if video_path.get():
        video_files.append(video_path.get())
    elif folder_path.get():
        for root, dirs, files in os.walk(folder_path.get()):
            video_files.extend([os.path.join(root, f) for f in files if f.endswith(('.mp4', '.mov'))])

    progress['maximum'] = len(video_files) * 100
    with ThreadPoolExecutor() as executor:
        for video_file in video_files:
            executor.submit(generate_thumbnails, video_file, update_progress)

def process_files():
    threading.Thread(target=process_files_thread, daemon=True).start()

class ToolTip(object):
    def __init__(self, widget, text):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.text = text
        self.widget.bind("<Enter>", self.showtip)
        self.widget.bind("<Leave>", self.hidetip)

    def showtip(self, event=None):
        if self.tipwindow or not self.text:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify=tk.LEFT, background="#ffffe0", relief=tk.SOLID, borderwidth=1, font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self, event=None):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def create_tooltip(widget, text):
    ToolTip(widget, text)


def create_tooltip(widget, text):
    ToolTip(widget, text)

def fade_in(window):
    alpha = 0
    while alpha < 1:
        alpha += 0.03
        window.attributes("-alpha", alpha)
        window.update()
        time.sleep(0.01)

# Button hover effect
def on_enter(e):
    e.widget['background'] = '#6A1B9A'  # Darken the button color

def on_leave(e):
    e.widget['background'] = '#4B0082'  # Original color


class ToolTip(object):
    def __init__(self, widget, text, delay=500):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.text = text
        self.delay = delay
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.hidetip)
        self.widget.bind("<ButtonPress>", self.hidetip)

    def enter(self, event=None):
        self.schedule = self.widget.after(self.delay, self.showtip)

    def showtip(self, event=None):
        if self.tipwindow or not self.text:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry(f"+{x}+{y}")
        
        # Ensure the tooltip is above other windows
        tw.wm_attributes("-topmost", 1)
        
        label = tk.Label(tw, text=self.text, justify=tk.LEFT, background="#ffffe0", relief=tk.SOLID, borderwidth=1, font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self, event=None):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()
        if hasattr(self, 'schedule'):
            self.widget.after_cancel(self.schedule)

def create_tooltip(widget, text):
    ToolTip(widget, text)


root = tk.Tk()
root.geometry("500x420")
root.title("Thumbnail Generator")
root.configure(bg="#000000")
root.attributes("-topmost", True)  # Keep the window on top of all others
root.iconbitmap(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'thumbnailer.ico'))

title_label = tk.Label(root, text="Thumbnail Generator", bg="#000000", fg="#FFFFFF", font=("Impact", 24))
title_label.pack(pady=10)

video_path = tk.StringVar()
folder_path = tk.StringVar()

video_label = tk.Label(root, text="Input Video:", bg="#000000", fg="#FFFFFF", font=("Helvetica", 12, "bold"))
video_label.pack(anchor=tk.W, padx=10)
video_button = tk.Button(root, text="Select Video", command=select_video, bg="#4B0082", fg="#FFFFFF", font=("Helvetica", 12, "bold"))
video_button.pack(pady=5, padx=10)

folder_label = tk.Label(root, text="Input Folder:", bg="#000000", fg="#FFFFFF", font=("Helvetica", 12, "bold"))
folder_label.pack(anchor=tk.W, padx=10)
folder_button = tk.Button(root, text="Select Folder", command=select_folder, bg="#4B0082", fg="#FFFFFF", font=("Helvetica", 12, "bold"))
folder_button.pack(pady=5, padx=10)

size_label = tk.Label(root, text="Image Size (%):", bg="#000000", fg="#FFFFFF", font=("Helvetica", 12, "bold"))
size_label.pack(anchor=tk.W, padx=10, pady=5)
size_scale = tk.Scale(root, from_=10, to=100, orient="horizontal", bg="#1F1F1F", fg="#FFFFFF", sliderrelief="flat", highlightbackground="#4B0082", highlightcolor="#4B0082")
size_scale.set(100)
size_scale.pack(pady=5, padx=20)

run_button = tk.Button(root, text="Run", command=process_files, bg="#4B0082", fg="#FFFFFF", font=("Helvetica", 12, "bold"))
run_button.pack(pady=10, padx=10)

progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress.pack(pady=10, padx=20, fill="both")

video_button.bind("<Enter>", on_enter)
video_button.bind("<Leave>", on_leave)
folder_button.bind("<Enter>", on_enter)
folder_button.bind("<Leave>", on_leave)
run_button.bind("<Enter>", on_enter)
run_button.bind("<Leave>", on_leave)


create_tooltip(title_label, "Welcome to the Thumbnail Generator!")
create_tooltip(video_label, "Label indicating where to select the video file.")
create_tooltip(video_button, "Click to choose a single video file.")
create_tooltip(folder_label, "Label indicating where to select the folder containing videos.")
create_tooltip(folder_button, "Click to choose a folder containing videos. This will also operate on videos within subfolders!")
create_tooltip(size_label, "Label indicating the size of the generated thumbnails.")
create_tooltip(size_scale, "Adjust this slider to set the percentage size of the generated thumbnails relative to the original video frame size.")
create_tooltip(run_button, "Click this button to start generating thumbnails.")
create_tooltip(progress, "This bar indicates the progress of thumbnail generation.")


# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Get the width and height of the window
window_width = root.winfo_width()
window_height = root.winfo_height()

# Calculate the coordinates to center the window
x_coordinate = (screen_width // 2) - (window_width // 2)
y_coordinate = (screen_height // 2) - (window_height // 2)

root.geometry(f"+{x_coordinate}+{y_coordinate}")

fade_in(root)

root.mainloop()
