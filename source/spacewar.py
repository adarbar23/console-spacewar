# spacewar port from basic source
# see http://jsbasic.apphb.com/SpaceWar.htm
# (c) 2014, BG

import sys
import random
import readchar # sudo pip install readchar


def cls():
    sys.stdout.write("\x1b7\x1b[2J\x1b8")
    

def printxy(y, x, text):
    x+=1 # border
    sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (y, x, text))
    sys.stdout.flush()


def getch():
    return readchar.readkey()


def updatescores(player1score, player2score): # line 400
    printxy(1, 2,  "Player 1: %s" % player1score)
    printxy(1, 24, "Player 2: %s" % player2score)
    return    


def init(): # line 10

    cls()	
    printxy(5,  8, "S P A C E   W A R")
    printxy(8,  2, "Keys: 'A' to go up")
    printxy(9,  8, "'Z' to go down")
    printxy(10, 8, "<space> to shoot")
    printxy(13, 8, "First to 10 points wins")
    printxy(16, 8, "Press <space> to start")

    while getch() != " ":
        pass

    return

def go(lineno):
    return

def gosub(lineno):
    return

def fire_missile(id): # line 700 and 800
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
    else:
	ship = "   "

    return

def ai():
    r = random.randrange(0, 50) # todo: ?basic[fix(rnd*50)]
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
    # tbd	
    return

def score(): # line 900
    return

def lost(): #line 1000    
    return

def loop(): # line 300
    
    if (g.player1score == 10 and g.playertoexplode == 0): score() 
    if (g.player2score == 10 and g.playertoexplode == 0): score()
    if (g.playertoexplode != 0): lost()
    
    print(g.player1y)

    ship(1, 1)
    ship(2, 1)
 
    if (g.missile1x != 0): process_missile(1)
    if (g.missile2x != 0): process_missile(2)

    k = getch()
    if (k == "a" and g.player1y > g.miny):
	ship(1, 0)
	g.player1y-=1
    if (k == "z" and g.player1y < g.maxy):
	ship(1, 0)
	g.player1y+=1
    if (k == " "):
	fire_missile(2) 
    if (k == "q"):
	exit()

    ai() 

    return

def main():


    init() # line 10

    g.miny = 3; g.maxy = 17 # line 100

    cls() # line 200
    g.player1y  = 5;  g.player1x  = 5
    g.missile1y = 0;  g.missile1x = 0
    g.player2y  = 15; g.player2x  = 30
    g.missile2y = 0;  g.missile2x = 0
    g.player1score = 0; g.player2score = 0
    g.playertoexplode = 0

    updatescores(g.player1score, g.player2score) # gosub 400
    
    while 1:
	loop() #300-380

    return


# if __name__ == '__main__':

class config():
	def __init__(self):
	    player1y = player1x = 0
	    missile1y =  missile1x = 0
	    player2y = player2x  = 0
	    missile2y = missile2x = 0
	    player1score = player2score = playertoexplode = 0
    
g = config()

main()

exit()

"""


400-450 SUB UPDATE SCORES

500-590 SUB AI  
  GOSUB 650 -- clear ship 1
  GOSUB 800 -- process miss 1

600-620 SUB: clear ship 1

650-680 SUB: clear ship 2

700-740 SUB: init missile 1

750-790 SUB: process missile 1

800-840 SUB: init missile 2

850-890 SUB: process missile 2

900-950 player wins, GOTO 10

1000 explode a  ship
...
goto 1030 
...
1030 -- tight loop, slowdown
??? goto 300
cls
gosub 400 -- update scores
goto 300 -- reente main loop
"""