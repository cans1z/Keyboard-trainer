from tkinter import *
from tkinter import ttk
import time
import random

EN_LETTERS = list("abcdefghijklmnopqrstuvwxyz")
RU_LETTERS = list("йцукенгшщзхъфывапролджэячсмитьбю")

class MainActivity:
    def __init__(self):
        self.root = Tk()
        self.root.title("Keyboard Trainer")
        
        self.translations = {
            'EN': {
                'title': 'Keyboard Trainer',
                'errors': 'Errors',
                'speed': 'Speed',
                'mode_letters': 'Mode: Letters',
                'mode_words': 'Mode: Words',
                'mode_texts': 'Mode: Texts',
                'lang_en': 'Lang: EN',
                'lang_ru': 'Lang: RU',
                'highlight_on': 'Highlight: ON',
                'highlight_off': 'Highlight: OFF',
                'change_exercise': 'Change Exercise',
                'change_language': 'Change Language',
                'toggle_highlight': 'Toggle Highlight',
                'description_change_exercise': 'Change Exercise',
                'description_change_language': 'Change Language',
                'description_toggle_highlight': 'Toggle Highlight',
                'press_enter': 'Press Enter to continue',
                'time_up': 'Time is up! You did not complete the exercise.',
                'press_enter_new': 'Press Enter to start a new exercise'
            },
            'RU': {
                'title': 'Тренажер Клавиатуры',
                'errors': 'Ошибки',
                'speed': 'Скорость',
                'mode_letters': 'Режим: Буквы',
                'mode_words': 'Режим: Слова',
                'mode_texts': 'Режим: Тексты',
                'lang_en': 'Язык: EN',
                'lang_ru': 'Язык: RU',
                'highlight_on': 'Подсветка: ВКЛ',
                'highlight_off': 'Подсветка: ВЫКЛ',
                'change_exercise': 'Сменить Упражнение',
                'change_language': 'Сменить Язык',
                'toggle_highlight': 'Включить Подсветку',
                'description_change_exercise': 'Сменить Упражнение',
                'description_change_language': 'Сменить Язык',
                'description_toggle_highlight': 'Включить Подсветку',
                'press_enter': 'Нажмите Enter, чтобы продолжить',
                'time_up': 'Время вышло! Вы не справились с упражнением.',
                'press_enter_new': 'Нажмите Enter, чтобы начать новое упражнение'
            }
        }
        

        self.MIN_WIDTH = 800
        self.MIN_HEIGHT = 600
        self.MAX_WIDTH = 1920
        self.MAX_HEIGHT = 1080
        
        self.keyboard_positions = {
            'q': 'й', 'w': 'ц', 'e': 'у', 'r': 'к', 't': 'е', 'y': 'н', 'u': 'г', 'i': 'ш', 'o': 'щ', 'p': 'з', '[': 'х', ']': 'ъ',
            'a': 'ф', 's': 'ы', 'd': 'в', 'f': 'а', 'g': 'п', 'h': 'р', 'j': 'о', 'k': 'л', 'l': 'д', ';': 'ж', "'": 'э',
            'z': 'я', 'x': 'ч', 'c': 'с', 'v': 'м', 'b': 'и', 'n': 'т', 'm': 'ь', ',': 'б', '.': 'ю'
        }
        self.ru_positions = {v: k for k, v in self.keyboard_positions.items()}
        
        self.root.geometry(f"{self.MIN_WIDTH}x{self.MIN_HEIGHT}")
        self.center_window()
        
        self.root.minsize(self.MIN_WIDTH, self.MIN_HEIGHT)
        self.root.maxsize(self.MAX_WIDTH, self.MAX_HEIGHT)
        
        self.root.configure(bg="#f0f0f0")
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self.language = 'EN'
        self.mode = 'letters'
        self.highlight = True
        self.time_left = 30
        self.mistakes = 0
        self.total_chars = 0
        self.is_running = False
        self.current_text = ''
        self.error_count = 0
        self.last_checked_position = 0
        self.final_stats = None  # Store final statistics

        self.init_styles()
        self.init_gui()
        self.set_exercise()
        
        self.root.bind('<Configure>', self.on_window_resize)
        
    def init_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("NoBorder.TEntry",
                       fieldbackground="#f0f0f0",
                       borderwidth=0,
                       relief="flat",
                       padding=5,
                       font=("Arial", 20, "bold"))

    def init_gui(self):
        self.top_frame = Frame(self.root, bg="#f0f0f0")
        self.left_frame = Frame(self.root, bg="#f0f0f0")
        self.center_frame = Frame(self.root, bg="#f0f0f0")
        self.bottom_frame = Frame(self.root, bg="#f0f0f0")

        self.top_frame.grid(row=0, column=0, columnspan=3, sticky="ew", pady=5)
        self.left_frame.grid(row=1, column=0, sticky="ns", padx=10)
        self.center_frame.grid(row=1, column=1, sticky="nsew")
        self.bottom_frame.grid(row=2, column=0, columnspan=3, sticky="ew", pady=10)

        self.setup_top_frame()
        self.setup_left_frame()
        self.setup_center_frame()
        self.setup_bottom_frame()

    def setup_top_frame(self):
        timer_frame = Frame(self.top_frame, bg="#f0f0f0")
        timer_frame.pack(fill=X, pady=(0, 5))
        
        self.timer_label = Label(timer_frame, text="01:00", 
                               font=("Arial", 14, "bold"), bg="#f0f0f0", fg="black")
        self.timer_label.pack(expand=True)
        
        self.stats_label = Label(self.top_frame, text="Errors: 0 | Speed: 0 WPM", 
                               font=("Arial", 14), bg="#f0f0f0")
        self.stats_label.pack(fill=X, expand=True)

    def setup_left_frame(self):
        button_configs = [
            ("Mode: Letters", "description_change_exercise", self.toggle_mode),
            ("Lang: EN", "description_change_language", self.toggle_language),
            ("Highlight: ON", "description_toggle_highlight", self.toggle_highlight)
        ]

        self.description_labels = []
        for btn_text, label_key, command in button_configs:
            label = Label(self.left_frame, text=self.translations[self.language][label_key], 
                         font=("Arial", 10), bg="#f0f0f0")
            label.pack(pady=(10, 0))
            self.description_labels.append(label)
            
            btn = Button(self.left_frame, text=btn_text, font=("Arial", 12),
                        width=14, command=command)
            btn.pack(pady=(0, 10))
            
            if btn_text.startswith("Mode"):
                self.mode_btn = btn
            elif btn_text.startswith("Lang"):
                self.lang_btn = btn
            else:
                self.hl_btn = btn

    def setup_center_frame(self):
        text_frame = Frame(self.center_frame, bg="#f0f0f0")
        text_frame.pack(fill=X, expand=True, padx=20, pady=0)

        self.display_label = Label(text_frame, text="", anchor="w",
                                  font=("Arial", 20, "bold"), fg="#aaaaaa", bg="#f0f0f0",
                                  wraplength=0, justify=LEFT)  # Will be set dynamically
        self.display_label.pack(fill=X, expand=True)

        input_frame = Frame(text_frame, bg="#f0f0f0")
        input_frame.pack(fill=BOTH, expand=True)

        self.input_text = Text(input_frame, font=("Arial", 20, "bold"),
                             fg="#000000", bg="#f0f0f0", borderwidth=0, highlightthickness=0,
                             insertbackground="#000000", height=3, wrap=WORD)
        self.input_text.pack(side=LEFT, fill=BOTH, expand=True)
        
        scrollbar = Scrollbar(input_frame, orient=VERTICAL, command=self.input_text.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.input_text.config(yscrollcommand=scrollbar.set)

        self.input_text.bind('<KeyRelease>', self.on_input_change)
        self.input_text.bind('<KeyPress>', self.on_key_press)
        self.input_text.bind('<Return>', self.handle_enter)
        self.input_text.bind('<FocusIn>', lambda e: self.input_text.mark_set("insert", "end"))
        
        self.root.bind('<Configure>', self.update_wraplength)

    def setup_bottom_frame(self):
        self.kb_frame = Frame(self.bottom_frame, bg="#f0f0f0")
        self.kb_frame.pack(expand=True)
        self.kb_keys = []
        self.draw_keyboard()

    def load_lines_from_file(self, filename, fallback=None):
        try:
            with open(filename, encoding='utf-8') as f:
                lines = [line.strip() for line in f if line.strip()]
            return lines if lines else fallback
        except Exception:
            return fallback

    def set_exercise(self):
        if self.mode == 'letters':
            letters = EN_LETTERS if self.language == 'EN' else RU_LETTERS
            random_letters = [random.choice(letters) for _ in range(20)]
            self.current_text = ' '.join(random_letters)
        elif self.mode == 'words':
            filename = 'en_words.txt' if self.language == 'EN' else 'ru_words.txt'
            words = self.load_lines_from_file(filename, [])
            if not words:
                letters = EN_LETTERS if self.language == 'EN' else RU_LETTERS
                random_letters = [random.choice(letters) for _ in range(20)]
                self.current_text = ' '.join(random_letters)
            else:
                selected_words = random.sample(words, min(15, len(words)))
                random.shuffle(selected_words)
                self.current_text = ' '.join(selected_words)
        else:
            filename = 'en_texts.txt' if self.language == 'EN' else 'ru_texts.txt'
            texts = self.load_lines_from_file(filename, [])
            if not texts:
                words = self.load_lines_from_file('en_words.txt' if self.language == 'EN' else 'ru_words.txt', [])
                if not words:
                    letters = EN_LETTERS if self.language == 'EN' else RU_LETTERS
                    random_letters = [random.choice(letters) for _ in range(20)]
                    self.current_text = ' '.join(random_letters)
                else:
                    selected_words = random.sample(words, min(15, len(words)))
                    random.shuffle(selected_words)
                    self.current_text = ' '.join(selected_words)
            else:
                self.current_text = random.choice(texts)
        self.update_display_label("")
        self.input_text.config(state=NORMAL)
        self.input_text.delete("1.0", "end")
        self.input_text.focus_set()
        self.mistakes = 0
        self.error_count = 0
        self.total_chars = 0
        self.last_checked_position = 0
        self.is_running = False
        self.time_left = 30
        self.update_stats()
        self.update_timer_label()
        self.draw_keyboard()

    def update_display_label(self, user_input):
        current_pos = len(user_input)

        remaining_text = self.current_text[current_pos:]

        if not remaining_text:
            self.display_label.config(text=self.translations[self.language]['press_enter'])
            return

        self.display_label.config(text=remaining_text)

        current_input = self.input_text.get("1.0", "end-1c")
        if len(current_input) > len(self.current_text):
            self.input_text.delete("1.0", "end")
            self.input_text.insert("1.0", current_input[:len(self.current_text)])

        self.input_text.see("end")

    def handle_enter(self, event):
        if not self.is_running:
            if self.input_text.cget('state') == 'disabled':
                self.final_stats = None
            self.set_exercise()
            self.display_label.config(text=self.current_text)
        return "break" 

    def on_input_change(self, event=None):
        if self.input_text.cget('state') == 'disabled':
            return

        user_input = self.input_text.get("1.0", "end-1c")
        self.update_display_label(user_input)

        if not self.is_running and user_input:
            self.is_running = True
            self.start_time = time.time()
            self.time_left = 30
            self.root.after(1000, self.update_timer)

        if len(user_input) > self.last_checked_position:
            for i in range(self.last_checked_position, len(user_input)):
                if i < len(self.current_text):
                    if user_input[i] != self.current_text[i] and user_input[i] != '\n':  # Ignore Enter key
                        self.error_count += 1
                else:
                    self.error_count += 1
            self.last_checked_position = len(user_input)
            self.mistakes = self.error_count

        self.total_chars = len(user_input.replace('\n', ''))

        if self.input_text.cget('state') != 'disabled':
            self.update_stats()
            self.highlight_keys(user_input)
        
        if user_input == self.current_text:
            self.is_running = False
            self.input_text.config(state=DISABLED)
            elapsed = time.time() - self.start_time
            if self.mode == 'letters':
                cpm = (self.total_chars / (elapsed / 60)) if elapsed > 0 else 0
                self.final_stats = f"{self.translations[self.language]['errors']}: {self.mistakes} | {self.translations[self.language]['speed']}: {cpm:.1f} CPM"
            else:
                wpm = (self.total_chars / 5) / (elapsed / 60) if elapsed > 0 else 0
                self.final_stats = f"{self.translations[self.language]['errors']}: {self.mistakes} | {self.translations[self.language]['speed']}: {wpm:.1f} WPM"
            self.update_stats(final=True)
            self.display_label.config(text=self.translations[self.language]['press_enter'])

    def update_timer_label(self):
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")

    def on_key_press(self, event):
        if self.input_text.cget('state') == 'disabled':
            return

        if not self.is_running:
            self.start_time = time.time()
            self.is_running = True
            self.time_left = 30
            self.root.after(1000, self.update_timer)
        input_text = self.input_text.get("1.0", "end-1c")
        self.total_chars = len(input_text)
        
        if self.input_text.cget('state') != 'disabled':
            self.update_stats()
            self.highlight_keys(input_text)
            
        if input_text == self.current_text:
            self.is_running = False
            self.input_text.config(state=DISABLED)

    def update_timer(self):
        if self.is_running and self.time_left > 0:
            self.time_left -= 1
            if self.input_text.cget('state') != 'disabled':
                self.update_stats()
            self.update_timer_label()
            self.root.after(1000, self.update_timer)
        elif self.time_left == 0:
            self.is_running = False
            self.input_text.config(state=DISABLED)
            self.update_timer_label()
            elapsed = time.time() - self.start_time
            if self.mode == 'letters':
                cpm = (self.total_chars / (elapsed / 60)) if elapsed > 0 else 0
                self.final_stats = f"{self.translations[self.language]['errors']}: {self.mistakes} | {self.translations[self.language]['speed']}: {cpm:.1f} CPM"
            else:
                wpm = (self.total_chars / 5) / (elapsed / 60) if elapsed > 0 else 0
                self.final_stats = f"{self.translations[self.language]['errors']}: {self.mistakes} | {self.translations[self.language]['speed']}: {wpm:.1f} WPM"
            self.update_stats(final=True)
            self.display_label.config(text=f"{self.translations[self.language]['time_up']}\n{self.translations[self.language]['press_enter_new']}")
            self.input_text.delete("1.0", "end")

    def update_stats(self, final=False):
        if self.input_text.cget('state') == 'disabled':
            if self.final_stats is not None:
                self.stats_label.config(text=self.final_stats)
            return

        if final and self.final_stats is not None:
            self.stats_label.config(text=self.final_stats)
            return

        elapsed = time.time() - self.start_time if self.is_running else 1
        if self.mode == 'letters':
            cpm = (self.total_chars / (elapsed / 60)) if elapsed > 0 else 0
            stats_text = f"{self.translations[self.language]['errors']}: {self.mistakes} | {self.translations[self.language]['speed']}: {cpm:.1f} CPM"
        else:
            wpm = (self.total_chars / 5) / (elapsed / 60) if elapsed > 0 else 0
            stats_text = f"{self.translations[self.language]['errors']}: {self.mistakes} | {self.translations[self.language]['speed']}: {wpm:.1f} WPM"
        
        if not final:
            self.stats_label.config(text=stats_text)
        else:
            self.final_stats = stats_text
            self.stats_label.config(text=stats_text)
            self.error_count = self.mistakes

    def highlight_keys(self, input_text):
        if not self.highlight:
            for btn in self.kb_keys:
                btn.config(bg="white")
            return

        layout = sum(self.get_keyboard_layout(), [])
        for btn in self.kb_keys:
            btn.config(bg="white")

        if input_text:
            last_char = input_text[-1]
            expected_char = self.current_text[len(input_text)-1] if len(input_text) <= len(self.current_text) else last_char
            
            physical_key = None
            if self.language == 'EN':
                if last_char in self.ru_positions:
                    physical_key = self.ru_positions[last_char]
                else:
                    physical_key = last_char
            else:
                if last_char in self.keyboard_positions:
                    physical_key = self.keyboard_positions[last_char]
                else:
                    physical_key = last_char

            correct = last_char == expected_char

            for btn, key in zip(self.kb_keys, layout):
                if key == physical_key:
                    btn.config(bg="#90ee90" if correct else "#ff6961")

    def toggle_mode(self):
        modes = ['letters', 'words', 'texts']
        idx = modes.index(self.mode)
        self.mode = modes[(idx + 1) % len(modes)]
        self.update_interface_language()
        self.set_exercise()

    def toggle_language(self):
        self.language = 'RU' if self.language == 'EN' else 'EN'
        self.update_interface_language()
        self.set_exercise()

    def toggle_highlight(self):
        self.highlight = not self.highlight
        self.update_interface_language()
        self.draw_keyboard()

    def draw_keyboard(self):
        for widget in self.kb_frame.winfo_children():
            widget.destroy()
        layout = self.get_keyboard_layout()
        self.kb_keys = []
        for row in layout:
            row_frame = Frame(self.kb_frame, bg="#f0f0f0")
            row_frame.pack()
            for key in row:
                btn = Label(row_frame, text=key, width=3, height=2, font=("Arial", 12), relief="ridge", bg="white")
                btn.pack(side=LEFT, padx=2, pady=2)
                self.kb_keys.append(btn)

    def get_keyboard_layout(self):
        if self.language == 'EN':
            return [
                list("qwertyuiop"),
                list("asdfghjkl"),
                list("zxcvbnm"),
                [" "]
            ]
        else:
            return [
                list("йцукенгшщзхъ"),
                list("фывапролджэ"),
                list("ячсмитьбю"),
                [" "]
            ]

    def center_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        x = (screen_width - self.MIN_WIDTH) // 2
        y = (screen_height - self.MIN_HEIGHT) // 2
        
        self.root.geometry(f"+{x}+{y}")

    def on_window_resize(self, event=None):
        if event and event.widget != self.root:
            return

        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()

        if window_width < self.MIN_WIDTH:
            self.root.geometry(f"{self.MIN_WIDTH}x{window_height}")
            window_width = self.MIN_WIDTH
        elif window_width > self.MAX_WIDTH:
            self.root.geometry(f"{self.MAX_WIDTH}x{window_height}")
            window_width = self.MAX_WIDTH

        if window_height < self.MIN_HEIGHT:
            self.root.geometry(f"{window_width}x{self.MIN_HEIGHT}")
            window_height = self.MIN_HEIGHT
        elif window_height > self.MAX_HEIGHT:
            self.root.geometry(f"{window_width}x{self.MAX_HEIGHT}")
            window_height = self.MAX_HEIGHT

        base_size = min(window_width // 60, window_height // 30)
        text_size = max(16, min(24, base_size))
        button_size = max(12, min(18, base_size - 2))
        
        self.stats_label.config(font=("Arial", text_size))
        self.timer_label.config(font=("Arial", text_size, "bold"))
        self.display_label.config(font=("Arial", text_size, "bold"))
        
        for btn in [self.mode_btn, self.lang_btn, self.hl_btn]:
            btn.config(font=("Arial", button_size))
            
        kb_key_size = max(10, min(16, base_size - 4))
        for key in self.kb_keys:
            key.config(font=("Arial", kb_key_size))

        text_height = max(2, min(4, window_height // 200))
        self.display_label.config(height=text_height)

    def update_interface_language(self):
        self.root.title(self.translations[self.language]['title'])
        
        mode_text = self.translations[self.language][f'mode_{self.mode}']
        self.mode_btn.config(text=mode_text)
        
        lang_text = self.translations[self.language][f'lang_{self.language.lower()}']
        self.lang_btn.config(text=lang_text)
        
        highlight_text = self.translations[self.language]['highlight_on' if self.highlight else 'highlight_off']
        self.hl_btn.config(text=highlight_text)
        
        self.description_labels[0].config(text=self.translations[self.language]['description_change_exercise'])
        self.description_labels[1].config(text=self.translations[self.language]['description_change_language'])
        self.description_labels[2].config(text=self.translations[self.language]['description_toggle_highlight'])
        
        if not self.is_running and self.input_text.cget('state') == 'disabled':
            self.update_stats(final=True)
            self.display_label.config(text=self.translations[self.language]['press_enter'])
        else:
            self.update_stats()

    def update_wraplength(self, event=None):
        if event and event.widget != self.root:
            return
        display_width = self.display_label.winfo_width()
        self.display_label.config(wraplength=display_width)        
        self.input_text.config(width=display_width // 12) 

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MainActivity()
    app.run()
