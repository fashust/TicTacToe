# -*- coding: utf-8 -*- #
"""
    main
"""
from __future__ import print_function, absolute_import
from random import seed, randint


__author__ = 'fashust'
__email__ = 'fashust.nefor@gmail.com'


USER = 'X'
CPU = 'O'


class Board(object):
    """
        game board
    """
    def __init__(self):
        """
            init
        """
        self.board = [['' for y in xrange(3)] for x in xrange(3)]

    def set_cell(self, x, y, user_symb=True):
        """
            set X or O in board cell
        """
        self.board[x - 1][y - 1] = USER if user_symb else CPU

    def get_cell(self, x, y):
        """
            get cell value
        """
        return self.board[x - 1][y - 1]

    def rows(self):
        """
            get board rows
        """
        return self.board

    def cols(self):
        """
            get board cols
        """
        return zip(*self.rows())

    def diagonals(self):
        """
            get board diagonals
        """
        return zip(*[(r[i], r[2 - i]) for i, r in enumerate(self.rows())])

    def is_win(self):
        """
            is win
        """
        solutions = (
            map(''.join, self.rows()) +
            map(''.join, list(self.cols())) +
            map(''.join, list(self.diagonals()))
        )
        return (
            'You win' if 'XXX' in solutions
            else 'CPU win' if 'OOO' in solutions
            else None
        )

    def show(self):
        """
            show game bord
        """
        for i, line in enumerate(self.board):
            print('|'.join(['\t{}\t'.format(_ if _ else '') for _ in line]))
            if i != len(self.board) - 1:
                print('-' * 25)


def main():
    """
        main
    """
    b = Board()
    b.show()
    while True:
        # user
        try:
            inp = raw_input('select cell (ex: 1,1), q for exit: ')
            x, y = map(lambda _: int(_.strip()), inp.split(','))
        except (TypeError, ValueError, NameError) as err:
            continue
        finally:
            if inp == 'q':
                return
        if (x not in xrange(1, len(b.board) + 1) or
            y not in xrange(1, len(b.board) + 1)):
            continue
        if not b.get_cell(x, y):
            b.set_cell(x, y)
            is_win = b.is_win()
            if is_win:
                print(is_win)
                return
        # user
        # cpu
        while True:
            x, y = randint(1, 3), randint(1, 3)
            if not b.get_cell(x, y):
                b.set_cell(x, y, False)
                is_win = b.is_win()
                if is_win:
                    print(is_win)
                    return
                break
        # cpu
        # b.is_win()
        b.show()


if __name__ == '__main__':
    main()