import pyglet, random, os, sys
from GameObjects import GamePiece

def grid():
    #returns a 10x10 grid
    board = [ ['.' for _ in range(10)] for _ in range(10)]
    return board

def shipcheck(base, fixed, size, board, occupied):
    if base + size > len(board):
        #checks if the ship fits the board
        return False
    for i in range(size):
        #uses coordinates to check if ship intersects another ship
        if orientation == 'vertical':
            if (base + i, fixed) in occupied:
                return False
        elif orientation == 'horizontal':
            if (fixed, base + i) in occupied:
                return False
    return True

def ai_shipcheck(base, fixed, size, ai_board, ai_occupied):
    if base + size > len(ai_board):
        #checks if the ship fits the board
        return False
    for i in range(size):
        #uses coordinates to check if ship intersects another ship
        if orientation == 'vertical':
            if (base + i, fixed) in ai_occupied:
                return False
        elif orientation == 'horizontal':
            if (fixed, base + i) in ai_occupied:
                return False
    return True

def place(board, base, fixed, size, orientation, occupied):
    for i in range(size):
        if orientation == 'vertical':
            occupied.append((base + i, fixed))
            board[base + i][fixed] = 'o'
        elif orientation == 'horizontal':
            occupied.append((fixed, base + i))
            board[fixed][base + i] = 'o'

def ai_place(ai_board, base, fixed, size, orientation, ai_occupied):
    for i in range(size):
        if orientation == 'vertical':
            ai_occupied.append((base + i, fixed))
            ai_board[base + i][fixed] = 'o'
        elif orientation == 'horizontal':
            ai_occupied.append((fixed, base + i))
            ai_board[fixed][base + i] = 'o'

def shipset(board, coordinates, orientation, ship):
    if orientation == 'vertical':
        base, fixed = coordinates[1], coordinates[0]
    elif orientation == 'horizontal':
        fixed, base = coordinates[1], coordinates[0]

    if ship == 'carrier':
        size = 5
    elif ship == 'battleship':
        size = 4
    elif ship == 'cruiser' or ship == 'submarine':
        size = 3
    elif ship == 'destroyer':
        size = 2
        
    if shipcheck(base, fixed, size, board, occupied):
        place(board, base, fixed, size, orientation, occupied)
        return True
    else:
        return 'Please try again.'

def ai_shipset(ai_board, coordinates, orientation, ship):
    if orientation == 'vertical':
        base, fixed = coordinates[1], coordinates[0]
    elif orientation == 'horizontal':
        fixed, base = coordinates[1], coordinates[0]

    if ship == 'carrier':
        size = 5
    elif ship == 'battleship':
        size = 4
    elif ship == 'cruiser' or ship == 'submarine':
        size = 3
    elif ship == 'destroyer':
        size = 2
        
    if ai_shipcheck(base, fixed, size, ai_board, ai_occupied):
        ai_place(ai_board, base, fixed, size, orientation, ai_occupied)
        return True

def hitcheck(board, coordinates, occupied):
    if coordinates in occupied:
        board[coordinates[0]][coordinates[1]] = 'x'
        ai_occupied.remove(coordinates)

#modified version of hitcheck
def ai_hitcheck(board, coordinates):
    if type(board) is not list:
        board.attack_positions.append((coordinates[1],coordinates[0]))
        board_list=board.grid
    if board_list[coordinates[0]][coordinates[1]] == 'o':
        board_list[coordinates[0]][coordinates[1]] = 'x'
        return True
    elif board_list[coordinates[0]][coordinates[1]] == '.' or board_list[coordinates[0]][coordinates[1]] == 'm':
        board_list[coordinates[0]][coordinates[1]] = 'm'
        return False

#chooses logical coordinates
#if the attempts to choose a logical coordinate exceeds 10
#it will choose any coordinate
def ai_coordinates(player_ships, board):
    if type(board) is not list:
        board_list=board.grid
    attempt = 0
    while True:
        attempt += 1
        if attempt == 10:
            while True:
                x = random.randint(0, 9)
                y = random.randint(0, 9)
                coordinates = (x, y)
                if board_list[x][y] == '.' or board_list[x][y] == 'o':
                    return coordinates
        #x = int(input())
        #y = int(input())
        x = random.randint(0, 9)
        y = random.randint(0, 9)
        coordinates = (x, y)
        if player_ships[-1] == 'destroyer':
            n = 2
        elif player_ships[-1] == 'submarine' or player_ships[-1] == 'cruiser':
            n = 3
        elif player_ships[-1] == 'battleship':
            n = 4
        elif player_ships[-1] == 'carrier':
            n = 5
        if board_list[x][y] == '.' or board_list[x][y] == 'o':
            counter1 = 1
            counter2 = 1
            for p in range(1, n):
                if x + n <= 9:
                    if board_list[x + n][y] == '.' or board_list[x + n][y] == 'o':
                        counter1 += 1
                if x - n >= 0:
                    if board_list[x - n][y] == '.' or board_list[x - n][y] == 'o':
                        counter1 += 1
                if y + n <= 9:
                    if board_list[x][y + n] == '.' or board_list[x][y + n] == 'o':
                        counter2 += 1
                if y - n >= 0:
                    if board_list[x][y - n] == '.' or board_list[x][y - n] == 'o':
                        counter2 += 1
            if counter1 == n or counter2 == n:
                break
    return coordinates


