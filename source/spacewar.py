# http://jsbasic.apphb.com/SpaceWar.htm

import sys
import readchar # sudo pip install readchar

def cls():
    sys.stdout.write("\x1b7\x1b[2J\x1b8")
    
def printxy(y, x, text):
    x+=1 # border
    sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (y, x, text))
    sys.stdout.flush()

def getch():
    return readchar.readkey()

cls()
printxy(5,  8, "S P A C E   W A R")
printxy(8,  2, "Keys: 'A' to go up")
printxy(9,  8, "'Z' to go down")
printxy(10, 8, "<space> to shoot")
printxy(13, 8, "First to 10 points wins")
printxy(16, 8, "Press <space> to start")

while getch() != " ":
  pass

# line 100
minY = 3; maxY = 17

# line 200
cls()
player1y  = 5;  player1x  = 5
missile1y = 0;  missile1x = 0
player2y  = 15; player2x  = 30
missile2y = 0;  missile2x = 0
player1score = 0; player2score = 0
playertoexplode = 0
#400()

#300 main loop

exit()

"""
i$
playerToExplode$
j$
player1y
player2y
string$
x$
y$
miny$ = 3
maxy$ = 17
space$


10 -- header
90 GOTO 90 -- wait

100 -- const

200 -- init
240 GOSUB 400 -- update scores
enter main loop:

300 -- main loop
GOTO 900 -- win condition
GOTO 1000 -- lose condition
GOSUB 750 -- process missile 1
GOSUB 850 -- process missile 2
GOSUB 610 -- clear ship 1
GOSUB 700 -- init missile 1
GOSUB 500 -- sub ai: 650 clear ship 2, 800 init missile 2
GOTO 300 -- loop

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