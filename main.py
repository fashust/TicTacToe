# -*- coding: utf-8 -*- #
"""
    main
"""
from __future__ import print_function, absolute_import
from random import seed, randint, choice
import itertools


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


class CPUPlayer(object):
    """
        simple cpu ai
    """
    def __init__(self, board):
        """
            init
        """
        self.moves = {x: '' for x in itertools.product(xrange(3), repeat=2)}
        self.board = board
        self.last_move = None
        self.last_user_move = None

    def move(self):
        """
            cpu move
        """
        rows = map(''.join, self.board.rows())
        cols = map(''.join, self.board.cols())
        diags = map(''.join, self.board.diagonals())
        moves = [_[0] for _ in self.moves.iteritems() if not _[1]]
        if 'XX' in rows and len(moves) > 1:
            # block row
            moves = [
                _ for _ in moves if _[0] in [
                    i for i, x in enumerate(rows) if x == 'XX'
                ]
            ]
            print('x_filter', moves)
        if 'XX' in cols and len(moves) > 1:
            # block colum
            moves = [
                _ for _ in moves if _[1] in [
                    i for i, x in enumerate(cols) if x == 'XX'
                ]
            ]
        if 'XX' in diags and len(moves) > 1:
            # block diagonal
            moves = [
                _ for _ in moves if _ in (
                    [(i, 2 - i) for i in xrange(3)] if diags.index('XX')
                    else [(i, i) for i in xrange(3)]
                )
            ]
        self.last_move = choice(moves)
        self.moves[self.last_move] = CPU
        x, y = self.last_move
        return x + 1, y + 1

    def set_user_move(self, x, y):
        """
            update last user move
        """
        self.last_user_move = x - 1, y - 1
        self.moves[self.last_user_move] = USER


def main():
    """
        main
    """
    b = Board()
    cpu = CPUPlayer(b)
    b.show()
    moves = 9
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
            cpu.set_user_move(x, y)
            is_win = b.is_win()
            moves -= 1
            if moves == 0:
                print('Dare')
                return
            if is_win:
                b.show()
                print(is_win)
                return
        else:
            continue
        # user
        # cpu
        while True:
            # x, y = randint(1, 3), randint(1, 3)
            x, y = cpu.move()
            if not b.get_cell(x, y):
                b.set_cell(x, y, False)
                moves -= 1
                if moves == 0:
                    print('Dare')
                    return
                is_win = b.is_win()
                if is_win:
                    b.show()
                    print(is_win)
                    return
                break
            else:
                continue
        # cpu
        if moves == 0:
            print('Dare')
            return
        b.show()


if __name__ == '__main__':
    main()