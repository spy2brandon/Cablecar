from Model.interface import PlayerMove
from playerData import PlayerData
import copy

"""
Cable Car: Student Computer Player

Complete these function stubs in order to implement your AI.
Author: Adam Oest (amo9149@rit.edu)
Author: Brandon Montoya (bvm5795@rit.edu)
Author: YOUR NAME HERE (your email address)
Author: YOUR NAME HERE (your email address)
"""

def init(playerId, numPlayers, startTile, logger, arg = "None"):
    """The engine calls this function at the start of the game in order to:
        -tell you your player id (0 through 5)
        -tell you how many players there are (1 through 6)
        -tell you what your start tile is (a letter a through i)
        -give you an instance of the logger (use logger.write("str") 
            to log a message) (use of this is optional)
        -inform you of an additional argument passed 
            via the config file (use of this is optional)
        
    Parameters:
        playerId - your player id (0-5)
        numPlayers - the number of players in the game (1-6)
        startTile - the letter of your start tile (a-j)
        logger - and instance of the logger object
        arg - an extra argument as specified via the config file (optional)

    You return:
        playerData - your player data, which is any data structure
                     that contains whatever you need to keep track of.
                     Consider this your permanent state.
    """
    
    # Put your data in here.  
    # This will be permanently accessible by you in all functions.
    # It can be an object, list, or dictionary
    playerData = PlayerData(logger, playerId, startTile, numPlayers)

    # This is how you write data to the log file
    playerData.logger.write("Player %s starting up" % playerId)
    
    # This is how you print out your data to standard output (not logged)
    print(playerData)
    
    return playerData

def move(playerData):  
    """The engine calls this function when it wants you to make a move.
    
    Parameters:
        playerData - your player data, 
            which contains whatever you need to keep track of
        
    You return:
        playerData - your player data, 
            which contains whatever you need to keep track of
        playerMove - your next move
    """

    playerData.logger.write("move() called")
    
    # Populate these values
    playerId = playerData.playerId # 0-5
    position = None # (row, column)
    tileName = playerData.currentTile # a-j
    rotation = None # 0-3 (0 = north, 1 = east, 2 = south, 3 = west)
    for row in range(8):
        for col in range(8):
            if playerData.board[row][col] == (None,None):
                #Place a tile
                if row == 7 or row == 0 or col == 7 or col == 0:
                    #tile is on sides
                    if row + col == 7 or row + col == 14 or row + col == 0:
                        #tile is corner piece
                        carIds = getCarId((row,col))
                        copyPlayerData =copy.deepcopy(playerData)
                        for arotation in range(4):
                            copyPlayerData.board[row][col] = (tileName,arotation)
                            #first carId
                            if not route_complete(copyPlayerData,carIds[0]):
                                #route is not complete
                                valid1 = True
                            elif route_score(copyPlayerData,carIds[0]) > 1:
                                #score greater than one
                                valid1 = True
                            else:
                                #route complete in one tile
                                valid1 = False
                            #second carId
                            if not route_complete(copyPlayerData,carIds[1]):
                                #route is not complete
                                valid2 = True
                            elif route_score(copyPlayerData,carIds[1]) > 1:
                                #score greater than one
                                valid2 = True
                            else:
                                #route complete in one tile
                                valid2 = False
                            if valid1 and valid2:
                                #tile rotation valid in for both carIDs
                                position = (row,col)
                                rotation = arotation
                            else:
                                #tile invalid for all rotations
                                pass
                    else:
                        #tile is sides but not corner
                        carId = getCarId((row,col))
                        copyPlayerData =copy.deepcopy(playerData)
                        for arotation in range(4):
                            copyPlayerData.board[row][col] = (tileName,arotation)
                            if not route_complete(copyPlayerData,carId[0]):
                                #route is not complete
                                valid1 = True
                            elif route_score(copyPlayerData,carId[0]) > 1:
                                #score greater than one
                                valid1 = True
                            else:
                                #route complete in one tile
                                valid1 = False
                            if valid1:
                                #tile rotation valid in for both carIDs
                                position = (row,col)
                                rotation = arotation
                            else:
                                #tile invalid for all rotations
                                pass
                else:
                    #tile is in center
                    if playerData.board[row-1][col] != (None,None)\
                    and playerData.board[row-1][col] != ('ps',0):
                        #check if top tile placed
                        position = (row,col)
                        rotation = 0
                    elif playerData.board[row][col-1] != (None,None)\
                    and playerData.board[row][col-1] != ('ps',0):
                        #check if left tile placed
                        position = (row,col)
                        rotation = 0
                    elif playerData.board[row][col+1] != (None,None)\
                    and playerData.board[row][col+1] != ('ps',0):
                        #check if right tile placed
                        position = (row,col)
                        rotation = 0
                    elif playerData.board[row+1][col] != (None,None)\
                    and playerData.board[row+1][col] != ('ps',0):
                        #check if bottom tile placed
                        position = (row,col)
                        rotation = 0
                    else:
                        #No tiles around tile
                        pass
            else:
                #Go to next tile
                pass
            if position != None:
                #break from second for loop
                break
            else:
                pass
        if position != None:
            #break from first for loop
            break
        else:
            pass
    if position == None:
        #Last resort
        for row in range(8):
            for col in range(8):
                if playerData.board[row][col] == (None,None):
                    #space was empty
                    position = (row,col)
                    rotation = 0
                else:
                    #space was not empty
                    pass
                if position != None:
                    #break from second loop
                    break
                else:
                    pass
            if position != None:
                #break from first loop
                break
            else:
                pass
        
    playerData.board[position[0]][position[1]] = (tileName,rotation)

       

    return playerData, PlayerMove(playerId, position, tileName, rotation)

