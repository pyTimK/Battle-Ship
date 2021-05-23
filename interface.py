import pyglet, engine, time, math, random, os
from interfaceObjects import Image, Sprite, Text, Background, Animation, Laser, Cat_home_screen

#INITIALIZES ALL NECESSARY VARIABLES
width = 1200
height = 600
player_name=''
ai_name=''

#Order in Sprites and Texts
background = pyglet.graphics.OrderedGroup(0)
foreground = pyglet.graphics.OrderedGroup(1)

#Background shades
bg_white = Background(0,0,width,height)
bg_gray = Background(0,0,width,height,(233,233,233,255))
ship_shade = Background(0, 0, 0, 0, color=(255,255,255,10))
must_shade = False

#Start Button
start_bg = Background(width-320, 25, 300, 150)
start_text = Text('START', start_bg.posx+start_bg.box_width//2,start_bg.posy+start_bg.box_height//2,anchor_x='center',anchor_y='center')

#explosion animation
explosion = Animation('explosion.png', 4, 5, 40, 40, x=400, y=200)
explosion_list=[]

#laser animation
laser_list=[]

#Load All Bongo Cats
game_screen_batch = pyglet.graphics.Batch()
bongo_ai = Sprite('bongo_ai.png', batch=game_screen_batch,group=foreground)

#Board textures
success_hit = Image('success_hit.png')
fail_hit = Image('fail_hit.png')


#THIS SECTION IS DIVIDED INTO DIFFERENT SCREEN STATES (BEGUN BY '########')

######## Home Screen ########
choose_player_screen_batch = pyglet.graphics.Batch()
text_score=Text('100',width//2, height-90, anchor_x='center', batch=game_screen_batch)
home_screen_batch = pyglet.graphics.Batch()
cat_display = Cat_home_screen(batch=home_screen_batch)
home_background = pyglet.image.load_animation('res/sprites/home_background.gif')
bin2 = pyglet.image.atlas.TextureBin()
home_background.add_to_texture_bin(bin2)
home_bacground_sprite = pyglet.sprite.Sprite(img=home_background, x=0, y=0)
home_bacground_sprite.scale=2.4

def initialize_home_screen(bongo_cats):
	Text('Click Anywhere To Continue', width//2, 30, anchor_x='center', batch=home_screen_batch)

def random_cat_draw():
	global cat_display
	distance = 160
	cat_display.sprite.x+=1
	cat_display.sprite.opacity=(distance//2-abs((2*cat_display.x_initial+distance)//2-cat_display.sprite.x))*(190/(distance//2))
	if cat_display.sprite.x - cat_display.x_initial>distance:
		cat_display = Cat_home_screen(batch=home_screen_batch)

def home_screen(bongo_cats):
	home_bacground_sprite.draw()
	home_screen_batch.draw()
	random_cat_draw()


######## Choose Player Screenn ########
def initialize_choose_player_screen(bongo_cats):
	n=len(bongo_cats)
	start_x = (4*(width-1000))//11
	margin_right = start_x//4
	for i in range(n):
		if i<4:
			bongo_cats[i].sprite.position = (start_x+i*(bongo_cats[i].image.width+margin_right),212)
		elif 4<=i<=8:
			bongo_cats[i].sprite.position = (start_x+(i-4)*(bongo_cats[i].image.width+margin_right),12)

def show_name_on_hover(bongo_cats, show_name):
	for i in range(len(bongo_cats)):
		if bongo_cats[i] == show_name:
			pyglet.text.Label(bongo_cats[i].name, font_size=20, x=bongo_cats[i].sprite.x+bongo_cats[i].image.width//2, y=bongo_cats[i].sprite.y+25, anchor_x='center', anchor_y='center', color=(0,0,0,255)).draw()

happy = Sprite('bongo1_happy.png')
def choose_player_screen(bongo_cats, show_name, player_name,chosen_hero):
	bg_gray.draw()
	choose_player_screen_batch.draw()
	if player_name!='':
		Text(player_name.upper(),width//2,height-70, anchor_x='center').draw()
		Text('You Can Change Your Name!',width//2,height-100, font_size=12, anchor_x='center',batch=choose_player_screen_batch)
		Text('(Type it)',width//2, height-120,font_size=12, anchor_x='center',batch=choose_player_screen_batch)
	if chosen_hero != None:
		start_bg.draw()
		start_text.draw()
		happy.sprite.image = pyglet.image.load('res/sprites/'+chosen_hero.image_name+'_happy.png')
		happy.sprite.position = (chosen_hero.sprite.x-10, chosen_hero.sprite.y)
		happy.sprite.draw()
		pyglet.text.Label(chosen_hero.name, font_size=20, x=chosen_hero.sprite.x+chosen_hero.image.width//2, y=chosen_hero.sprite.y+25, anchor_x='center', anchor_y='center', color=(0,0,0,255)).draw()
	else:
		if show_name!=None:
			happy.sprite.image = pyglet.image.load('res/sprites/'+show_name.image_name+'_happy.png')
			happy.sprite.scale=1.1
			happy.sprite.position = (show_name.sprite.x-10, show_name.sprite.y)
			happy.sprite.draw()
		Text('Chose Your Hero', width//2, height-150, anchor_x='center').draw()
	show_name_on_hover(bongo_cats, show_name)


######## Set Ship Screen ########
def set_shade(human_board, image_being_dragged, orientation):
	'''Computes and displays the location of the shade of the ship if being placed on board'''
	if orientation=='vertical':
		ship_shade.box_width = image_being_dragged.image.height
		ship_shade.box_height = image_being_dragged.image.width
		x = (image_being_dragged.sprite.x-human_board.sprite.x - image_being_dragged.image.height//2)//40
		y = (image_being_dragged.sprite.y-human_board.sprite.y - image_being_dragged.image.width//2)//40

	elif orientation=='horizontal':
		ship_shade.box_width = image_being_dragged.image.width
		ship_shade.box_height = image_being_dragged.image.height
		x = (image_being_dragged.sprite.x-human_board.sprite.x - image_being_dragged.image.width//2)//40
		y = (image_being_dragged.sprite.y-human_board.sprite.y - image_being_dragged.image.height//2)//40

	ship_shade.posx = human_board.sprite.x+x*40
	ship_shade.posy = human_board.sprite.y+y*40
	if ship_shade.posy<human_board.sprite.y:
		ship_shade.posy=human_board.sprite.y
	elif ship_shade.posy+ship_shade.box_height>human_board.sprite.y+human_board.image.height:
		ship_shade.posy=human_board.sprite.y+human_board.image.height-ship_shade.box_height

	if ship_shade.posx<human_board.sprite.x:
		ship_shade.posx=human_board.sprite.x
	elif ship_shade.posx+ship_shade.box_width>human_board.sprite.x+human_board.image.width:
		ship_shade.posx=human_board.sprite.x+human_board.image.width-ship_shade.box_width

	#Draws the shade of the ship
	if ship_shade.color==(255,255,255,100):
		bg_whitebox = pyglet.image.load('res/sprites/bg_whitebox.png')
	else:
		bg_whitebox = pyglet.image.load('res/sprites/bg_graybox.png')

	bg_whitebox.width=ship_shade.box_width
	bg_whitebox.height=ship_shade.box_height
	bg_whitebox_sprite = pyglet.sprite.Sprite(bg_whitebox, x=ship_shade.posx, y=ship_shade.posy)
	bg_whitebox_sprite.draw()

def set_ship_screen(chosen_hero, human_board, image_being_dragged, human_ship_list):
	bg_gray.draw()
	chosen_hero.sprite.position = (0,height-chosen_hero.image.height)
	chosen_hero.draw()
	human_board.draw()
	Text('Place your Ships!', 650, 350, anchor_x='center').draw()
	Text('Right Click to Rotate', 650, 320, anchor_x='center', font_size=13).draw()
		
	if must_shade and image_being_dragged!=None:
		set_shade(human_board, image_being_dragged, image_being_dragged.orientation)
		engine.orientation=image_being_dragged.orientation

		x=(ship_shade.posx - human_board.sprite.x)//40
		y=(human_board.image.height+human_board.sprite.x - (ship_shade.posy + ship_shade.box_height))//40-1
		if engine.orientation == 'vertical':
		    base, fixed = y,x
		elif engine.orientation == 'horizontal':
		    fixed, base = y,x

		if engine.shipcheck(base, fixed, image_being_dragged.size, human_board.grid, human_board.occupied_positions):
			ship_shade.color=(255,255,255,100)
		else:
			ship_shade.color=(100,100,100,100)

	if len(human_board.occupied_positions)==17:
		start_bg.draw()
		start_text.draw()

	for human_ship in human_ship_list:
		human_ship.draw()


######## Game Screen ########
def if_success_hit(coordinate, board, ship_list):
	global explosion_list
	board.success_hit_sprite_list.append(pyglet.sprite.Sprite(success_hit.image, x=board.sprite.x+coordinate[0]*40, y=board.sprite.y+(9-coordinate[1])*40, batch=game_screen_batch))
	explosion.update(board.sprite.x+coordinate[0]*40, board.sprite.y+(9-coordinate[1])*40)
	for ship in ship_list:
		if set(ship.coordinates).issubset(board.attack_positions) and ship.visibility=='hidden':
			explosion_list=[]
			ship.sprite.batch=game_screen_batch
			ship.visibility='visible'
			for coordinate in ship.coordinates:
				explosion_list.append(Animation('explosion.png', 4, 5, 40, 40, x=board.sprite.x+coordinate[0]*40, y=board.sprite.y+(9-coordinate[1])*40))
				for hit_sprite in board.success_hit_sprite_list:
					if hit_sprite.position == (board.sprite.x+coordinate[0]*40, board.sprite.y+(9-coordinate[1])*40):
						board.success_hit_sprite_list.remove(hit_sprite)
						break

def hide_destroyed_human_ship(human_ship_list, human_board):
	for human_ship in human_ship_list:
		if set(human_ship.coordinates).issubset(human_board.attack_positions):
			human_ship.sprite.batch=None

def ai_laser_hit(coordinates, human_board, ai_num_hits):
	global laser_list
	laser_list=[]
	for i in range(ai_num_hits):
		laser_list.append(Laser())
		laser_list[i].visibility='visible'
		laser_list[i].sprite.position= (1078,549)
		laser_list[i].x_target=(human_board.sprite.x+coordinates[i][0]*40+20)
		laser_list[i].y_target=(human_board.sprite.y+(9-coordinates[i][1])*40+20)
		laser_list[i].x_distance = (laser_list[i].sprite.x-laser_list[i].x_target)
		laser_list[i].y_distance = (laser_list[i].sprite.y-laser_list[i].y_target)
		laser_list[i].sprite.rotation = 180+math.degrees(math.atan(laser_list[i].x_distance/laser_list[i].y_distance))

def initialize_game_screen(player, chosen_hero, human_ship_list):
	global player_name, ai_name
	player_name = Text(player.name,chosen_hero.image.width+20, height-40, batch=game_screen_batch, group=foreground)
	Text('vs',width//2, height-40, anchor_x='center', batch=game_screen_batch, group=foreground)
	ai_name = Text('SKYNET',width-bongo_ai.image.width-20, height-40, anchor_x='right', batch=game_screen_batch, group=foreground)
	Text('(Score)',width//2, height-110, anchor_x='center', font_size=13, batch=game_screen_batch)
	for human_ship in human_ship_list:
		human_ship.sprite.batch=game_screen_batch

sprites_game_screen=[Sprite('bg_whitebox.png', x=245, y=height-50,image_width=width, image_height=50, batch=game_screen_batch, group=background)]

def change_emotion(chosen_hero, emotion):
	if emotion=='happy':
		chosen_hero.sprite.image = pyglet.image.load('res/sprites/'+chosen_hero.image_name+'_happy.png')
	else:
		chosen_hero.sprite.image = pyglet.image.load('res/sprites/'+chosen_hero.image_name+'.png')

def player_click_turn(player, human_board, human_ship_list):
	text_score.text.text = str(player.score)

def game_screen(chosen_hero,human_board,ai_board, ai_ship_list, player, game):
	bg_gray.draw()

	#Draw the cats
	human_board.draw()
	ai_board.draw()
	game_screen_batch.draw()

	#animations
	for explode_animation in explosion_list:
		explode_animation.animate()
	for laser in laser_list:
		laser.animate()

	if game.game_over:
		if game.winner=='human':
			chosen_hero.sprite.x+=10
			chosen_hero.sprite.y-=4
		else:
			bongo_ai.sprite.x-=10
			bongo_ai.sprite.y-=4
	else:
		chosen_hero.sprite.position=(-5,height-chosen_hero.image.height+5)
		bongo_ai.sprite.position = (width-bongo_ai.image.width+5,height-chosen_hero.image.height+5)

	chosen_hero.draw()

game_over_screen_batch=pyglet.graphics.Batch()
laser = Laser(x=width, y=height, batch=game_over_screen_batch)
laser2 = Laser(x=0, y=height, batch=game_over_screen_batch)
highscore_image=None
play_again_button = Sprite('bg_whitebox.png', x=120, y=300,image_width=230, image_height=100, batch=game_over_screen_batch, group=background)
quit_button = Sprite('bg_whitebox.png', x=150, y=150,image_width=170, image_height=100, batch=game_over_screen_batch, group=background)


######## Game Over Screen ########
def initialize_game_over_screen(player, chosen_hero, game):
	global highscore_image

	if game.winner=='human':
		Text('You Win!',width//2,height-185,anchor_x='center', batch=game_over_screen_batch)
		chosen_hero.sprite.batch=game_over_screen_batch
		Text(player.name,width//2, 185,anchor_x='center', batch=game_over_screen_batch)
	else:
		Text('Try Harder!',width//2,height-185,anchor_x='center', batch=game_over_screen_batch)
		Text('SKYNET',width//2, 185, anchor_x='center', batch=game_over_screen_batch)
		bongo_ai.sprite.batch=game_over_screen_batch
	
	Text('Play Again',play_again_button.sprite.x+play_again_button.image.width//2, play_again_button.sprite.y+play_again_button.image.height//2, anchor_x='center', anchor_y='center', font_size=30, batch=game_over_screen_batch, group=foreground)
	Text('Quit',quit_button.sprite.x+quit_button.image.width//2, quit_button.sprite.y+quit_button.image.height//2, anchor_x='center', anchor_y='center', font_size=30, batch=game_over_screen_batch, group=foreground)
	Text('Winner',width//2, 170, anchor_x='center', font_size=13, batch=game_over_screen_batch)
	Text(str(player.score), width//2, 120, anchor_x='center', batch=game_over_screen_batch)
	Text('Score',width//2, 105, anchor_x='center', font_size=13, batch=game_over_screen_batch)

	#reads the high score
	file_name='highscore.txt'
	hsfile=open(file_name)
	highscore=hsfile.readline().rstrip()
	hs_name=hsfile.readline().rstrip()
	hs_cat=hsfile.readline().rstrip()

	highscore_image=Sprite(str(hs_cat)+'_happy.png',x=870, y=235, batch=game_over_screen_batch)
	highscore_image.sprite.scale=0.8
	hs_name_posx=960
	hs_name_posy=200
	Text(hs_name,hs_name_posx, hs_name_posy,anchor_x='center',font_size=20, batch=game_over_screen_batch)
	Text('High Score', hs_name_posx, hs_name_posy-12, anchor_x='center', font_size=10, batch=game_over_screen_batch)
	Text(highscore,hs_name_posx, hs_name_posy-60,anchor_x='center',font_size=20, batch=game_over_screen_batch)
	Text('Score',hs_name_posx, hs_name_posy-72, anchor_x='center', font_size=10, batch=game_over_screen_batch)
	laser.visibility='visible'
	laser.x_target = random.randint(-10,width)
	laser.y_target = -10
	laser.x_distance = (laser.sprite.x-laser.x_target)
	laser.y_distance = (laser.sprite.y-laser.y_target)
	laser.sprite.rotation = 180+math.degrees(math.atan(laser.x_distance/laser.y_distance))
	laser2.visibility='visible'
	laser2.x_target = random.randint(0,width+10)
	laser2.y_target = -10
	laser2.x_distance = (laser2.x_target-laser2.sprite.x)
	laser2.y_distance = (laser2.sprite.y-laser2.y_target)
	laser2.sprite.rotation = 180-math.degrees(math.atan(laser2.x_distance/laser2.y_distance))
def game_over_screen():
	bg_gray.draw()
	game_over_screen_batch.draw()
	laser.animate('infinite')
	laser2.animate('infinite', origin='left')
