# coding=utf-8

"""
spacewar: a python port from an old gw-basic game (not mine)
see the original gw-basic source at http://jsbasic.apphb.com/SpaceWar.htm
author: bartoszgo; licence: free for any use
"""

import sys
import random


# todo: use http://www.lfd.uci.edu/~gohlke/pythonlibs/#curses
# todo: make compatible with python 2 and 3
# todo: oo
# todo: pylint
# todo: doctests, other tests

input_method = 0

try:
    import readchar as key_input
    input_method = 1
except ImportError:
    try:
        import msvcrt as key_input
        input_method = 2
    except ImportError:
        print "Readchar and Msvcrt libraries missing!"
        exit()


# ----------

def getch():  # todo: make platform-independent
    while key_input.kbhit():
        key_input.getch()
    key = key_input.getch()
    while key in '\x00\xe0':
        key_input.getch()
        key = key_input.getch()
    return key.decode()
   

#def readchar2():
#
#    # "Get a single character on Windows."
#    if input_method == 2:
#        while key_input.kbhit():
#            key_input.getch()
#        key = key_input.getch()
#        while key in '\x00\xe0':
#            key_input.getch()
#            key = key_input.getch()
#        return key.decode()
#    
#    if input_method == 2:
#        return readchar.readkey()

    
# ----------
    
#class GameConfig(object):
#    def __init__(self):
#        self.PLAYER1Y = self.PLAYER1X = 0
#        self.MISSILE1Y = self.MISSILE1X = 0
#        self.PLAYER2Y = self.PLAYER2X = 0
#        self.MISSILE2Y = self.MISSILE2X = 0
#        self.PLAYER1SCORE = self.PLAYER1SCORE = 0
#        self.FRAME = 0
#        self.PLAYERTOEXPLODE = 0
#        self.MAXY = self.MAXY = self.minx = self.MINY = 0


def cls():  # todo: make platform-independent
    sys.stdout.write("\x1b7\x1b[2J\x1b8")


def printxy(ylocation, xlocation, text):  # todo: make platform-independent
    xlocation += 1  # border
    sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (ylocation, xlocation, text))
    sys.stdout.flush()

def updatescores(PLAYER1SCORE, PLAYER1SCORE):
    printxy(1, 2, "Player 1: %s" % PLAYER1SCORE)
    printxy(1, 24, "Player 2: %s" % PLAYER1SCORE)
    return


def fire_missile(missile_nr, MISSILE1Y, \
MISSILE2Y, PLAYER1X, PLAYER1Y, PLAYER2X, PLAYER2Y):
    if missile_nr == 1:
        if MISSILE1Y == 0:
            MISSILE1Y = PLAYER1Y
            MISSILE1X = PLAYER1X + 3
    if missile_nr == 2:
        if MISSILE2Y == 0:
            MISSILE2Y = PLAYER2Y
            MISSILE2X = PLAYER2X - 1
    return


def ship(ship_nr, operation, PLAYER1X, PLAYER1Y, PLAYER2X, PLAYER2Y):
    if operation == 1:
        if ship_nr == 1:
            pic = ">=-"
            printxy(PLAYER1Y, PLAYER1X, pic)
        elif ship_nr == 2:
            pic = "-=<"
            printxy(PLAYER2Y, PLAYER2X, pic)
        return

    if operation == 0:
        pic = "   "
        if ship_nr == 1:
            printxy(PLAYER1Y, PLAYER1X, pic)
        elif ship_nr == 2:
            printxy(PLAYER2Y, PLAYER2X, pic)
    return


def artificial_intelligence(PLAYER1X, PLAYER1Y, PLAYER2X, PLAYER2Y, \
MINY, MAXY, MISSILE1X, MISSILE1Y, MISSILE2X, MISSILE2Y):
    decision = random.randrange(1, 4)
    if decision == 1 and PLAYER2Y > MINY:
        ship(2, 0, PLAYER1X, PLAYER1Y, PLAYER2X, PLAYER2Y)
        PLAYER2Y -= 1
    if decision == 2 and PLAYER2Y < MAXY:
        ship(2, 0, PLAYER1X, PLAYER1Y, PLAYER2X, PLAYER2Y)
        PLAYER2Y += 1
    if decision == 3 or PLAYER1Y == PLAYER2Y:
        fire_missile(2, MISSILE1Y, \
        MISSILE2Y, PLAYER1X, PLAYER1Y, PLAYER2X, PLAYER2Y)
        
    return


