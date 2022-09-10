from decimal import DefaultContext
from venv import create
import pygame

def createScreen():
    window = pygame.display.set_mode((800,800))
    pygame.display.set_caption('Tic Tac Toe')
    backgroundColor = (234,212,252)
    window.fill(backgroundColor)

def createBorders(window):
    #horizontal line
    pygame.draw.line(window,(0,0,0),(65,290),(735,290),width=3)
    pygame.draw.line(window,(0,0,0),(69,515),(735,515),width=3)
    #vertical lines
    pygame.draw.line(window,(0,0,0),(290,65),(290,735),width=3)
    pygame.draw.line(window,(0,0,0),(515,69),(515,735),width=3)

def draw(pos,window,shape,gameboard,turn): #draws the shape on the screen, returns True if smooth, False if box is occupied, 'win' if one side has won
    if isinstance(pos,tuple) == False:
        box = pos
    else:
        box = checkPress(pos,gameboard)
    
    if box is False:
        print('unav')
        return False
    #first row
    elif box == 0:
        window.blit(shape,(78,78))
    elif box == 1:
        window.blit(shape,(303,78))
    elif box == 2:
        window.blit(shape,(528,78))
    #second row
    elif box == 3:
        window.blit(shape,(78,303))
    elif box == 4:
        window.blit(shape,(303,303))
    elif box == 5:
        window.blit(shape,(528,303))
    #third row
    elif box == 6:
        window.blit(shape,(78,528))
    elif box == 7:
        window.blit(shape,(303,528))
    elif box == 8:
        window.blit(shape,(528,528))
    
    gameboard[box] = turn
    win = checkWin(gameboard,window)
    pygame.display.flip()
    if win == True:
        return 'win'
    
    return True

def checkPress(pos,gameboard): #returns which box is being pressed, false if that box is occupied
    print(pos)
    box = None
    x = pos[0]
    y = pos[1]
    
    #first row
    if 65 <= x <= 285 and 65 <= y <= 285:
        box = 0
    elif 290 <= x <= 290+220 and 65 <= y <= 65+220:
        box = 1
    elif 515 <= x <= 515+220 and 65 <= y <= 65+220:
        box = 2
    #second row
    elif 65 <= x <= 65+220 and 290 <= y <= 290+220:
        box = 3
    elif 290 <= x <= 290+220 and 290 <= y <= 290+220:
        box = 4
    elif 515 <= x <= 515+220 and 290 <= y <= 290+220:
        box = 5
    #third row
    elif 65 <= x <= 65+220 and 515 <= y <= 515+220:
        box = 6
    elif 290 <= x <= 290+220 and 515 <= y <= 515+220:
        box = 7
    elif 515 <= x <= 515+220 and 515 <= y <= 515+220:
        box = 8

    try: 
        if gameboard[box] != 0:
            return False
    except:
        return False
    
    return box 

def checkWin(gameboard,window): #checks if any side has won, returns True if yes
    #check horizontal
    for x in range(0,8,3):
        if gameboard[x] == gameboard[x+1] == gameboard[x+2] and gameboard[x] != 0:
            if x == 0:
                ycoor = 175
            elif x == 3:
                ycoor = 395
            elif x == 6:
                ycoor = 615

            pygame.draw.line(window,(0,0,0),(65,ycoor),(735,ycoor),width=25) #winning line

            return True

    #check vertical
    for x in range(0,3):
        if gameboard[x] == gameboard[x+3] == gameboard[x+6] and gameboard[x] != 0:
            if x == 0:
                xcoor = 175
            elif x == 1:
                xcoor = 395
            elif x == 2:
                print('yes')
                xcoor = 615

            pygame.draw.line(window,(0,0,0),(xcoor,65),(xcoor,735),width=25)

            return True

    #check diagonal
    if gameboard[0] == gameboard[4] == gameboard[8] and gameboard[4] != 0:
        pygame.draw.line(window,(0,0,0),(65,65),(735,735),width=25)
        return True

    elif gameboard[2] == gameboard[4] == gameboard[6] and gameboard[4] != 0:
        pygame.draw.line(window,(0,0,0),(65,735),(735,65),width=25)
        return True

    return False

'''minimax algorithm'''
def checkRemainingMove(gameboard):
    for x in gameboard:
        if x == 0:
            return True    
    return False

def evaluate(gameboard):
    #Check row for X or O victory
    for x in range(0,8,3):
        if gameboard[x] == gameboard[x+1] == gameboard[x+2] and gameboard[x] != 0:
            if gameboard[x] == 'o': #computer wins
                return 10
            elif gameboard[x] == 'x': #player/enemy wins
                return -10
            
    #Check columns for X or O victory
    for x in range(0,3):
        if gameboard[x] == gameboard[x+3] == gameboard[x+6] and gameboard[x] != 0:
            if gameboard[x] == 'o':
                return 10
            elif gameboard[x] == 'x':
                return -10

    #Check diagonals for X or O victory
    if gameboard[0] == gameboard[4] == gameboard[8] and gameboard[4] != 0:
        if gameboard[0] == 'o':
            return 10
        elif gameboard[0] == 'x':
            return -10
    
    elif gameboard[2] == gameboard[4] == gameboard[6] and gameboard[4] != 0:
        if gameboard[2] == 'o':
            return 10
        elif gameboard[2] == 'x':
            return -10

    return 0

