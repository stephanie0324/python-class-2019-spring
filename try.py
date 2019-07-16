import random, sys, pygame, time, copy
from pygame.locals import *

#畫面設定區
FPS = 1000 # FPS 值
window_width = 640  # 視窗寬度
window_height = 480  # 視窗高度
piece_size = 50  # 棋盤的高度與框度(像素)
column_number = 8  # 棋盤的列數
row_number = 8  # 棋盤的行數
whiteTile = 'whiteTile'  # white子
blackTile = 'blackTile'  # black子
EMPTY_SPACE = 'EMPTY_SPACE'  # 空格區
hintmark = 'hintmark'  # 提示
ANIMATIONSPEED = 25  # 動畫速度
X_edge = int((window_width - (column_number * piece_size)) / 2)  #設定左、右所佔的空間
Y_edge = int((window_height - (row_number * piece_size)) / 2)  #設定上、下所佔的空間

#顏色區
#              R    G    B
white        = (255, 255, 255)
black        = (  0,   0,   0)
green        = (  0, 155,   0)
blue         = (  0,  50, 255)
red          = (255,   0,   0)
gold         = (255, 215,   0)
seashell     = (255, 245, 238)

#文字框框顏色
text_rect_color_blue = blue
text_rect_color_green = green
text_rect_color_white = white
text_rect_color_gold = gold
text_rect_color_seashell = seashell

#棋盤線條顏色
line_color = black

#字體顏色
text_color = black
HINTCOLOR = red

#AI設定
POSITIVE_INFINITE = float('inf')
NEGATIVE_INFINITE = float('-inf')

#weight matrix
WEIGHT_MATRIX = [
                [99, -8, 8, 6, 6, 8, -8,99],
                [-8,-24,-4,-3,-3,-4,-24,-8],
                [ 8, -4, 7, 4, 4, 7, -4, 8],
                [ 6, -3, 4, 0, 0, 4, -3, 6],
                [ 6, -3, 4, 0, 0, 4, -3, 6],
                [ 8, -4, 7, 4, 4, 7, -4, 8],
                [-8,-24,-4,-3,-3,-4,-24,-8],
                [99, -8, 8, 6, 6, 8, -8,99]
                ]


def main():
    global MAINCLOCK, DISPLAYSURF, FONT, BIGFONT, BGIMAGE , newGameSurf ,newGameRect , hintsRect , hintsSurf, text2Surf,text2Rect,yesRect,yesSurf,noRect,noSurf
    #設計視窗樣式:
    pygame.init()
    MAINCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption('Reversi')                   #遊戲名稱
    FONT = pygame.font.Font('freesansbold.ttf', 16)         #設定字體與大小
    BIGFONT = pygame.font.Font('freesansbold.ttf', 32)

    #遊戲背景
    boardImage = pygame.image.load('wood.png')
    boardImage = pygame.transform.smoothscale(boardImage, (column_number * piece_size, row_number * piece_size))  #將圖片伸縮制方匡大小
    #將boardImage鑲入棋盤
    boardImageRect = boardImage.get_rect()        
    boardImageRect.topleft = (X_edge, Y_edge)            #找出放置棋盤最左上角的座標
    BGIMAGE = pygame.image.load('background.jpg')        #輸入背景圖
    BGIMAGE = pygame.transform.smoothscale(BGIMAGE, (window_width, window_height))  #將背景圖鑲入視窗
    BGIMAGE.blit(boardImage, boardImageRect)             #背景加上棋盤圖

    #New game 選項:
    newGameSurf = FONT.render('New Game', True, text_color, text_rect_color_gold)
    newGameRect = newGameSurf.get_rect()
    newGameRect.topright = (window_width - 8, 10)
    #Hint 選項:
    hintsSurf = FONT.render('Hints', True, text_color, text_rect_color_gold)
    hintsRect = hintsSurf.get_rect()
    hintsRect.topright = (window_width - 8, 40)

    # 詢問玩家是否再來一局:
    text2Surf = BIGFONT.render('Play again?', True, text_color, text_rect_color_white)
    text2Rect = text2Surf.get_rect()
    text2Rect.center = (int(window_width / 2), int(window_height / 2) + 50)
    # 製作Yes鈕:
    yesSurf = BIGFONT.render('Yes', True, text_color, text_rect_color_white)
    yesRect = yesSurf.get_rect()
    yesRect.center = (int(window_width / 2) - 60, int(window_height / 2) + 90)
    # 製作No鈕:
    noSurf = BIGFONT.render('No', True, text_color, text_rect_color_white)
    noRect = noSurf.get_rect()
    noRect.center = (int(window_width / 2) + 60, int(window_height / 2) + 90)
    
    while True:
        #進入遊戲
        newImage = pygame.image.load('new.jpg')        #遊戲封面
        newImage = pygame.transform.smoothscale(newImage,(window_width,window_height))
        DISPLAYSURF.blit(newImage,[0,0])
        choice = play_game()     #是否進入遊戲
        if choice == 'play':
            Enter_the_game()
        else:
            break