#makes a decision if the ai hits a ship
def ai_repeat(board, coordinates, decision, player_ships):
    if type(board) is not list:
        board_list=board.grid
    counter = 0
    lock = 0
    result = False
    x = coordinates[0]
    y = coordinates[1]
    check0 = False
    check1 = False
    check2 = False
    check3 = False
    if x + 1 <= 9:
       if board_list[x + 1][y] == '.' or board_list[x + 1][y] == 'o':
           check0 = True
    if x - 1 >= 0:
       if board_list[x - 1][y] == '.' or board_list[x - 1][y] == 'o':
           check1 = True
    if y + 1 <= 9:
       if board_list[x][y + 1] == '.' or board_list[x][y + 1] == 'o':
           check2 = True
    if y - 1 >= 0:
       if board_list[x][y - 1] == '.' or board_list[x][y - 1] == 'o':
           check3 = True
    while True:
       counter += 1
       if counter == 10:
           coordinates = ai_coordinates(player_ships, board)
           result = ai_hitcheck(board, coordinates)
           if result == False:
               break
           elif result == True:
               ai_repeat(board, coordinates, decision, player_ships)
       lock += 1
       if decision == 0:
           x += 1
           if x <= 9 and check0 == True:
               lock += 1
           else:
               x -=1
               choices = [1, 2, 3]
               decision = random.choice(choices)
               lock = 0
               continue
       elif decision == 1:
           x -= 1
           if x >= 0 and check1 == True:
               lock += 1
           else:
               x += 1
               choices = [0, 2, 3]
               decision = random.choice(choices)
               lock = 0
               continue
       elif decision == 2:
           y += 1
           if y <= 9 and check2 == True:
               lock += 1
           else:
               y -= 1
               choices = [0, 1, 3]
               decision = random.choice(choices)
               lock = 0
               continue
       elif decision == 3:
           y -= 1
           if y >= 0 and check3 == True:
               lock += 1
           else:
               y += 1
               choices = [0, 1, 2]
               decision = random.choice(choices)
               lock = 0
               continue
       coordinates = (x, y)
       if lock == 1:
           coordinates = ai_coordinates(player_ships, board)
       result = ai_hitcheck(board, coordinates)
       lock = 0
       if result == False:
           break

#checks if the ai has any possible move left
def no_moves(board):
    if type(board) is not list:
        board_list=board.grid

    counter = 0
    for x in range(10):
        for y in range(10):
            if board_list[x][y] == 'x' or board_list[x][y] == 'm':
                counter += 1
    if counter == 100:
        return True
    else:
        return False

#what the ai does in its turn
def ai_hit(board, player_ships):
    if no_moves(board) == False:
        result = False
        decision = 4
        coordinates = ai_coordinates(player_ships, board)
        result = ai_hitcheck(board, coordinates)
        if result == True:
            decision = random.randint(0, 3)
            ai_repeat(board, coordinates, decision, player_ships)
    else:
        print('There are no possible moves left')


def ship_unset(board, coordinates, orientation, ship):
  #executes if ship is dragged away if already in the board
    if orientation == 'vertical':
        base, fixed = coordinates[1], coordinates[0]
    elif orientation == 'horizontal':
        fixed, base = coordinates[1], coordinates[0]

    if ship == 'carrier':
        size = 5
    elif ship == 'battleship':
        size = 4
    elif ship == 'cruiser' or ship == 'submarine':
        size = 3
    elif ship == 'destroyer':
        size = 2
        
    for i in range(size):
        if orientation == 'vertical' and ((base + i, fixed) in occupied):
            occupied.remove((base + i, fixed))
            board[base + i][fixed] = '.'
        elif orientation == 'horizontal' and ((fixed, base + i) in occupied):
            occupied.remove((fixed, base + i))
            board[fixed][base + i] = '.'


