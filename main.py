from termcolor import colored
import tkinter as tk
from tkinter import filedialog
import customtkinter as ct
from PIL import Image, ImageTk
from os import getcwd
from os import startfile
from os import open
from io import open
import youtube_dlc as yp
import socket


golden = "#AB8000"
black = "#1a1919"
global eta_minutes, progress

def check_internet_connection():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except socket.error:
        return False
    

def check_valid_url(video_url):
    extractors = yp.extractor.gen_extractors()
    for e in extractors:
        if e.suitable(video_url) and e.IE_NAME != 'generic':
            return True
    return False



def playlist_func(url):
    if('list' in url):
        ydl_opts = {
            'extract_flat': 'in_playlist',
            'skip_download': True,
            'quiet': True,
        }

        with yp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_urls = [entry['url'] for entry in info['entries']]

        return video_urls
    else:
        url = url.replace("https://www.youtube.com/watch?v=","")
        return url


url_u= []

def actual_down(op1, op2, url, path):
    if check_internet_connection() == False:
        pperc.configure(text="Intennet Connection Problem.", text_color="red")
        print("Intenet")
    print(colored('Pass 1', 'red'))
    
    try:
        if 'list' in url:
            if 'start' in url or 'index=' in url:
                loc = url.find("&list")
                url = url[0:loc]
                total_vids = 1
            else:
                url_u = playlist_func(url)
                total_vids = len(url_u)
        else:
             total_vids = 1
    except:
        pass
    def progress_hook_video(d):
        c=1
        if d['status'] == 'downloading':
            download1.configure(state="disabled")

            total_bytes = d.get('total_bytes')
            downloaded_bytes = d.get('downloaded_bytes')
            
            if total_bytes and downloaded_bytes:
                progress = int((downloaded_bytes / total_bytes) * 100)
                pbar.set(progress/100)
            pperc.configure(text=f"Downloading Video {c} of {total_vids} ( {progress} %)", text_color=golden)

            splash_screen.update_idletasks()
            c=c+1

        elif d['status'] == 'finished':
            pperc.configure(text="Download Complete", text_color="green")
            download1.configure(state="normal")

    def progress_hook_audio(d):
        c=1
        if d['status'] == 'downloading':
            download1.configure(state="disabled")

            total_bytes = d.get('total_bytes')
            downloaded_bytes = d.get('downloaded_bytes')
            
            if total_bytes and downloaded_bytes:
                progress = int((downloaded_bytes / total_bytes) * 100)
                pbar.set(progress/100)
            pperc.configure(text=f"Downloading Audio {c} of {total_vids} ( {progress} %)", text_color=golden)

            splash_screen.update_idletasks()
            c=c+1

        elif d['status'] == 'finished':
            pperc.configure(text="Download Complete", text_color="green")
            download1.configure(state="normal")    




    if(op1 == True):
        try:
            ydl_opts = {
                'format': 'best',
                'merge_output_format': 'mp4',
                'outtmpl': f'{path}/%(title)s.%(ext)s',
                'ignoreerrors': True,
                'verbose': True,
                'progress_hooks': [progress_hook_video]

            }
            if check_internet_connection() == True:
                ydl = yp.YoutubeDL(ydl_opts)
                with ydl:
                    info = ydl.extract_info(url, download=True)
                    if 'entries' in info:
                        total_vids = len(info['entries'])
                    else:
                        total_vids = 1
                    
        except:
            pperc.configure(text=f"Internal Error. Please try again later ", text_color="red")




    if(op2==True):
        try:
            ydl_opts = {
            'format': f'bestaudio/mp3',
            'outtmpl': f'{path}/%(title)s.%(ext)s',
            'ignoreerrors': True,
            'verbose': True,
            'progress_hooks': [progress_hook_audio]
        }
            if check_internet_connection() == True:
                ydl = yp.YoutubeDL(ydl_opts)
                with ydl:
                    info = ydl.extract_info(url, download=True)
                    if 'entries' in info:
                        total_vids = len(info['entries'])
                    else:
                        total_vids = 1
        except:
            pperc.configure(text=f"Internal Error. Please try again later ", text_color="red")
            










##########################################################UI################################################################
ct.set_appearance_mode("System")
ct.set_default_color_theme("dark-blue")
bgg = "#b8860b"
working_directory = getcwd()
def save_path(path):
    with open('path.txt', 'w') as file:
        file.write(path)

def load_path():
    try:
        file = open(working_directory + "\\data\\txt\\path.txt", mode='r', encoding='utf-8')
        content = file.read()
        file.close()
        return content.strip()  
    except FileNotFoundError:
        return ''

def get_path():
    path = filedialog.askdirectory()
    save_path(path)
    print(path)

def pathf():
    path = load_path()
    if path == '':
        path = getcwd()
    
    return path
def readme():
    try:
        startfile(working_directory + '\\data\\txt\\Read Me.txt')
    except:
        pass

