import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
from datetime import datetime
import winsound

class NaijaQuiz:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🇳🇬 Naija Brain Battle 🇳🇬")
        self.root.geometry("900x680")
        self.root.resizable(False, False)
        self.root.configure(bg="#008751")
        
        self.score = 0
        self.current_question = 0
        self.time_left = 10
        self.timer_id = None  # Important: Track timer ID
        self.high_scores = self.load_high_scores()
        
        self.show_main_menu()
        
    def load_high_scores(self):
        try:
            with open("highscores.json", "r") as f:
                return json.load(f)
        except:
            return []
    
    def save_high_score(self):
        self.high_scores.append({"score": self.score, "date": str(datetime.now().date())})
        self.high_scores = sorted(self.high_scores, key=lambda x: x["score"], reverse=True)[:10]
        with open("highscores.json", "w") as f:
            json.dump(self.high_scores, f, indent=2)
    
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
        
        tk.Label(self.root, text="Oya! Prove You Be Real Naija Person 🔥", 
                font=("Arial", 16), fg="#FFD700", bg="#008751").pack(pady=10)
        
        btn_frame = tk.Frame(self.root, bg="#008751")
        btn_frame.pack(pady=40)
        
        ttk.Button(btn_frame, text="🚀 START QUIZ", command=self.start_quiz).pack(pady=12, ipadx=40, ipady=12)
        ttk.Button(btn_frame, text="🏆 HIGH SCORES", command=self.show_high_scores).pack(pady=12, ipadx=40, ipady=12)
        ttk.Button(btn_frame, text="Exit", command=self.root.quit).pack(pady=30)
    
    def start_quiz(self):
        self.score = 0
        self.current_question = 0
        self.time_left = 10
        self.load_naija_questions()
        self.show_question()
    
    def load_naija_questions(self):
        self.questions = [
            {"q": "Who is the current President of Nigeria?", "a": "Bola Ahmed Tinubu", "options": ["Bola Ahmed Tinubu", "Atiku Abubakar", "Peter Obi", "Muhammadu Buhari"]},
            {"q": "What does 'How Far?' mean in Pidgin?", "a": "How are you?", "options": ["How are you?", "Where are you?", "What happened?", "Goodbye"]},
            {"q": "Who sang the song 'Essence'?", "a": "Wizkid", "options": ["Davido", "Burna Boy", "Wizkid", "Rema"]},
            {"q": "Which state is known as the Centre of Excellence?", "a": "Lagos", "options": ["Lagos", "Abuja", "Kano", "Rivers"]},
            {"q": "What is Nigeria's national anthem first line?", "a": "Arise, O compatriots", "options": ["Arise, O compatriots", "Nigeria we hail thee", "God bless our land", "One Nigeria"]},
            {"q": "Which city is called the Garden City?", "a": "Port Harcourt", "options": ["Port Harcourt", "Ibadan", "Enugu", "Jos"]},
            {"q": "What is the most popular Nigerian soup?", "a": "Egusi", "options": ["Egusi", "Ogbono", "Okro", "Efo Riro"]},
            {"q": "Who won BBNaija Season 7?", "a": "Phyna", "options": ["Phyna", "Bella", "Sheggz", "Chioma"]},
            {"q": "Which Nigerian musician is called 'Odogwu'?", "a": "Burna Boy", "options": ["Davido", "Burna Boy", "Wizkid", "Flavour"]},
            {"q": "What is the capital of Nigeria?", "a": "Abuja", "options": ["Lagos", "Abuja", "Kano", "Ibadan"]},
            {"q": "Who sang 'Fall'?", "a": "Wizkid", "options": ["Wizkid", "Davido", "Rema", "Tems"]},
            {"q": "Which state is famous for Suya?", "a": "Kano", "options": ["Kano", "Lagos", "Benue", "Oyo"]},
        ]
        random.shuffle(self.questions)
    
    def show_question(self):
        self.cancel_timer()   # Cancel any running timer
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
        
        tk.Label(self.root, text=q["q"], font=("Arial", 16), wraplength=750, 
                bg="#008751", fg="white", justify="center").pack(pady=40)
        
        for option in q["options"]:
            btn = tk.Button(self.root, text=option, font=("Arial", 13), width=60, height=2,
                          bg="#ffffff", fg="#000000", command=lambda o=option: self.check_answer(o, q["a"]))
            btn.pack(pady=7)
        
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
            messagebox.showinfo("✅ CORRECT!", "You try no be small! 🔥")
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
            
        tk.Label(self.root, text="Quiz Don Finish!", font=("Arial", 28, "bold"), 
                fg="#FFD700", bg="#008751").pack(pady=40)
        
        tk.Label(self.root, text=f"Your Score: {self.score} Points", 
                font=("Arial", 24), fg="white", bg="#008751").pack(pady=20)
        
        ttk.Button(self.root, text="Play Again", command=self.show_main_menu).pack(pady=30, ipadx=40, ipady=12)
    
    def show_high_scores(self):
        self.cancel_timer()
        if not self.high_scores:
            messagebox.showinfo("High Scores", "No high scores yet. Go play!")
            return
            
        text = "🏆 TOP HIGH SCORES 🏆\n\n"
        for i, hs in enumerate(self.high_scores[:5], 1):
            text += f"{i}. {hs['score']} points   -   {hs['date']}\n"
        messagebox.showinfo("High Scores", text)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    game = NaijaQuiz()
    game.run()