def Enter_the_game():
    mainBoard = Open_new_game()
    Remake_board(mainBoard)
    showHints = False
    difficulty = ''
    playerImage = pygame.image.load('player.png')
    playerImage = pygame.transform.smoothscale(playerImage,(window_width,window_height))
    DISPLAYSURF.blit(playerImage,[0,0])
    player_num = Choose_player_number()
    if player_num =='one':
        difficultyImage = pygame.image.load('difficulty.png')
        difficultyImage = pygame.transform.smoothscale(difficultyImage,(window_width,window_height))
        DISPLAYSURF.blit(difficultyImage,[0,0])
        difficulty=Choose_difficulty()
        if difficulty=='hard':        #與ai玩     
            colorImage = pygame.image.load('blackorwhite.png')
            colorImage = pygame.transform.smoothscale(colorImage,(window_width,window_height))
            DISPLAYSURF.blit(colorImage,[0,0])
            playerTile, aiTile = Choose_tile_color()
            mainBoard = Open_new_game()
            Remake_board(mainBoard)
            Draw_the_board(mainBoard)
            showHints = False
            turn = random.choice(['ai', 'player'])
            #遊戲:
            while True:
                #玩家回合:
                if turn == 'player':
                    #如果玩家不能move則遊戲結束:
                    if Get_valid_move(mainBoard, playerTile) == []:
                        break
                    # 繪製遊戲board:
                    Draw_the_board(mainBoard)
                    Score_turn_random(mainBoard, playerTile, aiTile, turn)
                    #顯示New Game及 Hint的按鈕:
                    DISPLAYSURF.blit(newGameSurf, newGameRect)
                    DISPLAYSURF.blit(hintsSurf, hintsRect)
                    MAINCLOCK.tick(FPS)
                    pygame.display.update()
                    move = None
                    # 如果玩家沒做出valid_move就繼續迴圈
                    while move == None:
                        if showHints:
                            hints(mainBoard, boardToDraw , playerTile, aiTile,turn)
                            DISPLAYSURF.blit(newGameSurf, newGameRect)
                            DISPLAYSURF.blit(hintsSurf, hintsRect)
                            MAINCLOCK.tick(FPS)
                            pygame.display.update()
                        else:
                            boardToDraw = mainBoard
                            Draw_the_board(boardToDraw)
                            Score_turn_random(boardToDraw, playerTile, aiTile, turn)
                            MAINCLOCK.tick(FPS)
                            DISPLAYSURF.blit(newGameSurf, newGameRect)
                            DISPLAYSURF.blit(hintsSurf, hintsRect)
                            MAINCLOCK.tick(FPS)
                            pygame.display.update()
                        Check_skip()
                        #Click點擊位置:
                        for event in pygame.event.get():
                            if event.type == MOUSEBUTTONUP:
                                Clickx, Clicky = event.pos
                                #點擊Open_new_game:
                                if newGameRect.collidepoint( (Clickx, Clicky) ):
                                    pygame.draw.rect(DISPLAYSURF,black,[0,0,window_width,window_height])
                                    return True
                                # 點擊給提示:
                                elif hintsRect.collidepoint( (Clickx, Clicky) ):
                                    showHints = not showHints
                                move = Get_click_position_board(Clickx, Clicky)
                                if move != None and not This_is_valid_move(mainBoard, playerTile, move[0], move[1]):
                                    move = None
                                elif move != None and This_is_valid_move(mainBoard, playerTile, move[0], move[1]):
                                    break                
                    #Make_move並結束回合:
                    Make_move(mainBoard, playerTile, move[0], move[1], True)
                    #只有電腦還能move才會進入電腦回合:
                    if Get_valid_move(mainBoard, aiTile) != []:
                        turn = 'ai'
                        continue
                    else:
                        break
                else:
                    #Draw_the_board:
                    Draw_the_board(mainBoard)
                    Score_turn_random(mainBoard, playerTile, aiTile, turn)
                    #繪製New Game及 Hint的按鈕:
                    DISPLAYSURF.blit(newGameSurf, newGameRect)
                    DISPLAYSURF.blit(hintsSurf, hintsRect)
                    MAINCLOCK.tick(FPS)
                    pygame.display.update()
                    暫停 = time.time() + random.randint(5, 15) * 0.1  #暫停一下讓電腦看起來像思考
                    while time.time() < 暫停:
                        pygame.display.update()
                    abs = AlphaBetaSearch(aiTile , 3 ,mainBoard)
                    nex = abs.executeSearch(mainBoard)
                    mainBoard = nex
                    #只有玩家還能move才會進入玩家回合:
                    if Get_valid_move(mainBoard, playerTile) != []:
                        turn = 'player'
                        continue
                    else:
                        break
            #展示最後score:
            Draw_the_board(mainBoard)
            scores = Get_current_score(mainBoard)
            playagainImage = pygame.image.load('newgameback.jpg')
            DISPLAYSURF.blit(playagainImage,[0,0])
            #最後評分樣貌:
            if scores[playerTile] > scores[aiTile]:
                R = 'You beat the computer by %s points! Congratulations!' %(scores[playerTile] - scores[aiTile])
            elif scores[playerTile] < scores[aiTile]:
                R = 'You lost. The computer beat you by %s points.' %(scores[aiTile] - scores[playerTile])
            else:
                R = 'The game was a tie!'
            RSurf = FONT.render(R, True, text_color, text_rect_color_white)
            RRect = RSurf.get_rect()
            RRect.center = (int(window_width / 2), int(window_height / 2))
            DISPLAYSURF.blit(RSurf, RRect)
            #顯示再玩一次
            DISPLAYSURF.blit(text2Surf, text2Rect)
            DISPLAYSURF.blit(yesSurf, yesRect)
            DISPLAYSURF.blit(noSurf, noRect)
            pygame.display.update()
            MAINCLOCK.tick(FPS)
            while True:
                Check_skip()
                for event in pygame.event.get():
                    pygame.draw.rect(DISPLAYSURF,black,[0,0,window_width,window_height])
                    if event.type == MOUSEBUTTONUP:
                        Clickx, Clicky = event.pos
                        if yesRect.collidepoint( (Clickx, Clicky) ):
                            return True
                        elif noRect.collidepoint( (Clickx, Clicky) ):
                            return False

        elif difficulty=='easy':
            colorImage = pygame.image.load('blackorwhite.png')
            colorImage = pygame.transform.smoothscale(colorImage,(window_width,window_height))
            DISPLAYSURF.blit(colorImage,[0,0])
            playerTile, computerTile = Choose_tile_color()
            mainBoard = Open_new_game()
            Remake_board(mainBoard)
            Draw_the_board(mainBoard)
            showHints = False
            turn = random.choice(['computer', 'player'])
            #遊戲:
            while True:
                #玩家回合:
                if turn == 'player':
                    #如果玩家不能move則遊戲結束:
                    if Get_valid_move(mainBoard, playerTile) == []:
                        break
                    # 繪製遊戲board:
                    Draw_the_board(mainBoard)
                    Score_turn_random(mainBoard, playerTile, computerTile, turn)
                    DISPLAYSURF.blit(newGameSurf, newGameRect)
                    DISPLAYSURF.blit(hintsSurf, hintsRect)
                    MAINCLOCK.tick(FPS)
                    pygame.display.update()
                    move = None
                    #如果玩家沒做出valid_move就繼續迴圈 
                    while move == None:
                        if showHints:
                            hints(mainBoard, boardToDraw , playerTile, computerTile,turn)
                            #顯示hints&newgame
                            DISPLAYSURF.blit(newGameSurf, newGameRect)
                            DISPLAYSURF.blit(hintsSurf, hintsRect)
                            MAINCLOCK.tick(FPS)
                            pygame.display.update()
                        else:
                            boardToDraw = mainBoard
                            Draw_the_board(boardToDraw)
                            Score_turn_random(boardToDraw, playerTile, computerTile, turn)
                            MAINCLOCK.tick(FPS)
                            #顯示New Game及 Hint的按鈕:
                            DISPLAYSURF.blit(newGameSurf, newGameRect)
                            DISPLAYSURF.blit(hintsSurf, hintsRect)
                            MAINCLOCK.tick(FPS)
                            pygame.display.update()
                        Check_skip()
                        #Click點擊位置:
                        for event in pygame.event.get():
                            if event.type == MOUSEBUTTONUP:
                                Clickx, Clicky = event.pos
                                #點擊Open_new_game:
                                if newGameRect.collidepoint( (Clickx, Clicky) ):
                                    pygame.draw.rect(DISPLAYSURF,black,[0,0,window_width,window_height])
                                    return True
                                # 點擊給提示:
                                elif hintsRect.collidepoint( (Clickx, Clicky) ):
                                    showHints = not showHints
                                move = Get_click_position_board(Clickx, Clicky)
                                if move != None and not This_is_valid_move(mainBoard, playerTile, move[0], move[1]):
                                    move = None
                                elif move != None and This_is_valid_move(mainBoard, playerTile, move[0], move[1]):
                                    break                
                    #Make_move並結束回合:
                    Make_move(mainBoard, playerTile, move[0], move[1], True)
                    #只有電腦還能move才會進入電腦回合:
                    if Get_valid_move(mainBoard, computerTile) != []:
                        turn = 'computer'
                        continue
                    else:
                        break
                else:
                    #Draw_the_board:
                    Draw_the_board(mainBoard)
                    Score_turn_random(mainBoard, playerTile, computerTile, turn)
                    #顯示New Game及 Hint的按鈕:
                    DISPLAYSURF.blit(newGameSurf, newGameRect)
                    DISPLAYSURF.blit(hintsSurf, hintsRect)
                    MAINCLOCK.tick(FPS)
                    pygame.display.update()
                    暫停 = time.time() + random.randint(5, 15) * 0.1
                    while time.time() < 暫停:
                        pygame.display.update()
                        #Make_move並結束回合:
                    x, y = Get_random_move(mainBoard, computerTile)
                    Make_move(mainBoard, computerTile, x, y, True)

                    #只有玩家還能move才會進入玩家回合:
                    if Get_valid_move(mainBoard, playerTile) != []:
                        turn = 'player'
                        continue
                    else:
                        break
            #展示最後score:
            Draw_the_board(mainBoard)
            scores = Get_current_score(mainBoard)
            playagainImage = pygame.image.load('newgameback.jpg')
            DISPLAYSURF.blit(playagainImage,[0,0])
            #最後評分出樣貌:
            if scores[playerTile] > scores[computerTile]:
                R = 'You beat the computer by %s points! Congratulations!' %(scores[playerTile] - scores[computerTile])
            elif scores[playerTile] < scores[computerTile]:
                R = 'You lost. The computer beat you by %s points.' %(scores[computerTile] - scores[playerTile])
            else:
                R = 'The game was a tie!'
            RSurf = FONT.render(R, True, text_color, text_rect_color_white)
            RRect = RSurf.get_rect()
            RRect.center = (int(window_width / 2), int(window_height / 2))
            DISPLAYSURF.blit(RSurf, RRect)
            #顯示再玩一次
            DISPLAYSURF.blit(text2Surf, text2Rect)
            DISPLAYSURF.blit(yesSurf, yesRect)
            DISPLAYSURF.blit(noSurf, noRect)
            pygame.display.update()
            MAINCLOCK.tick(FPS)
            while True:
                Check_skip()
                for event in pygame.event.get():
                    pygame.draw.rect(DISPLAYSURF,black,[0,0,window_width,window_height])
                    if event.type == MOUSEBUTTONUP:
                        Clickx, Clicky = event.pos
                        if yesRect.collidepoint( (Clickx, Clicky) ):
                            return True
                        elif noRect.collidepoint( (Clickx, Clicky) ):
                            return False
    
    #兩個玩家    
    elif player_num =='two':
        player_1_tile , player_2_tile = blackTile , whiteTile #直接分配旗子顏色(1為黑棋, 2為白棋)
        mainBoard = Open_new_game()
        Remake_board(mainBoard)
        Draw_the_board(mainBoard)
        showHints = False
        turn = random.choice(['player_1', 'player_2'])
        #遊戲:
        while True:
            #玩家回合:
            if turn == 'player_1':
                #如果玩家不能move則遊戲結束:
                    if Get_valid_move(mainBoard, player_1_tile) == []:
                        break
                    # 繪製遊戲board:
                    Draw_the_board(mainBoard)
                    Score_turn_player(mainBoard, player_1_tile, player_2_tile, turn)
                    #顯示New Game及 Hint的按鈕:
                    DISPLAYSURF.blit(newGameSurf, newGameRect)
                    DISPLAYSURF.blit(hintsSurf, hintsRect)
                    MAINCLOCK.tick(FPS)
                    pygame.display.update()
                    move = None
                    # 如果玩家沒做出valid_move就繼續迴圈
                    while move == None:
                        if showHints:
                            hints(mainBoard, boardToDraw , player_1_tile, player_2_tile,turn)
                            #顯示New Game及 Hint的按鈕:
                            DISPLAYSURF.blit(newGameSurf, newGameRect)
                            DISPLAYSURF.blit(hintsSurf, hintsRect)
                            MAINCLOCK.tick(FPS)
                            pygame.display.update()
                        else:
                            boardToDraw = mainBoard
                            Draw_the_board(boardToDraw)
                            Score_turn_player(boardToDraw, player_1_tile, player_2_tile, turn)
                            MAINCLOCK.tick(FPS)
                            #顯示New Game及 Hint的按鈕:
                            DISPLAYSURF.blit(newGameSurf, newGameRect)
                            DISPLAYSURF.blit(hintsSurf, hintsRect)
                            MAINCLOCK.tick(FPS)
                            pygame.display.update()
                        Check_skip()
                        #Click點擊位置:
                        for event in pygame.event.get():
                            if event.type == MOUSEBUTTONUP:
                                Clickx, Clicky = event.pos
                                #點擊Open_new_game:
                                if newGameRect.collidepoint( (Clickx, Clicky) ):
                                    pygame.draw.rect(DISPLAYSURF,black,[0,0,window_width,window_height])
                                    return True
                                # 點擊給提示:
                                elif hintsRect.collidepoint( (Clickx, Clicky) ):
                                    showHints = not showHints
                                move = Get_click_position_board(Clickx, Clicky)
                                if move != None and not This_is_valid_move(mainBoard, player_1_tile, move[0], move[1]):
                                    move = None
                                elif move != None and This_is_valid_move(mainBoard, player_1_tile, move[0], move[1]):
                                    break                
                    #Make_move並結束回合:
                    Make_move(mainBoard, player_1_tile, move[0], move[1], True)
                    #只有電腦還能move才會進入電腦回合:
                    if Get_valid_move(mainBoard, player_2_tile) != []:
                        turn = 'player_2'
                        continue
                    else:
                        break
            else:
                if Get_valid_move(mainBoard, player_2_tile) == []:
                    break
                # 繪製遊戲board:
                Draw_the_board(mainBoard)
                Score_turn_player(mainBoard, player_1_tile, player_2_tile, turn)
                #顯示New Game及 Hint的按鈕:
                DISPLAYSURF.blit(newGameSurf, newGameRect)
                DISPLAYSURF.blit(hintsSurf, hintsRect)
                MAINCLOCK.tick(FPS)
                pygame.display.update()
                move = None
                # 如果玩家沒做出valid_move就繼續迴圈
                while move == None:
                    if showHints:
                        boardToDraw = Get_current_valid_move(mainBoard, player_2_tile)
                        Draw_the_board(boardToDraw)
                        Score_turn_player(boardToDraw, player_1_tile, player_2_tile, turn)
                        MAINCLOCK.tick(FPS)
                        #顯示New Game及 Hint的按鈕:
                        DISPLAYSURF.blit(newGameSurf, newGameRect)
                        DISPLAYSURF.blit(hintsSurf, hintsRect)
                        MAINCLOCK.tick(FPS)
                        pygame.display.update()
                    else:
                        boardToDraw = mainBoard
                        Draw_the_board(boardToDraw)
                        Score_turn_player(boardToDraw, player_1_tile, player_2_tile, turn)
                        MAINCLOCK.tick(FPS)
                        #顯示New Game及 Hint的按鈕:
                        DISPLAYSURF.blit(newGameSurf, newGameRect)
                        DISPLAYSURF.blit(hintsSurf, hintsRect)
                        MAINCLOCK.tick(FPS)
                        pygame.display.update()
                    Check_skip()
                    #Click點擊位置:
                    for event in pygame.event.get():
                        if event.type == MOUSEBUTTONUP:
                            Clickx, Clicky = event.pos
                            #點擊Open_new_game:
                            if newGameRect.collidepoint( (Clickx, Clicky) ):
                                pygame.draw.rect(DISPLAYSURF,black,[0,0,window_width,window_height])
                                return True
                            # 點擊給提示:
                            elif hintsRect.collidepoint( (Clickx, Clicky) ):
                                showHints = not showHints
                            move = Get_click_position_board(Clickx, Clicky)
                            if move != None and not This_is_valid_move(mainBoard, player_2_tile, move[0], move[1]):
                                move = None
                            elif move != None and This_is_valid_move(mainBoard, player_2_tile, move[0], move[1]):
                                break                
                #Make_move並結束回合:
                Make_move(mainBoard, player_2_tile, move[0], move[1], True)
                #只有電腦還能move才會進入電腦回合:
                if Get_valid_move(mainBoard, player_1_tile) != []:
                    turn = 'player_1'
                    continue
                else:
                    break
        #展示最後score:
        Draw_the_board(mainBoard)
        scores = Get_current_score(mainBoard)
        playagainImage = pygame.image.load('newgameback.jpg')
        DISPLAYSURF.blit(playagainImage,[0,0])
        #最後評分樣貌:
        if scores[player_1_tile] > scores[player_2_tile]:
            R = 'Player_1 beat Player_2 by %s points! Congratulations!' %(scores[player_1_tile] - scores[player_2_tile])
        elif scores[player_1_tile] < scores[Player_2_tile]:
            R = 'Player_2 beat Player_1 by %s points.' %(scores[player_2_tile] - scores[player_1_tile])
        else:
            R = 'The game was a tie!'
        RSurf = FONT.render(R, True, text_color, text_rect_color_white)
        RRect = RSurf.get_rect()
        RRect.center = (int(window_width / 2), int(window_height / 2))
        DISPLAYSURF.blit(RSurf, RRect)
        #顯示再玩一次
        DISPLAYSURF.blit(text2Surf, text2Rect)
        DISPLAYSURF.blit(yesSurf, yesRect)
        DISPLAYSURF.blit(noSurf, noRect)
        pygame.display.update()
        MAINCLOCK.tick(FPS)
        while True:
            Check_skip()
            for event in pygame.event.get():
                pygame.draw.rect(DISPLAYSURF,black,[0,0,window_width,window_height])
                if event.type == MOUSEBUTTONUP:
                    Clickx, Clicky = event.pos
                    if yesRect.collidepoint( (Clickx, Clicky) ):
                        return True
                    elif noRect.collidepoint( (Clickx, Clicky) ):
                        return False
         