def main_window():
    win = ct.CTk()
    win.title("YT Downloader")
    win.resizable (False,False)
    win.geometry("680x560")
    imagel =ImageTk.PhotoImage(Image.open(working_directory + "\\data\\UI\\bg.png"))
    framem = ct.CTkLabel(master=win, image=imagel )
    framem.pack(fill="both", expand=True)

    def on_enter_folder(event):
        folder_label.configure(image=ctk_image_folder_icon)
        folder_label_text.place(x=290, y=15)


    def on_leave_folder(event):
        try:
            folder_label_text.place_forget()
        except:
            pass
        folder_label.configure(image=ctk_folder)


    folder_icon = Image.open(working_directory + "\\data\\UI\\folder.png")
    folder_enter_icon = Image.open(working_directory + "\\data\\UI\\folder_1.png")

    folder_icon = folder_icon.resize((44, 44))
    folder_enter_icon = folder_enter_icon.resize((45,45))

    ctk_folder = ImageTk.PhotoImage(folder_icon)
    ctk_image_folder_icon = ImageTk.PhotoImage(folder_enter_icon)
    folder_label = ct.CTkLabel(win, image=ctk_folder, text="")

    folder_label_text = ct.CTkLabel(win, text="Change Download Destination", font=("Arial", 9))
    folder_label.configure(fg_color=black)

    folder_label.bind("<Button-1>", lambda event: get_path())
    folder_label.bind("<Enter>", on_enter_folder)
    folder_label.bind("<Leave>", on_leave_folder)

    folder_label.place(x=420, y =10)

    def on_enter_setting(event):
       setting_label.configure(image=ctk_image_setting_icon)
       setting_label_text.place(x=520, y=15)

    def on_leave_setting(event):
        try:
            setting_label_text.place_forget()
        except:
            pass
        setting_label.configure(image=ctk_setting)


    setting_icon = Image.open(working_directory + "\\data\\UI\\question.png")
    setting_enter_icon = Image.open(working_directory + "\\data\\UI\\question_1.png")

    setting_icon = setting_icon.resize((44, 44))
    setting_enter_icon = setting_enter_icon.resize((45, 45))

    ctk_setting = ImageTk.PhotoImage(setting_icon)
    ctk_image_setting_icon = ImageTk.PhotoImage(setting_enter_icon)
    setting_label = ct.CTkLabel(win, image=ctk_setting, text="")
    
    # Configure label appearance
    setting_label_text = ct.CTkLabel(win, text="Open Readme", font=("Arial", 9))
    setting_label.configure(fg_color=black)

    setting_label.bind("<Button-1>", lambda event: readme())
    setting_label.bind("<Enter>", on_enter_setting)
    setting_label.bind("<Leave>", on_leave_setting)
    setting_label.place(x=470, y =10)

    frame = ct.CTkFrame(master=win)
    frame.configure(height=422, width=330)
    frame.propagate(0)
    frame.place(x=175, y=68)
    label = ct.CTkLabel(master=frame, text="Youtube Downloader", font=("Arial", 24, "bold"), text_color="#AB8000")
    label.pack(padx=5, pady=15)


    def sdownload():
        video_url = url_link.get()
        if check_valid_url(video_url):
            print("URL seems to be valid")
            return True
        else:
            print("URL is not valid.")
            return False
        
    def update_label(): 
        result = sdownload()  
        if result:
            entry2.configure(text="URL Link is Valid", text_color="#009000")
            ui()
        else:
            entry2.configure(text="URL Link is Invalid", text_color="#9b111e")
        

    def destroy_ui():
        if 'checkbox1' in globals():
            checkbox1.destroy()
        if 'checkbox2' in globals():
            checkbox2.destroy()
        if 'download1' in globals():
            download1.destroy()
        if 'pbar' in globals():
            pbar.destroy()
        if 'pperc' in globals():
            pperc.destroy()


    def recreate_ui():
        global checkbox1, checkbox2, download1, pbar, pperc
        option1 = tk.BooleanVar()
        option2 = tk.BooleanVar()

        checkbox1 = ct.CTkCheckBox(master=frame, text="MP4", variable=option1, text_color=golden)
        checkbox1.pack(pady=10, padx=10)

        checkbox2 = ct.CTkCheckBox(master=frame, text="MP3/WEBM", variable=option2, text_color=golden)
        checkbox2.pack(pady=10, padx=10)

                                
        download1 = ct.CTkButton(frame, text="Download", text_color='black',font=("Calibri", 16, "bold"), command=lambda: actual_down(option1.get(), option2.get(), url_link.get(), pathf()), fg_color=bgg)
        download1.pack(pady=12, padx=15)

        
        pbar = ct.CTkProgressBar(frame, width=400)
        pbar.set(0)
        pbar.pack(pady=12, padx=15)

        pperc = ct.CTkLabel(frame, text="0%", text_color=golden)
        pperc.pack()

    def ui():
        destroy_ui()
        recreate_ui()

        
    
    url_link=tk.StringVar()
    entry1 = ct.CTkEntry(master=frame, placeholder_text="Enter your video Link here", width=300, textvariable=url_link)
    entry1.pack(pady=12, padx=15)

    download = ct.CTkButton(frame, text="Check", text_color=black,font=("Calibri", 16, "bold"), command=update_label, fg_color=bgg)
    download.pack(pady=12, padx=15)

    entry2 = ct.CTkLabel(master=frame, text="")
    entry2.pack(pady=2, padx=2)
 
   
    win.mainloop()

splash_screen = ct.CTk()
splash_screen.overrideredirect(True)
splash_screen.geometry("240x300")
window_width = 240
window_height = 300
screen_width = splash_screen.winfo_screenwidth()
screen_height = splash_screen.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
splash_screen.geometry(f"{window_width}x{window_height}+{x}+{y}")
splash_screen.resizable(False, False)


file = working_directory + "\\data\\UI\\splash.gif"
image = Image.open(file)
label = ct.CTkLabel(splash_screen)
label.pack()

frames = []
try:
    while True:
        frames.append(ImageTk.PhotoImage(master=splash_screen,  image=image))
        image.seek(len(frames))  
except EOFError:
    pass

def animate_gif(frame_index):
    try:
        label.configure(text="",image=frames[frame_index])
        splash_screen.after(100, animate_gif, (frame_index + 1))
    except IndexError:     
        splash_screen.destroy()
        main_window()


animate_gif(0)

splash_screen.mainloop()