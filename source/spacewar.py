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


INPUTMETHOD = 0
try:
    import readchar as key_input
    INPUTMETHOD = 1
except ImportError:
    try:
        import msvcrt as key_input
        INPUTMETHOD = 2
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
   

def cls():  # todo: make platform-independent
    sys.stdout.write("\x1b7\x1b[2J\x1b8")


def printxy(ylocation, xlocation, text):  # todo: make platform-independent
    xlocation += 1  # border
    sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (ylocation, xlocation, text))
    sys.stdout.flush()

def updatescores(p1score, p2score):
    printxy(1, 2, "Player 1: %s" % p1score)
    printxy(1, 24, "Player 2: %s" % p2score)
    return 


def fire_missile(missile_nr, miss1x, miss1y, miss2x, miss2y, \
pl1x, pl1y, pl2x, pl2y):
    if missile_nr == 1:
        if miss1y == 0:
            miss1y = pl1y
            miss1x = pl1x + 3
    if missile_nr == 2:
        if miss2y == 0:
            miss2y = pl2y
            miss2x = pl2x - 1
    return miss1x, miss1y, miss2x, miss2y


def ship(ship_nr, operation, pl1x, pl1y, pl2x, pl2y):
    if operation == 1:
        if ship_nr == 1:
            pic = ">=-"
            printxy(pl1y, pl1x, pic)
        elif ship_nr == 2:
            pic = "-=<"
            printxy(pl2y, pl2x, pic)

    if operation == 0:
        pic = "   "
        if ship_nr == 1:
            printxy(pl1y, pl1x, pic)
        elif ship_nr == 2:
            printxy(pl2y, pl2x, pic)
    return


def artificial_intelligence(pl1x, pl1y, pl2x, pl2y, \
miny, maxy, miss1x, miss1y, miss2x, miss2y):
    decision = random.randrange(1, 4)
    if decision == 1 and pl2y > miny:
        ship(2, 0, pl1x, pl1y, pl2x, pl2y)
        pl2y -= 1
    if decision == 2 and pl2y < maxy:
        ship(2, 0, pl1x, pl1y, pl2x, pl2y)
        pl2y += 1
    if decision == 3 or pl1y == pl2y:
        
        miss1x, miss1y, miss2x, miss2y = fire_missile(2, \
        miss1x, miss1y, miss2x, miss2y, pl1x, pl1y, \
        pl2x, pl2y)
        
    return miss1x, miss1y, miss2x, miss2y, pl2y


#  todo: multiple returns with many parameters is dangerous, could differ
def process_missile(missile_nr, miss1x, miss1y, miss2x, miss2y, \
pl1x, pl1y, pl2x, pl2y, toexplode, myframe, pl1sc):
    if missile_nr == 1:
        printxy(miss1y, miss1x, " ")
        # missed, erase
        if miss1x == pl1x + 3:
            miss1y = miss1x = 0
            return miss1x, miss1y, miss2x, miss2y, toexplode, myframe, pl1sc
        miss1x += 1
        printxy(miss1y, miss1x, ".")
        # collision
        if miss1y == pl2y and miss1x == pl2x:
            miss1y = miss1x = 0
            pl1sc += 1
            toexplode = 2
            myframe = 1
        return miss1x, miss1y, miss2x, miss2y, toexplode, myframe, pl1sc

    if missile_nr == 2:
        printxy(miss2y, miss2x, " ")
        # missed, erase
        if miss2x == pl1x - 1:
            miss2y = miss2x = 0
            return miss1x, miss1y, miss2x, miss2y, toexplode, myframe, pl1sc
        miss2x -= 1
        printxy(miss2y, miss2x, ".")
        # collision
        if miss2y == pl1y and pl1x <= \
        miss2x < pl1x + 3:
            miss2y = miss2x = 0
            pl1sc += 1
            toexplode = 1
            myframe = 1
    return miss1x, miss1y, miss2x, miss2y, toexplode, myframe, pl1sc


