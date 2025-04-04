from tkinter import *
from tkinter import ttk


class MainActivity:
    def __init__(self):
        self.root = Tk()
        self.root.title("Праздник Ураза-Байрам | Ахмат Сила")
        self.root.geometry("1250x600")
        self.root.configure(bg="#f0f0f0")  # Светлый фон

        self.time_left = 30  # 30 секунд
        self.init_styles()
        self.init_gui()
        self.update_timer()  # Запуск таймера

    def init_styles(self):
        """Настройка стилей для полей ввода без границ"""
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("NoBorder.TEntry",
                        fieldbackground="#f0f0f0",
                        borderwidth=0,
                        relief="flat",
                        padding=5,
                        font=("Arial", 14))

    def create_entry_with_underline(self, parent, entry_width, line_width):
        """Создание поля ввода с подчеркиванием"""
        frame = Frame(parent, bg="#f0f0f0")
        frame.pack(pady=10)

        entry = ttk.Entry(frame, style="NoBorder.TEntry", width=entry_width, justify="center")
        entry.pack()

        underline = Canvas(frame, height=2, bg="#f0f0f0", highlightthickness=0)
        underline.pack(fill=X)
        underline.create_line(0, 0, line_width, 0, fill="black", width=2)  # ЧЕРНАЯ полоска

        return entry

    def create_circle_button(self, parent, text):
        """Создание кнопки в кружке"""
        frame = Frame(parent, bg="#f0f0f0")
        frame.pack()

        btn = Button(frame, text=text, bg="white", fg="black",
                     font=("Arial", 12, "bold"), borderwidth=2, relief="solid",
                     width=3, height=1)
        btn.pack(pady=5)

    def update_timer(self):
        """Обновление таймера каждую секунду"""
        if self.time_left > 0:
            self.timer_label.config(text=f"00:{self.time_left:02d}")  # Формат 00:30, 00:29 и т. д.
            self.time_left -= 1
            self.root.after(1000, self.update_timer)  # Запуск через 1 секунду
        else:
            self.timer_label.config(text="00:00")  # Когда время кончилось

    def init_gui(self):
        """Создание графического интерфейса"""

        # Таймер сверху
        timer_frame = Frame(self.root, bg="#f0f0f0")
        timer_frame.pack(pady=10)
        self.timer_label = Label(timer_frame, text="30:00", font=("Arial", 16, "bold"), bg="#f0f0f0", fg="black")
        self.timer_label.pack()

        # Размещение полей по центру
        center_frame = Frame(self.root, bg="#f0f0f0")
        center_frame.pack(expand=True)

        self.entry1 = self.create_entry_with_underline(center_frame, entry_width=30, line_width=200)
        self.entry2 = self.create_entry_with_underline(center_frame, entry_width=50, line_width=400)

        # Кнопки в кружках сбоку
        left_frame = Frame(self.root, bg="#f0f0f0")
        left_frame.place(x=20, y=150)  # Размещаем слева

        self.create_circle_button(left_frame, "3")
        self.create_circle_button(left_frame, "4")
        self.create_circle_button(left_frame, "5")

        # Цифра сверху
        top_frame = Frame(self.root, bg="#f0f0f0")
        top_frame.pack(pady=10)

        Label(top_frame, text="1", font=("Arial", 14, "bold"), bg="#f0f0f0").pack()

        line1 = Canvas(top_frame, width=100, height=2, bg="#f0f0f0", highlightthickness=0)
        line1.pack()
        line1.create_line(0, 0, 100, 0, fill="black", width=2)

        # Линия под первой
        line2 = Canvas(self.root, width=500, height=2, bg="#f0f0f0", highlightthickness=0)
        line2.pack()
        line2.create_line(0, 0, 500, 0, fill="black", width=2)

    def run(self):
        """Запуск главного цикла приложения"""
        self.root.mainloop()


# Запуск приложения
if __name__ == "__main__":
    app = MainActivity()
    app.run()
