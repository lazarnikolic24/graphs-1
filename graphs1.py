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
col_darkgray = pg.Color("azure4")
col_darkyellow = pg.Color("yellow4")
col_darkpurp = pg.Color("purple3")
col_darkerpurp = pg.Color("purple4")
col_turquoise = pg.Color("turquoise")
col_lime = pg.Color("lightgreen")


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



# GRAPH
# CODE



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
			#if not node2 in self.connections[node1]:
			#	self.connections[node1].append(node2)
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
node1 = graph.append(Node(screenX // 2, screenY // 2))
node2 = graph.append(Node(screenX // 2, screenY // 2 + 100))
graph.link(node2, node1)

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
	x1 = (x - 10, x)
	y1 = (y, y - 10)
	x2 = (x + 10, x)
	y2 = (y, y + 10)

	for nodeA in graph.connections:
		for nodeB in graph.connections[nodeA]:
			for i in range(0, 2):
				x3 = nodeA.x
				y3 = nodeA.y
				x4 = nodeB.x
				y4 = nodeB.y

				divisor = (x1[i] - x2[i]) * (y3 - y4) - (y1[i] - y2[i]) * (x3 - x4)

#				print(x1[i], ":", y1[i], x2[i], ":", y2[i], x3, ":", y3, x4, ":", y4)
#				print((x1[i] - x2[i]), " ", (y3 - y4), " ", (y1[i] - y2[i]), " ", (x3 - x4))
#				print(divisor)

				if divisor == 0:
					x3 += 5
					y3 += 5
					divisor = (x1[i] - x2[i]) * (y3 - y4) - (y1[i] - y2[i]) * (x3 - x4)
#					print(x1[i], ":", y1[i], x2[i], ":", y2[i], x3, ":", y3, x4, ":", y4)
#					print((x1[i] - x2[i]), " ", (y3 - y4), " ", (y1[i] - y2[i]), " ", (x3 - x4))
#					print(divisor)

				t = (x1[i] - x3) * (y3 - y4) - (y1[i] - y3) * (x3 - x4)
				t /= divisor
				u = -1 * ((x1[i] - x2[i]) * (y1[i] - y3) - (y1[i] - y2[i]) * (x1[i] - x3))
				u /= divisor


				if divisor == 0 or (t >= 0 and t <= 1 and u >= 0 and u <= 1):
					return (True, nodeA, nodeB)

	return (False, None, None)

	# old code, doesn't work as well and is slow

#	for nodeA in graph.connections:
#		for nodeB in graph.connections[nodeA]:
#			r = 10
#			d = pg.math.Vector2((nodeB.x - nodeA.x), (nodeB.y - nodeA.y))
#			f = pg.math.Vector2((nodeA.x - x), (nodeA.y - y))
#		
#			a = d.dot(d)
#			b = 2 * f.dot(d)
#			c = f.dot(f) - r * r
#
#			if b * b - 4 * a * c >= 0:
#				return (True, nodeA, nodeB)
#	return (False, None, None)



# GRAPH
# CODE/



# UI
# CODE



class uiObject:
	def __init__(self, x, y, width, height, text, textsize, parent, clickEvent):
		self.x = x
		self.y = y

		self.width = width
		self.height = height

		self.text = text
		self.textsize = textsize

		self.parent = parent

		self.clickEvent = clickEvent

		self.children = []
		self.enabled = True

	def childDestroyed(self, child):
		while child in self.children:
			self.children.remove(child)

	def get_children(self):
		returnval = []

		reversedChildren = self.children.copy()
		reversedChildren.reverse()
		for child in reversedChildren:
			returnval.append(child)

		return returnval

	def get_rect(self, dx = 0, dy = 0, dw = 0, dh = 0):
		return (self.x + dx, self.y + dy, self.width + dw, self.height + dh)

	def set_rect(self, *rect):
		self.x = rect[0]
		self.y = rect[1]
		self.width = rect[2]
		self.height = rect[3]

	def onClick(self):
		pass

	def colTest(self, x, y):
		if x > self.x - 5 and x < self.x + self.width + 5 and y > self.y - 5 and y < self.y + self.height + 5:
			return True
		else: return False

	def drawSelf(self):
		pass

	def destroy(self):
		for child in self.children:
			child.destroy()

		del self.children
		self.parent.childDestroyed(self)

	def clearChildren(self):
		while len(self.children) > 0:
			self.children[0].destroy()

		self.children.clear()

	def handleEvent(self, event, *args):
		pass

class uiManagerClass():
	def __init__(self, layers):
		self.layers = []
		self.text = "uiManager"
		for i in range(0, layers):
			self.layers.append([])

	def drawSelf(self):
		pass

	def colTest(self, x, y):
		return False

	def get_children(self):
		returnval = []

		for layer in self.layers:
			reversedLayer = layer.copy()
			reversedLayer.reverse()
			for child in reversedLayer:
				returnval.append(child)

		return returnval

	def create(self, object, layer = 0):
		if layer == None:
			layer = len(self.layers)

		while len(self.layers) <= layer:
			self.layers.append([])

		self.layers[layer].append(object)

		return object

	def childDestroyed(self, child):
		for layer in self.layers:
			while child in layer:
				layer.remove(child)

class uiPanel(uiObject):
	def __init__(self, x, y, width, height, text, parent, color):
		super().__init__(x, y, width, height, text, None, parent, None)

		self.color = color

	def drawSelf(self):
		pg.draw.rect(mainSurface, col_white, self.get_rect())
		pg.draw.rect(mainSurface, self.color, self.get_rect(2, 2, -4, -4))

	def encapsulateChildren(self):
		min_x = screenX
		min_y = screenY
		max_x = 0
		max_y = 0

		for child in self.children:
			for i in range(0, 2):
				x = child.x + child.width * i
				y = child.y + child.height * i

				if x < min_x: min_x = x
				if x > max_x: max_x = x
				if y < min_y: min_y = y
				if y > max_y: max_y = y

		self.x = min_x - 4
		self.y = min_y - 4
		self.width = max_x - self.x + 4
		self.height = max_y - self.y + 4

class uiText(uiObject):
	def __init__(self, x, y, width, height, text, textsize, parent, color, fitToText = True):
		super().__init__(x, y, width, height, text, textsize, parent, None)

		self.color = color
		if fitToText:
			self.fitToText()

	def drawSelf(self):
		font = pg.font.SysFont("Verdana", self.textsize, True)
		text = font.render(self.text, True, col_black, self.color)
		text.set_colorkey(self.color)
		textRect = text.get_rect()
		textRect.center = ((self.x + self.width // 2), (self.y + self.height // 2))

		mainSurface.blit(text, textRect)

	def fitToText(self, lockLeft = True, lockTop = True):
		font = pg.font.SysFont("Verdana", self.textsize, True)
		textSize = font.size(self.text)

		self.width = textSize[0]
		if not lockLeft:
			self.x -= self.width

		self.height = textSize[1]
		if not lockTop:
			self.y -= self.height

class uiButton(uiObject):
	def __init__(self, x, y, width, height, padding, text, textsize, parent, clickEvent, color, fitToText = True):
		super().__init__(x, y, width, height, text, textsize, parent, clickEvent)
		self.padding = padding

		self.value = False
		self.color = color

		if fitToText:
			self.fitToText()

	def drawSelf(self):
		self.internalDraw(self.color)

	def internalDraw(self, color):
		font = pg.font.SysFont("Verdana", self.textsize, True)
		text = font.render(self.text, True, col_black, color)
		text.set_colorkey(color)
		textRect = text.get_rect()
		textRect.center = ((self.x + self.width // 2), (self.y + self.height // 2))

		pg.draw.rect(mainSurface, col_white, self.get_rect())
		pg.draw.rect(mainSurface, color, self.get_rect(2, 2, -4, -4))

		mainSurface.blit(text, textRect)

	def fitToText(self, lockLeft = True, lockTop = True, horizontalCenter = False):
		font = pg.font.SysFont("Verdana", self.textsize, True)
		textSize = font.size(self.text)

		if horizontalCenter:
			self.width = textSize[0] + self.padding
			self.x -= self.width // 2
		else:
			self.width = textSize[0] + self.padding
			if not lockLeft:
				self.x -= self.width

		self.height = textSize[1] + self.padding
		if not lockTop:
			self.y -= self.height

	def onClick(self):
		if self.clickEvent != None:
			self.clickEvent(self)
		else:
			print("Clicked " + self.text)

class uiToggleButton(uiButton):
	def __init__(self, x, y, width, height, padding, text, textsize, parent, clickEvent, color, colorB, fitToText = True):
		super().__init__(x, y, width, height, padding, text, textsize, parent, clickEvent, color, fitToText)

		self.colorB = colorB

	def drawSelf(self):
		if self.value:
			self.internalDraw(self.color)
		else:
			self.internalDraw(self.colorB)

	def onClick(self):
		if self.value:
			self.value = False
		else:
			self.value = True

		if self.clickEvent != None:
			self.clickEvent(self)
		else:
			print(self.value)

class uiCheckbox(uiToggleButton):
	def __init__(self, x, y, width, text, textsize, parent, clickEvent, color, colorB):
		super().__init__(x, y, width, width, 0, text, textsize, parent, clickEvent, color, colorB, False)

	def internalDraw(self, color):
		pg.draw.rect(mainSurface, col_gray, self.get_rect())
		pg.draw.rect(mainSurface, color, self.get_rect(2, 2, -4, -4))

	
def algorithmsClickEvent(self):
	global algorithmMode, algoSearchFullGraph

	if algorithmMode == 2:
		if self.value:
			self.value = False
		else: self.value = True
		return

	if self.value:
		algoSearchFullGraph = False
		tempButton = uiButton(screenX - 20, self.y + self.height + 8, 0, 0, 20, "BFS", 18, self, bfsClickEvent, self.colorB, False)
		tempButton.fitToText(False, True)
		self.children.append(tempButton)

		#tempButton = uiButton(screenX - 20, tempButton.y + tempButton.height + 8, 0, 0, 20, "DFS", 18, self, None, self.colorB, False)
		#tempButton.fitToText(False, True)
		#self.children.append(tempButton)
	else:
		self.clearChildren()

		algorithmMode = 0
		global algoStartNode, algoEndNode, selectedNodeA, selectedNodeB
		selectedNodeA = algoStartNode
		selectedNodeB = None
		algoStartNode = None
		algoEndNode = None
		algoSearchFullGraph = False

def bfsClickEvent(self):
	global algorithmMode

	if algorithmMode == 2: return

	if algorithmMode == 0:
		algorithmMode = 1
		algorithm = "BFS"

		global algoStartNode, algoEndNode, selectedNodeA, selectedNodeB
		algoStartNode = selectedNodeA
		algoEndNode = None
		selectedNodeA = None
		selectedNodeB = None
	
		self.clearChildren()
	
		tempPanel = uiPanel(100, 100, 100, 100, "panel", self, col_darkerpurp)
		self.children.append(tempPanel)
	
		tempText = uiText(tempPanel.x + 4, tempPanel.y + 4, 0, 0, "Start", 15, tempPanel, col_darkerpurp, True)
		tempPanel.children.append(tempText)
	
		tempText3 = tempText

		tempText = uiText(tempPanel.x + 4, tempText.y + tempText.height + 4, 0, 0, "Search full graph", 15, tempPanel, col_darkerpurp, True)
		tempPanel.children.append(tempText)
	
		tempText2 = tempText
	
		tempCheckbox = uiCheckbox(tempText2.x + 4 + tempText2.width, tempText2.y, 20, "Full graph?", 15, tempPanel, searchClickEvent, col_white, col_darkgray)
		tempPanel.children.append(tempCheckbox)
	
		tempText = uiText(tempPanel.x + 4, tempText.y + tempText.height + 4, 0, 0, "End", 15, tempPanel, col_darkerpurp, True)
		tempPanel.children.append(tempText)

		tempText4 = tempText
	
		tempPanel.encapsulateChildren()

		global algoFieldA, algoFieldB

		tempButton =  uiButton(tempPanel.x + tempPanel.width, tempText3.y, 0, 0, 8, "mmmmm", 15, tempPanel, fieldClickEvent, col_white, False)
		tempButton.fitToText(False, True, False)
		tempButton.height = tempText3.height
		tempButton.text = ""
		tempPanel.children.append(tempButton)

		algoFieldA = tempButton

		if algoStartNode != None:
			i = 0
			while graph.nodes[i] != algoStartNode:
				i += 1
			algoFieldA.text = str(i)

		tempButton =  uiButton(tempPanel.x + tempPanel.width, tempText4.y, 0, 0, 8, "mmmmm", 15, tempPanel, fieldClickEvent, col_white, False)
		tempButton.fitToText(False, True, False)
		tempButton.height = tempText4.height
		tempButton.text = ""
		tempPanel.children.append(tempButton)

		algoFieldB = tempButton

		tempButton =  uiButton(tempPanel.x + tempPanel.width // 2, tempPanel.y + tempPanel.height, 0, 0, 10, "Search", 16, tempPanel, startClickEvent, self.color, False)
		tempButton.fitToText(False, True, True)
		tempPanel.children.append(tempButton)
	
		tempPanel.encapsulateChildren()

def fieldClickEvent(self):
	global algoStartNode, algoEndNode, algoFieldA, algoFieldB

	self.text = ""

	if self == algoFieldA:
		algoStartNode = None
	else:
		algoEndNode = None

def startClickEvent(self):
	global algorithmMode, algoSteps, algoStartNode, algoEndNode
	if algoStartNode != None and (algoEndNode != None or algoSearchFullGraph):
		algorithmMode = 2
		algoSteps = 0
		self.parent.destroy()

		tempButton =  uiManager.create(uiButton(100, 100, 0, 0, 20, "Step", 18, uiManager, stepClickEvent, col_darkpurp, True))

def searchClickEvent(self):
	global algoSearchFullGraph, algoFieldB, algoEndNode
	if self.value:
		algoSearchFullGraph = True
		algoFieldB.text = ""
		algoFieldB.color = col_gray
		algoEndNode = None
	else:
		algoSearchFullGraph = False
		algoFieldB.color = col_white

def stepClickEvent(self):
	global algoSteps, algoStartNode, algoEndNode, algorithmMode, finished
	
	if finished:
		algorithmMode = 0
		finished = False
		algoReset()
		self.destroy()
	else:
	
		algoSteps += 1
		#print(algoSteps)
		bfs(algoStartNode, algoEndNode, algoSteps)
	
		if finished:
			self.y += self.height + 2
			self.text = "Finish"
			self.fitToText()


uiManager = uiManagerClass(3)
tempButton = uiManager.create(uiToggleButton(screenX - 20, 20, 0, 0, 20, "Algorithms", 19, uiManager, algorithmsClickEvent, col_darkpurp, col_darkerpurp, False))
tempButton.fitToText(False, True)



# UI
# CODE/

def algoReset():
	global visitedNodes, bfs_neighbours, currentNode, currentNodeB, finished, path, finalPath
	visitedNodes = []
	bfs_neighbours = []
	currentNode = None
	currentNodeB = None
	finished = None
	path = {}
	finalPath = {}

visitedNodes = []

bfs_neighbours = []

currentNode = None
currentNodeB = None

finished = False

path = {}
finalPath = {}

def bfs(start, end, step):
	global visitedNodes, bfs_neighbours, currentNode, currentNodeB, finished, path

	visitedNodes = []

	bfs_neighbours = [start]

	currentNode = start
	currentNodeB = None

	finished = False
	path = {}
	finapPath = {}

	n_neighbours = 1

	i = 0
	steps = 0
	while i < n_neighbours and steps < step:
		currentNode = bfs_neighbours[i]

		steps += 1
		if steps < step:

			for node in graph.connections[currentNode]:
				if steps >= step: break

				currentNodeB = node

				steps += 1
				if steps < step:

					if not node in visitedNodes and not node in bfs_neighbours:
						bfs_neighbours.append(node)
						n_neighbours += 1

						path[node] = bfs_neighbours[i]

						steps += 1
						if steps < step:
							if node == end and not algoSearchFullGraph:
								finished = True
								oldPath = path.copy()

								path.clear()

								temp = end
								while temp != start:
									finalPath[temp] = oldPath[temp]
									temp = finalPath[temp]


								return
							else: steps -= 1



					else: 
						steps -= 1
						if node in visitedNodes:
							temp = bfs_neighbours[i]
							while temp != node:
								finalPath[temp] = path[temp]
								temp = path[temp]
							finalPath[temp] = bfs_neighbours[i]


				steps += 1
			
			if steps < step:
				currentNodeB = None
	
				steps += 1
				if steps < step:
	
					visitedNodes.append(bfs_neighbours[i])
	
					i += 1
					steps += 1

	#currentNode = bfs_neighbours[i]
	#for node in graph.connections[currentNode]:
	#	if not node in visitedNodes:
	#		bfs_neighbours.append(node)
	#		n_neighbours += 1

	#print(visitedNodes)
	#print(bfs_neighbours)

	steps += 1
	if steps < step:
		finished = True


algorithmMode = 0
# 0 - not running
# 1 - configuring
# 2 - running

algorithm = ""

algoStartNode = None
algoEndNode = None
algoSearchFullGraph = False

algoSteps = 0


selectedNodeA = None
selectedNodeB = None

dragging = False

def recursiveClick(object, x, y):
	global clickConsumed
	for obj in object.get_children():
		recursiveClick(obj, x, y)
		if clickConsumed:
			return
	if object.colTest(x, y):
		object.onClick()
		clickConsumed = True

def handleEvent(event):
	global graph, selectedNodeA, selectedNodeB, dragging, algorithmMode, algoSearchFullGraph

	if event.type == pg.KEYDOWN:
		if event.key == pg.K_ESCAPE:
			selectedNodeA = None
			selectedNodeB = None

	elif event.type == pg.MOUSEBUTTONDOWN:
		if event.button == 1 and not dragging:
			#LEFT CLICK

			global clickConsumed, uiManager, algoStartNode, algoEndNode, algoFieldA, algoFieldB
			clickConsumed = False

			recursiveClick(uiManager, event.pos[0], event.pos[1])

			if not clickConsumed:

				if algorithmMode == 1:
					selection = selectNode(event.pos[0], event.pos[1])
					if selection[0]:

						if algoStartNode == None or algoSearchFullGraph:
							algoStartNode = selection[1]

							i = 0
							while graph.nodes[i] != selection[1]:
								i += 1

							algoFieldA.text = str(i)
						else:
							algoEndNode = selection[1]

							i = 0
							while graph.nodes[i] != selection[1]:
								i += 1

							algoFieldB.text = str(i)


				elif algorithmMode == 0:
					selection = selectNode(event.pos[0], event.pos[1])
					if selection[0]:
						selectedNodeB = selectedNodeA
						selectedNodeA = selection[1]
						if selectedNodeB != None:
							graph.link(selectedNodeA, selectedNodeB)
						selectedNodeB = None
					else:
						selectedNodeB = selectedNodeA
						selectedNodeA = graph.append(Node(event.pos[0], event.pos[1]))
						
						selection = selectConnection(event.pos[0], event.pos[1])
		
						if selection[0]:
							graph.disconnect(selection[1], selection[2])
							graph.link(selectedNodeA, selection[1])
							graph.link(selectedNodeA, selection[2])
	
						if selectedNodeB != None:
							graph.link(selectedNodeA, selectedNodeB)
						selectedNodeB = None


		elif event.button == 3 and not dragging:
			#RIGHT CLICK

			if algorithmMode == 1:

				selection = selectNode(event.pos[0], event.pos[1])
				if selection[0]:
					if selection[1] == algoStartNode:
						algoStartNode = None
						algoFieldA.text = ""
					if selection[1] == algoEndNode:
						algoEndNode = None
						algoFieldB.text = ""

			elif algorithmMode == 0:
				if selectedNodeA == None:
					selection = selectNode(event.pos[0], event.pos[1])
					if selection[0]:
						graph.remove(selection[1])
					else:
						selection = selectConnection(event.pos[0], event.pos[1])
						if selection[0]:
							graph.disconnect(selection[1], selection[2])
	
				selectedNodeA = None
				selectedNodeB = None

		elif event.button == 2:
			#MIDDLE CLICK

			if algorithmMode == 1:
				pass
			elif algorithmMode == 0:
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

def recursiveDraw(object):
	object.drawSelf()

	for obj in object.get_children():
		recursiveDraw(obj)

def uiDraw():
	global uiManager
	recursiveDraw(uiManager)

def drawArrow(surface, color, pos1, pos2, width):
	seglen = 30

	pg.draw.line(surface, color, pos1, pos2, width)
	dx = pos1[0] - pos2[0]
	dy = pos1[1] - pos2[1]
	angle = math.atan2(dy, dx)

	angle1 = angle - math.pi/4
	dx1 = seglen * math.cos(angle1)
	dy1 = seglen * math.sin(angle1)

	x1 = pos2[0] + dx1
	y1 = pos2[1] + dy1

	angle2 = angle + math.pi/4
	dx2 = seglen * math.cos(angle2)
	dy2 = seglen * math.sin(angle2)

	x2 = pos2[0] + dx2
	y2 = pos2[1] + dy2

	pg.draw.line(surface, color, pos2, (x1, y1), width)
	pg.draw.line(surface, color, pos2, (x2, y2), width)

def draw():
	mainSurface.lock()

	mainSurface.fill(col_black)

	mousePos = pg.mouse.get_pos()

	closestNode = (False, None)
	if not dragging:
		closestNode = selectNode(mousePos[0], mousePos[1])

	closestConnection = selectConnection(mousePos[0], mousePos[1])
	for node in graph.connections:
		for link in graph.connections[node]:
			col = linkCol

			if not dragging and (selectedNodeA == None or True) and not closestNode[0] and algorithmMode == 0:
				if closestConnection[0] and (node == closestConnection[1] and link == closestConnection[2]) or (node == closestConnection[2] and link == closestConnection[1]):
					col = col_darkyellow

			if algorithmMode == 2 and finished == True:
				if (node in finalPath and finalPath[node] == link) or (link in finalPath and finalPath[link] == node):
					col = col_turquoise

			drawArrow(mainSurface, col, node.get_pos(), link.get_pos(), 2)


	if selectedNodeA != None and not dragging and algorithmMode == 0:
		closestNode = selectNode(mousePos[0], mousePos[1])
		if closestNode[0]:
			pg.draw.line(mainSurface, col_gray, selectedNodeA.get_pos(), closestNode[1].get_pos(), 2)
		else:
			pg.draw.line(mainSurface, col_gray, selectedNodeA.get_pos(), mousePos, 2)


	for node in graph.nodes:
		if algorithmMode == 1:
			col = nodeCol
			selected = False

			if node == algoEndNode:
				selected = True
				col = col_turquoise
				pg.draw.circle(mainSurface, col, node.get_pos(), nodeSize + 3)

			if node == algoStartNode:
				selected = True
				col = selectedCol
				pg.draw.circle(mainSurface, col, node.get_pos(), nodeSize + 1)

			if not dragging and selectedNodeA == None:
				if closestNode[0] and node == closestNode[1]:
					col = col_darkyellow
					if selected:
						pg.draw.circle(mainSurface, col, node.get_pos(), nodeSize)

			if not selected:
				pg.draw.circle(mainSurface, col, node.get_pos(), nodeSize)

		elif algorithmMode == 2:
			col = nodeCol
			selected = False

			if node == currentNode and not finished:
				selected = True
				col = col_lime
				pg.draw.circle(mainSurface, col, node.get_pos(), nodeSize + 5)

			if node == currentNodeB and not finished:
				selected = True
				col = col_orange
				pg.draw.circle(mainSurface, col, node.get_pos(), nodeSize + 4)

			if node in finalPath and finished:
				col = col_turquoise

			if node == algoEndNode:
				selected = True
				col = col_turquoise
				pg.draw.circle(mainSurface, col, node.get_pos(), nodeSize + 3)

			if node == algoStartNode:
				selected = True
				col = selectedCol
				pg.draw.circle(mainSurface, col, node.get_pos(), nodeSize + 1)

			if node in bfs_neighbours and not node in visitedNodes and not finished:
				col = col_darkyellow
				if selected:
					pg.draw.circle(mainSurface, col, node.get_pos(), nodeSize)
			elif node in visitedNodes and not finished:
				col = col_red
				if selected:
					pg.draw.circle(mainSurface, col, node.get_pos(), nodeSize)

			if not selected:
				pg.draw.circle(mainSurface, col, node.get_pos(), nodeSize)

		else:
			col = nodeCol
			if node == selectedNodeA:
				col = selectedCol
	
			if not dragging and selectedNodeA == None:
				if closestNode[0] and node == closestNode[1]:
					col = col_darkyellow
	
			pg.draw.circle(mainSurface, col, node.get_pos(), nodeSize)


	mainSurface.unlock()

	for i in range(0, len(graph.nodes)):
		col = nodeCol
		if graph.nodes[i] == selectedNodeA:
			col = selectedCol
		if graph.nodes[i] == closestNode[1]:
			col = col_darkyellow

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