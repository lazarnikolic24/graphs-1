import random
import math
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
col_gray = pg.Color("gray")
col_darkyellow = pg.Color("yellow4")


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

def dist(A, B):
	return math.sqrt(math.fabs(A[0] - B[0])**2 + math.fabs(A[1] - B[1])**2)


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
		if node1 != node2:
			self.connections.setdefault(node1, [])
			if not node2 in self.connections[node1]:
				self.connections[node1].append(node2)
			self.connections.setdefault(node2, [])
			if not node1 in self.connections[node2]:
				self.connections[node2].append(node1)

	def remove(self, node):
		while node in self.nodes:
			self.nodes.remove(node)

		while node in self.connections:
			self.connections.pop(node)

		for connection in self.connections:
			while node in self.connections[connection]:
				self.connections[connection].remove(node)

	def disconnect(self, nodeA, nodeB):
		while nodeB in self.connections[nodeA]:
			self.connections[nodeA].remove(nodeB)

		while nodeA in self.connections[nodeB]:
			self.connections[nodeB].remove(nodeA)

graph = Graph()
#node1 = graph.append(Node(screenX // 2, screenY // 2))
#node2 = graph.append(Node(screenX // 2, screenY // 2 + 100))
#graph.link(node1, node2)

selectedNodeA = None
selectedNodeB = None

dragging = False

def selectNode(x, y):
	min_dist = screenX * screenY
	min_node = None
	for node in graph.nodes:
		distance = dist((x, y), node.get_pos())
		if  distance < nodeSize + 10 and distance < min_dist:
			min_dist = distance
			min_node = node

	if min_node != None:
		return (True, min_node)
	else:
		return (False, None)

# Currently has issues, will be reworked
def selectConnection(x, y):
	for nodeA in graph.connections:
		for nodeB in graph.connections[nodeA]:
			r = 10
			d = pg.math.Vector2((nodeB.x - nodeA.x), (nodeB.y - nodeA.y))
			f = pg.math.Vector2((nodeA.x - x), (nodeA.y - y))
		
			a = d.dot(d)
			b = 2 * f.dot(d)
			c = f.dot(f) - r * r

			if b * b - 4 * a * c >= 0:
				return (True, nodeA, nodeB)
	return (False, None, None)

def handleEvent(event):
	global graph, selectedNodeA, selectedNodeB, dragging

	if event.type == pg.KEYDOWN:
		if event.key == pg.K_ESCAPE:
			selectedNodeA = None

	elif event.type == pg.MOUSEBUTTONDOWN:
		if event.button == 1 and not dragging:
			#LEFT CLICK
			selection = selectNode(event.pos[0], event.pos[1])
			if selection[0]:
				selectedNodeB = selectedNodeA
				selectedNodeA = selection[1]
			else:
				selectedNodeB = selectedNodeA
				selectedNodeA = graph.append(Node(event.pos[0], event.pos[1]))

			if selectedNodeB != None:
				graph.link(selectedNodeA, selectedNodeB)
			selectedNodeB = None

		elif event.button == 3 and not dragging:
			#RIGHT CLICK
			selection = selectNode(event.pos[0], event.pos[1])
			if selection[0]:
				graph.remove(selection[1])
			elif selectedNodeA == None and False:
				# Has issues, will be reworked
				selection = selectConnection(event.pos[0], event.pos[1])
				if selection[0]:
					graph.disconnect(selection[1], selection[2])

			selectedNodeA = None
			selectedNodeB = None

		elif event.button == 2:
			#MIDDLE CLICK
			selection = selectNode(event.pos[0], event.pos[1])
			if selection[0]:
				selectedNodeA = selection[1]
				dragging = True

	elif event.type == pg.MOUSEBUTTONUP:
		if event.button == 2:
			#MIDDLE CLICK
			if dragging:
				dragging = False
				selectedNodeA = None


def update():
	mouseRel = pg.mouse.get_rel()
	if dragging:
		selectedNodeA.x += mouseRel[0]
		selectedNodeA.y += mouseRel[1]



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


	mousePos = pg.mouse.get_pos()
#	if not dragging and selectedNodeA == None:
#		closestConnection = selectConnection(mousePos[0], mousePos[1])
#		if closestConnection[0]:
#			pg.draw.line(mainSurface, col_darkyellow, closestConnection[1].get_pos(), closestConnection[2].get_pos(), 3)

	if selectedNodeA != None and not dragging:
		closestNode = selectNode(mousePos[0], mousePos[1])
		if closestNode[0]:
			pg.draw.line(mainSurface, col_gray, selectedNodeA.get_pos(), closestNode[1].get_pos(), 2)
		else:
			pg.draw.line(mainSurface, col_gray, selectedNodeA.get_pos(), mousePos, 2)


	for node in graph.nodes:
		col = nodeCol
		if node == selectedNodeA:
			col = selectedCol
		pg.draw.circle(mainSurface, col, node.get_pos(), nodeSize)


#	if not dragging and selectedNodeA == None:
#		closestNode = selectNode(mousePos[0], mousePos[1])
#		if closestNode[0]:
#			pg.draw.circle(mainSurface, col_darkyellow, closestNode[1].get_pos(), nodeSize + 1)

	mainSurface.unlock()

	for i in range(0, len(graph.nodes)):
		col = nodeCol
		if graph.nodes[i] == selectedNodeA:
			col = selectedCol

		string = str(i)
		if len(string) == 2:
			font = pg.font.SysFont("Verdana", int(nodeSize), True)
		elif len(string) == 3:
			font = pg.font.SysFont("Verdana", int(nodeSize * 0.7), True)
		else:
			font = pg.font.SysFont("Verdana", int(nodeSize * 1.2 / len(string)), True)

		text = font.render(string, True, col_black, col)
		text.set_colorkey(col)
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