def win(pl1score):
    if pl1score == 10:
        message = "PLAYER ONE WINS!!!!"
    else:
        message = "PLAYER TWO WINS!!!!"
    printxy(7, 10, message)
    printxy(9, 9, "Press 'C' to continue")

    while getch() != "c":
        pass

    return


def lose(toexplode, pl1x, pl1y, pl2x, pl2y, \
myframe, pl1sc, pl2sc, miny, maxy):
    if toexplode == 1:
        current_x = pl1x + 1
        current_y = pl1y
    else:
        current_x = pl2x + 1
        current_y = pl2y
    if myframe != 4:  # magic number - explosion step?
        printxy(current_y - myframe, current_x, "*")
        printxy(current_y + myframe, current_x, "*")
        printxy(current_y - myframe, current_x - myframe, ".")
        printxy(current_y - myframe, current_x + myframe, ".")
        printxy(current_y + myframe, current_x + myframe, ".")
        printxy(current_y + myframe, current_x - myframe, ".")
    for j in range(1, 1000):  
        j = j # todo: need to replace this with time delay; cheating pylint
        printxy(current_y, current_x - myframe, '*' * (myframe * 2 + 1))
    myframe += 1
    if myframe >= 5:
        toexplode = 0
        cls()
        updatescores(pl1sc, pl2sc)
        pl1y = miny + 1
        pl2y = maxy - 1
    
    return myframe, toexplode, pl1sc, pl2sc, pl1y, pl2y

#  todo: multiple returns with many parameters is dangerous, could differ    
def main():

    miny = 3
    maxy = 17
    player1y = 5
    player1x = 5
    missile1y = 0
    missile1x = 0
    player2y = 15
    player2x = 30
    missile2y = 0
    missile2x = 0
    player1score = 0
    player2score = 0
    playertoexplode = 0
    frame = 0

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
    updatescores(player1score, player2score)

    while 1:
        # noone dies, someone wins
        if playertoexplode == 0 and \
                (player1score == 10 or player1score == 10):
            win(player1score)
            return
        # someone dies
        if playertoexplode != 0:
            frame, playertoexplode, player1score, player2score, \
            player1y, player2y = lose(playertoexplode, player1x, player1y, \
            player2x, player2y, frame, player1score, player2score, miny, maxy)
            return
        # rewrite ships
        ship(1, 1, player1x, player1y, player2x, player2y)
        ship(2, 1, player1x, player1y, player2x, player2y)
        # rewrite missiles
        if missile1x != 0:
            missile1x, missile1y, missile2x, missile2y, playertoexplode, \
            frame, player1score = \
            process_missile(1, missile1x, missile1y, missile2x, missile2y, \
            player1x, player1y, player2x, player2y, playertoexplode, \
            frame, player1score)
        if missile2x != 0:
            missile1x, missile1y, missile2x, missile2y, playertoexplode, \
            frame, player1score = \
            process_missile(2, missile1x, missile1y, missile2x, missile2y, \
            player1x, player1y, player2x, player2y, playertoexplode, frame, \
            player1score)

        # process user's control
        key = getch()
        if key == "a" and player1y > miny:
            ship(1, 0, player1x, player1y, player2x, player2y)
            player1y -= 1
        if key == "z" and player1y < maxy:
            ship(1, 0, player1x, player1y, player2x, player2y)
            player1y += 1
        if key == " " or key == "j":  # todo: accept space
            missile1x, missile1y, missile2x, missile2y = fire_missile(1, \
            missile1x, missile1y, missile2x, missile2y, \
            player1x, player1y, player2x, player2y)
            
        if key == "q":
            cls()
            exit()
        # process ai's control
        missile1x, missile1y, missile2x, missile2y, player2y = \
        artificial_intelligence(player1x, player1y, player2x, player2y, \
        miny, maxy, missile1x, missile1y, missile2x, missile2y)

    return


if __name__ == '__main__':
    main()
    exit()
