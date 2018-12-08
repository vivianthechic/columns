# Vivian Zhang (18217735)
# ICS 32A Project 5
# Game Mechanics

import random

class InvalidMoveError(Exception):
    pass

class NoFallerError(Exception):
    pass

class GameOverError(Exception):
    pass


class GameState:

    def __init__(self, rows: int, cols: int):
        self._rows = rows
        self._cols = cols
        self._contents = self._empty_contents()
        self._faller = None
        self._matchfound = False



    def _empty_contents(self) -> [list]:
        contents = []
        for row in range(self._rows):
            temp = []
            for col in range(self._cols):
                temp.append('   ')
            contents.append(temp)
        return contents

                

    def contents(self) -> [list]:
        return self._contents



    def fill_bottom(self) -> None:
        for r in range(self._rows -1):
            for c in range(self._cols):
                if self._contents[r][c] != '   ' and self._contents[r+1][c] == '   ':
                    for r2 in list(range(r+1))[::-1]:
                        temp = self._contents[r2+1][c]
                        self._contents[r2+1][c] = self._contents[r2][c]
                        self._contents[r2][c] = temp
                        
                

    def _new_faller(self, col: int, letters: list) -> None:
        if col < 1 or col > self._cols:
            raise InvalidMoveError()
        else:
            self._faller = []
            for letter in range(len(letters)):
                self._faller.append(['[' + letters[letter] + ']'
                                     ,letter - len(letters), col-1])
            self.tick_time()
        return self._faller



    def _create_faller(self) -> None:
        rand_col = random.randint(1,self._cols)
        rand_letters = []
        d = { 1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G',
              8: 'H', 9: 'I', 10: 'J'}
        for i in range(3):
            rand_num = random.randint(1,10)
            rand_letter = d[rand_num]
            rand_letters.append(rand_letter)
        self._new_faller(rand_col, rand_letters)
        

    def get_faller(self) -> list:
        return self._faller



    def rotate_faller(self) -> None:
        if self._faller == None:
            raise NoFallerError()
        elif self._faller[0][0].startswith('|'):
            raise InvalidMoveError()
        else:
            temp = self._faller[-1][0]
            for jewel in list(range(len(self._faller)))[::-1]:
                x = self._faller[jewel-1][0]
                self._faller[jewel][0] = x
            self._faller[0][0] = temp



    def tick_time(self) -> None:
        if self._faller == None:
            if self._matchfound == True:
                for r in range(self._rows):
                    for c in range(self._cols):
                        if self._contents[r][c].startswith('*'):
                            self._contents[r][c] = '   '
                self.fill_bottom()
                self._matchfound = False
            else:
                match = self._find_match()
                if match == True:
                    self._matchfound = True
                else:
                    self._create_faller()
        elif (self._faller[-1][1] < self._rows-1
              and self._contents[self._faller[-1][1]+1][self._faller[-1][2]] == '   '):
            for jewel in range(len(self._faller)):
                self._faller[jewel][1] += 1
        elif self._faller[0][0].startswith('|'):
            if self.game_over() == False:
                for jewel in range(len(self._faller)):
                    r = self._faller[jewel][1]
                    c = self._faller[jewel][2]
                    self._contents[r][c] = ' ' + self._faller[jewel][0][1] + ' '
                self._faller = None
                self.tick_time()
            else:
                raise GameOverError()
        else:
            for jewel in range(len(self._faller)):
                letter = self._faller[jewel][0][1]
                self._faller[jewel][0] = '|' + letter + '|'
        

    def move_down(self) -> None:
        if self._faller == None:
            raise NoFallerError()
        elif self._faller[0][0].startswith('|'):
            raise InvalidMoveError()
        else:
            if (self._faller[-1][1] < self._rows-1
              and self._contents[self._faller[-1][1]+1][self._faller[-1][2]] == '   '):
                for jewel in range(len(self._faller)):
                    self._faller[jewel][1] += 1
            

    def move_left(self) -> None:
        if self._faller == None:
            raise NoFallerError()
        elif self._faller[0][0].startswith('|'):
            raise InvalidMoveError()
        else:
            is_blocked = self._is_blocked(-1)
            if is_blocked == False:
                for jewel in range(len(self._faller)):
                    self._faller[jewel][2] -= 1



    def move_right(self) -> None:
        if self._faller == None:
            raise NoFallerError()
        elif self._faller[0][0].startswith('|'):
            raise InvalidMoveError()
        else:
            is_blocked = self._is_blocked(1)
            if is_blocked == False:
                for jewel in range(len(self._faller)):
                    self._faller[jewel][2] += 1



    def _is_blocked(self, leftright: int) -> bool:
        blocked = False
        for jewel in range(len(self._faller)):
            current_row = self._faller[jewel][1]
            current_col = self._faller[jewel][2]
            new_col = current_col + leftright
            if new_col < 0 or new_col >= self._cols:
                blocked = True
            elif current_row >= 0 and self._contents[current_row][new_col] != '   ':
                blocked = True
        return blocked



    def _find_match(self) -> bool:
        match_found = False
        for r in range(self._rows):
            for c in range(self._cols):
                if self._match_sequence(r, c):
                        match_found = True
        return match_found



    def _match_sequence(self, r: int, c: int):
        return self._match(r, c, 0, 1) \
               or self._match(r, c, 1, 1) \
               or self._match(r, c, 1, 0) \
               or self._match(r, c, 1, -1) \
               or self._match(r, c, 0, -1) \
               or self._match(r, c, -1, -1) \
               or self._match(r, c, -1, 0) \
               or self._match(r, c, -1, 1)



    def _match(self, r: int, c: int, rdel: int, cdel: int):
        start = self._contents[r][c]
        coords = []
        if start == '   ':
            return False
        else:
            for i in range(1, 3):
                if c+cdel*i >= self._cols or c+cdel*i < 0 \
                   or r+rdel*i >= self._rows or r+rdel*i < 0:
                    return False
                elif self._contents[r+rdel*i][c+cdel*i][1] != start[1]:
                    return False
            for j in range(3):
                self._contents[r+rdel*j][c+cdel*j] = '*' + self._contents[r+rdel*j][c+cdel*j][1] + '*'
            return True                
                


    def game_over(self) -> bool:
        if self._faller[0][0].startswith('|') and self._faller[0][1] < 0:
            return True
        else:
            return False