def getCarId(pos):
    cars = []
    if pos[0] == 0:
        car = 1
        for i in range(8):
            if pos[1] == i:
                cars.append(car)
                break
            else:
                car += 1
    if pos[1] == 7:
        car = 9
        for i in range(8):
            if pos[0] == i:
                cars.append(car)
                break
            else:
                car += 1
    if pos[0] == 7:
        car = 24
        for i in range(8):
            if pos[1] == i:
                cars.append(car)
                break
            else:
                car -= 1
    if pos[1] == 0:
        car = 32
        for i in range(8):
            if pos[0] == i:
                cars.append(car)
                break
            else:
                car -= 1
    return cars


def move_info(playerData, playerMove, nextTile):
    """The engine calls this function to notify you of:
        -other players' moves
        -your and other players' next tiles
        
    The function is called with your player's data, as well as the valid move of
    the other player.  Your updated player data should be returned.
    
    Parameters:
        playerData - your player data, 
            which contains whatever you need to keep track of
        playerMove - the move of another player in the game, or None if own move
        nextTile - the next tile for the player specified in playerMove, 
                    or if playerMove is None, then own next tile
                    nextTile can be none if we're on the last move
    You return:
        playerData - your player data, 
            which contains whatever you need to keep track of
    """
    if playerMove != None:
        playerData.board[playerMove.position[0]][playerMove.position[1]] =\
        (playerMove.tileName,playerMove.rotation)
    else:
        playerData.currentTile = nextTile
    
    playerData.logger.write("move_info() called")
    
    return playerData


################################# PART ONE FUNCTIONS #######################
# These functions are called by the engine during part 1 to verify your board 
# data structure
# If logging is enabled, the engine will tell you exactly which tests failed
# , if any

