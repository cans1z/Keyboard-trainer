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
        
        # Set minimum and maximum window sizes
        self.MIN_WIDTH = 800
        self.MIN_HEIGHT = 600
        self.MAX_WIDTH = 1600
        self.MAX_HEIGHT = 900
        
        # Keyboard layout mapping based on physical position
        self.keyboard_positions = {
            # First row
            'q': 'й', 'w': 'ц', 'e': 'у', 'r': 'к', 't': 'е', 'y': 'н', 'u': 'г', 'i': 'ш', 'o': 'щ', 'p': 'з', '[': 'х', ']': 'ъ',
            # Second row
            'a': 'ф', 's': 'ы', 'd': 'в', 'f': 'а', 'g': 'п', 'h': 'р', 'j': 'о', 'k': 'л', 'l': 'д', ';': 'ж', "'": 'э',
            # Third row
            'z': 'я', 'x': 'ч', 'c': 'с', 'v': 'м', 'b': 'и', 'n': 'т', 'm': 'ь', ',': 'б', '.': 'ю'
        }
        self.ru_positions = {v: k for k, v in self.keyboard_positions.items()}
        
        # Set initial size and position window in center of screen
        self.root.geometry(f"{self.MIN_WIDTH}x{self.MIN_HEIGHT}")
        self.center_window()
        
        # Configure size restrictions
        self.root.minsize(self.MIN_WIDTH, self.MIN_HEIGHT)
        self.root.maxsize(self.MAX_WIDTH, self.MAX_HEIGHT)
        
        self.root.configure(bg="#f0f0f0")
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # State
        self.language = 'EN'
        self.mode = 'letters'
        self.highlight = True
        self.time_left = 60
        self.mistakes = 0
        self.total_chars = 0
        self.is_running = False
        self.current_text = ''

        self.init_styles()
        self.init_gui()
        self.set_exercise()
        
        # Bind resize event
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
        # Create main frames with grid
        self.top_frame = Frame(self.root, bg="#f0f0f0")
        self.left_frame = Frame(self.root, bg="#f0f0f0")
        self.center_frame = Frame(self.root, bg="#f0f0f0")
        self.bottom_frame = Frame(self.root, bg="#f0f0f0")

        # Grid layout for main frames
        self.top_frame.grid(row=0, column=0, columnspan=3, sticky="ew", pady=5)
        self.left_frame.grid(row=1, column=0, sticky="ns", padx=10)
        self.center_frame.grid(row=1, column=1, sticky="nsew")
        self.bottom_frame.grid(row=2, column=0, columnspan=3, sticky="ew", pady=10)

        self.setup_top_frame()
        self.setup_left_frame()
        self.setup_center_frame()
        self.setup_bottom_frame()

    def setup_top_frame(self):
        # Stats and Timer with pack
        self.stats_label = Label(self.top_frame, text="Errors: 0 | Speed: 0 WPM", 
                               font=("Arial", 14), bg="#f0f0f0")
        self.timer_label = Label(self.top_frame, text="01:00", 
                               font=("Arial", 14, "bold"), bg="#f0f0f0", fg="black")
        
        self.stats_label.pack(side=LEFT, padx=10, expand=True)
        self.timer_label.pack(side=LEFT, padx=10)

    def setup_left_frame(self):
        # Control buttons with pack
        button_configs = [
            ("Mode: Letters", "Change Exercise", self.toggle_mode),
            ("Lang: EN", "Change Language", self.toggle_language),
            ("Highlight: ON", "Toggle Highlight", self.toggle_highlight)
        ]

        for btn_text, label_text, command in button_configs:
            btn = Button(self.left_frame, text=btn_text, font=("Arial", 12),
                        width=14, command=command)
            btn.pack(pady=5)
            if btn_text.startswith("Mode"):
                self.mode_btn = btn
            elif btn_text.startswith("Lang"):
                self.lang_btn = btn
            else:
                self.hl_btn = btn
            
            Label(self.left_frame, text=label_text, 
                  font=("Arial", 10), bg="#f0f0f0").pack(pady=(0, 10))

    def setup_center_frame(self):
        # Create a frame to hold the text display
        text_frame = Frame(self.center_frame, bg="#f0f0f0")
        text_frame.pack(fill=X, expand=True, padx=20, pady=0)

        # Create display label (dimmed text)
        self.display_label = Label(text_frame, text="", anchor="w",
                                  font=("Arial", 20, "bold"), fg="#aaaaaa", bg="#f0f0f0")
        self.display_label.pack(fill=X, expand=True)

        # Create input text widget (user types here)
        self.input_text = Text(text_frame, font=("Arial", 20, "bold"),
                             fg="#000000", bg="#f0f0f0", borderwidth=0, highlightthickness=0,
                             insertbackground="#000000", height=1)
        self.input_text.pack(fill=X, expand=True)
        self.input_text.bind('<KeyRelease>', self.on_input_change)
        self.input_text.bind('<FocusIn>', lambda e: self.input_text.mark_set("insert", "end"))

        # Underline
        self.underline = Canvas(self.center_frame, height=2, bg="#f0f0f0",
                              highlightthickness=0)
        self.underline.pack(fill=X)
        self.underline.create_line(0, 0, 1000, 0, fill="black", width=2,
                                 tags="underline")

        # Next button
        self.next_btn = Button(self.center_frame, text="Next Exercise",
                              font=("Arial", 12), command=self.set_exercise)
        self.next_btn.pack(pady=10)
        self.next_btn.pack_forget()

    def setup_bottom_frame(self):
        # Keyboard frame with pack
        self.kb_frame = Frame(self.bottom_frame, bg="#f0f0f0")
        self.kb_frame.pack(expand=True)
        self.kb_keys = []
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
            letters = EN_LETTERS if self.language == 'EN' else RU_LETTERS
            random_letters = [random.choice(letters) for _ in range(20)]
            self.current_text = ' '.join(random_letters)
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
        self.update_display_label("")
        self.input_text.config(state=NORMAL)
        self.input_text.delete("1.0", "end")
        self.input_text.focus_set()
        self.mistakes = 0
        self.total_chars = 0
        self.is_running = False
        self.time_left = 30
        self.next_btn.pack_forget()
        self.update_stats()
        self.update_timer_label()
        self.draw_keyboard()

    def update_display_label(self, user_input):
        # Show the current_text, but erase chars that have been typed correctly
        display_chars = list(self.current_text)
        for i, c in enumerate(user_input):
            if i < len(display_chars) and c == display_chars[i]:
                display_chars[i] = " "  # Erase correct char
        display_str = "".join(display_chars)
        self.display_label.config(text=display_str)
        
        # Update input field to match display text length
        current_input = self.input_text.get("1.0", "end-1c")
        if len(current_input) > len(self.current_text):
            self.input_text.delete("1.0", "end")
            self.input_text.insert("1.0", current_input[:len(self.current_text)])

    def on_input_change(self, event=None):
        user_input = self.input_text.get("1.0", "end-1c")
        self.update_display_label(user_input)
        
        # Start timer on first input if not running
        if not self.is_running and user_input:
            self.is_running = True
            self.start_time = time.time()
            self.time_left = 30
            self.root.after(1000, self.update_timer)
        
        # Only check for new mistakes in the newly typed character
        if len(user_input) > self.total_chars:
            if user_input[-1] != self.current_text[len(user_input)-1]:
                self.mistakes += 1
        
        self.total_chars = len(user_input)
        self.update_stats()
        self.highlight_keys(user_input)
        
        # Stop timer and disable input when text is completed
        if user_input == self.current_text:
            self.is_running = False
            self.input_text.config(state=DISABLED)
            self.next_btn.pack(pady=10)
            self.update_stats(final=True)

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
        input_text = self.input_text.get("1.0", "end-1c")
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
            self.input_text.config(state=DISABLED)
            self.next_btn.pack(pady=10)

    def update_timer(self):
        if self.is_running and self.time_left > 0:
            self.time_left -= 1
            self.update_stats()
            self.update_timer_label()
            self.root.after(1000, self.update_timer)
        elif self.time_left == 0:
            self.is_running = False
            self.input_text.config(state=DISABLED)
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
        # Reset all keys to white
        for btn in self.kb_keys:
            btn.config(bg="white")

        if input_text:
            last_char = input_text[-1]
            # Get the expected character from the current text
            expected_char = self.current_text[len(input_text)-1] if len(input_text) <= len(self.current_text) else last_char
            
            # Get the physical key position
            physical_key = None
            if self.language == 'EN':
                # If we're typing in English but text is in Russian
                if last_char in self.ru_positions:
                    physical_key = self.ru_positions[last_char]
                else:
                    physical_key = last_char
            else:
                # If we're typing in Russian but text is in English
                if last_char in self.keyboard_positions:
                    physical_key = self.keyboard_positions[last_char]
                else:
                    physical_key = last_char

            # Check if the typed character matches the expected character
            correct = last_char == expected_char

            # Highlight the key at the physical position
            for btn, key in zip(self.kb_keys, layout):
                if key == physical_key:
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

    def center_window(self):
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calculate position coordinates
        x = (screen_width - self.MIN_WIDTH) // 2
        y = (screen_height - self.MIN_HEIGHT) // 2
        
        # Set window position
        self.root.geometry(f"+{x}+{y}")

    def on_window_resize(self, event=None):
        # Only handle window resize events and enforce size limits
        if event and event.widget != self.root:
            return

        # Get window dimensions
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()

        # Enforce size limits
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

        # Scale fonts based on window size
        base_size = min(window_width // 60, window_height // 30)
        text_size = max(16, min(24, base_size))
        button_size = max(12, min(18, base_size - 2))
        
        # Update font sizes
        self.stats_label.config(font=("Arial", text_size))
        self.timer_label.config(font=("Arial", text_size, "bold"))
        self.display_label.config(font=("Arial", text_size, "bold"))
        
        # Update button fonts
        for btn in [self.mode_btn, self.lang_btn, self.hl_btn]:
            btn.config(font=("Arial", button_size))
            
        # Scale keyboard
        kb_key_size = max(10, min(16, base_size - 4))
        for key in self.kb_keys:
            key.config(font=("Arial", kb_key_size))
            
        # Update the underline
        self.underline.delete("underline")
        self.underline.create_line(0, 0, window_width, 0, 
                                 fill="black", width=2, tags="underline")

        # Adjust text display height based on window height
        text_height = max(2, min(4, window_height // 200))
        self.display_label.config(height=text_height)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MainActivity()
    app.run()
