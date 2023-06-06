import pygame
import Figures


class InputWindow:
    '''
    Класс окна с постановкой фигур пользователя на доску
    '''

    def __init__(self):
        '''
        Инициализация окна с интерактивной доской для ввода координат K фигур
        '''
        with open('input.txt', 'r') as f:
            NL = tuple(f)[0]

        # Объявление необходимых переменных
        self.output = NL  # Строка содержащая вводные данные и координаты фигур поставленных пользователем
        N = int(NL.split()[0])# Размерность доски

        cell_size = 400 // N  # Размер одной лкетки поля
        board_size = cell_size * N  # Размер доски
        self.N = N  # Размерность доски
        self.board = [[0 for _ in range(N)] for _ in range(N)]  # Матрица доски
        self.placed = 0  # Количество поставленных фигур
        self.buttons: list['Buttons'] = []  # Список содержащий клеки доски в виде экземпляров класса Button

        # Инициализация доски и кнопки подтверждения
        pygame.init()

        self.display = pygame.display.set_mode((board_size + 1, board_size + 100))
        self.display.fill('white')
        pygame.draw.rect(self.display, 'black', (0, 0, board_size + 1, board_size + 1))
        pygame.display.flip()

        # Создание интерактивной доски в виде кнопок
        for lines in range(N):
            for rows in range(N):
                self.buttons += [
                    Buttons(self.display, cell_size * lines + 1, cell_size * rows + 1, cell_size, cell_size,
                            onClickFunc=self.place_figure)]

        # Кнопка завершения ввода координат
        self.buttons += [
            Buttons(self.display, 40, board_size + 20, 200, 50, text='Записать вводные данные', color='gray',
                    onClickFunc=self.close)]

        self.run = True
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            for button in self.buttons:  # Проверка взаимодействия пользователя с кнопками
                button.running()

            pygame.display.update()

    def close(self, *args): # Костыль в виде *args, надо подумать над решением
        '''
        Функция завершающая работу окна
        '''

        # Запись полученных координат и вводных данных в файл
        with open('input.txt', 'w') as f:
            self.output = self.output + f' {self.count_figures()}\n'
            self.add_coords()  # Считывание координат введеных пользователем
            f.write(self.output)

        # Завершение работы окна
        self.run = False
        pygame.quit()


    def count_figures(self):
        '''
        Функция считающая количество поставленных пользователем фигур
        '''
        f_count = 0
        for i in range(self.N):
            for j in range(self.N):
                if self.board[i][j] < 0: # Если в этих координатах стоит фигура, то увеличивает счетчик
                    f_count += 1

        return f_count

    def add_coords(self):
        '''
        Добавляет введенные пользователем координаты к уже существующей строке NLK
        '''
        for i in range(self.N):
            for j in range(self.N):
                if self.board[i][j] < 0:
                    self.output = self.output + f'{j} {i}\n'

    def place_figure(self, i, j):
        '''
        Функция выставляющая фигуру на доску

        Парметры:
            i, j: int
                Координаты для добавления фигуры
        '''

        self.board = Figures.PrincessFigure().figure_attack(self.board, i, j, self.N)
        self.redraw()
        self.placed += 1

    def remove_figure(self, i, j):
        '''
        Функция убирающая фигуру с доски

        Параметры:
            i, j: int
                 Координаты фигуры, которую необходимо убрать
        '''
        self.board = Figures.PrincessFigure().figure_retreat(self.board, i, j, self.N)
        self.redraw()
        self.placed -= 1

    def redraw(self):
        '''
        Функция отвечающая за отрисовку изменений на доске
        '''

        btn_num = 0  # Номер оперируемой кнопки

        for i in range(self.N):
            for j in range(self.N):

                button = self.buttons[btn_num]

                if self.board[i][j] < 0:  # Если клетка фигуры
                    button.color = 'red'
                    button.onClickFunction = self.remove_figure
                elif self.board[i][j] > 0:  # Если клетка боя
                    button.color = 'blue'
                    button.clickable = False
                else:  # Иначе обычное поле
                    button.color = 'white'
                    button.clickable = True
                    button.onClickFunction = self.place_figure

                btn_num += 1  # переход к следующей кнопке


class Buttons:
    '''
    Класс для создания кнопок
    '''
    def __init__(self, screen, x: int, y: int, width: int, height: int, color: str = 'white', text: str = '',
                 onClickFunc=None, clickable=True):
        '''
        Инициализация кнопки на экране

        Параметры:
            screen:
                Экран на который будет добавлена кнопка
            x, y: int
                Положение кнопки на экране
            width, height: int
                Размерность кнопки
            color: str
                Цвет кнопки
            text: str
                Текст внутри кнопки
            onClickFunc: function
                Функция выполняемая при нажатии
            clickable: bool
                Является ли кнопка кликабельной
        '''
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.clickable = clickable
        self.onClickFunction = onClickFunc
        self.color = color
        self.pressed = False # Проверка на то что кнопка нажимается 1 раз
        self.text = text

        # Создание надписи внутри кнопки
        self.button_surf = pygame.Surface((self.width - 1, self.height - 1))
        self.button_txt = pygame.font.SysFont('TimesNewRoman', 15).render(self.text, True, 'black')

        # Задавание размеров кнопки и ее положения
        self.button_rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def running(self):
        '''
        Функция вызываемая во время работы окна для проверки взаимодействия пользователя с кнопкой
        '''

        self.button_surf.fill(self.color) # Закрашивание кнопки ее цветом

        mouse = pygame.mouse.get_pos() # Позиция мыши на экран

        # Если кнопка кликабельна
        if self.clickable:
            if self.button_rect.collidepoint(mouse): # Проверка на положение мыши внутри рамки кнопки
                # Если при этом кнопка была нажата
                if pygame.mouse.get_pressed()[0]:
                    if not self.pressed:
                        # Возможно добавить сюда обработчик ошибки
                        self.onClickFunction(self.x // self.width, self.y // self.height)
                        self.pressed = True
                else:
                    self.pressed = False

        # Задавание положения текста внутри кнопки
        self.button_surf.blit(self.button_txt, [
            self.button_rect.width / 2 - self.button_txt.get_rect().width / 2,
            self.button_rect.height / 2 - self.button_txt.get_rect().height / 2
        ])

        # Отображение кнопки в заданном окне
        self.screen.blit(self.button_surf, self.button_rect)


if __name__ == '__main__':
    InputWindow()
