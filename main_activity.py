from tkinter import *
from tkinter import ttk
import time
import random

# --- Data for letter mode (arrays) ---
EN_LETTERS = list("abcdefghijklmnopqrstuvwxyz")
RU_LETTERS = list("йцукенгшщзхъфывапролджэячсмитьбю")

# --- Placeholder for loading phrases/texts from files ---
EN_PHRASES = ["hello world", "type fast"]
RU_PHRASES = ["привет мир", "быстро печатай"]
EN_TEXTS = ["The quick brown fox jumps over the lazy dog."]
RU_TEXTS = ["Съешь ещё этих мягких французских булок, да выпей чаю."]

class MainActivity:
    def __init__(self):
        self.root = Tk()
        self.root.title("Keyboard Trainer")
        self.root.geometry("1000x600")
        self.root.configure(bg="#f0f0f0")

        # State
        self.language = 'EN'  # or 'RU'
        self.mode = 'letters'  # or 'phrases', 'texts'
        self.highlight = True
        self.time_left = 60
        self.mistakes = 0
        self.total_chars = 0
        self.is_running = False
        self.current_text = ''

        self.init_styles()
        self.init_gui()
        self.set_exercise()

    def init_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("NoBorder.TEntry",
                       fieldbackground="#f0f0f0",
                       borderwidth=0,
                       relief="flat",
                       padding=5,
                       font=("Arial", 16))

    def init_gui(self):
        # --- Top: Stats and Timer ---
        stats_frame = Frame(self.root, bg="#f0f0f0")
        stats_frame.pack(pady=10)
        self.stats_label = Label(stats_frame, text="Errors: 0 | Speed: 0 WPM", font=("Arial", 14), bg="#f0f0f0")
        self.stats_label.pack(side=LEFT, padx=10)
        self.timer_label = Label(stats_frame, text="01:00", font=("Arial", 14, "bold"), bg="#f0f0f0", fg="black")
        self.timer_label.pack(side=LEFT, padx=10)

        # --- Center: Required text and input ---
        center_frame = Frame(self.root, bg="#f0f0f0")
        center_frame.pack(pady=10)
        self.text_display = Text(center_frame, height=2, width=60, wrap=WORD, font=("Arial", 16), bg="#f0f0f0", borderwidth=0, highlightthickness=0, state=DISABLED)
        self.text_display.pack()
        self.input_entry = ttk.Entry(center_frame, style="NoBorder.TEntry", width=60, font=("Arial", 16))
        self.input_entry.pack(pady=5)
        self.input_entry.bind('<Key>', self.on_key_press)
        underline = Canvas(center_frame, height=2, bg="#f0f0f0", highlightthickness=0)
        underline.pack(fill=X)
        underline.create_line(0, 0, 600, 0, fill="black", width=2)
        self.next_btn = Button(center_frame, text="Next Exercise", font=("Arial", 12), command=self.set_exercise)
        self.next_btn.pack(pady=10)
        self.next_btn.pack_forget()

        # --- Left: Buttons with labels ---
        left_frame = Frame(self.root, bg="#f0f0f0")
        left_frame.place(x=20, y=120)
        self.mode_btn = Button(left_frame, text="Mode: Letters", font=("Arial", 12), width=14, command=self.toggle_mode)
        self.mode_btn.pack(pady=10)
        Label(left_frame, text="Change Exercise", font=("Arial", 10), bg="#f0f0f0").pack()
        self.lang_btn = Button(left_frame, text="Lang: EN", font=("Arial", 12), width=14, command=self.toggle_language)
        self.lang_btn.pack(pady=10)
        Label(left_frame, text="Change Language", font=("Arial", 10), bg="#f0f0f0").pack()
        self.hl_btn = Button(left_frame, text="Highlight: ON", font=("Arial", 12), width=14, command=self.toggle_highlight)
        self.hl_btn.pack(pady=10)
        Label(left_frame, text="Toggle Highlight", font=("Arial", 10), bg="#f0f0f0").pack()

        # --- Bottom: Virtual Keyboard ---
        kb_frame = Frame(self.root, bg="#f0f0f0")
        kb_frame.pack(side=BOTTOM, pady=20)
        self.kb_keys = []
        self.kb_frame = kb_frame
        self.draw_keyboard()

    def load_lines_from_file(self, filename, fallback):
        try:
            with open(filename, encoding='utf-8') as f:
                lines = [line.strip() for line in f if line.strip()]
            return lines if lines else fallback
        except Exception:
            return fallback

    def set_exercise(self):
        if self.mode == 'letters':
            self.current_text = random.choice(EN_LETTERS if self.language == 'EN' else RU_LETTERS)
        elif self.mode == 'phrases':
            if self.language == 'EN':
                phrases = self.load_lines_from_file('en_phrases.txt', EN_PHRASES)
            else:
                phrases = self.load_lines_from_file('ru_phrases.txt', RU_PHRASES)
            self.current_text = random.choice(phrases)
        else:
            if self.language == 'EN':
                texts = self.load_lines_from_file('en_texts.txt', EN_TEXTS)
            else:
                texts = self.load_lines_from_file('ru_texts.txt', RU_TEXTS)
            self.current_text = random.choice(texts)
        self.text_display.config(state=NORMAL)
        self.text_display.delete('1.0', END)
        self.text_display.insert(END, self.current_text)
        self.text_display.config(state=DISABLED)
        self.input_entry.config(state=NORMAL)
        self.input_entry.delete(0, END)
        self.input_entry.focus_set()
        self.mistakes = 0
        self.total_chars = 0
        self.is_running = False
        self.time_left = 60
        self.next_btn.pack_forget()
        self.update_stats()
        self.update_timer_label()
        self.draw_keyboard()

    def update_timer_label(self):
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")

    def on_key_press(self, event):
        if not self.is_running:
            self.start_time = time.time()
            self.is_running = True
            self.time_left = 60
            self.root.after(1000, self.update_timer)
        input_text = self.input_entry.get()
        compare_len = min(len(input_text), len(self.current_text))
        self.mistakes = 0
        for i in range(compare_len):
            if input_text[i] != self.current_text[i]:
                self.mistakes += 1
        self.total_chars = len(input_text)
        self.update_stats()
        self.highlight_keys(input_text)
        if input_text == self.current_text:
            self.is_running = False
            self.input_entry.config(state=DISABLED)
            self.next_btn.pack(pady=10)

    def update_timer(self):
        if self.is_running and self.time_left > 0:
            self.time_left -= 1
            self.update_stats()
            self.update_timer_label()
            self.root.after(1000, self.update_timer)
        elif self.time_left == 0:
            self.is_running = False
            self.input_entry.config(state=DISABLED)
            self.next_btn.pack(pady=10)
            self.update_stats(final=True)
            self.update_timer_label()

    def update_stats(self, final=False):
        elapsed = 60 - self.time_left if self.is_running or final else 1
        wpm = (self.total_chars / 5) / (elapsed / 60) if elapsed > 0 else 0
        self.stats_label.config(text=f"Errors: {self.mistakes} | Speed: {wpm:.1f} WPM")

    def highlight_keys(self, input_text):
        if not self.highlight:
            for btn in self.kb_keys:
                btn.config(bg="white")
            return
        layout = sum(self.get_keyboard_layout(), [])
        # Highlight last typed key
        for btn, key in zip(self.kb_keys, layout):
            btn.config(bg="white")
        if input_text:
            last_char = input_text[-1]
            correct = len(input_text) <= len(self.current_text) and \
                      last_char == self.current_text[len(input_text)-1]
            for btn, key in zip(self.kb_keys, layout):
                if key == last_char.lower():
                    btn.config(bg="#90ee90" if correct else "#ff6961")

    def toggle_mode(self):
        modes = ['letters', 'phrases', 'texts']
        mode_names = {'letters': 'Letters', 'phrases': 'Phrases', 'texts': 'Texts'}
        idx = modes.index(self.mode)
        self.mode = modes[(idx + 1) % len(modes)]
        self.mode_btn.config(text=f"Mode: {mode_names[self.mode]}")
        self.set_exercise()

    def toggle_language(self):
        self.language = 'RU' if self.language == 'EN' else 'EN'
        self.lang_btn.config(text=f"Lang: {self.language}")
        self.set_exercise()

    def toggle_highlight(self):
        self.highlight = not self.highlight
        self.hl_btn.config(text=f"Highlight: {'ON' if self.highlight else 'OFF'}")
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

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MainActivity()
    app.run()
