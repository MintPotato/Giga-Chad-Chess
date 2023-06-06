from abc import ABC, abstractmethod


class Figure(ABC):
    '''
    Абстрактный класс для всевозможных фигур
    '''

    @abstractmethod
    def figure_attack(self, doska: list[list], i: int, j: int, N: int) -> list[list]:
        '''
        Функция отвечающая за запись фигуры и ее клеток боя на заданную доску

        Параметры:
            doska: list[list]
                Заданная доска для подстановки фигуры
            i: int
                Индекс строки для подстановки фигуры
            j: int
                Индекс столбца для подстановки фигуры
            N: int
                Размерность заданной доски
        '''
        pass

    def figure_retreat(self, doska: list[list], y: int, x: int, N: int) -> list[list]:
        '''
        Функция отвечающая за очистку доски от фигуры и клеток ее боя

        Параметры:
            doska: list[list]
                Заданная доска для подстановки фигуры
            i: int
                Индекс строки для подстановки фигуры
            j: int
                Индекс столбца для подстановки фигуры
            N: int
                Размерность заданной доски
        '''
        pass


class PrincessFigure(Figure):
    '''
    Класс фигуры Принцесса
    '''

    def figure_attack(self, doska, y, x, N):
        doska = [doska[i].copy() for i in range(N)]

        for el in (y-3, x-3), (y-3, x), (y-3, x+3), (y-2, x-2), (y-2, x), (y-2, x+2), \
                (y-1, x-1), (y-1, x), (y-1, x+1), (y, x-3), (y, x-2), (y, x - 1), (y, x+1), (y, x+2), (y, x+3), \
                (y+1, x-1), (y+1, x), (y+1, x + 1), (y+2, x-2), (y+2, x), (y+2, x+2), (y+3, x-3), (y+3, x), (y+3, x+3):
            if 0 <= el[0] < N and 0 <= el[1] < N:
                doska[el[0]][el[1]] += 1

        doska[y][x] -= 1
        return doska

    def figure_retreat(self, doska, y, x, N):
        doska = [doska[i].copy() for i in range(N)]

        for el in (y-3, x-3), (y-3, x), (y-3, x+3), (y-2, x-2), (y-2, x), (y-2, x+2), \
                (y-1, x-1), (y-1, x), (y-1, x+1), (y, x-3), (y, x-2), (y, x - 1), (y, x+1), (y, x+2), (y, x+3), \
                (y+1, x-1), (y+1, x), (y+1, x + 1), (y+2, x-2), (y+2, x), (y+2, x+2), (y+3, x-3), (y+3, x), (y+3, x+3):
            if 0 <= el[0] < N and 0 <= el[1] < N:
                doska[el[0]][el[1]] -= 1

        doska[y][x] += 1
        return doska


if __name__ == '__main__':
    board = [[0 for _ in range(7)] for _ in range(7)]
    figure = PrincessFigure
    board = figure().figure_attack(board, 3, 3, 7)
    board = figure().figure_attack(board, 0, 1, 7)
    for el in board:
        print(el)
