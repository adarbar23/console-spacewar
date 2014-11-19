#
# spacewar: a python port from an old gw-basic game (not mine)
# see the original gw-basic source at http://jsbasic.apphb.com/SpaceWar.htm
# author: bartoszgo; licence: free for any use
#

import sys
import random
import readchar # sudo pip install readchar # todo: make platform-independent


class config():
	def __init__(self):
	    player1y = player1x = 0
	    missile1y =  missile1x = 0
	    player2y = player2x  = 0
	    missile2y = missile2x = 0
	    player1score = player2score = playertoexplode = 0


def cls(): # todo: make platform-independent
    sys.stdout.write("\x1b7\x1b[2J\x1b8")
    

def printxy(y, x, text): # todo: make platform-independent
    x+=1 # border
    sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (y, x, text))
    sys.stdout.flush()


def getch(): # todo: make platform-independent
    return readchar.readkey()


def updatescores(player1score, player2score):
    printxy(1, 2,  "Player 1: %s" % player1score)
    printxy(1, 24, "Player 2: %s" % player2score)
    return    


def fire_missile(id):
    if (id == 1):
	if (g.missile1y == 0):
	    g.missile1y = g.player1y
    	    g.missile1x = g.player1x + 3
    if (id == 2):
        if (g.missile2y == 0):
	    g.missile2y = g.player2y
    	    g.missile2x = g.player2x - 1
    return


def ship(id, op):
    if (op == 1):
	if (id == 1): 
	    ship = ">=-"
	    printxy(g.player1y, g.player1x, ship)
	elif (id == 2):
	    ship = "-=<"
	    printxy(g.player2y, g.player2x, ship)
	return

    if (op == 0):
	ship = "   "
	if (id == 1):
	    printxy(g.player1y, g.player1x, ship)
	elif (id == 2):
	    printxy(g.player2y, g.player2x, ship)
    return


def ai(): 
    r = random.randrange(1, 4) 
    if (r == 1 and g.player2y > g.miny):
	ship(2, 0) 
	g.player2y-=1
    if (r == 2 and g.player2y < g.maxy):
	ship(2, 0) 
	g.player2y+=1
    if (r == 3 or g.player1y == g.player2y):
	fire_missile(2) 
    return


def process_missile(id): 
    if (id == 1):
	printxy(g.missile1y, g. missile1x, " ")
	# missed, erase
	if (g.missile1x == g.player1x + 3):
	    g.missile1y = g.missile1x = 0
	    return
	g.missile1x += 1
	printxy(g.missile1y, g.missile1x, ".")
	# collision
	if (g.missile1y == g.player2y and g.missile1x == g.player2x):
	    g.missile1y = g.missile1x = 0
	    g.player1score += 1
	    g.playertoexplode = 2
	    g.i = 1
	return
    
    if (id == 2):
	printxy(g.missile2y, g. missile2x, " ")
	# missed, erase
	if (g.missile2x == g.player1x - 1):
	    g.missile2y = g.missile2x = 0
	    return
	g.missile2x -= 1
	printxy(g.missile2y, g.missile2x, ".")
	# collision
	if (g.missile2y == g.player1y and g.missile2x >= g.player1x \
	and g.missile2x < g.player1x + 3):
	    g.missile2y = g.missile2x = 0
	    g.player2score += 1
	    g.playertoexplode = 1
	    g.i = 1
    return


def win():
    if (g.player1score == 10):
	message = "PLAYER ONE WINS!!!!"
    else:
	message = "PLAYER TWO WINS!!!!"
    printxy(7, 10, message)
    printxy(9, 9, "Press 'C' to continue")

    while getch() != "c":
	pass

    return


def lose():
    if (g.playertoexplode == 1):
	x = g.player1x + 1
	y = g.player1y
    else:
	x = g.player2x + 1
	y = g.player2y
    if (g.i != 4): # magic number - explosion step?
	printxy(y - g.i, x, "*")
	printxy(y + g.i, x, "*")
	printxy(y - g.i, x - g.i, ".")
	printxy(y - g.i, x + g.i, ".")
	printxy(y + g.i, x + g.i, ".")
	printxy(y + g.i, x - g.i, ".")
    for j in range (1, 1000): # todo: check border values; possible use delay
	printxy(y, x - g.i,  '*' * (g.i * 2 + 1) )
    g.i+=1
    if (g.i < 5):
	return

    g.playertoexplode = 0
    cls()
    updatescores(g.player1score, g.player2score)
    g.player1y = g.miny + 1
    g.player2y = g.maxy - 1
    return

def loop(): 
    # noone dies, someone wins
    if (g.playertoexplode == 0 and \
	(g.player1score == 10 or g.player2score == 10)): 
	    win()
	    return

    # someone dies
    if (g.playertoexplode != 0):
	lose()
	return
    
    # rewrite ships
    ship(1, 1)
    ship(2, 1)
    # rewrite missiles
    if (g.missile1x != 0):
	process_missile(1)
    if (g.missile2x != 0):
	process_missile(2)
    # process user's control
    k = getch()
    if (k == "a" and g.player1y > g.miny):
	ship(1, 0)
	g.player1y-=1
    if (k == "z" and g.player1y < g.maxy):
	ship(1, 0)
	g.player1y+=1
    if (k == " " or k == "j"): # todo: accept space
	fire_missile(2) 
    if (k == "q"):
	cls()
	exit()

    # process ai's control
    ai() 
    return


def init():
    cls()	
    printxy(5,  8, "S P A C E   W A R")
    printxy(8,  2, "Keys: 'A' to go up")
    printxy(9,  8, "'Z' to go down")
    printxy(10, 8, "<space> to shoot")
    printxy(13, 8, "First to 10 points wins")
    printxy(16, 8, "Press <space> to start")
    g.miny = 3; g.maxy = 17 
    g.player1y  = 5;  g.player1x  = 5
    g.missile1y = 0;  g.missile1x = 0
    g.player2y  = 15; g.player2x  = 30
    g.missile2y = 0;  g.missile2x = 0
    g.player1score = 0; g.player2score = 0
    g.playertoexplode = 0
    g.i = 0
    while getch() != " ":
        pass
    cls() 
    updatescores(g.player1score, g.player2score)
    return


def main():
    init() 
    while 1:
	loop()
    return

    
if (__name__ == '__main__'):
    g = config()
    main()
    exit()
