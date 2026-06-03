import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
from datetime import datetime
import winsound
import os

class NaijaQuiz:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🇳🇬 Who Wants to Be a Naija Millionaire? 🇳🇬")
        self.root.geometry("1000x680")
        self.root.resizable(False, False)
        self.root.configure(bg="#0a0a2e")  # Deep dark blue
        
        self.score = 0
        self.current_question = 0
        self.time_left = 10
        self.timer_id = None
        self.high_scores = self.load_high_scores()
        
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
                winsound.Beep(1200, 250)
                winsound.Beep(1500, 200)
            elif sound_type == "wrong":
                winsound.Beep(500, 400)
        except:
            pass
    
    def cancel_timer(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
    
    def show_main_menu(self):
        self.cancel_timer()
        for widget in self.root.winfo_children():
            widget.destroy()
            
        tk.Label(self.root, text="WHO WANTS TO BE A", 
                font=("Arial", 28, "bold"), fg="#FFD700", bg="#0a0a2e").pack(pady=20)
        tk.Label(self.root, text="NAIJA MILLIONAIRE?", 
                font=("Arial", 42, "bold"), fg="#FF0000", bg="#0a0a2e").pack(pady=10)
        
        tk.Label(self.root, text="🇳🇬 Let's Play! 🔥", 
                font=("Arial", 18), fg="#00FFAA", bg="#0a0a2e").pack(pady=20)
        
        btn_frame = tk.Frame(self.root, bg="#0a0a2e")
        btn_frame.pack(pady=50)
        
        ttk.Button(btn_frame, text="🚀 START GAME", command=self.show_category_selection).pack(pady=15, ipadx=50, ipady=15)
        ttk.Button(btn_frame, text="🏆 HIGH SCORES", command=self.show_high_scores).pack(pady=15, ipadx=50, ipady=12)
        ttk.Button(btn_frame, text="Quit", command=self.root.quit).pack(pady=20)
    
    def show_category_selection(self):
        for widget in self.root.winfo_children():
            widget.destroy()
            
        tk.Label(self.root, text="SELECT CATEGORY", 
                font=("Arial", 24, "bold"), fg="#FFD700", bg="#0a0a2e").pack(pady=40)
        
        categories = ["All Categories", "Music & Afrobeats", "Food & Culture", 
                     "Politics & History", "Geography", "Nollywood & Entertainment", 
                     "General Knowledge"]
        
        self.cat_var = tk.StringVar(value="All Categories")
        
        for cat in categories:
            rb = tk.Radiobutton(self.root, text=cat, variable=self.cat_var, value=cat,
                              font=("Arial", 14), bg="#0a0a2e", fg="#FFFFFF", selectcolor="#FF9500")
            rb.pack(pady=12)
        
        btn_frame = tk.Frame(self.root, bg="#0a0a2e")
        btn_frame.pack(pady=50)
        
        ttk.Button(btn_frame, text="CONFIRM & START", command=self.start_filtered_quiz).pack(ipadx=40, ipady=12)
    
    def start_filtered_quiz(self):
        self.score = 0
        self.current_question = 0
        self.time_left = 10
        self.load_filtered_questions()
        self.show_question()
    
    def load_filtered_questions(self):
        all_questions = [
            {"q": "Who sang 'Essence'?", "a": "Wizkid", "options": ["Davido", "Burna Boy", "Wizkid", "Rema"], "cat": "Music & Afrobeats"},
            {"q": "Who is the current President of Nigeria?", "a": "Bola Ahmed Tinubu", "options": ["Bola Ahmed Tinubu", "Atiku Abubakar", "Peter Obi", "Muhammadu Buhari"], "cat": "Politics & History"},
            {"q": "What is Nigeria's most popular rice dish?", "a": "Jollof Rice", "options": ["Jollof Rice", "Fried Rice", "Coconut Rice", "Ofada Rice"], "cat": "Food & Culture"},
            {"q": "What is the capital of Nigeria?", "a": "Abuja", "options": ["Lagos", "Abuja", "Kano", "Ibadan"], "cat": "Geography"},
            # Add more questions here if needed
        ]
        
        if self.cat_var.get() == "All Categories":
            self.questions = all_questions
        else:
            self.questions = [q for q in all_questions if q["cat"] == self.cat_var.get()]
        
        random.shuffle(self.questions)
    
    def show_question(self):
        self.cancel_timer()
        for widget in self.root.winfo_children():
            widget.destroy()
            
        q = self.questions[self.current_question]
        letters = ["A", "B", "C", "D"]
        
        # Header
        tk.Label(self.root, text=f"QUESTION {self.current_question + 1}", 
                font=("Arial", 16, "bold"), fg="#FFD700", bg="#0a0a2e").pack(pady=10)
        
        tk.Label(self.root, text=f"Score: ₦{self.score:,}", 
                font=("Arial", 18, "bold"), fg="#00FFAA", bg="#0a0a2e").pack()
        
        # Timer
        self.timer_label = tk.Label(self.root, text=f"⏳ {self.time_left}s", 
                                  font=("Arial", 20, "bold"), fg="#FF3333", bg="#0a0a2e")
        self.timer_label.pack(pady=10)
        
        # Question Box
        q_frame = tk.Frame(self.root, bg="#1a1a4d", relief="raised", bd=4)
        q_frame.pack(pady=30, padx=80, fill="x")
        
        tk.Label(q_frame, text=q["q"], font=("Arial", 18, "bold"), 
                fg="white", bg="#1a1a4d", wraplength=800, justify="center").pack(pady=40, padx=30)
        
        # Options
        opt_frame = tk.Frame(self.root, bg="#0a0a2e")
        opt_frame.pack(pady=20)
        
        for i, option in enumerate(q["options"]):
            btn = tk.Button(opt_frame, text=f"{letters[i]}. {option}", 
                          font=("Arial", 14, "bold"), width=50, height=2,
                          bg="#003366", fg="#FFFFFF", activebackground="#FFCC00",
                          command=lambda o=option: self.check_answer(o, q["a"]))
            btn.pack(pady=8)
    
        self.update_timer()
    
    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"⏳ {self.time_left}s")
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            self.time_up()
    
    def check_answer(self, selected, correct):
        self.cancel_timer()
        if selected == correct:
            self.score += 50
            self.play_sound("correct")
            messagebox.showinfo("✅ CORRECT!", "Well done! You're on fire 🔥")
        else:
            self.play_sound("wrong")
            messagebox.showerror("❌ Wrong Answer", f"The correct answer was:\n{correct}")
        self.next_question()
    
    def time_up(self):
        self.cancel_timer()
        self.play_sound("wrong")
        messagebox.showwarning("⏰ Time's Up!", "You ran out of time!")
        self.next_question()
    
    def next_question(self):
        self.current_question += 1
        self.time_left = 10
        if self.current_question < len(self.questions):
            self.show_question()
        else:
            self.show_final_score()
    
    def show_final_score(self):
        self.cancel_timer()
        self.save_high_score()
        for widget in self.root.winfo_children():
            widget.destroy()
            
        tk.Label(self.root, text="GAME OVER", 
                font=("Arial", 36, "bold"), fg="#FFD700", bg="#0a0a2e").pack(pady=40)
        
        tk.Label(self.root, text=f"You Won: ₦{self.score:,}", 
                font=("Arial", 28, "bold"), fg="#00FFAA", bg="#0a0a2e").pack(pady=20)
        
        ttk.Button(self.root, text="Play Again", command=self.show_main_menu).pack(pady=30, ipadx=40, ipady=15)
    
    def show_high_scores(self):
        self.cancel_timer()
        if not self.high_scores:
            messagebox.showinfo("High Scores", "No scores yet. Play the game!")
            return
            
        text = "🏆 TOP NAIIJA MILLIONAIRES 🏆\n\n"
        for i, hs in enumerate(self.high_scores, 1):
            text += f"{i}. ₦{hs['score']:,}   —   {hs['date']}\n"
        messagebox.showinfo("High Scores", text)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    game = NaijaQuiz()
    game.run()
