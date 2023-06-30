def main_window():
    win = ct.CTk()
    win.title("tbd")
    win.resizable (False,False)
    win.geometry("680x560")
    imagel =ImageTk.PhotoImage(Image.open(working_directory + "\\data\\UI\\bg.png"))
    framem = ct.CTkLabel(master=win, image=imagel )
    framem.pack(fill="both", expand=True)

    def buttons_disable():
        download.configure(state="disabled")
        download1.configure(state="disabled")
    def buttons_enable():
        download.configure(state="normal")
        download1.configure(state="normal")


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
    folder_label.configure(fg_color="#1a1919")

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
    setting_label.configure(fg_color="#1a1919")

    setting_label.bind("<Button-1>", lambda event: readme())
    setting_label.bind("<Enter>", on_enter_setting)
    setting_label.bind("<Leave>", on_leave_setting)
    setting_label.place(x=470, y =10)


    # button_setting = ct.CTkButton(master=win,
    #                               image=setting_icon,
    #                               text="",
    #                               width=10,
    #                             height=10, 
    #                             command=readme,
                                
    #                               )

    # Create the label with the loaded image
    # button_setting = ct.CTkLabel(win, image=setting_icon, text="",width=10, height=10)
    # button_setting.pack()

    # # Attach a click event to the label
    # button_setting.bind("<Button-1>", lambda event: readme())
    # button_setting.place(x=400, y =10)
    # # = ct.CTkButton(master=win,
    #                               image=folder_icon,
    #                               text="",
    #                               width=10,
    #                             height=10,
    #                             command=get_path,
    #                               )

    

    #button_folder.place(x=350, y =10)



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

        checkbox1 = ct.CTkCheckBox(master=frame, text="MP4", variable=option1, text_color="#AB8000")
        checkbox1.pack(pady=10, padx=10)

        checkbox2 = ct.CTkCheckBox(master=frame, text="MP3/WEBM", variable=option2, text_color="#AB8000")
        checkbox2.pack(pady=10, padx=10)

                                
        download1 = ct.CTkButton(frame, text="Download", command=lambda: actual_down(option1.get(), option2.get(), url_link.get(), pathf()), fg_color=bgg)
        download1.pack(pady=12, padx=15)

        
        pbar = ct.CTkProgressBar(frame, width=400)
        pbar.set(0)
        pbar.pack(pady=12, padx=15)

        pperc = ct.CTkLabel(frame, text="0%", text_color='#AB8000')
        pperc.pack()
    def ui():
        destroy_ui()
        recreate_ui()

        
    
    url_link=tk.StringVar()
    entry1 = ct.CTkEntry(master=frame, placeholder_text="Enter your video Link here", width=300, textvariable=url_link)
    entry1.pack(pady=12, padx=15)

    download = ct.CTkButton(frame, text="Check", command=update_label, fg_color=bgg)
    download.pack(pady=12, padx=15)

    entry2 = ct.CTkLabel(master=frame, text="")
    entry2.pack(pady=2, padx=2)
    print(url_link) 

    

    
   
    win.mainloop()
