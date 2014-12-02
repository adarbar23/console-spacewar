# coding=utf-8

"""
spacewar: a python port from an old gw-basic game (not mine)
see the original gw-basic source at http://jsbasic.apphb.com/SpaceWar.htm
author: bartoszgo; licence: free for any use
"""

import sys
import random
#import readchar as keyinput

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


# ----------

def getch():  # todo: make platform-independent
    """

    :return:
    """
    if INPUTMETHOD == 1:
        return readchar.readkey()
    elif INPUTMETHOD == 2:
        return msvcrt.getch()
    

def cls():  # todo: make platform-independent
    """
    :rtype : object
    :return:
    """
    sys.stdout.write("\x1b7\x1b[2J\x1b8")
    return


def fake(faked):
    """
    :param faked:
    :return:
    """
    return faked


def printxy(ylocation, xlocation, text):  # todo: make platform-independent
    """

    :param ylocation:
    :param xlocation:
    :param text:
    :return:
    """
    xlocation += 1  # border
    sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (ylocation, xlocation, text))
    sys.stdout.flush()


def updatescores(p1score, p2score):
    """

    :rtype : None
    """
    printxy(1, 2, "Player 1: %s" % p1score)
    printxy(1, 24, "Player 2: %s" % p2score)
    return


def fire_missile(missile_nr, missiles, players):
    """

    :param missile_nr:
    :param missiles:
    :param players:
    :return:
    """
    [miss1x, miss1y, miss2x, miss2y] = missiles
    [pl1x, pl1y, pl2x, pl2y] = players

    if missile_nr == 1:
        if miss1y == 0:
            miss1y = pl1y
            miss1x = pl1x + 3
    if missile_nr == 2:
        if miss2y == 0:
            miss2y = pl2y
            miss2x = pl2x - 1

    missiles = [miss1x, miss1y, miss2x, miss2y]

    return missiles


def ship(ship_nr, operation, players):
    """
    :param ship_nr:
    :param operation:
    :param players:
    :return:
    """
    [pl1x, pl1y, pl2x, pl2y] = players
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


def artificial_intelligence(players, bordery, missiles):
    """
    :param players:
    :param bordery:
    :param missiles:
    :return:
    """

    [miny, maxy] = bordery
    pl1y = players[1]
    pl2y = players[3]

    [miss1x, miss1y, miss2x, miss2y] = missiles

    decision = random.randrange(1, 8)

    if decision == 1 and pl2y > miny:
        ship(2, 0, players)
        pl2y -= 1
    if decision == 2 and pl2y < maxy:
        ship(2, 0, players)
        pl2y += 1
    if decision == 3 or pl1y == pl2y:
        missiles = [miss1x, miss1y, miss2x, miss2y]
        missiles = fire_missile(2, missiles, players)

    # assert isinstance(pl2y, int)
    return missiles, pl2y
"""
750 rem Process player one's missile
752 locate missile1y$, missile1x$
753 print " "
755 if missile1x$ = player2x$ + 3 then missile1y$ = 0 : missile1x$ = 0 : return
757 missile1x$ = missile1x$ + 1
760 locate missile1y$, missile1x$
770 print "."
780 if missile1y$ = player2y$ and missile1x$ = player2x$ then missile1y$ = 0 : missile1x$ = 0 : player1Score$ = player1Score$ + 1 : playerToExplode$ = 2 : i$ = 1
790 return

800 rem initialise player two's missile
810 if missile2y$ <> 0 then return
820 missile2y$ = player2y$
830 missile2x$ = player2x$ - 1
840 return

850 rem Process player two's missile
852 locate missile2y$, missile2x$
853 print " "
855 if missile2x$ = player1x$ - 1 then missile2y$ = 0 : missile2x$ = 0 : return
857 missile2x$ = missile2x$ - 1
860 locate missile2y$, missile2x$
870 print "."
880 if missile2y$ = player1y$ and missile2x$ >= player1x$ and missile2x$ < player1x$ + 3 then missile2y$ = 0 : missile2x$ = 0 : player2Score$ = player2Score$ + 1 : playerToExplode$ = 1 : i$ = 1
890 return

"""