def process_missile(missile_nr, MISSILE1X, MISSILE1Y, MISSILE2X, MISSILE2Y, \
PLAYER1X, PLAYER1Y, PLAYER2X, PLAYER2Y):
    if missile_nr == 1:
        printxy(MISSILE1Y, MISSILE1X, " ")
        # missed, erase
        if MISSILE1X == PLAYER1X + 3:
            MISSILE1Y = MISSILE1X = 0
            return
        MISSILE1X += 1
        printxy(MISSILE1Y, MISSILE1X, ".")
        # collision
        if MISSILE1Y == PLAYER2Y and MISSILE1X == PLAYER2X:
            MISSILE1Y = MISSILE1X = 0
            PLAYER1SCORE += 1
            PLAYERTOEXPLODE = 2
            FRAME = 1
        return

    if missile_nr == 2:
        printxy(MISSILE2Y, MISSILE2X, " ")
        # missed, erase
        if MISSILE2X == PLAYER1X - 1:
            MISSILE2Y = MISSILE2X = 0
            return
        MISSILE2X -= 1
        printxy(MISSILE2Y, MISSILE2X, ".")
        # collision
        if MISSILE2Y == PLAYER1Y and PLAYER1X <= \
        MISSILE2X < PLAYER1X + 3:
            MISSILE2Y = MISSILE2X = 0
            PLAYER1SCORE += 1
            PLAYERTOEXPLODE = 1
            FRAME = 1
    return


def win(PLAYER1SCORE):
    if PLAYER1SCORE == 10:
        message = "PLAYER ONE WINS!!!!"
    else:
        message = "PLAYER TWO WINS!!!!"
    printxy(7, 10, message)
    printxy(9, 9, "Press 'C' to continue")

    while getch() != "c":
        pass

    return


def lose(PLAYERTOEXPLODE, PLAYER1X, PLAYER1Y, PLAYER2X, PLAYER2Y, \
FRAME, PLAYER1SCORE, PLAYER2SCORE, MINY, MAXY):
    if PLAYERTOEXPLODE == 1:
        current_x = PLAYER1X + 1
        current_y = PLAYER1Y
    else:
        current_x = PLAYER2X + 1
        current_y = PLAYER2Y
    if FRAME != 4:  # magic number - explosion step?
        printxy(current_y - FRAME, current_x, "*")
        printxy(current_y + FRAME, current_x, "*")
        printxy(current_y - FRAME, current_x - FRAME, ".")
        printxy(current_y - FRAME, current_x + FRAME, ".")
        printxy(current_y + FRAME, current_x + FRAME, ".")
        printxy(current_y + FRAME, current_x - FRAME, ".")
    for j in range(1, 1000):  # todo: check border values; possible use delay
        j = j # FY, pylint
        printxy(current_y, current_x - FRAME, '*' * (FRAME * 2 + 1))
    FRAME += 1
    if FRAME < 5:
        return

    PLAYERTOEXPLODE = 0
    cls()
    updatescores(PLAYER1SCORE, PLAYER1SCORE)
    PLAYER1Y = MINY + 1
    PLAYER2Y = MAXY - 1
    return

def init(PLAYER1SCORE, PLAYER1SCORE):
    
    # variables should be set here?
    cls()
    printxy(5, 8, "S P A C E   W A R")
    printxy(8, 2, "Keys: 'A' to go up")
    printxy(9, 8, "'Z' to go down")
    printxy(10, 8, "<space> to shoot")
    printxy(13, 8, "First to 10 points wins")
    printxy(16, 8, "Press <space> to start")
    
    while getch() != " ":
        pass
    cls()
    updatescores(PLAYER1SCORE, PLAYER1SCORE)
    return


def main(PLAYER1SCORE, PLAYER1SCORE):
    init()

    MINY = 3
    MAXY = 17
    PLAYER1Y = 5
    PLAYER1X = 5
    MISSILE1Y = 0
    MISSILE1X = 0
    PLAYER2Y = 15
    PLAYER2X = 30
    MISSILE2Y = 0
    MISSILE2X = 0
    PLAYER1SCORE = 0
    PLAYER2SCORE = 0
    PLAYERTOEXPLODE = 0
    FRAME = 0

    while 1:
        # noone dies, someone wins
        if PLAYERTOEXPLODE == 0 and \
                (PLAYER1SCORE == 10 or PLAYER1SCORE == 10):
            win(PLAYER1SCORE)
            return
        # someone dies
        if PLAYERTOEXPLODE != 0:
            lose(PLAYERTOEXPLODE, PLAYER1X, PLAYER1Y, PLAYER2X, \
            PLAYER2Y, FRAME, PLAYER1SCORE, PLAYER2SCORE, MINY, MAXY)
            return
        # rewrite ships
        ship(1, 1)
        ship(2, 1)
        # rewrite missiles
        if MISSILE1X != 0:
            process_missile(1)
        if MISSILE2X != 0:
            process_missile(2)
        # process user's control
        key = getch()
        if key == "a" and PLAYER1Y > MINY:
            ship(1, 0)
            PLAYER1Y -= 1
        if key == "z" and PLAYER1Y < MAXY:
            ship(1, 0, PLAYER1X, PLAYER1Y, PLAYER2X, PLAYER2Y)
            PLAYER1Y += 1
        if key == " " or key == "j":  # todo: accept space
            fire_missile(1, MISSILE1Y, MISSILE2Y, \
            PLAYER1X, PLAYER1Y, PLAYER2X, PLAYER2Y)
            
        if key == "q":
            cls()
            exit()
        # process ai's control
        artificial_intelligence(PLAYER1X, PLAYER1Y, PLAYER2X, PLAYER2Y, \
        MINY, MAXY, MISSILE1X, MISSILE1Y, MISSILE2X, MISSILE2Y)

    return


if __name__ == '__main__':
    main()
    exit()
