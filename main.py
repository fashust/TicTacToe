# -*- coding: utf-8 -*- #
"""
    main
"""
from __future__ import print_function, absolute_import
from random import seed, random, choice
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
        seed(random())
        self.last_move = choice(self.get_best_move())
        x, y = self.last_move
        if self.board.get_cell(x + 1, y + 1):
            self.move()
        else:
            self.moves[self.last_move] = CPU
            self.board.set_cell(x + 1, y + 1, False)
        return self.board.is_win()

    def get_best_move(self):
        """
            select best move for block
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
        return moves

    def set_user_move(self, x, y):
        """
            update last user move
        """
        self.last_user_move = x - 1, y - 1
        self.moves[self.last_user_move] = USER


class UserPlayer(object):
    """
        user player
    """

    def __init__(self, board):
        """
            init
        """
        self.board = board
        self.x, self.y = None, None
        self.behavior = {
            None: self.write_move,
            'c': self.move,
            'e': lambda: exit()
        }

    def move(self):
        """
            user move
        """
        return self.behavior[
            self.check_input(raw_input('select cell (ex: 1,1), q for exit: '))
        ]()

    def check_input(self, inp):
        """
            check user input
        """
        try:
            x, y = map(lambda _: int(_.strip()), inp.split(','))
        except (TypeError, ValueError, NameError) as err:
            return 'c'
        finally:
            if inp == 'q':
                return 'e'
        if (x not in xrange(1, len(self.board.board) + 1) or
                y not in xrange(1, len(self.board.board) + 1)):
            return 'c'
        if self.board.get_cell(x, y):
            return 'c'
        self.x, self.y = x, y

    def write_move(self):
        """
            store user move
        """
        self.board.set_cell(self.x, self.y)
        return self.x, self.y, self.board.is_win()


def main():
    """
        main
    """
    board = Board()
    cpu = CPUPlayer(board)
    user = UserPlayer(board)
    board.show()
    moves = 9
    while True:
        # user
        # ==== work
        # try:
        #     inp = raw_input('select cell (ex: 1,1), q for exit: ')
        #     x, y = map(lambda _: int(_.strip()), inp.split(','))
        # except (TypeError, ValueError, NameError) as err:
        #     continue
        # finally:
        #     if inp == 'q':
        #         return
        # if (x not in xrange(1, len(board.board) + 1) or
        #         y not in xrange(1, len(board.board) + 1)):
        #     continue
        # if not board.get_cell(x, y):
        #     board.set_cell(x, y)
        #     cpu.set_user_move(x, y)
        #     is_win = board.is_win()
        #     moves -= 1
        #     if moves == 0:
        #         print('Dare')
        #         return
        #     if is_win:
        #         board.show()
        #         print(is_win)
        #         return
        # else:
        #     continue
        # ==== work
        ux, uy, result = user.move()
        if not result:
            cpu.set_user_move(ux, uy)
            moves -= 1
        else:
            board.show()
            print(result)
            return
        # user
        # cpu
        # ===== work
        # while True:
        #     x, y = cpu.move()
        #     if not board.get_cell(x, y):
        #         board.set_cell(x, y, False)
        #         moves -= 1
        #         if moves == 0:
        #             print('Dare')
        #             return
        #         is_win = board.is_win()
        #         if is_win:
        #             board.show()
        #             print(is_win)
        #             return
        #         break
        #     else:
        #         continue
        # ===== work
        result =  cpu.move()
        if not result:
            moves -= 1
        else:
            board.show()
            print(result)
            return
        # cpu
        if moves == 0:
            print('Dare')
            return
        board.show()


if __name__ == '__main__':
    main()