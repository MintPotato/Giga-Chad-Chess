import tkinter as tk
import tkinter.ttk as ttk
from MyErrors import EmptyNLK
import Game, CoordsVvod


class NLWindow(tk.Tk):
    """
    Класс в котором реализуется создание окна с вводом значений:
        n - размерность доски

        l - количество фигур дл подстановки
    """

    def __init__(self):
        '''
        Инициализация параметров окна и его объектов
        '''
        super().__init__()
        self.geometry('150x200')
        self.resizable(False, False)

        # Создание команд валидации для записи значени N, L, K
        vcmd_n = (self.register(self.is_valid_n), '%P')
        vcmd_lk = (self.register(self.is_valid), '%P')

        # Инициализация фрейма для записи значения N
        self.frame_n = ttk.Frame(self, padding=[8, 5])
        self.frame_n.pack()
        self.label_n = ttk.Label(self.frame_n, text='Введите N').pack()
        self.entry_n = ttk.Entry(self.frame_n, validate='key', validatecommand=vcmd_n)
        self.entry_n.pack()

        # Инициализация фрейма для записи значения L
        self.frame_l = ttk.Frame(self, padding=[8, 5])
        self.frame_l.pack()
        self.label_l = ttk.Label(self.frame_l, text='Введите L').pack()
        self.entry_l = ttk.Entry(self.frame_l, validate='key', validatecommand=vcmd_lk)
        self.entry_l.pack()

        # Инициализация кнопки перехода к окну записи координат
        self.frame_btn = ttk.Frame(self, padding=[8, 6])
        self.frame_btn.pack()
        self.btn = ttk.Button(self.frame_btn, text='Далее', command=self.open_input_window).pack()

    def is_valid_n(self, string: str) -> bool:
        '''
        Функция валидации поля ввода значения N

        Параметры:
            string: str
                Строка из поля ввода значения N
        '''

        # Нужна для возможности удалять первый написаный элемент
        if string == '':
            return True

        try:
            # Проверка на то что введено число
            string = int(string)
            if string > 20:  # Если введенная размерность не превышает максимально допустимую (0-19)
                return False
            else:
                return True

        except:
            return False

    def is_valid(self, string: str) -> bool:
        '''
        Функция валидации поля ввода значения L и K

        Параметры:
            string: str
                Строка из поля ввода значения N или K
        '''

        # Нужна для возможности удалять первый написаный элемент
        if string == '':
            return True

        try:

            # Проверка на то что введено число
            string = int(string)
            return True
        except:
            return False

    def open_input_window(self):
        '''
        Функция кнопки вызывающая окно ввода координат если введенное K отлично от 0,
        или вызывающая функцию записи координат в файл
        '''

        # Получение значений полей ввода
        n, l = self.entry_n.get().strip(), self.entry_l.get().strip()


        # Проверка на то, что ни одно поле ввода не было пустым
        if not n or not l:
            self.destroy()
            NLWindow()
            Game.Game().error_occured(EmptyNLK, 'Как минимум одно из полей для ввода значений является пустым')
        else:
            nl = '{} {}'.format(n, l) # Строка значений для файла "input.txt"

            with open('input.txt', 'w') as f: # Запись вводных данных в файл
                f.write(nl)

            self.destroy()
            CoordsVvod.InputWindow()
