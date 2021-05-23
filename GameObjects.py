import pyglet

class Bongo:
	show_name = False
	def __init__(self, image, name, batch=None):
		self.image_name=image
		self.image = pyglet.image.load('res/sprites/'+image+'.png')
		self.name = name
		self.sprite = pyglet.sprite.Sprite(self.image, x=0, y=0, batch=batch)


	def draw(self):
		self.sprite.draw()




class Player:
	def __init__(self):
		self.name = ''
		self.score = 100
		self.state = 'home_screen'

	def update(self):
		pass


class Game:
	def __init__(self, turn):
		self.turn=turn
		self.allowed_to_click=True
		self.game_over = False
		self.winner = None

class Board:
	def __init__(self,in_control,grid,x=0,y=0):
		self.texture = pyglet.image.Texture.create(400,400)
		self.image = pyglet.image.load('res/sprites/board.png')
		self.in_control = in_control
		self.grid = grid
		self.sprite = pyglet.sprite.Sprite(self.image, x=x, y=y)

		#occupied_positions and attack_positions are both lists of tuples
		self.occupied_positions = []
		self.attack_positions = []
		self.fail_hit_sprite_list = []
		self.success_hit_sprite_list = []

	def draw(self):
		self.sprite.draw()	

class GamePiece:
	def __init__(self,name,size,x=0,y=0):
		self.image = pyglet.image.load('res/sprites/'+name+'.png')
		self.image.anchor_x=self.image.width//2
		self.image.anchor_y=self.image.height//2
		self.name = name
		self.size = size
		self.x_initial = x
		self.y_initial = y
		self.orientation = 'horizontal'
		self.coordinates=[]
		self.sprite = pyglet.sprite.Sprite(self.image, x=x, y=y)
		self.visibility='hidden'
	def switch_orientation(self):
		if self.orientation=='vertical':
			self.orientation='horizontal'
			self.sprite.rotation=0
		elif self.orientation=='horizontal':
			self.orientation='vertical'
			self.sprite.rotation=90


	def draw(self):
		self.sprite.draw()