#要不要玩
def play_game():
    #play 選項
    playSurf = BIGFONT.render('Play', True, text_color, text_rect_color_white)
    playRect = playSurf.get_rect()
    playRect.center = (int(window_width / 2) - 120, int(window_height / 2) + 180)
    #quit 選項
    quitSurf = BIGFONT.render('Quit', True, text_color, text_rect_color_white)
    quitRect = quitSurf.get_rect()
    quitRect.center = (int(window_width / 2) + 100, int(window_height / 2) + 180)
    while True:
        Check_skip()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                Clickx, Clicky = event.pos
                if playRect.collidepoint( (Clickx, Clicky) ):
                    return 'play'
                elif quitRect.collidepoint( (Clickx, Clicky) ):
                    return 'quit'  
        DISPLAYSURF.blit(playSurf, playRect)
        DISPLAYSURF.blit(quitSurf, quitRect)
        pygame.display.update()
        MAINCLOCK.tick(FPS)        

#選擇玩家數
def Choose_player_number():
    playerSurf=FONT.render('One player or two players?', True, text_color, text_rect_color_white)
    playerRect = playerSurf.get_rect()
    playerRect.center = (int(window_width / 2), int(window_height / 2)+100)

    #one 選項
    oneSurf = BIGFONT.render('One', True, text_color, text_rect_color_white)
    oneRect = oneSurf.get_rect()
    oneRect.center = (int(window_width / 2) - 160, int(window_height / 2) + 140)
    #two 選項
    twoSurf = BIGFONT.render('Two', True, text_color, text_rect_color_white)
    twoRect = twoSurf.get_rect()
    twoRect.center = (int(window_width / 2) + 160, int(window_height / 2) + 140)
    while True:
        Check_skip()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                Clickx, Clicky = event.pos
                if oneRect.collidepoint( (Clickx, Clicky) ):
                    return 'one'
                elif twoRect.collidepoint( (Clickx, Clicky) ):
                    return 'two'
        DISPLAYSURF.blit(playerSurf, playerRect)
        DISPLAYSURF.blit(oneSurf, oneRect)
        DISPLAYSURF.blit(twoSurf, twoRect)
        pygame.display.update()
        MAINCLOCK.tick(FPS)
    

