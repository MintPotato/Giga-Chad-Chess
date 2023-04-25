import tkinter as tk
import tkinter.ttk as ttk
from MyErrors import EmptyNLK
import Game, CoordsVvod


def write_coords(coords: str):
    '''
    Функция записывающая полученную строку в файл "input.txt"

    Параметры:
        coords: str
             Строка состоящая из значений N, L, K (+ координат фигур)
    '''

    with open('input.txt', 'w') as f:
        f.write(coords)

class NLKWindow(tk.Tk):
    """
    Класс в котором реализуется создание окна с вводом значений:
        n - размерность доски

        l - количество фигур дл подстановки

        k - количество уже стоящих фигур (не под боем)
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

        # Инициализация фрейма для записи значения K
        self.frame_k = ttk.Frame(self, padding=[8, 5])
        self.frame_k.pack()
        self.label_k = ttk.Label(self.frame_k, text='Введите K').pack()
        self.entry_k = ttk.Entry(self.frame_k, validate='key', validatecommand=vcmd_lk)
        self.entry_k.pack()

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
        # Проверка о том, что во всех полях присутсвуют значения
        # try:
        #
        #     # Значения полей (обрезать пробелы по бокам не обязательно, однако сделано для красоты записи в файл)
        #     n, l, k = self.entry_n.get().strip(), self.entry_l.get().strip(), self.entry_k.get().strip()
        #
        #     # Первая строка файла 'input.txt'
        #     nlk = '{} {} {}'.format(n, l, k)
        #
        #     write_coords(nlk)
        #     if k == '0':  # Если вводить координаты не нужно, записываем данные в 'input.txt' и закрываем окно
        #         self.quit()
        #
        #     else:  # Иначе открываем окно для записи координат
        #         CoordsVvod.InputWindow()
        # except :
        #     # Закрываем окно и открываем новое для повторной попытки записи значений
        #     self.destroy()
        #     NLKWindow()
        #     Game.Game().error_occured(EmptyNLK, 'Как минимум одно из полей для ввода значений является пустым')
        n, l, k = self.entry_n.get().strip(), self.entry_l.get().strip(), self.entry_k.get().strip()

        if not n or not l or not k:
            self.destroy()
            NLKWindow()
            Game.Game().error_occured(EmptyNLK, 'Как минимум одно из полей для ввода значений является пустым')
        else:
            nlk = '{} {} {}'.format(n, l, k)
            write_coords(nlk)

            if k == '0':  # Если вводить координаты не нужно, записываем данные в 'input.txt' и закрываем окно
                self.destroy()
            else:
                self.destroy()
                CoordsVvod.InputWindow()




