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
        self.root.title("🇳🇬 Naija Brain Battle 🇳🇬")
        self.root.geometry("920x700")
        self.root.resizable(False, False)
        self.root.configure(bg="#008751")
        
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
        
        # Remove old entry from same day if exists
        self.high_scores = [hs for hs in self.high_scores if hs["date"] != today]
        
        # Add new score
        self.high_scores.append({"score": self.score, "date": today})
        
        # Sort and keep top 10
        self.high_scores = sorted(self.high_scores, key=lambda x: x["score"], reverse=True)[:10]
        
        try:
            with open("highscores.json", "w") as f:
                json.dump(self.high_scores, f, indent=2)
        except:
            pass  # Fail silently if save fails
    
    def play_sound(self, sound_type):
        try:
            if sound_type == "correct":
                winsound.Beep(1000, 200)
                winsound.Beep(1300, 150)
            elif sound_type == "wrong":
                winsound.Beep(400, 300)
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
            
        tk.Label(self.root, text="🇳🇬 NAIIJA BRAIN BATTLE 🇳🇬", 
                font=("Arial", 32, "bold"), fg="white", bg="#008751").pack(pady=50)
        
        tk.Label(self.root, text="How Well You Know Your Country? 🔥", 
                font=("Arial", 16), fg="#FFD700", bg="#008751").pack(pady=10)
        
        btn_frame = tk.Frame(self.root, bg="#008751")
        btn_frame.pack(pady=40)
        
        ttk.Button(btn_frame, text="🚀 START QUIZ", command=self.show_category_selection).pack(pady=12, ipadx=40, ipady=12)
        ttk.Button(btn_frame, text="🏆 HIGH SCORES", command=self.show_high_scores).pack(pady=12, ipadx=40, ipady=12)
        ttk.Button(btn_frame, text="Exit", command=self.root.quit).pack(pady=30)
    
    def show_category_selection(self):
        for widget in self.root.winfo_children():
            widget.destroy()
            
        tk.Label(self.root, text="Choose Category", 
                font=("Arial", 24, "bold"), fg="white", bg="#008751").pack(pady=30)
        
        categories = [
            "All Categories", "Music & Afrobeats", "Food & Culture", 
            "Politics & History", "Geography", "Nollywood & Entertainment", 
            "General Knowledge"
        ]
        
        cat_frame = tk.Frame(self.root, bg="#008751")
        cat_frame.pack(pady=20)
        
        self.cat_var = tk.StringVar(value="All Categories")
        
        for cat in categories:
            rb = tk.Radiobutton(cat_frame, text=cat, variable=self.cat_var, value=cat,
                              font=("Arial", 13), bg="#008751", fg="white", selectcolor="#FF9500")
            rb.pack(pady=8, anchor="w", padx=100)
        
        btn_frame = tk.Frame(self.root, bg="#008751")
        btn_frame.pack(pady=40)
        
        ttk.Button(btn_frame, text="Start Quiz", command=self.start_filtered_quiz).pack(ipadx=30, ipady=10)
        ttk.Button(btn_frame, text="Back to Menu", command=self.show_main_menu).pack(ipadx=20, ipady=8, pady=10)
    
    def start_filtered_quiz(self):
        self.score = 0
        self.current_question = 0
        self.time_left = 10
        self.load_filtered_questions()
        if not self.questions:
            messagebox.showwarning("No Questions", "No questions available for this category.")
            self.show_main_menu()
        else:
            self.show_question()
    
    def load_filtered_questions(self):
        all_questions = [
            {"q": "Who sang 'Essence'?", "a": "Wizkid", "options": ["Davido", "Burna Boy", "Wizkid", "Rema"], "cat": "Music & Afrobeats"},
            {"q": "Who is popularly called 'Odogwu'?", "a": "Burna Boy", "options": ["Davido", "Burna Boy", "Wizkid", "Olamide"], "cat": "Music & Afrobeats"},
            {"q": "What is Nigeria's most famous rice dish?", "a": "Jollof Rice", "options": ["Jollof Rice", "Fried Rice", "Coconut Rice", "Ofada Rice"], "cat": "Food & Culture"},
            {"q": "Which soup is made with melon seeds?", "a": "Egusi", "options": ["Egusi", "Ogbono", "Okro", "Efo Riro"], "cat": "Food & Culture"},
            {"q": "Who is the current President of Nigeria?", "a": "Bola Ahmed Tinubu", "options": ["Bola Ahmed Tinubu", "Atiku Abubakar", "Peter Obi", "Muhammadu Buhari"], "cat": "Politics & History"},
            {"q": "What is the capital city of Nigeria?", "a": "Abuja", "options": ["Lagos", "Abuja", "Kano", "Ibadan"], "cat": "Geography"},
            {"q": "Who won BBNaija Season 7?", "a": "Phyna", "options": ["Phyna", "Bella", "Sheggz", "Chioma"], "cat": "Nollywood & Entertainment"},
            {"q": "What is the currency of Nigeria?", "a": "Naira", "options": ["Naira", "Cedi", "Rand", "Dollar"], "cat": "General Knowledge"},
            # Add more as needed...
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
        
        tk.Label(self.root, text=f"Question {self.current_question + 1} / {len(self.questions)}", 
                font=("Arial", 14), bg="#008751", fg="white").pack(pady=10)
        
        tk.Label(self.root, text=f"Score: {self.score}", font=("Arial", 18, "bold"), 
                bg="#008751", fg="#FFD700").pack()
        
        self.timer_label = tk.Label(self.root, text=f"⏳ {self.time_left}s", 
                                  font=("Arial", 22, "bold"), fg="#FF0000", bg="#008751")
        self.timer_label.pack(pady=15)
        
        tk.Label(self.root, text=q["q"], font=("Arial", 16), wraplength=780, 
                bg="#008751", fg="white", justify="center").pack(pady=40)
        
        for option in q["options"]:
            btn = tk.Button(self.root, text=option, font=("Arial", 13), width=65, height=2,
                          bg="#ffffff", fg="#000000", command=lambda o=option: self.check_answer(o, q["a"]))
            btn.pack(pady=6)
        
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
            self.score += 25
            self.play_sound("correct")
            messagebox.showinfo("✅ CORRECT!", "You try! Well done my guy 🔥")
        else:
            self.play_sound("wrong")
            messagebox.showerror("❌ Wrong Answer", f"Correct answer na:\n{correct}")
        self.next_question()
    
    def time_up(self):
        self.cancel_timer()
        self.play_sound("wrong")
        messagebox.showwarning("⏰ Time Up!", "You no finish on time!")
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
            
        is_new_high = self.score >= (self.high_scores[0]["score"] if self.high_scores else 0)
        
        tk.Label(self.root, text="Quiz Don Finish!", font=("Arial", 28, "bold"), 
                fg="#FFD700", bg="#008751").pack(pady=30)
        
        tk.Label(self.root, text=f"Your Score: {self.score} Points", 
                font=("Arial", 24), fg="white", bg="#008751").pack(pady=10)
        
        if is_new_high and self.score > 0:
            tk.Label(self.root, text="🎉 NEW HIGH SCORE! 🎉", 
                    font=("Arial", 18, "bold"), fg="#00FF00", bg="#008751").pack(pady=10)
        
        ttk.Button(self.root, text="Play Again", command=self.show_main_menu).pack(pady=20, ipadx=40, ipady=12)
        ttk.Button(self.root, text="View High Scores", command=self.show_high_scores).pack(pady=10, ipadx=30, ipady=8)
    
    def show_high_scores(self):
        self.cancel_timer()
        if not self.high_scores:
            messagebox.showinfo("High Scores", "No high scores yet. Play to set records!")
            return
            
        text = "🏆 TOP 10 HIGH SCORES 🏆\n\n"
        for i, hs in enumerate(self.high_scores, 1):
            text += f"{i:2d}. {hs['score']:3d} points   —   {hs['date']}\n"
        
        messagebox.showinfo("Persistent High Scores", text)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    game = NaijaQuiz()
    game.run()