#選擇難度
def Choose_difficulty():
    diffSurf = FONT.render('Easy or Hard?', True, text_color, text_rect_color_white)
    diffRect =diffSurf.get_rect()
    diffRect.center = (int(window_width / 2), int(window_height / 2)+100)
    #easy 選項
    easySurf = BIGFONT.render('Easy', True, text_color, text_rect_color_white)
    easyRect = easySurf.get_rect()
    easyRect.center = (int(window_width / 2) - 160, int(window_height / 2) + 140)
    #hard 選項
    hardSurf = BIGFONT.render('Hard', True, text_color, text_rect_color_white)
    hardRect = hardSurf.get_rect()
    hardRect.center = (int(window_width / 2) + 160, int(window_height / 2) + 140)  
    while True:
        Check_skip()
        for event in pygame.event.get(): 
            if event.type == MOUSEBUTTONUP:
                Clickx, Clicky = event.pos
                if easyRect.collidepoint( (Clickx, Clicky) ):
                    return 'easy'
                elif hardRect.collidepoint( (Clickx, Clicky) ):
                    return 'hard'
        DISPLAYSURF.blit(diffSurf, diffRect)
        DISPLAYSURF.blit(easySurf, easyRect)
        DISPLAYSURF.blit(hardSurf, hardRect)
        pygame.display.update()
        MAINCLOCK.tick(FPS)


