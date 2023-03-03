import time
import curses
import pyautogui as pgui
from string import ascii_letters

monitor_w, monitor_h = pgui.size()

def ctrl(c):
    return ord(c) & 0o37

base_movement = 5

def generate_offsets_by_code(movement_options):
    base_offsets_by_dir = {
        'left': (-1, 0),
        'right': (1, 0),
        'up': (0, -1),
        'down': (0, 1)
    }
    offsets_by_code = {}
    for direction, opts in movement_options.items():
        base_offsets = base_offsets_by_dir[direction]
        for opt in opts:
            if isinstance(opt, str) and opt in ascii_letters:
                # Lower case letters move 'base_movement'
                offsets_lower = [base_movement * off for off in base_offsets]
                code_lower = ord(opt.lower())
                offsets_by_code[code_lower] = offsets_lower

                # Upper case letters move '10 x base_movement'
                offsets_upper = [10 * base_movement * off for off in base_offsets]
                code_upper = ord(opt.upper())
                offsets_by_code[code_upper] = offsets_upper

                # Ctrl + letter move by quarter of the screen , which is
                # width/4 when moving left and right and height/4 when moving
                # up and down
                if direction in ('left', 'right'):
                    offsets_ctrl = [monitor_w / 4 * off for off in base_offsets]
                    code_ctrl = ctrl(opt)
                elif direction in ('up', 'down'):
                    offsets_ctrl = [monitor_h / 4 * off for off in base_offsets]
                    code_ctrl = ctrl(opt)

                offsets_by_code[code_ctrl] = offsets_ctrl
            else:
                # Everything other than letters also moves 'base_movement'
                offsets = [base_movement * off for off in base_offsets]
                code = opt
                offsets_by_code[code] = offsets


    return offsets_by_code


def main(stdscr):

    movement_options = {
        'up': ('w', 'k', curses.KEY_UP),
        'down': ('s', 'j', curses.KEY_DOWN),
        'left': ('a', 'h', curses.KEY_LEFT),
        'right': ('d', 'l', curses.KEY_RIGHT)
    }

    offsets_by_code = generate_offsets_by_code(movement_options)

    point_a = None
    point_b = None

    c = stdscr.getch()
    while c != ord('q'):

        if c in offsets_by_code:
            x_off, y_off = offsets_by_code[c]
            pgui.move(x_off, y_off)
        elif c in (ord('q'), ord('n')):
            pgui.click(button='left')
        elif c in (ord('Q'), ord('N')):
            pgui.click(button='left', clicks=2)
        elif c in (ord('r'), ord('m')):
            pgui.click(button='right')
        elif c in (ord('R'), ord('M')):
            pgui.click(button='right', clicks=2)
        elif c in (ord('u'), ord('z')):
            point_a = pgui.position()
            stdscr.clear()
            stdscr.addstr(1, 1, 'Point a was set to {}'.format(point_a))
        elif c in (ord('o'), ord('c')):
            point_b = pgui.position()
            stdscr.clear()
            stdscr.addstr(1, 1, 'Point b was set to {}'.format(point_b))
        elif c in (ord('x'), ord('i')):
            point_a, point_b = point_b, point_a
            stdscr.clear()
            stdscr.addstr(1, 1, 'Points swapped: point_a={} point_b={}'.
                          format(point_a, point_b))
        elif c in (ord('b'), ord('r')):
            pgui.moveTo(point_a)
            pgui.dragTo(point_b.x, point_b.y, 1)


        c = stdscr.getch()


if __name__ == '__main__':
    curses.wrapper(main)
