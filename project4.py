# Vivian Zhang (18217735)
# ICS 32A Project 4
# Interface/testing

import p4_mech

def _run_interface():
    rows = int(input())
    columns = int(input())
    starting_field = input().upper()
    if starting_field == 'CONTENTS':
        contents = _get_contents(rows, columns)
    else:
        contents = _empty_field(rows, columns)
    game_state = p4_mech.GameState(rows, columns, contents)
    _print_board(rows, columns, game_state.contents())
    done = False
    faller = None
    while done == False:
        command = input()
        if command == '':
            try:
                game_state.tick_time()
                faller = game_state.get_faller()
                _print_board(rows,columns,_contents_with_faller(game_state, faller))
            except p4_mech.GameOverError:
                print('GAME OVER')
                done = True
        elif command == 'R':
            try:
                faller = game_state.rotate_faller()
            except p4_mech.NoFallerError:
                pass
            except p4_mech.InvalidMoveError:
                pass
            _print_board(rows,columns,_contents_with_faller(game_state, faller))
        elif command == '>':
            try:
                faller = game_state.move_right()
            except p4_mech.NoFallerError:
                pass
            except p4_mech.InvalidMoveError:
                pass
            _print_board(rows,columns,_contents_with_faller(game_state, faller))
        elif command == '<':
            try:
                faller = game_state.move_left()
            except p4_mech.NoFallerError:
                pass
            except p4_mech.InvalidMoveError:
                pass
            _print_board(rows,columns,_contents_with_faller(game_state, faller))
        elif command.startswith('F '):
            try:
                if game_state.get_faller() == None:
                    faller_info = command.split()
                    fall_column = faller_info[1]
                    faller_list = faller_info[2:]
                    faller_col = int(faller_info[1])
                    faller = game_state.new_faller(faller_col, faller_list)
            except p4_mech.InvalidMoveError:
                pass
            _print_board(rows, columns, _contents_with_faller(game_state, faller))
        elif command == 'Q':
            done = True
        else:
            print('Invalid command')
            


def _get_contents(r: int, c: int) -> list:
    field = []
    for row in range(r):
        add_to_field = False
        while add_to_field == False:
            line = input().upper()
            if len(line) != c:
                print('Incorrect number or characters')
            else:
                temp = []
                for char in line:
                    temp.append(char)
                add_to_field = True
                for t in temp:
                    if (t != ' ' and t != 'A' and t != 'B' and t != 'C' and
                     t != 'D' and t != 'E' and t != 'F' and t != 'G' and
                     t != 'H' and t != 'I' and t != 'J' and t != ' '):
                        add_to_field = False
                if add_to_field:
                    for t in range(len(temp)):
                        temp[t] = ' ' + temp[t] + ' '
                    field.append(temp)
                else:
                    print('Invalid input')
    return field



def _empty_field(r: int, c: int) -> list:
    field = []
    for row in range(r):
        temp = []
        for col in range(c):
            temp.append('   ')
        field.append(temp)
    return field



def _print_board(r: int, c: int, field: [list]):
    for row in range(r):
        print('|', end = '')
        for col in range(c):
            print(field[row][col], end = '')
        print('|')
    print(' ' + c*'---' + ' ')


def _contents_with_faller(game_state: p4_mech.GameState, faller: [list]) -> [list]:
    if faller == None:
        return game_state.contents()
    else:
        temp_field = []
        for content in range(len(game_state.contents())):
            temp = []
            for cont in range(len(game_state.contents()[content])):
                temp.append(game_state.contents()[content][cont])
            temp_field.append(temp)
        for jewel in range(len(faller)):
            r = faller[jewel][1]
            c = faller[jewel][2]
            if r >= 0:
                temp_field[r][c] = faller[jewel][0]
        return temp_field
    

if __name__ == '__main__':
    _run_interface()