#選擇黑棋或白棋    
def Choose_tile_color():
    textSurf = FONT.render('Do you want to be white or black?', True, text_color, text_rect_color_white)
    textRect = textSurf.get_rect()
    textRect.center = (int(window_width / 2), int(window_height / 2)+100)
    #white 選項
    xSurf = BIGFONT.render('white', True, text_color, text_rect_color_white)
    xRect = xSurf.get_rect()
    xRect.center = (int(window_width / 2) - 160, int(window_height / 2) + 140)
    #black 選項
    oSurf = BIGFONT.render('Black', True, text_color, text_rect_color_white)
    oRect = oSurf.get_rect()
    oRect.center = (int(window_width / 2) + 160, int(window_height / 2) + 140)
    while True:
        Check_skip()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                Clickx, Clicky = event.pos
                if xRect.collidepoint( (Clickx, Clicky) ):
                    return [whiteTile, blackTile]
                elif oRect.collidepoint( (Clickx, Clicky) ):
                    return [blackTile, whiteTile]
        DISPLAYSURF.blit(textSurf, textRect)
        DISPLAYSURF.blit(xSurf, xRect)
        DISPLAYSURF.blit(oSurf, oRect)
        pygame.display.update()
        MAINCLOCK.tick(FPS)

#開心局
def Open_new_game():
    #創建一乾乾淨淨的新board:
    board = []
    for i in range(column_number):
        board.append([EMPTY_SPACE] * row_number)
    return board

