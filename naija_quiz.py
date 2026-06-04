import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import random
import json
from datetime import datetime
import winsound
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class NaijaMillionaire:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("🇳🇬 Who Wants to Be a Naija Millionaire?")
        self.root.geometry("1200x780")
        self.root.resizable(False, False)
        
        self.score = 0
        self.current_question = 0
        self.time_left = 10
        self.timer_id = None
        self.high_scores = self.load_high_scores()
        self.lifelines = {"50:50": True, "Phone a Friend": True, "Ask the Audience": True}
        self.prizes = [0, 100, 200, 500, 1000, 2000, 5000, 10000, 25000, 50000, 100000]
        
        self.show_main_menu()
        
    def load_high_scores(self):
        try:
            if os.path.exists("highscores.json"):
                with open("highscores.json", "r") as f:
                    return json.load(f)
            return []
        except:
            return []
    
    def save_high_score(self):
        today = str(datetime.now().date())
        self.high_scores = [hs for hs in self.high_scores if hs["date"] != today]
        self.high_scores.append({"score": self.score, "date": today})
        self.high_scores = sorted(self.high_scores, key=lambda x: x["score"], reverse=True)[:10]
        with open("highscores.json", "w") as f:
            json.dump(self.high_scores, f, indent=2)
    
    def play_sound(self, sound_type):
        try:
            if sound_type == "correct":
                winsound.Beep(1300, 250)
                winsound.Beep(1800, 200)
            elif sound_type == "wrong":
                winsound.Beep(400, 700)
        except:
            pass
    
    def show_main_menu(self):
        self.clear_window()
        
        title = ctk.CTkLabel(self.root, text="WHO WANTS TO BE A", 
                           font=ctk.CTkFont(size=32, weight="bold"), text_color="#FFD700")
        title.pack(pady=20)
        
        title2 = ctk.CTkLabel(self.root, text="NAIJA MILLIONAIRE", 
                            font=ctk.CTkFont(size=52, weight="bold"), text_color="#FF3333")
        title2.pack(pady=5)
        
        ctk.CTkButton(self.root, text="🚀 START GAME", font=ctk.CTkFont(size=18, weight="bold"),
                     height=50, width=300, command=self.show_category_selection).pack(pady=40)
        
        ctk.CTkButton(self.root, text="🏆 HIGH SCORES", font=ctk.CTkFont(size=16),
                     height=40, width=250, command=self.show_high_scores).pack(pady=10)
    
    def show_category_selection(self):
        self.clear_window()
        
        ctk.CTkLabel(self.root, text="SELECT CATEGORY", 
                    font=ctk.CTkFont(size=28, weight="bold"), text_color="#FFD700").pack(pady=40)
        
        categories = ["All Categories", "Music & Afrobeats", "Food & Culture", 
                     "Politics & History", "Geography", "General Knowledge"]
        
        self.cat_var = tk.StringVar(value="All Categories")
        
        for cat in categories:
            rb = ctk.CTkRadioButton(self.root, text=cat, variable=self.cat_var, value=cat)
            rb.pack(pady=12)
        
        ctk.CTkButton(self.root, text="BEGIN GAME", font=ctk.CTkFont(size=18, weight="bold"),
                     command=self.start_game).pack(pady=50)
    
    def start_game(self):
        self.score = 0
        self.current_question = 0
        self.lifelines = {"50:50": True, "Phone a Friend": True, "Ask the Audience": True}
        self.load_filtered_questions()
        self.show_question()
    
    def load_filtered_questions(self):
        all_questions = [
            {"q": "Who sang 'Essence'?", "a": "Wizkid", "options": ["Davido", "Burna Boy", "Wizkid", "Rema"], "cat": "Music & Afrobeats"},
            {"q": "Who is the current President of Nigeria?", "a": "Bola Ahmed Tinubu", "options": ["Bola Ahmed Tinubu", "Atiku Abubakar", "Peter Obi", "Muhammadu Buhari"], "cat": "Politics & History"},
            {"q": "What is Nigeria's most popular rice dish?", "a": "Jollof Rice", "options": ["Jollof Rice", "Fried Rice", "Coconut Rice", "Ofada Rice"], "cat": "Food & Culture"},
            {"q": "What is the capital of Nigeria?", "a": "Abuja", "options": ["Lagos", "Abuja", "Kano", "Ibadan"], "cat": "Geography"},
        ]
        self.questions = all_questions
        random.shuffle(self.questions)
    
    def show_question(self):
        self.clear_window()
        
        q = self.questions[self.current_question]
        
        # Question Frame
        q_frame = ctk.CTkFrame(self.root, fg_color="#1a1a4d")
        q_frame.pack(pady=30, padx=80, fill="x")
        
        ctk.CTkLabel(q_frame, text=q["q"], font=ctk.CTkFont(size=20, weight="bold"), 
                    wraplength=900).pack(pady=40, padx=30)
        
        # Options
        for option in q["options"]:
            btn = ctk.CTkButton(self.root, text=option, font=ctk.CTkFont(size=16),
                              height=50, command=lambda o=option: self.check_answer(o, q["a"]))
            btn.pack(pady=12, padx=100)
    
    def check_answer(self, selected, correct):
        if selected == correct:
            self.score = self.prizes[self.current_question + 1]
            messagebox.showinfo("Correct", "Well done!")
            self.next_question()
        else:
            messagebox.showerror("Wrong", f"Correct answer was:\n{correct}")
            self.show_final_score()
    
    def next_question(self):
        self.current_question += 1
        if self.current_question < len(self.questions):
            self.show_question()
        else:
            self.show_final_score()
    
    def show_final_score(self):
        self.clear_window()
        ctk.CTkLabel(self.root, text="CONGRATULATIONS!", 
                    font=ctk.CTkFont(size=40, weight="bold"), text_color="#FFD700").pack(pady=80)
        ctk.CTkLabel(self.root, text=f"You Won\n₦{self.score:,}", 
                    font=ctk.CTkFont(size=32, weight="bold"), text_color="#00FFAA").pack(pady=20)
        ctk.CTkButton(self.root, text="PLAY AGAIN", command=self.show_main_menu).pack(pady=50)
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_high_scores(self):
        messagebox.showinfo("High Scores", "Coming Soon...")
    
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    game = NaijaMillionaire()
    game.run()
