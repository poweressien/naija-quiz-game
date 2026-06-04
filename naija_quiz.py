import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
from datetime import datetime
import winsound
import os

class NaijaMillionaire:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🇳🇬 Who Wants to Be a Naija Millionaire?")
        self.root.geometry("1150x740")
        self.root.resizable(False, False)
        self.root.configure(bg="#050520")
        
        self.score = 0
        self.current_question = 0
        self.time_left = 10
        self.timer_id = None
        self.high_scores = self.load_high_scores()
        self.lifelines = {"50:50": True, "Phone a Friend": True, "Ask the Audience": True}
        self.prizes = [0, 100, 200, 500, 1000, 2000, 5000, 10000, 25000, 50000, 100000]
        
        self.setup_styles()
        self.show_main_menu()
        
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TButton", font=("Arial", 12, "bold"), padding=10)
        style.configure("Accent.TButton", background="#FFD700", foreground="#000000")
        
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
    
    def cancel_timer(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
    
    def show_main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
            
        header = tk.Label(self.root, text="WHO WANTS TO BE A", font=("Arial", 28, "bold"), fg="#FFD700", bg="#050520")
        header.pack(pady=20)
        title = tk.Label(self.root, text="NAIJA MILLIONAIRE", font=("Arial", 48, "bold"), fg="#FF2222", bg="#050520")
        title.pack(pady=5)
        
        ttk.Button(self.root, text="🚀 START GAME", command=self.show_category_selection, style="Accent.TButton").pack(pady=60, ipadx=70, ipady=20)
        ttk.Button(self.root, text="🏆 HIGH SCORES", command=self.show_high_scores).pack(pady=15, ipadx=60)
    
    def show_category_selection(self):
        for widget in self.root.winfo_children():
            widget.destroy()
            
        tk.Label(self.root, text="SELECT CATEGORY", font=("Arial", 26, "bold"), fg="#FFD700", bg="#050520").pack(pady=50)
        
        categories = ["All Categories", "Music & Afrobeats", "Food & Culture", "Politics & History", "Geography", "General Knowledge"]
        self.cat_var = tk.StringVar(value="All Categories")
        
        for cat in categories:
            rb = tk.Radiobutton(self.root, text=cat, variable=self.cat_var, value=cat, font=("Arial", 14), bg="#050520", fg="#FFFFFF", selectcolor="#FF9500")
            rb.pack(pady=12)
        
        ttk.Button(self.root, text="BEGIN GAME", command=self.start_game, style="Accent.TButton").pack(pady=60, ipadx=70, ipady=18)
    
    def start_game(self):
        self.score = 0
        self.current_question = 0
        self.lifelines = {"50:50": True, "Phone a Friend": True, "Ask the Audience": True}
        self.load_filtered_questions()
        self.show_question()
    
    def load_filtered_questions(self):
        all_questions = [
            {"q": "Who sang the hit song 'Essence'?", "a": "Wizkid", "options": ["Davido", "Burna Boy", "Wizkid", "Rema"], "cat": "Music & Afrobeats"},
            {"q": "Who is the current President of Nigeria?", "a": "Bola Ahmed Tinubu", "options": ["Bola Ahmed Tinubu", "Atiku Abubakar", "Peter Obi", "Muhammadu Buhari"], "cat": "Politics & History"},
            {"q": "What is Nigeria's most popular rice dish worldwide?", "a": "Jollof Rice", "options": ["Jollof Rice", "Fried Rice", "Coconut Rice", "Ofada Rice"], "cat": "Food & Culture"},
            {"q": "What is the capital city of Nigeria?", "a": "Abuja", "options": ["Lagos", "Abuja", "Kano", "Ibadan"], "cat": "Geography"},
            {"q": "Which soup is traditionally made with melon seeds?", "a": "Egusi", "options": ["Egusi", "Ogbono", "Okro", "Efo Riro"], "cat": "Food & Culture"},
        ]
        if self.cat_var.get() == "All Categories":
            self.questions = all_questions
        else:
            self.questions = [q for q in all_questions if q["cat"] == self.cat_var.get()]
        random.shuffle(self.questions)
    
    def show_question(self, fade=0):
        self.cancel_timer()
        for widget in self.root.winfo_children():
            widget.destroy()
            
        q = self.questions[self.current_question]
        letters = ["A", "B", "C", "D"]
        
        main_frame = tk.Frame(self.root, bg="#050520")
        main_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Top Info
        top = tk.Frame(main_frame, bg="#050520")
        top.pack(fill="x")
        tk.Label(top, text=f"QUESTION {self.current_question + 1}", font=("Arial", 14, "bold"), fg="#FFD700", bg="#050520").pack(side="left")
        tk.Label(top, text=f"₦{self.prizes[self.current_question]:,}", font=("Arial", 20, "bold"), fg="#00FFAA", bg="#050520").pack(side="right")
        
        self.timer_label = tk.Label(main_frame, text=f"⏳ {self.time_left} SECONDS", font=("Arial", 18, "bold"), fg="#FF4444", bg="#050520")
        self.timer_label.pack(pady=8)
        
        # Question with fade effect
        q_frame = tk.Frame(main_frame, bg="#1a1a4d", relief="solid", bd=4)
        q_frame.pack(pady=25, fill="x", padx=40)
        self.question_label = tk.Label(q_frame, text=q["q"], font=("Arial", 18, "bold"), fg="white", bg="#1a1a4d", wraplength=850, justify="center")
        self.question_label.pack(pady=45, padx=30)
        
        # Animate question appearance
        if fade < 100:
            self.question_label.config(fg=f"#{int(255*fade/100):02x}{int(255*fade/100):02x}{int(255*fade/100):02x}")
            self.root.after(20, lambda: self.show_question(fade + 10))
            return
        
        # Options
        for i, option in enumerate(q["options"]):
            btn = tk.Button(main_frame, text=f"{letters[i]}. {option}", font=("Arial", 14, "bold"), 
                          width=55, height=2, bg="#112244", fg="#FFFFFF", activebackground="#FFCC00",
                          relief="raised", bd=4, command=lambda o=option: self.check_answer(o, q["a"]))
            btn.pack(pady=9)
        
        self.show_lifelines()
        self.show_money_ladder()
        self.update_timer()
    
    def show_lifelines(self):
        life_frame = tk.Frame(self.root, bg="#050520")
        life_frame.pack(pady=15)
        tk.Label(life_frame, text="LIFELINES", font=("Arial", 12, "bold"), fg="#FFD700", bg="#050520").pack()
        
        for name in self.lifelines:
            state = "normal" if self.lifelines[name] else "disabled"
            color = "#9933FF" if self.lifelines[name] else "#555555"
            btn = tk.Button(life_frame, text=name, font=("Arial", 10, "bold"), bg=color, fg="white",
                          state=state, command=lambda n=name: self.use_lifeline(n))
            btn.pack(side="left", padx=12, ipadx=15, ipady=8)
    
    def show_money_ladder(self):
        ladder_frame = tk.Frame(self.root, bg="#1a1a4d", width=230)
        ladder_frame.pack(side="right", fill="y", padx=20, pady=20)
        tk.Label(ladder_frame, text="PRIZE LADDER", font=("Arial", 14, "bold"), fg="#FFD700", bg="#1a1a4d").pack(pady=15)
        
        for i, prize in enumerate(reversed(self.prizes[1:])):
            level = len(self.prizes) - i - 1
            color = "#FFD700" if level == self.current_question else "#CCCCCC"
            bg = "#003300" if level == self.current_question else "#1a1a4d"
            tk.Label(ladder_frame, text=f"₦{prize:,}", font=("Arial", 11, "bold"), fg=color, bg=bg).pack(pady=6)
    
    def use_lifeline(self, lifeline):
        if not self.lifelines[lifeline]: return
        self.lifelines[lifeline] = False
        messagebox.showinfo(lifeline, f"{lifeline} activated!")
        self.show_question()
    
    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            color = "#FF0000" if self.time_left <= 3 else "#FF4444"
            self.timer_label.config(text=f"⏳ {self.time_left} SECONDS", fg=color)
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            self.time_up()
    
    def check_answer(self, selected, correct):
        self.cancel_timer()
        if selected == correct:
            self.score = self.prizes[self.current_question + 1]
            self.play_sound("correct")
            self.flash_correct()
            self.root.after(1200, self.next_question)
        else:
            self.play_sound("wrong")
            messagebox.showerror("❌ GAME OVER", f"Wrong!\nCorrect answer was:\n{correct}")
            self.show_final_score()
    
    def flash_correct(self):
        # Simple flash animation
        self.root.configure(bg="#003300")
        self.root.after(200, lambda: self.root.configure(bg="#050520"))
    
    def time_up(self):
        self.cancel_timer()
        messagebox.showwarning("⏰ Time's Up!", "You ran out of time!")
        self.show_final_score()
    
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
            
        tk.Label(self.root, text="CONGRATULATIONS!", font=("Arial", 36, "bold"), fg="#FFD700", bg="#050520").pack(pady=80)
        tk.Label(self.root, text=f"You Won\n₦{self.score:,}", font=("Arial", 32, "bold"), fg="#00FFAA", bg="#050520").pack(pady=20)
        ttk.Button(self.root, text="PLAY AGAIN", command=self.show_main_menu, style="Accent.TButton").pack(pady=50, ipadx=70, ipady=18)
    
    def show_high_scores(self):
        text = "🏆 TOP NAIIJA MILLIONAIRES 🏆\n\n"
        for i, hs in enumerate(self.high_scores[:8], 1):
            text += f"{i}. ₦{hs['score']:,}   —   {hs['date']}\n"
        messagebox.showinfo("High Scores", text if self.high_scores else "No scores yet!")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    game = NaijaMillionaire()
    game.run()
