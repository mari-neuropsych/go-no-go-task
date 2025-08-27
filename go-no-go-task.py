import tkinter as tk
import random
import time
import numpy as np

class GoNoGoTask:
    def __init__(self, master, trials=15, go_prob=0.7):
        self.master = master
        self.trials = trials
        self.current_trial = 0
        self.go_prob = go_prob
        self.results = []

        self.label = tk.Label(master, text="", font=("Arial", 48))
        self.label.pack(pady=20)

        self.button = tk.Button(master, text="Press for GO", width=20, height=3,
                                command=self.record_response)
        self.button.pack(pady=10)

        self.next_trial()

    def generate_synthetic_eeg(self, length=100):
        t = np.linspace(0, 1, length)
        signal = np.sin(2 * np.pi * 10 * t) + 0.5 * np.random.randn(length)
        return signal

    def next_trial(self):
        if self.current_trial < self.trials:
            self.is_go = random.random() < self.go_prob
            self.label.config(text="GO" if self.is_go else "NO-GO")
            self.start_time = time.time()
            self.current_eeg = self.generate_synthetic_eeg()
            # Wait 1 second before auto-recording no response for NO-GO
            self.master.after(1000, self.end_trial)
        else:
            self.show_results()

    def record_response(self):
        reaction_time = time.time() - self.start_time
        self.results.append({
            "trial": self.current_trial+1,
            "stimulus": "GO" if self.is_go else "NO-GO",
            "clicked": True,
            "correct": self.is_go,
            "reaction_time": reaction_time,
            "eeg_signal": self.current_eeg.tolist()
        })
        self.current_trial += 1
        self.next_trial()

    def end_trial(self):
        # Record no response for NO-GO or missed GO
        if len(self.results) < self.current_trial + 1:
            clicked = False
            correct = not self.is_go
            reaction_time = None
            self.results.append({
                "trial": self.current_trial+1,
                "stimulus": "GO" if self.is_go else "NO-GO",
                "clicked": clicked,
                "correct": correct,
                "reaction_time": reaction_time,
                "eeg_signal": self.current_eeg.tolist()
            })
        self.current_trial += 1
        self.next_trial()

    def show_results(self):
        self.label.config(text="Task Complete!")
        self.button.config(state="disabled")
        print("Trial | Stimulus | Clicked | Correct | Reaction Time")
        for r in self.results:
            print(f"{r['trial']} | {r['stimulus']} | {r['clicked']} | {r['correct']} | {r['reaction_time']}")
        print("\nSynthetic EEG data for each trial is available in 'eeg_signal' field.")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Go/No-Go Task")
    app = GoNoGoTask(root)
    root.mainloop()