def tile_info_at_coordinates(playerData, row, column):
    """The engine calls this function during 
        part 1 to validate your board state.
    
    Parameters:
        playerData - your player data as always
        row - the tile row (0-7)
        column - the tile column (0-7)
    
    You return:
        tileName - the letter of the tile at the given coordinates (a-j), 
            or 'ps' if power station or None if no tile
        tileRotation - the rotation of the tile 
            (0 is north, 1 is east, 2 is south, 3 is west.
            If the tile is a power station, it should be 0.  
            If there is no tile, it should be None.
    """      
    tileinfo = playerData.board[row][column]    
    tileName = tileinfo[0]
    tileRotation = tileinfo[1]
    
    return tileName, tileRotation

def route_complete(playerData, carId):
    """The engine calls this function 
        during part 1 to validate your route checking
    
    Parameters:
        playerData - your player data as always
        carId - the id of the car where the route starts (1-32)
        
    You return:
        isComplete - true or false depending on whether or not this car
             connects to another car or power station"""
             
             
    coord,pos = getStartLocation(carId)
    status = (False,0)
    while not status[0] and status[1] == 0:
        pos = connectPos(playerData.board[coord[0]][coord[1]],pos)#get next coord and first pos
        if pos == False:
            return False
        coord,pos = nextCoord(coord,pos)
        status = checkConnect(coord)#Bool  
    
    isComplete = status[0]
    
    return isComplete

def route_score(playerData, carId):
    """The engine calls this function 
        during route 1 to validate your route scoring
    
    Parameters:
        playerData - your player data as always
        carId - the id of the car where the route starts (1-32)
        
    You return:
        score - score is the length of the current route from the carId.
                if it reaches the power station, 
                the score is equal to twice the length.
    """
    coord,pos = getStartLocation(carId)
    status = (False,0)
    score = 0
    while not status[0] and status[1] == 0:
        pos = connectPos(playerData.board[coord[0]][coord[1]],pos)#get next coord and first pos
        if pos == False:
            return score 
        coord,pos = nextCoord(coord,pos)
        status = checkConnect(coord)
        score +=1
    if status[0] and status[1] == 1:
        return score * 2
    elif not status[0]:
        return None
    else:
        return score

def checkConnect(coord):
    if coord[0] == - 1 or coord[0] == 8:
        return (True,0)
    elif coord[1] == -1 or coord[1] == 8:
        return (True,0)
    elif coord == (3,3) or coord == (3,4)\
     or coord == (4,3) or coord == (4,4):
        return (True,1)
    elif 0 <= coord[0] <= 7 and 0 <= coord[1] <= 7: 
        return (False,0)
    else:
        return (False,1)
     
    

def nextCoord(coordx,posx):
    coord = coordx
    pos = posx
    if pos == 0 or pos == 1:
        coord = (coord[0]-1,coord[1])
        if pos == 0:
            pos = 5
        else:
            pos = 4
    elif pos == 5 or pos == 4:
        coord =(coord[0]+1,coord[1])
        if pos == 5:
            pos = 0
        else:
            pos = 1
    elif pos == 2 or pos == 3:
        coord = (coord[0],coord[1]+1)
        if pos == 2:
            pos = 7
        else:
            pos = 6
    else:
        coord = (coord[0],coord[1]-1)
        if pos == 7:
            pos = 2
        else:
            pos = 3
        
    return coord,pos

def getStartLocation(carId):
    car = carId
    if 1 <= car <=8: # top board
        x = -1
        while car != 0:
            car -= 1
            x +=1
        return (0,x),(0) #returns location next to car and connecting number
    elif 9 <= car <= 16: # right board
        y = -1
        while car != 8:
            car -= 1
            y +=1
        return (y,7),(2) #returns location next to car and connecting number
    elif 17 <= car <= 24: # bottom board       
        x = -1
        while car != 25:
            car += 1
            x +=1
        return (7,x),(4) #returns location next to car and connecting number
    else:                  # left board
        y = -1
        while car != 33:
            car += 1
            y +=1
        return (y,0),(6) #returns location next to car and connecting number

