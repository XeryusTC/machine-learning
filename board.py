# -*- coding: utf-8 -*-

class HareAndHoundsBoard:
    HOUND = 0
    HARE  = 1
    def __init__(self, width=5):
        if not(width >= 5 and width % 2 == 1):
            raise ValueError('The board width should be of odd size and' \
                    ' larger than 5')
        self.width = width
        self.height = 3
        self.hounds = [(0,1), (1,0), (1,2)]
        self.hare = (width-1, 1)

    def possible_moves(self, pos):
        if pos not in self.hounds and pos != self.hare:
            raise ValueError('{} is not a hound or hare'.format(pos))

        x, y = pos
        res = []

        # Generate all new positions
        tmp = [(x+i, y+j) for i in range(-1, 2) for j in range(-1, 2)
                if not (x == 0 and y == 0)]

        for p in tmp:
            # filter the current position
            if p == pos: continue
            # filter moves outside of the board
            if not (0 <= p[0] < self.width): continue
            if not (0 <= p[1] < 3): continue
            if p in ((0,0), (0, 2), (self.width-1, 0), (self.width-1, 2)):
                continue
            # filter diagonal moves on squares
            if ((x + y) % 2) == 0:
                if abs(x - p[0]) == 1 and abs(y - p[1]) == 1:
                    continue
            # filter the position of other pieces
            if p in self.hounds or p == self.hare: continue
            res.append(p)

        # Filter out back moves for hounds
        if pos in self.hounds:
            res = [p for p in res if p[0] >= x]
        return res

    def player_moves(self, player):
        if player == self.HOUND:
            return {hound: possible_moves(hound) for hound in self.hounds}
        elif player == self.HARE:
            return possible_moves(self, self.hare)

    def move(self, origin, new):
        if new not in self.possible_moves(origin):
            raise self.InvalidMoveException('New position is not reachable')

        if origin in self.hounds:
            self.hounds = [h for h in self.hounds if h != origin]
            self.hounds.append(new)
            self.hounds.sort()
        else:
            self.hare = new

    def __str__(self):
        res = ''
        for y in range(self.height):
            for x in range(self.width):
                if (x == 0 or x == self.width-1) and (y == 0 or y == 2):
                    res += '    '
                    continue

                if (x, y) in self.hounds:
                    res += 'O'
                elif (x, y) == self.hare:
                    res += 'A'
                else:
                    res += '*'

                if (x + ((y + 1) % 2)) != (self.width - 1):
                    res += ' - '
            res += '\n'
            if y == 0:
                res += '  / '
                for i in range(int(self.width/2)-1):
                    res += '| \\ | / '
                res += '| \\ \n'
            elif y == 1:
                res += '  \\ '
                for i in range(int(self.width/2)-1):
                    res += '| / | \\ '
                res += '| / \n'
        return res

    class InvalidMoveException(Exception):
        pass


if __name__ == '__main__':
    hah = HareAndHoundsBoard(7)
    print(hah)
    print((1, 0), hah.possible_moves((1, 0)))
    print((0, 1), hah.possible_moves((0, 1)))
    print((1, 2), hah.possible_moves((1, 2)))
    print((6, 1), hah.possible_moves((6, 1)))
    hah.move((6, 1), (5, 1))
    print((5, 1), hah.possible_moves((5, 1)))
    hah.move((5, 1), (4, 1))
    print((4, 1), hah.possible_moves((4, 1)))
    print(hah)
    hah.move((4, 1), (3, 0))
    print((3, 0), hah.possible_moves((3, 0)))
    print(hah)
