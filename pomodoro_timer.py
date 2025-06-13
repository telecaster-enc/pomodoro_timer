from functools import total_ordering
import tkinter as tk
from turtle import width
import customtkinter as ctk
import winsound as ws
from tkinter import messagebox
from tkinter.messagebox import showinfo

class pomodoro:
    #DEFAULT INPUT
    def default_timer(self):                        
        self.entry_var.set("25")                    #MINUTES POMODORO
        self.entry_seconds_var.set("00")            #SECONDS POMODORO
        self.entry_srest_var.set("05")              #MINUTES SHORT REST
        self.entry_srest_seconds_var.set("00")      #SECONDS SHORT REST
        self.entry_lrest_var.set("15")              #MINUTES LONG REST
        self.entry_lrest_seconds_var.set("00")      #SECONDS LONG REST

    def limiter(self, char, value):             
        if char.isdigit() and len(value) <= 2:
            return True
        return False

    def __init__(self):
        #MAIN INTERFACE
        self.root = ctk.CTk()
        self.root.title("Pomodoro")
        self.root.geometry("520x235")

        self.timer_running = False
        self.timer_id = None
        self.pomodoros_completed = 0
        self.where_is_time = 0              

        self.entry_var = ctk.StringVar()
        self.entry_seconds_var = ctk.StringVar()
        self.entry_srest_var = ctk.StringVar()
        self.entry_srest_seconds_var = ctk.StringVar()
        self.entry_lrest_var = ctk.StringVar()
        self.entry_lrest_seconds_var = ctk.StringVar()

        self.vcmd = self.root.register(self.limiter)

        self.label_complete = ctk.CTkLabel(self.root, text="", font=("Helvetica", 10), text_color="#ffe2bf")
        self.label_complete.pack(side = "bottom")

        #TOP FRAME
        self.top_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.top_frame.pack(pady=10, expand = True)

        self.label_main = ctk.CTkLabel(self.top_frame, text="Pomodoro Timer", font=("Helvetica", 50), text_color="#ffffff")
        self.label_main.pack(pady = 5, padx = 5, side = "left")

        self.reset_button = ctk.CTkButton(self.top_frame, text="Reset", font=("Helvetica", 13), height=50, width=50, corner_radius=8, fg_color="#454545", border_color="#2b2b2b", border_width=2, command=self.reset_timer, state="disabled")
        self.reset_button.pack(pady = 5, padx = 5, side = "right")

        self.start_button = ctk.CTkButton(self.top_frame, text="Focus", font=("Helvetica", 13), height=50, width=50, corner_radius=8, fg_color="#435fc4", hover_color="#2f53d6", border_color="#192e78", border_width=2, command=self.start_timer, state="normal")
        self.start_button.pack(pady = 5, padx = 5, side = "left")

        #FRAME POMODORO
        self.frame_work_time = ctk.CTkFrame(self.root, fg_color = "#e66357", border_width = 2, border_color = "#e33020")
        self.frame_work_time.pack(expand=True, side = "left", padx = 5)

        self.label_work_time = ctk.CTkLabel(self.frame_work_time, text="Pomodoro", font=("Helvetica", 30), text_color="#ffffff")
        self.label_work_time.pack(pady = 10, padx = 10)

        self.entry = ctk.CTkEntry(self.frame_work_time, text_color="#ffffff", height=45, width=60, font=("Helvetica", 40), validate="key", validatecommand=(self.vcmd, "%S", "%P"), textvariable=self.entry_var)
        self.entry.pack(side = "left", expand=True, pady = 5)

        self.dot_wtime = ctk.CTkLabel(self.frame_work_time, text=":" , font=("Helvetica", 40))
        self.dot_wtime.pack(side = "left", expand=True, pady = 5)

        self.entry_seconds = ctk.CTkEntry(self.frame_work_time, text_color="#ffffff", height=45, width=60, font=("Helvetica", 40), validate="key", validatecommand=(self.vcmd, "%S", "%P"), textvariable=self.entry_seconds_var)
        self.entry_seconds.pack(side = "right", expand=True, pady = 5)

        #FRAME SHORT REST
        self.frame_short_rest_time = ctk.CTkFrame(self.root, fg_color = "#5ed168", border_width = 2, border_color = "#21942a")
        self.frame_short_rest_time.pack(expand=True, side = "left", padx = 5)

        self.label_short_rest_time = ctk.CTkLabel(self.frame_short_rest_time, text="Short Rest", font=("Helvetica", 30), text_color="#ffffff")
        self.label_short_rest_time.pack(pady = 10, padx = 10)

        self.entry_srest = ctk.CTkEntry(self.frame_short_rest_time, height=45, width=60, font=("Helvetica", 40),  text_color="#ffffff", validate="key", validatecommand=(self.vcmd, "%S", "%P"), textvariable=self.entry_srest_var)
        self.entry_srest.pack(side = "left", expand=True, pady = 5)

        self.dot_srest = ctk.CTkLabel(self.frame_short_rest_time, text=":" , font=("Helvetica", 40))
        self.dot_srest.pack(side = "left", expand=True, pady = 5)

        self.entry_srest_seconds = ctk.CTkEntry(self.frame_short_rest_time, text_color="#ffffff", height=45, width=60, font=("Helvetica", 40), validate="key", validatecommand=(self.vcmd, "%S", "%P"), textvariable=self.entry_srest_seconds_var)
        self.entry_srest_seconds.pack(side = "right", expand=True, pady = 5)

        #FRAME LONG REST
        self.frame_long_rest_time = ctk.CTkFrame(self.root, fg_color = "#588cdb", border_width = 2, border_color = "#3062b0")
        self.frame_long_rest_time.pack(expand=True, side = "left", padx = 5)

        self.label_long_rest_time = ctk.CTkLabel(self.frame_long_rest_time, text="Long Rest", font=("Helvetica", 30), text_color="#ffffff")
        self.label_long_rest_time.pack(pady = 10, padx = 10)

        self.entry_lrest = ctk.CTkEntry(self.frame_long_rest_time, text_color="#ffffff", height=45, width=60, font=("Helvetica", 40), validate="key", validatecommand=(self.vcmd, "%S", "%P"), textvariable=self.entry_lrest_var)
        self.entry_lrest.pack(side = "left", expand=True, pady = 5)

        self.dot_lrest = ctk.CTkLabel(self.frame_long_rest_time, text=":" , font=("Helvetica", 40))
        self.dot_lrest.pack(side = "left", expand=True, pady = 5)

        self.entry_lrest_seconds = ctk.CTkEntry(self.frame_long_rest_time, text_color="#ffffff", height=45, width=60, font=("Helvetica", 40), validate="key", validatecommand=(self.vcmd, "%S", "%P"), textvariable=self.entry_lrest_seconds_var)
        self.entry_lrest_seconds.pack(side = "right", expand=True, pady = 5)

        self.default_timer()
        self.entry_var.trace_add("write", lambda *args: self.delay_time())
        self.entry_seconds_var.trace_add("write", lambda *args: self.delay_time())
        self.entry_srest_var.trace_add("write", lambda *args: self.delay_time())
        self.entry_srest_seconds_var.trace_add("write", lambda *args: self.delay_time())
        self.entry_lrest_var.trace_add("write", lambda *args: self.delay_time())
        self.entry_lrest_seconds_var.trace_add("write", lambda *args: self.delay_time())

        self.root.mainloop()

    def delay_time(self):
        if not self.timer_running:
            if hasattr(self, 'check_start_after_id'):
                self.root.after_cancel(self.check_start_after_id)
            self.check_start_after_id = self.root.after(20, self.take_time)

    def take_time(self):                            
        if not self.timer_running:
            minutes_wtime = int(self.entry_var.get())
            seconds_wtime = int(self.entry_seconds_var.get())
            minutes_srest = int(self.entry_srest_var.get())
            seconds_srest = int(self.entry_srest_seconds_var.get())
            minutes_lrest = int(self.entry_lrest_var.get())
            seconds_lrest = int(self.entry_lrest_seconds_var.get())
            self.work_time = minutes_wtime * 60 + seconds_wtime
            self.short_rest_time = minutes_srest * 60 + seconds_srest
            self.long_rest_time = minutes_lrest * 60 + seconds_lrest
            self.entry_var.set(f"{minutes_wtime:02}")
            self.entry_seconds_var.set(f"{seconds_wtime:02}")
            self.entry_srest_var.set(f"{minutes_srest:02}")
            self.entry_srest_seconds_var.set(f"{seconds_srest:02}")
            self.entry_lrest_var.set(f"{minutes_lrest:02}")
            self.entry_lrest_seconds_var.set(f"{seconds_lrest:02}")
            if self.work_time == 0 or self.short_rest_time == 0 or self.long_rest_time == 0:
                self.start_button.configure(state = "disabled")
            else:
                self.start_button.configure(state = "normal")

    def save_time(self):                            
        self.perm_work_time = self.work_time
        self.perm_long_rest = self.long_rest_time
        self.perm_short_rest = self.short_rest_time

    def countdown(self):                            
        if self.total_seconds > 0:
            self.total_seconds -= 1
            minutes = self.total_seconds // 60
            seconds = self.total_seconds % 60
            self.entry_var.set(f"{minutes:02}")
            self.entry_seconds_var.set(f"{seconds:02}")
            self.timer_id = self.root.after(1000, self.countdown)
        else:
            for _ in range(3):       
                ws.Beep(1000, 500)                  
            self.pomodoros_completed +=1
            self.label_complete.configure(text="You've crushed " + str(self.pomodoros_completed) + " pomodoros!")
            minutes = self.perm_work_time // 60
            seconds = self.perm_work_time % 60
            self.entry_var.set(f"{minutes:02}")
            self.entry_seconds_var.set(f"{seconds:02}")
            if self.pomodoros_completed % 4 == 0:
                self.where_is_time = 3
                self.total_seconds = self.perm_long_rest                
                self.countdown_long_rest()
                #LONG BREAK MESSAGE
                messagebox.showinfo("Long Break Time!", "Great job so far! Take a long break and give your mind a well-earned rest.")   
            else:
                self.where_is_time = 2
                self.total_seconds = self.perm_short_rest                
                self.countdown_short_rest()
                #SHORT BREAK MESSAGE
                messagebox.showinfo("Short Break Time!", "Quick break! Stretch, move around, or sip some water.")   
        
    def countdown_short_rest(self):
        if self.total_seconds > 0:
            self.total_seconds -= 1
            minutes = self.total_seconds // 60
            seconds = self.total_seconds % 60
            self.entry_srest_var.set(f"{minutes:02}")
            self.entry_srest_seconds_var.set(f"{seconds:02}")
            self.timer_id = self.root.after(1000, self.countdown_short_rest)
        else:
            ws.Beep(1000, 1000)
            minutes = self.perm_short_rest // 60
            seconds = self.perm_short_rest % 60
            self.entry_srest_var.set(f"{minutes:02}")
            self.entry_srest_seconds_var.set(f"{seconds:02}")
            self.where_is_time = 1
            self.total_seconds = self.perm_work_time            
            self.countdown()
            messagebox.showinfo("Back to Work!", "Break's over, let's dive back in and stay focused!")

    def countdown_long_rest(self):
        if self.total_seconds > 0:
            self.total_seconds -= 1            
            minutes = self.total_seconds // 60
            seconds = self.total_seconds % 60
            self.entry_lrest_var.set(f"{minutes:02}")
            self.entry_lrest_seconds_var.set(f"{seconds:02}")
            self.timer_id = self.root.after(1000, self.countdown_long_rest)
        else:
            for _ in range(2):
                ws.Beep(1000, 1000)
            minutes = self.perm_long_rest // 60
            seconds = self.perm_long_rest % 60
            self.entry_lrest_var.set(f"{minutes:02}")
            self.entry_lrest_seconds_var.set(f"{seconds:02}")
            self.where_is_time = 1
            self.total_seconds = self.perm_work_time            
            self.countdown()
            messagebox.showinfo("Back to Work!", "Break's over, let's dive back in and stay focused!")

    def reset_timer(self):
        self.pomodoros_completed = 0
        self.label_complete.configure(text="")
        self.default_timer()
        self.entry.configure(state="normal")
        self.entry_seconds.configure(state="normal")
        self.entry_srest.configure(state="normal")
        self.entry_srest_seconds.configure(state="normal")
        self.entry_lrest.configure(state="normal")
        self.entry_lrest_seconds.configure(state="normal")
        self.root.after(100, self.reset_button.configure(state = "disabled", fg_color="#454545", border_color="#2b2b2b"))
        self.where_is_time = 0
  
    def start_timer(self):
        if not self.timer_running:
            if self.where_is_time == 0:
                self.take_time()
                self.save_time()
                self.total_seconds = self.perm_work_time
                self.where_is_time = 1
                self.countdown()
            elif self.where_is_time == 1:
                self.countdown()
            elif self.where_is_time == 2:
                self.countdown_short_rest()
            elif self.where_is_time == 3:
                self.countdown_long_rest()
            self.timer_running = True
            self.entry.configure(state = "disabled")
            self.entry_seconds.configure(state = "disabled")
            self.entry_srest.configure(state = "disabled")
            self.entry_srest_seconds.configure(state = "disabled")
            self.entry_lrest.configure(state = "disabled")
            self.entry_lrest_seconds.configure(state = "disabled")
            self.reset_button.configure(state = "disabled", fg_color="#454545", border_color="#2b2b2b")
            self.start_button.configure(text = "Stop", fg_color="#f53838", hover_color="#f72828", border_color="#db2323")
        else:
            self.timer_running = False
            self.start_button.configure(text = "Focus", fg_color="#435fc4", hover_color="#2f53d6", border_color="#192e78")
            self.reset_button.configure(state="normal", fg_color="#f53838", hover_color="#f72828", border_color="#db2323")
            if self.timer_id:
                self.root.after_cancel(self.timer_id)
            
pomodoro()