#複製版面上的棋局
def Get_current_valid_move(board, Tile):
#回傳標記上hint的board:
    hintboard = copy.deepcopy(board)
    for x, y in Get_valid_move(hintboard, Tile):
        hintboard[x][y] = hintmark
    return hintboard

#有效移動
def Get_valid_move(board, Tile):
#回傳所有有效的move:
    valid_move = []
    for x in range(column_number):
        for y in range(row_number):
            if This_is_valid_move(board, Tile, x, y) != False:
                valid_move.append((x, y))
    return valid_move

#取得分數(算棋子數)
def Get_current_score(board):
    wscore = 0
    bscore= 0
    for x in range(column_number):
        for y in range(row_number):
            if board[x][y] == whiteTile:
                wscore += 1
            if board[x][y] == blackTile:
                bscore += 1
    return {whiteTile:wscore, blackTile:bscore}

#棋子在版面上的條件
def On_the_board(x, y):
# TileOn_the_board的條件:
    return x >= 0 and x < column_number and y >= 0 and y < row_number

#重製版子(恢復成原始狀態)
def Remake_board(board):
    # 宣告一為空的board:
    for x in range(column_number):
        for y in range(row_number):
            board[x][y] = EMPTY_SPACE
    
    # 將origin的二black子二white子加入:
    board[3][3] = whiteTile
    board[3][4] = blackTile
    board[4][3] = blackTile
    board[4][4] = whiteTile

#有效移動(下棋可吃掉對方棋子)
def This_is_valid_move(board, Tile, Originx, Originy):
# 如果不是valid_move 回傳 False
# 如果是valid_move 回傳 所有被捕獲Tile的位置清單
    if board[Originx][Originy] != EMPTY_SPACE or not On_the_board(Originx, Originy):
        return False
    board[Originx][Originy] = Tile
    if Tile == whiteTile:
        otherTile = blackTile
    else:
        otherTile = whiteTile
    flippedTile = []
    # 檢測八個direction:
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = Originx, Originy
        x += xdirection
        y += ydirection
        if not On_the_board(x, y):
            continue
        #若是此direction不為自己Tile的direction，便往此direction動:
        if On_the_board(x, y) and board[x][y] == otherTile:
            x += xdirection
            y += ydirection
            if not On_the_board(x, y):
                continue
            while board[x][y] == otherTile:
                x += xdirection
                y += ydirection
                if not On_the_board(x, y):
                    break 
            if not On_the_board(x, y):
                    continue
        #碰到自己的顏色:
            if board[x][y] == Tile:
                while True:
                    x -= xdirection
                    y -= ydirection
                    if x == Originx and y == Originy:
                        break
                    flippedTile.append([x, y])
    board[Originx][Originy] = EMPTY_SPACE 
    if len(flippedTile) == 0: # 若不會有Tile被翻，此move為非valid_move
        return False
    return flippedTile