def process_missile(missile_nr, missiles,
                    players, params):
    """

    :param missile_nr:
    :param missiles:
    :param players:
    :param params:
    :return:
    """
    [toexplode, myframe, pl1sc, pl2sc] = params
    [miss1x, miss1y, miss2x, miss2y] = missiles
    [pl1x, pl1y, pl2x, pl2y] = players
    if missile_nr == 1:
        printxy(miss1y, miss1x, " ")
        if miss1x == (pl1x + 3):
            miss1y = miss1x = 0

            missiles = [miss1x, miss1y, miss2x, miss2y]
            return missiles, toexplode, myframe, pl1sc, pl2sc

        else:
            miss1x += 1
            printxy(miss1y, miss1x, ".")
            # collision
            if (miss1y == pl2y) and (miss1x == pl2x):
                miss1y = miss1x = 0
                pl1sc += 1
                toexplode = 2
                myframe = 1

            missiles = [miss1x, miss1y, miss2x, miss2y]
            return missiles, toexplode, myframe, pl1sc, pl2sc

    if missile_nr == 2:
        printxy(miss2y, miss2x, " ")
        if miss2x == (pl2x - 1):
            miss2y = miss2x = 0
        else:
            miss2x -= 1
            printxy(miss2y, miss2x, ".")
            # collision
            if (miss2y == pl1y) and (pl1x <= miss2x < (pl1x + 3)):
                miss2y = miss2x = 0
                pl2sc += 1
                toexplode = 1
                myframe = 1

    missiles = [miss1x, miss1y, miss2x, miss2y]
    return missiles, toexplode, myframe, pl1sc, pl2sc


def win(pl1score):
    """

    :param pl1score:
    :return:
    """
    if pl1score == 10:
        message = "PLAYER ONE WINS!!!!"
    else:
        message = "PLAYER TWO WINS!!!!"
    printxy(7, 10, message)
    printxy(9, 9, "Press 'C' to continue")

    while getch() != "c":
        pass

    return


def lose(toexplode, players, myframe, params):
    """
    :param toexplode:
    :param myframe:
    :param players:
    :param params:
    :return:
    """
    [pl1x, pl1y, pl2x, pl2y] = players
    [pl1sc, pl2sc, miny, maxy] = params
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
    for j in range(1, 1000):  # todo: need to replace this with time delay
        fake(j)  # look pylint, I'm smarter!
        printxy(current_y, current_x - myframe, '*' * (myframe * 2 + 1))
    myframe += 1
    if myframe >= 5:
        toexplode = 0
        cls()
        updatescores(pl1sc, pl2sc)
        pl1y = miny + 1
        pl2y = maxy - 1

    return myframe, toexplode, pl1sc, pl2sc, pl1y, pl2y


def main():
    """

    :return:
    """
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
        players = [player1x, player1y, player2x, player2y]
        missiles = [missile1x, missile1y, missile2x, missile2y]
        # noone dies, someone wins
        if playertoexplode == 0 and \
                (score[0] == 10 or score[1] == 10):
            win(score[0])
            return  # player1x, player1y
        # someone dies
        if playertoexplode != 0:
            params = [score[0], score[1], bordery[0], bordery[1]]
            frame, playertoexplode, score[0], score[1], \
                player1y, player2y = lose(playertoexplode, players, frame,
                                          params)
            return  # player1x, player1y
        # rewrite ships
        ship(1, 1, players)
        ship(2, 1, players)
        # rewrite missiles
        params = [playertoexplode, frame, score[0], score[1]]
        if missile1x != 0:
            [missile1x, missile1y, missile2x, missile2y], playertoexplode, \
                frame, score[0], score[1] = process_missile(1, missiles,
                                                            players, params)
        if missile2x != 0:
            [missile1x, missile1y, missile2x, missile2y], playertoexplode, \
                frame, score[0], score[1] = process_missile(2, missiles,
                                                            players, params)

        # process user's control
        key = getch()
        if key == "a" and player1y > bordery[0]:
            ship(1, 0, players)
            player1y -= 1
        elif key == "z" and player1y < bordery[1]:
            ship(1, 0, players)
            player1y += 1
        elif key == " " or key == "j":  # todo: accept space
            missiles = fire_missile(1, missiles, players)
        elif key == "q":
            cls()
            exit()
        # process ai's control
        missiles, player2y = \
            artificial_intelligence(players, bordery, missiles)
    return  # player1x, player1y


if __name__ == '__main__':
    main()
    exit()
