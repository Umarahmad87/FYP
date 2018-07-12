import pygame
import numpy as np
resolution = (800,600)

pygame.init()
gamedisplay = pygame.display.set_mode(resolution)
pygame.display.update()
gameExit = False

#2.5 cm = 1 10x10 box
cm_per_pixel = 10
X = 0
Y = 0
oldX = -1
oldY = -1
def grid(cord,surface,color):
	pygame.draw.line(surface,color,(cord[0],cord[1]),(cord[2],cord[3]))

def make_grid():
	grid_x=0
	grid_y=0
	while grid_x < resolution[0]:
		grid([grid_x,grid_y,grid_x,resolution[1]],gamedisplay,(255,0,0))
		grid_x+=cm_per_pixel
	grid_x=0
	while grid_y < resolution[1]:
		grid([grid_x,grid_y,resolution[0],grid_y],gamedisplay,(255,0,0))
		grid_y+=cm_per_pixel
	grid_y=0
	return

make_grid()
pygame.display.update()

while not gameExit:
    for event in pygame.event.get():
        print (event)
        if(event.type==pygame.QUIT):
            gameExit=True
        if(event.type==pygame.KEYDOWN):
        	if event.unicode == 'q':
        		gameExit=True
        	elif event.unicode == 'c':
        		gamedisplay.fill((255,255,255))
        		make_grid()
        		pygame.display.update()
        	"""
        	elif event.unicode == 'o':
        		#pygame.draw.circle(gamedisplay,(0,0,0),(int((oldX*cm_per_pixel)+cm_per_pixel/2),int((oldY*cm_per_pixel)+cm_per_pixel/2))
        		#	,int(cm_per_pixel/2)-1)
        		pygame.draw.circle(gamedisplay,(255,255,255),(int((X*cm_per_pixel)+cm_per_pixel/2),int((Y*cm_per_pixel)+cm_per_pixel/2))
        			,int(cm_per_pixel/2)-1)
        		pygame.display.update()
        		oldX = X
        		oldY = Y
        		#X+=1
        		X = np.random.randint(0,resolution[0]/cm_per_pixel)
        		Y = np.random.randint(0,resolution[1]/cm_per_pixel)
        	"""
    pygame.draw.circle(gamedisplay,(255,255,255),(int((X*cm_per_pixel)+cm_per_pixel/2),int((Y*cm_per_pixel)+cm_per_pixel/2))
    	,int(cm_per_pixel/2)-1)
    X = np.random.randint(0,resolution[0]/cm_per_pixel)
    Y = np.random.randint(0,resolution[1]/cm_per_pixel)
    pygame.display.update()
pygame.quit()
