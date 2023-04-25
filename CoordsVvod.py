import pygame
import Figures


class InputWindow:
    def __init__(self):

        with open('input.txt', 'r') as f:
            NLK = tuple(f)[0]

        # Объявление необходимых переменных
        self.output = NLK + '\n'
        N, self.K = int(NLK.split()[0]), int(NLK.split()[-1])

        cell_size = 400 // N
        board_size = cell_size * N
        self.N = N
        self.board = [[0 for _ in range(N)] for _ in range(N)]
        self.placed = 0
        self.buttons: list['Buttons'] = [] # Список содержащий клеки доски в виде экземпляров класса Button

        # Работа с окном
        pygame.init()
        self.display = pygame.display.set_mode((board_size + 1, board_size + 100))
        self.display.fill('white')
        pygame.draw.rect(self.display, 'black', (0, 0, board_size + 1, board_size + 1))
        pygame.display.flip()


        for lines in range(N):
            for rows in range(N):
                self.buttons += [Buttons(self.display, cell_size * lines + 1, cell_size * rows + 1, cell_size, cell_size, onClickFunc=self.place_figure)]

        self.buttons += [Buttons(self.display, 40, board_size + 20, 200, 50, text='Записать вводные данные', color='gray', onClickFunc=self.close)]

        self.run = True
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            for button in self.buttons:
                button.running()

            pygame.display.update()


    def close(self, *args):
        self.add_coords()
        with open('input.txt', 'w') as f:
            f.write(self.output)
        self.run = False
        pygame.quit()

    def add_coords(self):
        '''
        Добавляет координаты к уже существующей строке NLK
        :return:
        '''
        for i in range(self.N):
            for j in range(self.N):
                if self.board[i][j] < 0:
                    self.output = self.output + f'{j} {i}\n'


    def place_figure(self, i, j):
        '''
        Функция выставляющая фигуру на доску
        :param i:
        :param j:
        :return:
        '''
        if self.placed < self.K:
            self.board = Figures.PrincessFigure().figure_attack(self.board, i, j, self.N)
            self.redraw()
            self.placed += 1

    def remove_figure(self, i, j):
        '''
        Функция убирающая фигуру с доски
        :param i:
        :param j:
        :return:
        '''
        self.board = Figures.PrincessFigure().figure_retreat(self.board, i, j, self.N)
        self.redraw()
        self.placed -= 1


    def redraw(self):
        '''
        Функция отвечающая за отрисовку изменений на доске
        :return:
        '''
        btn_num = 0
        for i in range(self.N):
            for j in range(self.N):
                button = self.buttons[btn_num]
                if self.board[i][j] < 0:
                    button.color = 'red'
                    button.onClickFunction = self.remove_figure
                elif self.board[i][j] > 0:
                    button.color = 'blue'
                    button.clickable = False
                else:
                    button.color = 'white'
                    button.clickable = True
                    button.onClickFunction = self.place_figure

                btn_num += 1



class Buttons:
    def __init__(self, screen, x, y, width, height, color='white', text='', onClickFunc=None, clickable=True):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.clickable = clickable
        self.onClickFunction = onClickFunc
        self.color = color
        self.pressed = False
        self.text = text

        self.button_surf = pygame.Surface((self.width - 1, self.height - 1))
        self.button_txt = pygame.font.SysFont('TimesNewRoman', 15).render(self.text, True, 'black')
        self.button_rect = pygame.Rect(self.x, self.y, self.width, self.height)


    def running(self):

        mouse = pygame.mouse.get_pos()
        self.button_surf.fill(self.color)
        if self.clickable:
            if self.button_rect.collidepoint(mouse):
                if pygame.mouse.get_pressed()[0]:
                    if not self.pressed:
                        # Возможно добавить сюда обработчик ошибки
                        self.onClickFunction(self.x // self.width, self.y // self.height)
                        self.pressed = True
                else:
                    self.pressed = False

        self.button_surf.blit(self.button_txt, [
            self.button_rect.width / 2 - self.button_txt.get_rect().width / 2,
            self.button_rect.height / 2 - self.button_txt.get_rect().height / 2
        ])
        self.screen.blit(self.button_surf, self.button_rect)


if __name__ == '__main__':
    InputWindow()