#在背景上繪製棋盤
def Draw_the_board(board):
    DISPLAYSURF.blit( BGIMAGE , BGIMAGE.get_rect())
    #繪製棋盤網格
    for x in range (column_number + 1):
        #畫橫的線
        xorigin = (x * piece_size) + X_edge
        yorigin = Y_edge
        xend = (x * piece_size ) + X_edge
        yend = Y_edge + (row_number * piece_size)
        pygame.draw.line(DISPLAYSURF,line_color,(xorigin,yorigin),(xend,yend))
    for y in range(row_number + 1):
        #畫直的線
        yorigin = (y * piece_size) + Y_edge
        xorigin = X_edge
        yend = (y * piece_size ) + Y_edge
        xend = X_edge + (row_number * piece_size)
        pygame.draw.line(DISPLAYSURF,line_color,(xorigin,yorigin),(xend,yend))
        #繪製black子、white和提示子
        for x in range(column_number):
            for y in range(row_number):
                centralx , centraly = Transformation(x,y)
                if board[x][y] == whiteTile or board[x][y] == blackTile:
                    if board[x][y] == whiteTile:
                        tileColor = white
                    else:
                        tileColor = black
                    pygame.draw.circle(DISPLAYSURF, tileColor, (centralx, centraly), int(piece_size / 2) - 4)
                if board[x][y] == hintmark:
                    pygame.draw.rect(DISPLAYSURF,HINTCOLOR,(centralx-4,centraly-4,8,8))

#改變座標
def Transformation(x, y):
    return X_edge + x * piece_size + int(piece_size / 2), Y_edge + y * piece_size + int(piece_size / 2)

#翻旗子
def Flip_tile(flippedTile, tileColor, additionalTile):
    if tileColor == whiteTile:
        additionalTileColor = black
    else:
        additionalTileColor = white
    additionalTileX, additionalTileY = Transformation(additionalTile[0], additionalTile[1])
    pygame.draw.circle(DISPLAYSURF, additionalTileColor, (additionalTileX, additionalTileY), int(piece_size /2) - 4)
    pygame.display.update()
    for rgbValues in range(0, 255, int(ANIMATIONSPEED * 2.55)):
        if rgbValues > 255:
            rgbValues = 255
        elif rgbValues < 0:
            rgbValues = 0
        if tileColor == whiteTile:
            color = tuple([rgbValues] * 3) # rgbValues goes from 0 to 255
        elif tileColor == blackTile:
            color = tuple([255 - rgbValues] * 3) # rgbValues goes from 255 to 0
        for x, y in flippedTile:
            centralx, centraly = Transformation(x, y)
            pygame.draw.circle(DISPLAYSURF, color, (centralx, centraly), int(piece_size / 2) - 4)
            pygame.display.update()
            MAINCLOCK.tick(FPS)
            Check_skip()

#顯示分數與輪到誰(電腦版)
def Score_turn_random(board, playerTile, computerTile, turn):
#顯示比賽資訊
    scores = Get_current_score(board)
    scoreSurf = FONT.render("Player score: %s    Computer score: %s    %s's Turn" % (str(scores[playerTile]), str(scores[computerTile]), turn.title()), True, text_color)
    scoreRect = scoreSurf.get_rect()
    scoreRect.bottomleft = (10, window_height - 5)
    colorSurf = FONT.render('Player color: %s    Computer color: %s   ' % (playerTile, computerTile), True, text_color)
    colorRect = colorSurf.get_rect()
    colorRect.topleft = (10,5)
    DISPLAYSURF.blit(colorSurf,colorRect)
    DISPLAYSURF.blit(scoreSurf, scoreRect)
    return DISPLAYSURF

#顯示分數與輪到誰(玩家版)
def Score_turn_player(board, playerTile, computerTile, turn):
#顯示比賽資訊
    scores = Get_current_score(board)
    scoreSurf = FONT.render("Player_1 score: %s    player_2_score: %s        %s's Turn" % (str(scores[playerTile]), str(scores[computerTile]), turn.title()), True, text_color)
    scoreRect = scoreSurf.get_rect()
    scoreRect.bottomleft = (10, window_height - 5)
    colorSurf = FONT.render('Player_1 color: %s    Player_2 color: %s   ' % (playerTile, computerTile), True, text_color)
    colorRect = colorSurf.get_rect()
    colorRect.topleft = (10,5)
    DISPLAYSURF.blit(colorSurf,colorRect)
    DISPLAYSURF.blit(scoreSurf, scoreRect)
    return DISPLAYSURF

#簡單電腦算出下棋後吃掉的棋子的多寡，並選出最高
def Get_random_move(board, randomTile):
    possiblemove = Get_valid_move(board, randomTile)
    random.shuffle(possiblemove)
    # 只要有可能優先move至角
    for x, y in possiblemove:
        if InCorner(x, y):
            return [x, y]
    best_score_random = -1
    for x, y in possiblemove:
        hintboard = copy.deepcopy(board)
        Make_move(hintboard,randomTile, x, y)
        score = Get_current_score(hintboard)[randomTile]
        if score > best_score_random:
            best_move_random = [x, y]
            best_score_random = score
    return best_move_random

#四個角落的位置
def InCorner(x, y):
    #回傳四個角落的座標:
    return (x == 0 and y == 0) or (x == column_number and y == 0) or (x == 0 and y == row_number) or (x == column_number and y == row_number)

#下棋後的棋盤輸出
def Make_move(board, Tile, Originx, Originy, realMove=False):
    flippedTile = This_is_valid_move(board, Tile, Originx, Originy)
    if flippedTile == False:
        return False
    board[Originx][Originy] = Tile
    if realMove:
        Flip_tile(flippedTile, Tile, (Originx, Originy))
        for x, y in flippedTile:
            board[x][y] = Tile
    return True

#確認點擊位置
def Get_click_position_board(Clickx, Clicky):
    #取得被點擊的棋盤方格位置:
    for x in range(column_number):
        for y in range(row_number):
            if Clickx > x * piece_size + X_edge and Clickx < (x + 1) * piece_size + X_edge and Clicky > y * piece_size + Y_edge and Clicky < (y + 1) * piece_size + Y_edge:
                return (x, y)
    return None

