import tkinter as tk
import random
import requests

BACKEND_URL = 'http://127.0.0.1:5000'

class BowlingGame:
    def __init__(self, root):
        self.root = root
        self.root.title('Simple Bowling Game')
        self.canvas = tk.Canvas(root, width=400, height=600, bg='tan')
        self.canvas.pack()
        self.reset_game()
        self.root.bind('<space>', self.roll_ball)
        self.draw_lane()
        self.draw_pins()
        self.draw_ball()
        self.score_label = tk.Label(root, text=f'Score: {self.score}')
        self.score_label.pack()
        self.highscore_label = tk.Label(root, text='High Scores:')
        self.highscore_label.pack()
        self.highscore_list = tk.Listbox(root)
        self.highscore_list.pack()
        self.update_highscores()

    def reset_game(self):
        self.score = 0
        self.pins = [True] * 10
        self.ball_pos = [200, 550]
        self.ball_radius = 20
        self.ball_rolled = False

    def draw_lane(self):
        self.canvas.create_rectangle(100, 50, 300, 580, fill='burlywood4')

    def draw_pins(self):
        self.pin_coords = [
            (200, 100), (185, 130), (215, 130),
            (170, 160), (200, 160), (230, 160),
            (155, 190), (185, 190), (215, 190), (245, 190)
        ]
        for i, (x, y) in enumerate(self.pin_coords):
            if self.pins[i]:
                self.canvas.create_oval(x-10, y-10, x+10, y+10, fill='white', outline='black')

    def draw_ball(self):
        x, y = self.ball_pos
        self.ball = self.canvas.create_oval(x-self.ball_radius, y-self.ball_radius, x+self.ball_radius, y+self.ball_radius, fill='black')

    def roll_ball(self, event=None):
        if self.ball_rolled:
            return
        self.ball_rolled = True
        self.animate_ball()

    def animate_ball(self):
        for _ in range(25):
            self.canvas.move(self.ball, 0, -20)
            self.root.update()
            self.root.after(20)
        self.check_pins()
        self.update_score()
        self.submit_score()
        self.update_highscores()
        self.root.after(2000, self.restart)

    def check_pins(self):
        hit = random.sample(range(10), random.randint(3, 10))
        for i in hit:
            self.pins[i] = False
        self.canvas.delete('all')
        self.draw_lane()
        self.draw_pins()
        self.draw_ball()

    def update_score(self):
        self.score = sum([not p for p in self.pins])
        self.score_label.config(text=f'Score: {self.score}')

    def submit_score(self):
        try:
            requests.post(f'{BACKEND_URL}/submit', json={'score': self.score})
        except Exception:
            pass

    def update_highscores(self):
        try:
            r = requests.get(f'{BACKEND_URL}/highscores')
            scores = r.json()
            self.highscore_list.delete(0, tk.END)
            for s in scores:
                self.highscore_list.insert(tk.END, s)
        except Exception:
            self.highscore_list.delete(0, tk.END)
            self.highscore_list.insert(tk.END, 'Backend not running')

    def restart(self):
        self.canvas.delete('all')
        self.reset_game()
        self.draw_lane()
        self.draw_pins()
        self.draw_ball()
        self.ball_rolled = False

if __name__ == '__main__':
    root = tk.Tk()
    game = BowlingGame(root)
    root.mainloop()
