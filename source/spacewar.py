# coding=utf-8

"""
spacewar: a python port from an old gw-basic game (not mine)
see the original gw-basic source at http://jsbasic.apphb.com/SpaceWar.htm
author: bartoszgo; licence: free for any use
"""

import sys
import random
import time

INPUTMETHOD = 0
try:
    import readchar
    INPUTMETHOD = 1

except ImportError:
    try:
        import msvcrt
        INPUTMETHOD = 2
    except ImportError:
        print "Readchar and Msvcrt libraries missing!"
        exit()


# http://forums.xkcd.com/viewtopic.php?f=11&t=99890
# the best solution seems to be pygame.
# if not, try the below. and not sure if it works on windows.
# ---
# import thread, time
#
# def input_thread(L):
#     raw_input()
#     L.append(None)
#
# def do_print():
#     L = []
#     thread.start_new_thread(input_thread, (L,))
#     while 1:
#         time.sleep(.1)
#         if L: break
#         print "Hi Mom!"
#
# do_print()
# --- or:
# http://code.activestate.com/recipes/134892/


def getch():  # todo: make platform-independent
    if INPUTMETHOD == 1:
        return readchar.readkey()
    elif INPUTMETHOD == 2:
        return msvcrt.getch()
    

def cls():  # todo: make platform-independent
    sys.stdout.write("\x1b7\x1b[2J\x1b8")
    return


def printxy(ylocation, xlocation, text):  # todo: make platform-independent
    xlocation += 1  # border
    sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (ylocation, xlocation, text))
    sys.stdout.flush()


def updatescores(p1score, p2score):
    printxy(1, 2, "Player 1: %s" % p1score)
    printxy(1, 24, "Player 2: %s" % p2score)
    return


def fire_missile(missile_nr, miss1x, miss1y, miss2x, miss2y, pl1x, pl1y, pl2x, pl2y):

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


def artificial_intelligence(pl1x, pl1y, pl2x, pl2y, bordery, miss1x, miss1y, miss2x, miss2y):

    [miny, maxy] = bordery
    decision = random.randrange(1, 8)

    if decision == 1 and pl2y > miny:
        ship(2, 0, pl1x, pl1y, pl2x, pl2y)
        pl2y -= 1
    if decision == 2 and pl2y < maxy:
        ship(2, 0, pl1x, pl1y, pl2x, pl2y)
        pl2y += 1
    if decision == 3 or pl1y == pl2y:
        [miss1x, miss1y, miss2x, miss2y] = fire_missile(2, miss1x, miss1y, miss2x, miss2y, pl1x, pl1y, pl2x, pl2y)

    return miss1x, miss1y, miss2x, miss2y, pl2y

def process_missile(missile_nr, miss1x, miss1y, miss2x, miss2y,
                    pl1x, pl1y, pl2x, pl2y, playertoexplode1, frame1, score1, score2):

    if missile_nr == 1:

        printxy(miss1y, miss1x, " ")
        if miss1x == (pl2x + 3):
            miss1y = 0
            miss1x = 0

        else:
            miss1x += 1
            printxy(miss1y, miss1x, ".")
            # collision
            if (miss1y == pl2y) and (miss1x == pl2x):
                miss1y = 0
                miss1x = 0
                score1 += 1
                playertoexplode1 = 2
                myframe = 1

    if missile_nr == 2:
        printxy(miss2y, miss2x, " ")
        if miss2x == (pl1x - 1):
            miss2y = 0
            miss2x = 0
        else:
            miss2x -= 1
            printxy(miss2y, miss2x, ".")
            # collision
            if (miss2y == pl1y) and (pl1x <= miss2x < (pl1x + 3)):
                miss2y = 0
                miss2x = 0
                score2 += 1
                playertoexplode1 = 1
                myframe = 1

    missiles = [miss1x, miss1y, miss2x, miss2y]
    return missiles, playertoexplode1, frame1, score1, score2


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


def lose(toexplode, player1x, player1y, player2x, player2y, myframe, params):
    [pl1x, pl1y, pl2x, pl2y] = [player1x, player1y, player2x, player2y]
    [pl1sc, pl2sc, miny, maxy] = params
    if toexplode == 1:
        current_x = pl1x + 1
        current_y = pl1y
    else:
        current_x = pl2x + 1
        current_y = pl2y

    while myframe < 5:
        #if myframe != 4:  # magic number - penultimate explosion step?
        printxy(current_y - myframe, current_x, "*")
        printxy(current_y + myframe, current_x, "*")
        printxy(current_y - myframe, current_x - myframe, ".")
        printxy(current_y - myframe, current_x + myframe, ".")
        printxy(current_y + myframe, current_x + myframe, ".")
        printxy(current_y + myframe, current_x - myframe, ".")


        printxy(current_y, current_x - myframe, '*' * (myframe * 2 + 1))
        time.sleep(.1)

        myframe += 1

    #if myframe >= 5:

    toexplode = 0
    cls()
    updatescores(pl1sc, pl2sc)
    pl1y = miny + 1
    pl2y = maxy - 1

    return myframe, toexplode, pl1sc, pl2sc, pl1y, pl2y


def main():
    bordery = [3, 17]
    player1y = 5
    player1x = 5
    missile1y = 0
    missile1x = 0
    player2y = 15
    player2x = 30
    missile2y = 0
    missile2x = 0
    score = [0, 0]
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
    updatescores(score[0], score[1])

    while 1:
        # noone dies, someone wins
        if playertoexplode == 0 and \
                (score[0] == 10 or score[1] == 10):
            win(score[0])
            return  # player1x, player1y
        # someone dies
        if playertoexplode != 0:
            params = [score[0], score[1], bordery[0], bordery[1]]
            frame, playertoexplode, score[0], score[1], \
                player1y, player2y = lose(playertoexplode, player1x, player1y, player2x, player2y, frame,
                                          params)
            return  # player1x, player1y
        # rewrite ships
        ship(1, 1, player1x, player1y, player2x, player2y)
        ship(2, 1, player1x, player1y, player2x, player2y)
        # rewrite missiles

        if missile1x != 0:
            [missile1x, missile1y, missile2x, missile2y], playertoexplode, \
                frame, score[0], score[1] = process_missile(1, missile1x, missile1y, missile2x, missile2y,
                                                            player1x, player1y, player2x, player2y, playertoexplode, frame, score[0], score[1])
        if missile2x != 0:
            [missile1x, missile1y, missile2x, missile2y], playertoexplode, \
                frame, score[0], score[1] = process_missile(2, missile1x, missile1y, missile2x, missile2y,
                                                            player1x, player1y, player2x, player2y, playertoexplode, frame, score[0], score[1])
        # process user's control
        key = getch()
        if key == "a" and player1y > bordery[0]:
            ship(1, 0, player1x, player1y, player2x, player2y)
            player1y -= 1
        elif key == "z" and player1y < bordery[1]:
            ship(1, 0, player1x, player1y, player2x, player2y)
            player1y += 1
        elif key == " " or key == "j":  # todo: accept space
            [missile1x, missile1y, missile2x, missile2y] = fire_missile(1, missile1x, missile1y, missile2x, missile2y, player1x, player1y, player2x, player2y)
        elif key == "q":
            cls()
            exit()
        # process ai's control
        [missile1x, missile1y, missile2x, missile2y, player2y] = \
            artificial_intelligence(player1x, player1y, player2x, player2y, bordery, missile1x, missile1y, missile2x, missile2y)

    return


if __name__ == '__main__':
    main()
    cls()
    print "Press any key..."
    key = getch()
    cls()
    exit()
