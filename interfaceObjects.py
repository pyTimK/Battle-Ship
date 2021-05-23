import pyglet, random, math

class Image:
	def __init__(self, image):
		self.image=pyglet.image.load('res/sprites/'+image)
class Sprite:
	def __init__(self, image, x=0, y=0, image_width=None, image_height=None, anchor_x='left', anchor_y='bottom', batch=None, group=None):
		self.image = pyglet.image.load('res/sprites/'+image)
		self.image.anchor = (anchor_x, anchor_y)
		if image_width!=None and image_height!=None:
			self.image.width=image_width
			self.image.height=image_height
		self.batch=batch
		self.sprite = pyglet.sprite.Sprite(self.image, x=x, y=y, batch=self.batch, group=group)

	def draw(self):
		self.sprite.draw()

class Text:
	def __init__(self, text_str,xpos,ypos,color=(0,0,0,255),anchor_x='left', anchor_y='bottom',font_size=25,batch=None, group=None ):
		self.text_str=text_str
		self.xpos=xpos
		self.ypos=ypos
		self.color=color
		self.font_size=font_size
		self.batch=batch
		self.anchor_x=anchor_x
		self.anchor_y=anchor_y
		self.text = pyglet.text.Label(self.text_str,
	                      font_size=self.font_size,
	                      x=self.xpos, y=self.ypos, anchor_x=self.anchor_x, anchor_y=self.anchor_y,
	        	          color=self.color, batch=self.batch, group=group)
	def draw(self):
		pyglet.text.Label(self.text_str,
	                      font_size=self.font_size,
	                      x=self.xpos, y=self.ypos, anchor_x=self.anchor_x, anchor_y=self.anchor_y,
	        	          color=self.color, batch=self.batch).draw()


class Background:
	def __init__(self, posx, posy, box_width, box_height,color=(255,255,255,255), batch=None):
		self.posx=posx
		self.posy=posy
		self.box_width=box_width
		self.box_height=box_height
		self.color=color
		self.image = pyglet.image.SolidColorImagePattern(self.color).create_image(self.box_width, self.box_height)
		self.image.batch=batch

	def draw(self):
		self.image.blit(self.posx, self.posy)

class Animation:
	def __init__(self, image, row, column, image_width, image_height, x=0, y=0, fps=0.03, looping=True, batch=None):
		self.row = row
		self.column = column
		self.fps = fps
		self.image = pyglet.image.load('res/sprites/'+image)
		self.seq = pyglet.image.ImageGrid(self.image, self.row, self.column, item_width=image_width, item_height=image_height)
		self.animation = pyglet.image.Animation.from_image_sequence(self.seq[0:], self.fps, loop=looping)
		self.sprite = pyglet.sprite.Sprite(self.animation, x,y, batch=batch)
		self.play_time = (self.row*self.column)*self.fps

	def animate(self):
	    self.play_time -= self.fps
	    if self.play_time > 0:
	    	self.sprite.draw()
	    else:
	    	self.sprite.position= (0,0)

	def update(self, x, y):
		self.play_time=(self.row*self.column)*self.fps
		self.sprite = pyglet.sprite.Sprite(self.animation, x,y)

class Laser:
	def __init__(self, x=1078, y=549, batch=None):
		self.image = pyglet.image.load('res/sprites/laser.png')
		self.sprite = pyglet.sprite.Sprite(self.image, x=x, y=y, batch=batch, group=pyglet.graphics.OrderedGroup(2))
		self.x_target = 0
		self.y_target = 0
		self.x_distance = 0
		self.y_distance = 0
		self.speed=20
		self.visibility='hidden'

	def animate(self, animate_type=None, origin='right'):
		if animate_type=='infinite' and origin=='right':
			if self.sprite.x >= self.x_target and self.sprite.y >= self.y_target:
				self.sprite.x-=self.x_distance//self.speed
				self.sprite.y-=self.y_distance//self.speed
				self.sprite.draw()
			else:
				self.sprite.x=1200
				self.sprite.y=600
				self.x_target = random.randint(-10,1200)
				self.y_target = -10
				self.x_distance = (self.sprite.x-self.x_target)
				self.y_distance = (self.sprite.y-self.y_target)
				self.sprite.rotation = 180+math.degrees(math.atan(self.x_distance/self.y_distance))

		elif animate_type=='infinite' and origin=='left':
			if self.sprite.x <= self.x_target and self.sprite.y >= self.y_target:
				self.sprite.x+=self.x_distance//self.speed
				self.sprite.y-=self.y_distance//self.speed
				self.sprite.draw()
			else:
				self.sprite.x=0
				self.sprite.y=600
				self.x_target = random.randint(0,1210)
				self.y_target = -10
				self.x_distance = (self.x_target-self.sprite.x)
				self.y_distance = (self.sprite.y-self.y_target)
				self.sprite.rotation = 180-math.degrees(math.atan(self.x_distance/self.y_distance))

		else:
			if self.sprite.x >= self.x_target+20 and self.sprite.y >= self.y_target+20 and self.visibility=='visible':
				self.sprite.x-=self.x_distance//self.speed
				self.sprite.y-=self.y_distance//self.speed
				self.sprite.draw()
			else:
				self.visibility='hidden'

class Cat_home_screen:
	def __init__(self, batch=None, width=1200):
		self.image = pyglet.image.load('res/sprites/bongo'+str(random.randint(1,7))+'_happy.png')
		self.sprite = pyglet.sprite.Sprite(self.image, x=random.randint(30,width//2), y=random.randint(50,250), batch=batch)
		self.sprite.scale = 2
		self.sprite.opacity = 0
		self.x_initial = self.sprite.x
		self.y_initial = self.sprite.y

	def animate(self):

		if self.sprite.x >= self.x_target+20 and self.sprite.y >= self.y_target+20 and self.visibility=='visible':
			self.sprite.x-=self.x_distance//self.speed
			self.sprite.y-=self.y_distance//self.speed
			self.sprite.draw()
		else:
			self.visibility='hidden'