def connectPos(tileandrotation,pos):
    """Returns pos it connects to"""
    letter = tileandrotation[0]
    rotation = tileandrotation[1]
    if letter == 'a':
        if pos == getNum(0,rotation):
            return getNum(1,rotation)
        if pos == getNum(1,rotation):
            return getNum(0,rotation)
        if pos == getNum(2,rotation):
            return getNum(7,rotation)
        if pos == getNum(3,rotation):
            return getNum(6,rotation)
        if pos == getNum(4,rotation):
            return getNum(5,rotation)
        if pos == getNum(5,rotation):
            return getNum(4,rotation)
        if pos == getNum(6,rotation):
            return getNum(3,rotation)
        if pos == getNum(7,rotation):
            return getNum(2,rotation)
    if letter == 'b':
        if pos == getNum(0,rotation):
            return getNum(3,rotation)
        if pos == getNum(1,rotation):
            return getNum(4,rotation)
        if pos == getNum(2,rotation):
            return getNum(7,rotation)
        if pos == getNum(3,rotation):
            return getNum(0,rotation)
        if pos == getNum(4,rotation):
            return getNum(1,rotation)
        if pos == getNum(5,rotation):
            return getNum(6,rotation)
        if pos == getNum(6,rotation):
            return getNum(5,rotation)
        if pos == getNum(7,rotation):
            return getNum(2,rotation)
    if letter == 'c':
        if pos == getNum(0,rotation):
            return getNum(3,rotation)
        if pos == getNum(1,rotation):
            return getNum(4,rotation)
        if pos == getNum(2,rotation):
            return getNum(5,rotation)
        if pos == getNum(3,rotation):
            return getNum(0,rotation)
        if pos == getNum(4,rotation):
            return getNum(1,rotation)
        if pos == getNum(5,rotation):
            return getNum(2,rotation)
        if pos == getNum(6,rotation):
            return getNum(7,rotation)
        if pos == getNum(7,rotation):
            return getNum(6,rotation)
    if letter == 'd':
        if pos == getNum(0,rotation):
            return getNum(1,rotation)
        if pos == getNum(1,rotation):
            return getNum(0,rotation)
        if pos == getNum(2,rotation):
            return getNum(7,rotation)
        if pos == getNum(3,rotation):
            return getNum(4,rotation)
        if pos == getNum(4,rotation):
            return getNum(3,rotation)
        if pos == getNum(5,rotation):
            return getNum(6,rotation)
        if pos == getNum(6,rotation):
            return getNum(5,rotation)
        if pos == getNum(7,rotation):
            return getNum(2,rotation)
    if letter == 'e':
        if pos == getNum(0,rotation):
            return getNum(1,rotation)
        if pos == getNum(1,rotation):
            return getNum(0,rotation)
        if pos == getNum(2,rotation):
            return getNum(3,rotation)
        if pos == getNum(3,rotation):
            return getNum(2,rotation)
        if pos == getNum(4,rotation):
            return getNum(7,rotation)
        if pos == getNum(5,rotation):
            return getNum(6,rotation)
        if pos == getNum(6,rotation):
            return getNum(5,rotation)
        if pos == getNum(7,rotation):
            return getNum(4,rotation)
    if letter == 'f':
        if pos == getNum(0,rotation):
            return getNum(5,rotation)
        if pos == getNum(1,rotation):
            return getNum(4,rotation)
        if pos == getNum(2,rotation):
            return getNum(7,rotation)
        if pos == getNum(3,rotation):
            return getNum(6,rotation)
        if pos == getNum(4,rotation):
            return getNum(1,rotation)
        if pos == getNum(5,rotation):
            return getNum(0,rotation)
        if pos == getNum(6,rotation):
            return getNum(3,rotation)
        if pos == getNum(7,rotation):
            return getNum(2,rotation)
    if letter == 'g':
        if pos == getNum(0,rotation):
            return getNum(1,rotation)
        if pos == getNum(1,rotation):
            return getNum(0,rotation)
        if pos == getNum(2,rotation):
            return getNum(3,rotation)
        if pos == getNum(3,rotation):
            return getNum(2,rotation)
        if pos == getNum(4,rotation):
            return getNum(5,rotation)
        if pos == getNum(5,rotation):
            return getNum(4,rotation)
        if pos == getNum(6,rotation):
            return getNum(7,rotation)
        if pos == getNum(7,rotation):
            return getNum(6,rotation)
    if letter == 'h':
        if pos == getNum(0,rotation):
            return getNum(7,rotation)
        if pos == getNum(1,rotation):
            return getNum(2,rotation)
        if pos == getNum(2,rotation):
            return getNum(1,rotation)
        if pos == getNum(3,rotation):
            return getNum(4,rotation)
        if pos == getNum(4,rotation):
            return getNum(3,rotation)
        if pos == getNum(5,rotation):
            return getNum(6,rotation)
        if pos == getNum(6,rotation):
            return getNum(5,rotation)
        if pos == getNum(7,rotation):
            return getNum(0,rotation)
    if letter == 'i':
        if pos == getNum(0,rotation):
            return getNum(3,rotation)
        if pos == getNum(1,rotation):
            return getNum(6,rotation)
        if pos == getNum(2,rotation):
            return getNum(5,rotation)
        if pos == getNum(3,rotation):
            return getNum(0,rotation)
        if pos == getNum(4,rotation):
            return getNum(7,rotation)
        if pos == getNum(5,rotation):
            return getNum(2,rotation)
        if pos == getNum(6,rotation):
            return getNum(1,rotation)
        if pos == getNum(7,rotation):
            return getNum(4,rotation)
    if letter == 'j':
        if pos == getNum(0,rotation):
            return getNum(7,rotation)
        if pos == getNum(1,rotation):
            return getNum(6,rotation)
        if pos == getNum(2,rotation):
            return getNum(5,rotation)
        if pos == getNum(3,rotation):
            return getNum(4,rotation)
        if pos == getNum(4,rotation):
            return getNum(3,rotation)
        if pos == getNum(5,rotation):
            return getNum(2,rotation)
        if pos == getNum(6,rotation):
            return getNum(1,rotation)
        if pos == getNum(7,rotation):
            return getNum(0,rotation)
    else:
        return False
        