#退出
def Check_skip():
    for event in pygame.event.get((QUIT, KEYUP)):
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
#提示
def hints(mainBoard ,boardToDraw , playerTile , computerTile , turn):
    boardToDraw = Get_current_valid_move(mainBoard, playerTile)
    Draw_the_board(boardToDraw)
    Score_turn_random(boardToDraw, playerTile, computerTile, turn)
    MAINCLOCK.tick(FPS)


#ai
class AlphaBetaSearch(object):
    """docstring for AlphaBetaSearch"""
    def __init__(self,initial_player, depth , state):
        self.depth_restriction = int(depth)
        self.state = state
        self.current_player = initial_player
        self.max_player = initial_player
        self.min_player = ""
        self.utility = 0
        self.action = ""
        self.current_depth = 0
        self.i = -1
        self.j = -1
        self.isTreeEnd = False
        self.isGoDown = True
        self.next_state = list()
        self.max_value = float('-inf')
        if initial_player == blackTile :
            self.min_player = whiteTile
        else :
            self.min_player = blackTile

    #開始往下搜三層
    def executeSearch(self, state):
        v = 0
        _state = state
        a = NEGATIVE_INFINITE
        b = POSITIVE_INFINITE

        v = self.getMaxValue(_state, a, b, 0)
        return self.next_state

    #顯示下棋後的結果
    def setResult (self, state, action):
        next_state = copy.deepcopy(state) #create a new state
        player = self.current_player
        if (player == blackTile) :
            opponent = whiteTile
        else :
            opponent = blackTile
        
        i = action[0]
        j = action[1]
        self.i = i
        self.j = j

        flipped = This_is_valid_move(next_state,player,self.i,self.j)
        next_state[self.i][self.j] = player
        if flipped != False:
            for x, y in flipped :
                next_state[x][y] = player
        return next_state

        
              
    #取得最大值(alpha_beta_algorithm)
    def getMaxValue (self, state, a, b, depth):
        current_depth = depth
        actions = list()
        self.current_player = self.max_player
        self.isGoDown = True
        if (self.depth_restriction <= current_depth):
            self.isTreeEnd = True
            return self.getUtility(state)
        elif Get_valid_move(state , self.max_player) == []:
            self.isTreeEnd = True
            return self.getUtility(state)
        else:
            self.isTreeEnd = False
            initial_v = POSITIVE_INFINITE
            v = NEGATIVE_INFINITE
            actions = Get_valid_move(state , self.max_player)
            for _action in actions :
                _i = _action[0]
                _j = _action[1]
                self.current_player = self.max_player
                _v = self.getMinValue(self.setResult(state, _action), a, b, current_depth + 1)
                v = max([v, _v]) 
                if v >= b :
                    if (self.isGoDown):
                        if (self.isTreeEnd):
                            self.isGoDown = False
                            self.isTreeEnd = False
                    else:
                        pass
                    return v
                else:
                    if (self.isGoDown):
                        if (self.isTreeEnd):
                            a = max([a, v])
                            self.isGoDown = False
                            self.isTreeEnd = False
                        else :
                            a = max([a, v])
                    else:
                        a = max([a, v])
            return v 

    #取得最小值(alpha_beta_algorithm)
    def getMinValue (self, state, a, b, depth):
        current_depth = depth
        actions = list()
        self.current_player = self.min_player
        self.isGoDown = True
        if (self.depth_restriction <= current_depth):
            self.isTreeEnd = True
            if current_depth == 1:
                self.setNextState(self.getUtility(state), state)
            return self.getUtility(state)
        elif Get_valid_move(state , self.min_player) == []:
            self.isTreeEnd = True
            if current_depth == 1:
                self.setNextState(self.getUtility(state), state)
            return self.getUtility(state)
        else:
            self.isTreeEnd = False
            initial_v = POSITIVE_INFINITE
            v = NEGATIVE_INFINITE
            actions = Get_valid_move(state , self.min_player)
            for _action in actions :
                self.current_player = self.min_player
                _i = _action[0]
                _j = _action[1]

                _v = self.getMaxValue(self.setResult(state, _action), a, b, current_depth + 1)
                if current_depth == 1: self.setNextState(_v, state)
                v = min([v, _v]) 
                if v <= a :
                    if (self.isGoDown):
                        if (self.isTreeEnd):
                            self.isGoDown = False
                            self.isTreeEnd = False
                    else:
                        pass
                    return v
                else:
                    if (self.isGoDown):
                        if (self.isTreeEnd):
                            b = min([b, v])
                            self.isGoDown = False
                            self.isTreeEnd = False
                        else :
                            b = min([b, v])
                    else:
                        b = min([b, v])
            return v

    #若無法取最大最小值，直接用上面的權重效益來計算效益
    def getUtility (self, state):
        value = 0
        _max = 0
        _min = 0

        for i, row in enumerate(state):
            for j, cell in enumerate(row):
                if cell == self.min_player:
                    _min += WEIGHT_MATRIX[i][j]
                elif cell == self.max_player:
                    _max += WEIGHT_MATRIX[i][j]
                else:
                    pass
        value = _max - _min
        return value

    #將alpha 值替換成最大值
    def setNextState (self, value, next_state):
        if (self.max_value < value):
            self.next_state = copy.deepcopy(next_state)
            self.max_value = value




 
if __name__=='__main__':
    main()

