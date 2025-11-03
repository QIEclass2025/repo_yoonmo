# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import font
import requests
from PIL import Image, ImageTk
import io
import random
import os

HIGHSCORE_FILE = "highscore.txt"

class DogBreedGame(tk.Tk):
    def __init__(self):
        super().__init__()

        # --- 상태 변수 초기화 ---
        self.score = 0
        self.high_score = 0
        self.current_question = 0
        self.total_questions = 10
        self.all_breeds = []
        self.correct_answer = ""

        # --- 윈도우 설정 ---
        self.title("강아지 품종 맞추기")
        self.geometry("600x800")
        self.configure(bg="#f0f2f5")

        # --- 폰트 설정 ---
        self.title_font = font.Font(family="Helvetica", size=24, weight="bold")
        self.subtitle_font = font.Font(family="Helvetica", size=16)
        self.comment_font = font.Font(family="Helvetica", size=18, weight="bold", slant="italic")
        self.score_font = font.Font(family="Helvetica", size=14)
        self.button_font = font.Font(family="Helvetica", size=12, weight="bold")
        self.result_font = font.Font(family="Helvetica", size=16, weight="bold")

        # --- UI 프레임 설정 ---
        self.game_frame = tk.Frame(self, bg="#f0f2f5")
        self.results_frame = tk.Frame(self, bg="#f0f2f5")

        self.create_game_widgets()
        self.create_results_widgets()

        # --- 게임 시작 ---
        self.load_high_score()
        self.show_frame(self.game_frame)
        self.load_breeds_and_start()

    def show_frame(self, frame_to_show):
        self.game_frame.pack_forget()
        self.results_frame.pack_forget()
        frame_to_show.pack(expand=True, fill=tk.BOTH)

    def create_game_widgets(self):
        main_frame = self.game_frame
        main_frame.configure(padx=20, pady=20)

        self.question_label = tk.Label(main_frame, text="", font=self.subtitle_font, bg="#f0f2f5", fg="#1c1e21")
        self.question_label.pack(pady=(0, 10))

        self.score_label = tk.Label(main_frame, text="점수: 0", font=self.score_font, bg="#f0f2f5", fg="#606770")
        self.score_label.pack(pady=(0, 20))

        self.image_bg = tk.Frame(main_frame, bg="white", bd=0, relief=tk.SUNKEN, padx=10, pady=10)
        self.image_bg.pack(pady=10)
        self.image_label = tk.Label(self.image_bg, bg="white")
        self.image_label.pack()

        self.options_frame = tk.Frame(main_frame, bg="#f0f2f5")
        self.options_frame.pack(pady=20, expand=True, fill=tk.X)
        self.option_buttons = []
        for i in range(4):
            button = tk.Button(self.options_frame, text="", font=self.button_font, width=20, pady=10, bg="#e7f3ff", fg="#1877f2", relief=tk.FLAT, borderwidth=0)
            self.option_buttons.append(button)
        
        self.options_frame.grid_columnconfigure(0, weight=1)
        self.options_frame.grid_columnconfigure(1, weight=1)
        self.option_buttons[0].grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.option_buttons[1].grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.option_buttons[2].grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        self.option_buttons[3].grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        self.result_label = tk.Label(main_frame, text="", font=self.result_font, bg="#f0f2f5")
        self.result_label.pack(pady=10)

        self.next_button = tk.Button(main_frame, text="다음 문제", font=self.button_font, bg="white", fg="red", relief=tk.FLAT, command=self.new_round, state=tk.DISABLED, disabledforeground="yellow")
        self.next_button.pack(pady=10)

    def create_results_widgets(self):
        results_frame = self.results_frame
        results_frame.configure(padx=20, pady=20)

        tk.Label(results_frame, text="게임 종료!", font=self.title_font, bg="#f0f2f5", fg="black").pack(pady=20)
        
        self.comment_label = tk.Label(results_frame, text="", font=self.comment_font, bg="#f0f2f5", fg="#007bff")
        self.comment_label.pack(pady=(10, 20))

        self.final_score_label = tk.Label(results_frame, text="", font=self.subtitle_font, bg="#f0f2f5", fg="black")
        self.final_score_label.pack(pady=10)
        self.highscore_label = tk.Label(results_frame, text="", font=self.subtitle_font, bg="#f0f2f5", fg="black")
        self.highscore_label.pack(pady=10)

        tk.Button(results_frame, text="다시 시작", font=self.button_font, bg="#1877f2", fg="white", command=self.restart_game).pack(pady=20)

    def load_high_score(self):
        if os.path.exists(HIGHSCORE_FILE):
            with open(HIGHSCORE_FILE, "r") as f:
                try:
                    self.high_score = int(f.read())
                except (ValueError, IOError):
                    self.high_score = 0
        else:
            self.high_score = 0

    def save_high_score(self):
        with open(HIGHSCORE_FILE, "w") as f:
            f.write(str(self.high_score))

    def load_breeds_and_start(self):
        self.after(100, self._fetch_all_breeds)

    def _fetch_all_breeds(self):
        try:
            response = requests.get("https://dog.ceo/api/breeds/list/all")
            response.raise_for_status()
            self.all_breeds = list(response.json()['message'].keys())
            self.new_round()
        except requests.RequestException as e:
            self.result_label.config(text="오류: 품종 목록 로드 실패", fg="red")

    def new_round(self):
        self.current_question += 1
        if self.current_question > self.total_questions:
            self.show_results()
            return

        self.question_label.config(text=f"문제 {self.current_question}/{self.total_questions}")
        self.result_label.config(text="")
        self.next_button.config(state=tk.DISABLED)
        for btn in self.option_buttons:
            btn.config(state=tk.NORMAL, bg="#e7f3ff", fg="#1877f2", text="...")
            btn.config(state=tk.DISABLED)

        self.image_label.config(image='')
        self.after(100, self._fetch_new_problem)

    def _fetch_new_problem(self):
        try:
            response = requests.get("https://dog.ceo/api/breeds/image/random")
            response.raise_for_status()
            data = response.json()
            image_url = data['message']

            image_response = requests.get(image_url)
            image_response.raise_for_status()
            image_data = image_response.content
            
            pil_image = Image.open(io.BytesIO(image_data))
            pil_image.thumbnail((400, 400))
            self.tk_image = ImageTk.PhotoImage(pil_image)
            self.image_label.config(image=self.tk_image)

            breed_url_part = image_url.split('/breeds/')[1]
            self.correct_answer = breed_url_part.split('/')[0].replace('-', ' ')

            options = self.generate_options(self.correct_answer)
            for i, option in enumerate(options):
                formatted_option = option.title()
                self.option_buttons[i].config(text=formatted_option, state=tk.NORMAL, command=lambda o=option: self.check_answer(o))
        except Exception as e:
            self.result_label.config(text="오류: 이미지 로드 실패", fg="red")
            self.next_button.config(state=tk.NORMAL)

    def generate_options(self, correct_answer):
        options = {correct_answer}
        while len(options) < 4:
            random_breed = random.choice(self.all_breeds).replace('-', ' ')
            options.add(random_breed)
        shuffled_options = list(options)
        random.shuffle(shuffled_options)
        return shuffled_options

    def check_answer(self, selected_option):
        for btn in self.option_buttons:
            btn.config(state=tk.DISABLED)
            btn_text = btn.cget('text').lower()
            if btn_text == self.correct_answer:
                btn.config(bg="#c8e6c9", fg="#2e7d32")
            elif btn_text == selected_option.lower():
                btn.config(bg="#ffcdd2", fg="#c62828")

        if selected_option.lower() == self.correct_answer:
            self.score += 1
            self.result_label.config(text="정답입니다!", fg="#2e7d32")
            self.next_button.config(fg="#28a745")
        else:
            correct_formatted = self.correct_answer.title()
            self.result_label.config(text=f"오답! 정답: {correct_formatted}", fg="#c62828")
            self.next_button.config(fg="red")
        
        self.score_label.config(text=f"점수: {self.score}")
        self.next_button.config(state=tk.NORMAL)

    def show_results(self):
        score = self.score
        comment = ""
        if score <= 3:
            comment = "강아지와 더 친해져야겠어요! 🐶"
        elif score <= 6:
            comment = "꽤 아시는군요! 일반인 수준은 넘으셨어요."
        elif score <= 9:
            comment = "대단해요! 강아지 전문가 수준입니다!"
        else: # score == 10
            comment = "완벽합니다! 당신을 강아지 마스터로 임명합니다! 👑"
        self.comment_label.config(text=comment)

        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
        
        self.final_score_label.config(text=f"나의 점수: {self.score} / {self.total_questions}")
        self.highscore_label.config(text=f"최고 점수: {self.high_score}")
        self.show_frame(self.results_frame)

    def restart_game(self):
        self.score = 0
        self.current_question = 0
        self.score_label.config(text=f"점수: {self.score}")
        self.show_frame(self.game_frame)
        self.new_round()

if __name__ == "__main__":
    app = DogBreedGame()
    app.mainloop()
