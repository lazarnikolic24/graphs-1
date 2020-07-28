import random
import pygame as pg
pg.init()



screenX = 800
screenY = 800

mainSurface = pg.display.set_mode((screenX, screenY))
pg.display.set_caption("Grafovi - @lazarnikolic24")

fpsLimit = 60



col_white = pg.Color("white")
col_black = pg.Color("black")
col_red = pg.Color("red")
col_blue = pg.Color("blue")
col_orange = pg.Color("orange")
col_yellow = pg.Color("yellow")

def col_random():
	return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 255)

def clamp(num, min, max):
	if num < min:
		num = min
	if num > max:
		num = max
	return num

def ilerp(a, b, t):
	t = clamp(t, 0, 1)
	return int(a + (b - a) * t)

def lerp(a, b, t):
	t = clamp(t, 0, 1)
	return a + (b - a) * t

def col_lerp(a, b, t):
	t = clamp(t, 0, 1)
	return (ilerp(a[0], b[0], t), ilerp(a[1], b[1], t), ilerp(a[2], b[2], t), ilerp(a[3], b[3], t))



class Node:
	def __init__(self, x, y):
		self.x = int(x)
		self.y = int(y)

nodes = []
nodes.append(Node(screenX // 2, screenY // 2))

nodeSize = 10
nodeCol = col_white



def handleEvent(event):
	if event.type == pg.MOUSEBUTTONDOWN:
		if event.button == 1:
			print("click")
		

def update():
	pass


def debugDraw():
	font = pg.font.SysFont("Verdana", 18)

	spacing = 4
	textX = spacing
	textY = spacing


	stringFPS = "FPS: " + str(int(fps))
	textFPS = font.render(stringFPS, True, col_black, col_white)
	mainSurface.blit(textFPS, (textX, textY))

	textY += textFPS.get_height() + spacing


	stringdT = "dT: " + str(dTime) + "s"
	textdT = font.render(stringdT, True, col_black, col_white)
	mainSurface.blit(textdT, (textX, textY))

	textY += textdT.get_height() + spacing

def draw():
	mainSurface.lock()

	mainSurface.fill(col_black)

	for node in nodes:
		pg.draw.circle(mainSurface, nodeCol, (node.x, node.y), nodeSize)

	mainSurface.unlock()

	for i in range(0, len(nodes)):

		font = pg.font.SysFont("Verdana", int(nodeSize * 1.2), True)
		string = str(i)
		text = font.render(string, True, col_black, col_white)
		textRect = text.get_rect()
		textRect.center = (nodes[i].x, nodes[i].y)
		mainSurface.blit(text, textRect)

	
	debugDraw()

	pg.display.update()


clock = pg.time.Clock()
dTime = 1
fps = 0
mainRunning = True
while mainRunning:
	for event in pg.event.get():
		if event.type == pg.QUIT:
			mainRunning = False

		handleEvent(event)

	update()

	draw()

	dTime = clock.tick(fpsLimit) / 1000
	fps = clock.get_fps()

pg.quit()
quit()