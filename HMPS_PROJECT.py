import pygame
import math 
from queue import PriorityQueue

WIDTH = 800
WINDOW = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("HMPS PROJECT:PATHFINDER")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Spot:
    def __init__(self, row, col, width, total_rows): #we inititalise the init fn
        self.row = row
        self.col = col
        self.x = row*width  
        self.y = col*width
        self.color= WHITE # a block with white color wld mean that the node is yet to be looked at by the algo
        self.neighbors = []
        self.width= width
        self.total_rows= total_rows

    def get_pos(self):
        return self.row, self.col #this fn will give us the position of the node we are looking for
    
    def is_closed(self):
        return self.color==RED #this wld mean that the block has been searched for
    
    def is_open(self):
        return self.color== GREEN #the node is currently in open set and being looked at
    
    def is_barrier(self):
        return self.color==BLACK#the node is an obstacle and cant be used as a path
    
    def is_start(self):
        return self.color== ORANGE#the node is the start point
    
    def is_end(self):
        return self.color== TURQUOISE #the node is the end point

    def reset(self):
        self.color = WHITE #will change it back to a normal node
    
    def make_closed(self):
        self.color = RED #changes the color of the node to red and hence marking it as a closed node
    
    def make_open(self):
        self.color = GREEN #changes the color of the node to green making it an open node
    
    def make_barrier(self):
        self.color = BLACK #changes the color to black making it an obstacle

    def make_end(self):
        self.color = TURQUOISE #changes color to turquoise making it an end point

    def make_path(self):
        self.color= PURPLE

    def draw(self,WINDOW):
        pygame.draw.rect(WINDOW, self.color, (self.x, self.y,self.width,self.width))#here self.x and self.y define the cordinates of the node that is going to be drawn
                                                                                    #self. color represents thte color we give to it which will represent its fn eg black means obstacle
    def update_neighbors(self,grid):
        pass
    
    def __lt__(self, other): #lt stands for less. we wld invoke this fn when comapring two nodes/spots as named here
        return False

def h(p1,p2): #this is the hysteric fn or the h score which will give us teh shortest dist between 2 points
    x1,y1= p1 #eg p1 is (8,10) then x1 and y1 will directly take value from it coz of python
    x2,y2,=p2
    return abs(x1-x2)+abs(y1-y2) #abs() is a default python fn it gives absolute value.

def make_grid(rows,width):#will hold all the nodes
    grid=[]
    gap = width // rows#width / rows will give the size or dimensions of the node
    for i in range(rows):# this is for loop for row.
        grid.append([])#makes and empty list for the data of node to sit in
        for j in range(rows):#for loop for col. we are assigning nodes their place in grid
            spot = Spot(i,j,gap,rows)#giving the nodes its values
            grid[i].append(spot)#assigning them to grid
        
        return grid


