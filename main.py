import pyglet, interface, engine, time
from pyglet.window import mouse
from pyglet.window import key
from interface import Text
from GameObjects import Bongo
from GameObjects import Player
from GameObjects import Game
from GameObjects import Board
from GameObjects import GamePiece
from interfaceObjects import Sprite

#Initalizes all necessary variables and objects
width,height = interface.width,interface.height
window = pyglet.window.Window(width,height,"Battle Ship",resizable=False)
game=Game('player')
bongo_cats = [Bongo('bongo1','BONGO CAT', batch=interface.choose_player_screen_batch), Bongo('bongo2','SHERLOCK', batch=interface.choose_player_screen_batch), Bongo('bongo3','VALENTINE', batch=interface.choose_player_screen_batch), Bongo('bongo4','EDGAR', batch=interface.choose_player_screen_batch), Bongo('bongo5','JOSE RIZAL', batch=interface.choose_player_screen_batch), Bongo('bongo6','Douglas MacArthur', batch=interface.choose_player_screen_batch), Bongo('bongo7','THANOS', batch=interface.choose_player_screen_batch)]
player = Player()
show_name=None
chosen_hero=None
image_being_dragged=None
human_board = Board('human',engine.grid(),50,5)
ai_board = Board('ai',engine.grid(), width-human_board.image.width-50, 5)
ai_board.sprite.x, ai_board.sprite.y = width-(ai_board.image.width+50),5
cursor_default = window.get_system_mouse_cursor(window.CURSOR_DEFAULT)
cursor_hand = window.get_system_mouse_cursor(window.CURSOR_HAND)
previous_num_hits=0
#Load all Ships
human_carrier = GamePiece('carrier', 5, 600, 50)
human_battleship = GamePiece('battleship', 4, 800, 100)
human_cruiser = GamePiece('cruiser', 3, 800, 220)
human_submarine = GamePiece('submarine', 3, 630, 110)
human_destroyer = GamePiece('destroyer', 2, 550, 200)
ai_carrier = GamePiece('carrier', 5)
ai_battleship = GamePiece('battleship', 4)
ai_cruiser = GamePiece('cruiser', 3)
ai_submarine = GamePiece('submarine', 3)
ai_destroyer = GamePiece('destroyer', 2)
human_ship_list=[human_carrier, human_battleship, human_cruiser, human_submarine, human_destroyer]
ai_ship_list=[ai_carrier, ai_battleship, ai_cruiser, ai_submarine, ai_destroyer]
interface.initialize_home_screen(bongo_cats)
engine.play_music('intro_music.wav')