def mouse_position_is_in(instance_name,x,y):
    if isinstance(instance_name, GamePiece):
        width=instance_name.image.width
        height=instance_name.image.height
        if instance_name.orientation=='vertical':
            width=instance_name.image.height
            height=instance_name.image.width

        if instance_name.sprite.x - width//2 <x<instance_name.sprite.x+width//2 and instance_name.sprite.y - height//2<y<instance_name.sprite.y+height//2:
            return True
        else:
            return False
    if instance_name.sprite.x<x<instance_name.sprite.x+instance_name.image.width and instance_name.sprite.y<y<instance_name.sprite.y+instance_name.image.height:
        return True
    return False

def ai_set_ships(ai_board,ai_ship_list):
    global orientation
    for ai_ship in ai_ship_list:
        while True:
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            coordinates = (x, y)
            temp = random.randint(0, 1)
            
            if temp == 1:
                ai_ship.switch_orientation()
            orientation= ai_ship.orientation
            result = shipset(ai_board.grid, coordinates, ai_ship.orientation, ai_ship.name)
            if result == True:
                if ai_ship.orientation=='vertical':
                    ai_ship.sprite.x = ai_board.sprite.x+x*40+ai_ship.image.height//2
                    ai_ship.sprite.y = ai_board.sprite.y+(10-y)*40 - ai_ship.image.width//2
                else:
                    ai_ship.sprite.x = ai_board.sprite.x+x*40+ai_ship.image.width//2
                    ai_ship.sprite.y = ai_board.sprite.y+(10-y)*40 - ai_ship.image.height//2
                if ai_ship.orientation=='vertical':
                    for i in range(ai_ship.size):
                        ai_ship.coordinates.append((x,y+i))
                else:
                    for i in range(ai_ship.size):
                        ai_ship.coordinates.append((x+i,y))
                break

def play_sound(sound):
    sound = pyglet.media.load('res/sounds/'+sound)
    sound.play()


# def play_music(music):
#     sound = pyglet.media.load('res/sounds/'+music)
#     looper = pyglet.media.SourceGroup(sound.audio_format, None)
#     looper.loop = True
#     looper.queue(sound)
#     player = pyglet.media.Player()
#     player.queue(looper)
#     player.play()
   
#?   NEWER
def play_music(music):
    sound = pyglet.media.load("res/sounds/" + music)
    # looper = pyglet.media.SourceGroup()
    # looper.loop = True
    # looper.queue(sound)
    player = pyglet.media.Player()
    player.loop = True
    player.queue(sound)
    player.play()

#Writes a new txt file for highscore if not exists
if not os.path.exists('highscore.txt'):
    hsfile=open('highscore.txt','w')
    hsfile.write('0\nTroy\nbongo1')
    hsfile.close()


def record_if_highscore(player, chosen_hero):
    #Checks and records if highscore is beated
    file_name='highscore.txt'
    hsfile = open(file_name,'r')
    highscore = int(hsfile.readline().rstrip())
    hsfile.close()
    if highscore<player.score:
        hsfile = open(file_name,'w')
        hsfile.write(str(player.score)+'\n'+player.name+'\n'+chosen_hero.image_name)
        hsfile.close()

def restart_program():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    '''This Code is from user Griboullis in the
    website:https://www.daniweb.com/programming/software-development/code/260268/restart-your-python-program'''
    python = sys.executable
    os.execl(python, python, * sys.argv)

if __name__ == '__main__':
    def print_board(board):
        for row in board:
            print(row)

    #sets up ai board
    ai_board = grid()
    board = grid()
    ai_occupied = []
    occupied = []
    previous = [4, (0, 0)]
    player_ships = ['carrier', 'battleship', 'cruiser', 'submarine', 'destroyer']
    ai_ships = ['carrier', 'battleship', 'cruiser', 'submarine', 'destroyer']
    for i in ('carrier', 'battleship', 'cruiser', 'submarine', 'destroyer'):
        while True:
            print_board(ai_board)
            print(ai_occupied)
            print('')
            print('Ai: I place my '+i+':')
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            coordinates = (x, y)
            temp = random.randint(0, 1)
            orientation = 'horizontal'
            if temp == 0:
                orientation = 'vertical'
            elif temp == 1:
                orientation = 'horizontal'
            result = ai_shipset(ai_board, coordinates, orientation, i)
            if result == True:
                break
            else:
                print(result)
        print_board(ai_board)
        print(ai_occupied)

    #sets up player board
    for i in ('carrier', 'battleship', 'cruiser', 'submarine', 'destroyer'):
        while True:
            print('')
            print('Place your '+i+':')
            x = int(input('Input x position(0-9):'))
            y = int(input('Input y position(0-9):'))
            coordinates = (x, y)
            orientation = input('Orientation(vertical/horizontal):')
            result = shipset(board, coordinates, orientation, i)
            if result == True:
                break
            else:
                print(result)
        print_board(board)
        print(occupied)