def minimax(gameboard, depth, isMax):
    score = evaluate(gameboard)

    if score == 10 or score == -10:
        return score
    
    if checkRemainingMove(gameboard) == False:
        return 0
    
    if isMax:
        best = -1000

        for x in range(9):
            if gameboard[x] == 0:
                gameboard[x] = 'o'
                best = max(best,minimax(gameboard, depth+1, not isMax))
                gameboard[x] = 0

        return best
    
    else:
        best = 1000

        for x in range(9):
            if gameboard[x] == 0:
                gameboard[x] = 'x'
                best = min(best,minimax(gameboard, depth+1, not isMax))
                gameboard[x] = 0
        
        return best

def findBestMove(gameboard):
    bestVal = -1000
    bestMove = -1

    for x in range(9):
        if gameboard[x] == 0:
            gameboard[x] = 'o'
            moveVal = minimax(gameboard, 0, False)
            gameboard[x] = 0

            if moveVal > bestVal:
                bestMove = x
                bestVal = moveVal

    return bestMove

def outro(window,win,xWinScreen,oWinScreen,tiescreen): #outputs the ending screen o
    if win == 'xWins':
        window.blit(xWinScreen,(100,250))
    elif win == 'oWins':
        window.blit(oWinScreen,(100,250))
    else:
        window.blit(tiescreen,(100,250))

    pygame.display.flip()

def main(): #main function
    #screen
    window = pygame.display.set_mode((800,800))
    pygame.display.set_caption('Tic Tac Toe')
    backgroundColor = (234,212,252)

    #load images 
    circleO = pygame.image.load('Assets\circleO.png')
    circleO = pygame.transform.scale(circleO,(200,200))
    crossX = pygame.image.load('Assets\crossX.png')
    crossX = pygame.transform.scale(crossX,(200,200))
    xWinScreen = pygame.image.load(r'Assets\xWinScreen.png')
    oWinScreen = pygame.image.load(r'Assets\oWinScreen.png')
    tiescreen = pygame.image.load(r'Assets\tie.png')
    againButton = pygame.Rect(167,418,212,102) #rectangular coordinates

    exitButton = pygame.Rect(418,418,212,102)
    chooseModeScreen = pygame.image.load(r'Assets\chooseMode.png')
    vsComp = pygame.Rect(249,299,333,103)
    vsPlayer = pygame.Rect(249,422,333,103)
    
    
    # window.blit(chooseModeScreen,(110,250))
    # pygame.draw.rect(window,(255,0,0),vsPlayer)
    # pygame.draw.rect(window,(0,255,255),vsComp)


    turn = 'x'
    #setup
    gameboard = [0,0,0,0,0,0,0,0,0]
    win = False
    window.fill(backgroundColor)
    window.blit(chooseModeScreen,(110,250))
    pygame.display.flip()



    start = False
    running = True

    while running:
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                print("game quit")
                running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                # pint('gameboard = ' +str(gameboard))
                pos = pygame.mouse.get_pos()

                if start == False:
                    if vsComp.collidepoint(pos):
                        mode = 'vsComp'
                    elif vsPlayer.collidepoint(pos):
                        mode = 'vsPlayer'
                    else:
                        continue

                    window.fill(backgroundColor)
                    createBorders(window)
                    pygame.display.flip()

                    start = True

                elif win == False:
                    if mode == 'vsPlayer':
                    # pos = pygame.mouse.get_pos()
                        if turn == 'x':
                            play = draw(pos,window,crossX,gameboard,'x')
                            if play == True:
                                turn = 'o'
                            elif play == False:
                                turn = 'x'    
                            elif play == 'win':
                                print('x wins')
                                win = 'xWins'
                                outro(window,win,xWinScreen,oWinScreen,tiescreen)
                                turn = 'x'
                        elif turn == 'o':
                            play = draw(pos,window,circleO,gameboard,'o')
                            if play == True:
                                turn = 'x'
                            elif play == False:
                                turn =  'o'    
                            elif play == 'win':
                                print('o wins')
                                win = 'oWins'
                                outro(window,win,xWinScreen,oWinScreen,tiescreen)
                                turn = 'x'
                        if all(x != 0 for x in gameboard) and win == False:
                            win = 'Tie'
                            outro(window,win,xWinScreen,oWinScreen,tiescreen)
                            turn = 'x'
                        
                    if mode == 'vsComp':
                        #player moves   
                        play = draw(pos,window,crossX,gameboard,'x')
                        if play == True:
                            turn = 'o'
                        elif play == False:
                            turn = 'x'    
                        elif play == 'win':
                            print('x wins')
                            win = 'xWins'
                            outro(window,win,xWinScreen,oWinScreen,tiescreen)
                            turn = 'x'
                        
                        if all(x != 0 for x in gameboard) and win == False:#no available space
                            win = 'Tie'
                            outro(window,win,xWinScreen,oWinScreen,tiescreen)
                            turn = 'x'
                        else:
                            #computer moves
                            bestMove = findBestMove(gameboard)
                            play = draw(bestMove,window,circleO,gameboard,'o')
                            if play == 'win':
                                print('o wins')
                                win = 'oWins'
                                outro(window,win,xWinScreen,oWinScreen,tiescreen)
                                turn = 'x'
                            print(gameboard)

                else:
                    # pos = pygame.mouse.get_pos()
                    if againButton.collidepoint(pos):
                        print('again button pressed')
                        #reset
                        gameboard = [0,0,0,0,0,0,0,0,0]
                        window.fill(backgroundColor)
                        # createBorders(window)
                        window.blit(chooseModeScreen,(110,250))
                        pygame.display.flip()
                        start = False
                        win = False
                        continue
                    elif exitButton.collidepoint(pos):
                        print("Game finished, exit game")
                        running = False
                        
main()