def setting_ships_in_grid(setting,ship_object):
	'''Uses engine to update the grid(list) attribute of the human board'''
	engine.occupied = human_board.occupied_positions
	engine.orientation = ship_object.orientation
	x = (ship_object.sprite.x - human_board.sprite.x - ship_object.sprite.width//2)//40
	y = (human_board.image.height+human_board.sprite.y - (ship_object.sprite.y + ship_object.image.height//2))//40
	if ship_object.orientation=='vertical':
		x = (ship_object.sprite.x - human_board.sprite.x - ship_object.sprite.height//2)//40
		y = (human_board.image.height+human_board.sprite.y - (ship_object.sprite.y + ship_object.image.width//2))//40
	if setting=='set':
		engine.shipset(human_board.grid, (x,y), engine.orientation, ship_object.name)
		if ship_object.orientation=='vertical':
			for i in range(ship_object.size):
				ship_object.coordinates.append((x,y+i))
		else:
			for i in range(ship_object.size):
				ship_object.coordinates.append((x+i,y))
	else:
		engine.ship_unset(human_board.grid, (x,y), engine.orientation, ship_object.name)
		ship_object.coordinates=[]

	human_board.occupied_positions = engine.occupied
	

#mouse events
@window.event
def on_mouse_motion(x, y, dx, dy):
	global show_name
	if player.state == 'choose_player_screen':
		'''casts some animation while the mouse hovers over the heros'''
		for bongo_cat in bongo_cats:
			if engine.mouse_position_is_in(bongo_cat,x,y):
				window.set_mouse_cursor(cursor_hand)
				show_name=bongo_cat
				break
			elif chosen_hero!=None and interface.start_bg.posx<=x<=interface.start_bg.posx+interface.start_bg.box_width and interface.start_bg.posy<=y<=interface.start_bg.posy+interface.start_bg.box_height:
				window.set_mouse_cursor(cursor_hand)
			else:
				show_name=None
				window.set_mouse_cursor(cursor_default)

	elif player.state == 'set_ship_screen':
		'''casts some animation while the mouse hovers over the ships that are to be placed'''
		for human_ship in human_ship_list:
			if engine.mouse_position_is_in(human_ship,x,y):
				window.set_mouse_cursor(cursor_hand)
				break
			elif len(human_board.occupied_positions)==17 and interface.start_bg.posx<=x<=interface.start_bg.posx+interface.start_bg.box_width and interface.start_bg.posy<=y<=interface.start_bg.posy+interface.start_bg.box_height:
				window.set_mouse_cursor(cursor_hand)
			else:
				window.set_mouse_cursor(cursor_default)

	elif player.state == 'game_screen':
		'''casts the cursor to be a hand while the mouse hovers over the ai's board'''
		if engine.mouse_position_is_in(ai_board,x,y):
			window.set_mouse_cursor(cursor_hand)
		else:
			window.set_mouse_cursor(cursor_default)
	elif player.state == 'game_over_screen':
		'''casts the cursor to be a hand while the mouse hovers over the buttons'''
		if engine.mouse_position_is_in(interface.play_again_button,x,y) or engine.mouse_position_is_in(interface.quit_button,x,y):
			window.set_mouse_cursor(cursor_hand)
		else:
			window.set_mouse_cursor(cursor_default)

@window.event
def on_mouse_release(x,y,button,modifier):
	global image_being_dragged
	if player.state == 'set_ship_screen':
		'''Places a ship if the desired coordinates are free'''
		if image_being_dragged!=None:
			if interface.must_shade and interface.ship_shade.color==(255,255,255,100):
				image_being_dragged.sprite.x = interface.ship_shade.posx + interface.ship_shade.box_width//2
				image_being_dragged.sprite.y = interface.ship_shade.posy + interface.ship_shade.box_height//2
				setting_ships_in_grid('set',image_being_dragged)
				
			else:
				image_being_dragged.sprite.x = image_being_dragged.x_initial
				image_being_dragged.sprite.y = image_being_dragged.y_initial
		image_being_dragged=None
	interface.must_shade=False

@window.event
def on_mouse_drag(x, y, dx, dy, button, modifiers):
	if player.state=='set_ship_screen':
		'''Animates the ship picked to follow the cursor'''
		if button==mouse.LEFT and image_being_dragged!=None:
			image_being_dragged.sprite.x=x
			image_being_dragged.sprite.y=y
		if engine.mouse_position_is_in(human_board,x,y) and image_being_dragged!=None:
			interface.must_shade=True

		else:
			interface.must_shade=False

@window.event
def on_mouse_press(x,y,button,modifier):
	global chosen_hero, mouse_dragging, image_being_dragged, previous_num_hits
	if button==mouse.LEFT:
		if player.state=='home_screen':
			'''Functions when the user clicks while in home screen'''
			player.state='choose_player_screen'
			interface.initialize_choose_player_screen(bongo_cats)

		elif player.state=='choose_player_screen':
			'''Functions when the user clicks while the player chooses a player'''
			if chosen_hero!=None and interface.start_bg.posx<=x<=interface.start_bg.posx+interface.start_bg.box_width and interface.start_bg.posy<=y<=interface.start_bg.posy+interface.start_bg.box_height:
					player.state = 'set_ship_screen'
			elif show_name!=None:
					player.name = show_name.name			
					chosen_hero=show_name

		elif player.state =='set_ship_screen':
			'''Functions when the user clicks while the player sets his/her ship'''
			for human_ship in human_ship_list:
				if engine.mouse_position_is_in(human_ship,x,y):
					image_being_dragged=human_ship
			if image_being_dragged!=None and engine.mouse_position_is_in(human_board,x,y):
				setting_ships_in_grid('unset',image_being_dragged)
			if len(human_board.occupied_positions)==17 and interface.start_bg.posx<=x<=interface.start_bg.posx+interface.start_bg.box_width and interface.start_bg.posy<=y<=interface.start_bg.posy+interface.start_bg.box_height:
				player.state='game_screen'
				interface.initialize_game_screen(player, chosen_hero, human_ship_list)
				for i in range(len(human_board.occupied_positions)):
					x, y = human_board.occupied_positions[i]
					human_board.occupied_positions[i] = y, x
				window.set_mouse_cursor(cursor_default)
				engine.occupied = []
				engine.ai_set_ships(ai_board,ai_ship_list)
				for coordinate in engine.occupied:
					y, x = coordinate
					ai_board.occupied_positions.append((x,y))

		elif player.state == 'game_screen':
			'''Functions when the user clicks while playing'''
			if engine.mouse_position_is_in(ai_board,x,y):
				coordinate = ((x-ai_board.sprite.x)//40,9-(y-ai_board.sprite.y)//40)
				if coordinate not in ai_board.attack_positions:
					ai_board.attack_positions.append(coordinate)
					if coordinate in ai_board.occupied_positions:
						game.turn='player'
						interface.if_success_hit(coordinate, ai_board, ai_ship_list)
						interface.change_emotion(chosen_hero, 'happy')
						if set(ai_board.occupied_positions).issubset(ai_board.attack_positions):
							game.winner = 'human'
							window.set_mouse_cursor(cursor_default)
							engine.record_if_highscore(player, chosen_hero)
							interface.initialize_game_over_screen(player, chosen_hero, game)
							player.state = 'game_over_screen'
							game.game_over = True
					else:
						ai_board.fail_hit_sprite_list.append(pyglet.sprite.Sprite(interface.fail_hit.image, x=ai_board.sprite.x+coordinate[0]*40, y=ai_board.sprite.y+(9-coordinate[1])*40, batch=interface.game_screen_batch))
						interface.change_emotion(chosen_hero, None)
						player.score-=1
						game.turn='ai'
					interface.player_click_turn(player, human_board, human_ship_list)

					#Ai's Turn Code
					ai_num_hits=1
					while game.turn=='ai':
						engine.play_sound('laser_sound.wav')
						engine.player_ships = ['carrier', 'battleship', 'cruiser', 'submarine', 'destroyer']
						for coordinate in human_board.occupied_positions:
							y, x =coordinate
							engine.occupied.append((x,y))
						engine.ai_hit(human_board, engine.player_ships)
						ai_num_hits=len(human_board.attack_positions)-previous_num_hits
						previous_num_hits=len(human_board.attack_positions)
						interface.ai_laser_hit(human_board.attack_positions[-1*(ai_num_hits):], human_board, ai_num_hits)
						for i in range(1,ai_num_hits+1):
							if human_board.attack_positions[-1*i] not in human_board.occupied_positions:
								human_board.fail_hit_sprite_list.append(pyglet.sprite.Sprite(interface.fail_hit.image, x=human_board.sprite.x+human_board.attack_positions[-1*i][0]*40, y=human_board.sprite.y+(9-human_board.attack_positions[-1*i][1])*40, batch=interface.game_screen_batch))
							elif set(human_board.occupied_positions).issubset(human_board.attack_positions):
								interface.hide_destroyed_human_ship(human_ship_list, human_board)
								player.score=0
								game.winner = 'ai'
								window.set_mouse_cursor(cursor_default)
								engine.record_if_highscore(player, chosen_hero)
								interface.initialize_game_over_screen(player, chosen_hero, game)
								player.state = 'game_over_screen'
								game.game_over = True
								break
							else:
								interface.if_success_hit(human_board.attack_positions[-1*i], human_board, human_ship_list)
								interface.hide_destroyed_human_ship(human_ship_list, human_board)
							game.turn='human'

		elif player.state == 'game_over_screen':
			'''Functions when the user clicks while in game over screen'''
			if engine.mouse_position_is_in(interface.play_again_button,x,y):
				engine.restart_program()
			elif engine.mouse_position_is_in(interface.quit_button,x,y):
				quit()

	if button==mouse.RIGHT:
		if player.state =='set_ship_screen':
			'''Functions when the user right clicks while setting the ship'''
			for human_ship in human_ship_list:
				if engine.mouse_position_is_in(human_ship,x,y):
					if engine.mouse_position_is_in(human_board,x,y):
						setting_ships_in_grid('unset',human_ship)
					human_ship.switch_orientation()

#keyboard events
@window.event
def on_key_press(symbol, modifiers):

	if player.state =='choose_player_screen':
		if 97<=symbol<=122 and len(player.name)<=15:
			player.name+=chr(symbol).upper()
		elif symbol==key.SPACE and 1<=len(player.name)<=15:
			player.name+=' '
		elif symbol==key.ENTER and 1<=len(player.name):
			player.state = 'set_ship_screen'

	if symbol==key.R:
		#Auto places all the human ships in random positions
		#still has a bug, only used for debugging :)
		if player.state=='set_ship_screen':
			engine.occupied = []
			human_board.occupied_positions=[]
			engine.ai_set_ships(human_board,human_ship_list)
			for coordinate in engine.occupied:
				y, x = coordinate
				human_board.occupied_positions.append((x,y))

@window.event
def on_text_motion(motion):
	if motion == key.MOTION_BACKSPACE and len(player.name)>0:
		player.name=player.name[:-1]

@window.event
def on_draw():

	window.clear()

	if player.state=='home_screen':
		interface.home_screen(bongo_cats)

	elif player.state=='choose_player_screen':
		interface.choose_player_screen(bongo_cats,show_name,player.name,chosen_hero)

	elif player.state=='set_ship_screen':
		interface.set_ship_screen(chosen_hero, human_board, image_being_dragged, human_ship_list)

	elif player.state=='game_screen' or (game.game_over and (chosen_hero.sprite.x<width//2-chosen_hero.image.width//2 and interface.bongo_ai.sprite.x>width//2-interface.bongo_ai.image.width//2)):
		interface.game_screen(chosen_hero,human_board,ai_board, ai_ship_list, player, game)

	elif player.state=='game_over_screen':
		interface.game_over_screen()

@window.event
def update(dt):
	pass

if __name__ == "__main__":
	pyglet.clock.schedule_interval(update, 1/120)
	pyglet.app.run()