# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import font, Toplevel
import requests
from PIL import Image, ImageTk
import io
import random
import os

# 하이스코어 파일명 패턴
HIGHSCORE_FILE_TEMPLATE = "dog_game_highscore_{}.txt"

class DogBreedGame(tk.Tk):
    def __init__(self):
        super().__init__()

        # --- 상태 변수 ---
        self.score = 0
        self.high_score = 0
        self.current_question = 0
        self.total_questions = 10 
        self.all_breeds = []
        self.correct_answer = ""
        self.current_pil_image = None 

        # --- 윈도우 설정 ---
        self.title("강아지 품종 맞추기")
        self.geometry("600x900") 
        self.resizable(True, True) 
        self.configure(bg="#f0f2f5")

        # --- 폰트 설정 ---
        self.title_font = font.Font(family="Helvetica", size=24, weight="bold")
        self.subtitle_font = font.Font(family="Helvetica", size=16)
        self.comment_font = font.Font(family="Helvetica", size=18, weight="bold", slant="italic")
        self.score_font = font.Font(family="Helvetica", size=14)
        self.button_font = font.Font(family="Helvetica", size=12, weight="bold")
        self.result_font = font.Font(family="Helvetica", size=16, weight="bold")

        # --- UI 프레임 ---
        self.start_frame = tk.Frame(self, bg="#f0f2f5")
        self.game_frame = tk.Frame(self, bg="#f0f2f5")
        self.results_frame = tk.Frame(self, bg="#f0f2f5")

        self.create_start_screen()
        self.create_game_widgets()
        self.create_results_widgets() # 이제 이 함수가 아래에 있어서 에러 안 남!

        # --- 앱 시작 ---
        self.show_frame(self.start_frame)

    def show_frame(self, frame_to_show):
        self.start_frame.pack_forget()
        self.game_frame.pack_forget()
        self.results_frame.pack_forget()
        frame_to_show.pack(expand=True, fill=tk.BOTH)

    def create_start_screen(self):
        frame = self.start_frame
        for widget in frame.winfo_children():
            widget.destroy()

        frame.configure(padx=20, pady=50)

        tk.Label(frame, text="🐶 멍멍!", font=("Helvetica", 50), bg="#f0f2f5").pack(pady=10)
        tk.Label(frame, text="강아지 품종 맞추기", font=self.title_font, bg="#f0f2f5", fg="#1c1e21").pack(pady=10)
        
        desc = "문제 개수를 선택하고 도전하세요!\n(사진 클릭 시 확대 가능)"
        tk.Label(frame, text=desc, font=self.subtitle_font, bg="#f0f2f5", fg="#606770", justify="center").pack(pady=30)

        modes = [10, 20, 50]
        for mode in modes:
            hs = self.get_highscore_for_mode(mode)
            btn_text = f"{mode} 문제 도전! (최고: {hs}점)"
            btn = tk.Button(frame, text=btn_text, font=self.button_font, bg="white", fg="#1877f2", 
                            width=25, height=2, relief=tk.RAISED,
                            command=lambda m=mode: self.start_game(m))
            btn.pack(pady=10)

    def get_highscore_for_mode(self, mode):
        filename = HIGHSCORE_FILE_TEMPLATE.format(mode)
        if os.path.exists(filename):
            with open(filename, "r") as f:
                try:
                    return int(f.read())
                except:
                    return 0
        return 0

    def start_game(self, total_questions):
        self.total_questions = total_questions
        self.score = 0
        self.high_score = self.get_highscore_for_mode(total_questions)
        self.current_question = 0
        self.show_frame(self.game_frame)
        self.load_breeds_and_start()

    def create_game_widgets(self):
        main_frame = self.game_frame
        main_frame.configure(padx=20, pady=20)

        self.question_label = tk.Label(main_frame, text="", font=self.subtitle_font, bg="#f0f2f5", fg="#1c1e21")
        self.question_label.pack(pady=(0, 10))

        self.score_label = tk.Label(main_frame, text="점수: 0", font=self.score_font, bg="#f0f2f5", fg="#606770")
        self.score_label.pack(pady=(0, 10))

        tk.Label(main_frame, text="🔍 사진을 누르면 크게 보입니다", font=("Helvetica", 10), bg="#f0f2f5", fg="#888").pack()

        self.image_bg = tk.Frame(main_frame, bg="white", bd=0, relief=tk.SUNKEN, padx=5, pady=5)
        self.image_bg.pack(pady=5)
        
        self.image_label = tk.Label(self.image_bg, bg="white", cursor="hand2")
        self.image_label.pack()
        self.image_label.bind("<Button-1>", self.enlarge_image)

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

        self.next_button = tk.Button(main_frame, text="다음 문제", font=self.button_font, bg="white", fg="red", relief=tk.FLAT, command=self.new_round, state=tk.DISABLED, disabledforeground="green")
        self.next_button.pack(pady=20, side=tk.BOTTOM) 

    def enlarge_image(self, event):
        if self.current_pil_image:
            top = Toplevel(self)
            top.title("사진 크게 보기")
            top.geometry("650x650") 
            img = self.current_pil_image.copy()
            img.thumbnail((600, 600))
            tk_img = ImageTk.PhotoImage(img)
            lbl = tk.Label(top, image=tk_img)
            lbl.image = tk_img
            lbl.pack(expand=True, fill=tk.BOTH)

    # --- [복구됨] 아까 빠졌던 함수 ---
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

        tk.Button(results_frame, text="처음으로", font=self.button_font, bg="#1877f2", fg="white", command=self.restart_game).pack(pady=20)

    def load_breeds_and_start(self):
        self.result_label.config(text="데이터 로딩 중...", fg="blue")
        self.after(100, self._fetch_all_breeds)

    def _fetch_all_breeds(self):
        try:
            if not self.all_breeds:
                response = requests.get("https://dog.ceo/api/breeds/list/all")
                response.raise_for_status()
                self.all_breeds = list(response.json()['message'].keys())
            self.new_round()
        except requests.RequestException:
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
        self.result_label.config(text="강아지 섭외 중... 🐕", fg="blue")
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
            
            self.current_pil_image = Image.open(io.BytesIO(image_data))
            
            display_img = self.current_pil_image.copy()
            display_img.thumbnail((400, 400))
            self.tk_image = ImageTk.PhotoImage(display_img)
            self.image_label.config(image=self.tk_image)
            self.result_label.config(text="") 

            breed_url_part = image_url.split('/breeds/')[1]
            self.correct_answer = breed_url_part.split('/')[0].replace('-', ' ')

            options = self.generate_options(self.correct_answer)
            for i, option in enumerate(options):
                formatted_option = option.title()
                self.option_buttons[i].config(text=formatted_option, state=tk.NORMAL, command=lambda o=option: self.check_answer(o))
        except Exception:
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
            self.result_label.config(text="정답입니다! 🙆‍♂️", fg="#2e7d32")
            self.next_button.config(fg="#28a745")
        else:
            correct_formatted = self.correct_answer.title()
            self.result_label.config(text=f"땡! 정답은 {correct_formatted} 🙅‍♂️", fg="#c62828")
            self.next_button.config(fg="red")
        
        self.score_label.config(text=f"점수: {self.score}")
        self.next_button.config(state=tk.NORMAL)

    def show_results(self):
        if self.score > self.high_score:
            self.high_score = self.score
            filename = HIGHSCORE_FILE_TEMPLATE.format(self.total_questions)
            with open(filename, "w") as f:
                f.write(str(self.high_score))
        
        percentage = (self.score / self.total_questions) * 100
        comment = ""
        if percentage <= 30:
            comment = "조금 더 분발하세요! 🐶"
        elif percentage <= 60:
            comment = "좋아요! 가능성이 보여요 👏"
        elif percentage < 100:
            comment = "훌륭해요! 🎓"
        else:
            comment = "당신은 전설의 강아지 마스터! 👑"
            
        self.comment_label.config(text=comment)
        self.final_score_label.config(text=f"최종 점수: {self.score} / {self.total_questions}")
        self.highscore_label.config(text=f"최고 기록: {self.high_score}")
        self.show_frame(self.results_frame)

    def restart_game(self):
        self.create_start_screen() 
        self.show_frame(self.start_frame)

if __name__ == "__main__":
    app = DogBreedGame()
    app.mainloop()