def getNum(num,rotation):
    if rotation > 0:
        return ( num + ( rotation * 2 ) ) % 8
    else:
        return num

      
def tileConnect(tileId,curPos):
    x = curPos[1]
    y = curPos[0]
    if tileId == 0:
        return 5, (y-1,x)
    elif tileId == 1:
        return 4, (y-1,x)
    elif tileId == 2:
        return 7, (y,x+1)
    elif tileId == 3:
        return 6, (y,x+1)
    elif tileId == 4:
        return 1, (y+1,x)
    elif tileId == 5:
        return 0, (y+1,x)
    elif tileId == 6:
        return 3, (y,x-1)
    elif tileId == 7:
        return 2, (y,x-1)
    

    

def game_over(playerData, historyFileName = None):
    """The engine calls this function after the game is over 
        (regardless of whether or not you have been kicked out)

    You can use it for testing purposes or anything else you might need to do...
    
    Parameters:
        playerData - your player data as always       
        historyFileName - name of the current history file, 
            or None if not being used 
    """
    
    # Test things here, changing the function calls...
    print "History File: %s" % historyFileName
    print "If it says False below, you are doing something wrong"
    
    if historyFileName == "example_complete_start.data":
        print tile_info_at_coordinates(playerData, 4, 3) == ('ps', 0)
        print route_complete(playerData, 1) == True
        print route_score(playerData, 1) == 3
    elif historyFileName == "SECOND_HISTORY_FILE_NAME":
        print "Second history file test cases here..."
    elif historyFileName == "THIRD_HISTORY_FILE_NAME":
        print "Third history file test cases here..."
    
    