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


nodeSize = 10
nodeCol = col_white
linkCol = col_white
selectedCol = col_yellow



#Tona ipo utlity funkcija koje su preostale iz prethodnog projekta pa ih nisam sklonio odavde

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

	def get_pos(self):
		return (self.x, self.y)



class Graph:
	def __init__(self):
		self.nodes = []
		self.connections = {}

	def append(self, node):
		self.nodes.append(node)
		return node

	def link(self, node1, node2):
		self.connections.setdefault(node1, [])
		self.connections[node1].append(node2)
		self.connections.setdefault(node2, [])
		self.connections[node2].append(node1)

graph = Graph()
node1 = graph.append(Node(screenX // 2, screenY // 2))
node2 = graph.append(Node(screenX // 2, screenY // 2 + 100))
graph.link(node1, node2)

selectedNode = None
cursorMode = "move"
# Cursor modes:
# "move"
# "link"
# "place"
# "delete"

def handleEvent(event):
	if event.type == pg.MOUSEBUTTONDOWN:
		if event.button == 1:
			global graph, selectedNode
			selectedNode = graph.append(Node(event.pos[0], event.pos[1]))


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

def uiDraw():
	pass

def draw():
	mainSurface.lock()

	mainSurface.fill(col_black)

	for node in graph.connections:
		for link in graph.connections[node]:
			pg.draw.line(mainSurface, linkCol, node.get_pos(), link.get_pos(), 2)

	for node in graph.nodes:
		col = nodeCol
		if node == selectedNode:
			col = selectedCol
		pg.draw.circle(mainSurface, col, node.get_pos(), nodeSize)

	mainSurface.unlock()

	for i in range(0, len(graph.nodes)):
		col = nodeCol
		if graph.nodes[i] == selectedNode:
			col = selectedCol

		string = str(i)
		if len(string) == 2:
			font = pg.font.SysFont("Verdana", int(nodeSize), True)
		elif len(string) == 3:
			font = pg.font.SysFont("Verdana", int(nodeSize * 0.7), True)
		else:
			font = pg.font.SysFont("Verdana", int(nodeSize * 1.2 / len(string)), True)

		text = font.render(string, True, col_black, col)
		textRect = text.get_rect()
		textRect.center = (graph.nodes[i].get_pos())
		mainSurface.blit(text, textRect)

	uiDraw()
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