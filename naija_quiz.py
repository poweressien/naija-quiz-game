import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
from datetime import datetime

class NaijaQuiz:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🇳🇬 Naija Brain Battle 🇳🇬")
        self.root.geometry("850x650")
        self.root.resizable(False, False)
        self.root.configure(bg="#008751")
        
        self.score = 0
        self.current_question = 0
        self.time_left = 15
        self.high_score = self.load_high_score()
        self.questions = []
        
        self.show_main_menu()
        
    def load_high_score(self):
        try:
            with open("highscore.json", "r") as f:
                return json.load(f)["highscore"]
        except:
            return 0
    
    def save_high_score(self):
        if self.score > self.high_score:
            with open("highscore.json", "w") as f:
                json.dump({"highscore": self.score, "date": str(datetime.now())}, f)
    
    def show_main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
            
        tk.Label(self.root, text="🇳🇬 NAIIJA BRAIN BATTLE 🇳🇬", 
                font=("Arial", 32, "bold"), fg="white", bg="#008751").pack(pady=50)
        
        tk.Label(self.root, text="Oya! Show Us How Naija You Are 🔥", 
                font=("Arial", 16), fg="#FFD700", bg="#008751").pack(pady=10)
        
        btn_frame = tk.Frame(self.root, bg="#008751")
        btn_frame.pack(pady=40)
        
        ttk.Button(btn_frame, text="🚀 START QUIZ", command=self.start_quiz).pack(pady=12, ipadx=30, ipady=10)
        ttk.Button(btn_frame, text="🏆 HIGH SCORE", command=self.show_high_score).pack(pady=12, ipadx=30, ipady=10)
        ttk.Button(btn_frame, text="Exit", command=self.root.quit).pack(pady=30)
    
    def start_quiz(self):
        self.score = 0
        self.current_question = 0
        self.load_naija_questions()
        self.show_question()
    
    def load_naija_questions(self):
        self.questions = [
            {"q": "Who is the President of Nigeria in 2025?", "a": "Bola Ahmed Tinubu", "options": ["Bola Ahmed Tinubu", "Atiku Abubakar", "Peter Obi", "Muhammadu Buhari"]},
            {"q": "What does 'How Far?' mean?", "a": "How are you?", "options": ["How are you?", "Where are you going?", "What is happening?", "Goodbye"]},
            {"q": "Who sang 'Essence'?", "a": "Wizkid", "options": ["Davido", "Burna Boy", "Wizkid", "Rema"]},
            {"q": "Which state is called 'Centre of Excellence'?", "a": "Lagos", "options": ["Lagos", "Abuja", "Kano", "Rivers"]},
            {"q": "What is Nigeria's national anthem first line?", "a": "Arise, O compatriots", "options": ["Arise, O compatriots", "Nigeria we hail thee", "God bless Nigeria", "One Nigeria"]},
        ]
        random.shuffle(self.questions)
    
    def show_question(self):
        for widget in self.root.winfo_children():
            widget.destroy()
            
        q = self.questions[self.current_question]
        
        tk.Label(self.root, text=f"Question {self.current_question + 1} of {len(self.questions)}", 
                font=("Arial", 14), bg="#008751", fg="white").pack(pady=10)
        
        tk.Label(self.root, text=f"Score: {self.score}", font=("Arial", 18, "bold"), 
                bg="#008751", fg="#FFD700").pack()
        
        self.timer_label = tk.Label(self.root, text=f"⏳ {self.time_left}s", 
                                  font=("Arial", 20, "bold"), fg="red", bg="#008751")
        self.timer_label.pack(pady=15)
        
        tk.Label(self.root, text=q["q"], font=("Arial", 16), wraplength=700, 
                bg="#008751", fg="white", justify="center").pack(pady=40)
        
        for option in q["options"]:
            btn = tk.Button(self.root, text=option, font=("Arial", 13), width=60, height=2,
                          bg="#ffffff", fg="#000000", command=lambda o=option: self.check_answer(o, q["a"]))
            btn.pack(pady=8)
        
        self.update_timer()
    
    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"⏳ {self.time_left}s")
            self.root.after(1000, self.update_timer)
        else:
            self.time_up()
    
    def check_answer(self, selected, correct):
        if selected == correct:
            self.score += 20
            messagebox.showinfo("✅ CORRECT!", "You try! 🔥 Correct answer!")
        else:
            messagebox.showerror("❌ Wrong", f"Correct answer na:\n{correct}")
        self.next_question()
    
    def time_up(self):
        messagebox.showwarning("Time Up!", "You no finish on time!")
        self.next_question()
    
    def next_question(self):
        self.current_question += 1
        self.time_left = 15
        if self.current_question < len(self.questions):
            self.show_question()
        else:
            self.show_final_score()
    
    def show_final_score(self):
        self.save_high_score()
        for widget in self.root.winfo_children():
            widget.destroy()
            
        tk.Label(self.root, text="Quiz Don Finish!", font=("Arial", 28, "bold"), 
                fg="#FFD700", bg="#008751").pack(pady=50)
        tk.Label(self.root, text=f"Your Score: {self.score} Points", 
                font=("Arial", 22), fg="white", bg="#008751").pack(pady=20)
        ttk.Button(self.root, text="Play Again", command=self.show_main_menu).pack(pady=30, ipadx=30)
    
    def show_high_score(self):
        messagebox.showinfo("High Score", f"Best Score: {self.high_score} points")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    game = NaijaQuiz()
    game.run()
