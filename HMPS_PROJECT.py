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
    
    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = TURQUOISE #changes color to turquoise making it an end point

    def make_path(self):
        self.color= PURPLE

    def draw(self,window):
        pygame.draw.rect(window, self.color, (self.x, self.y,self.width,self.width))#here self.x and self.y define the cordinates of the node that is going to be drawn
    #self. color represents thte color we give to it which will represent its fn eg black means obstacle

    def update_neighbors(self,grid):#we are using this class so that the start or end point dont end up in a circle of barrier and hence being unreachable
        self.neighbors=[]
        if self.row < self.total_rows-1 and not grid[self.row+1][self.col].is_barrier():
            self.neighbors.append(grid[self.row+1][self.col])
        # self.row < self.total_rows-1 is checking if the current row has a row below it
        #grid[self.row+1][self.col].is_barrier() is checking if the node *below* our current node is a barrier or not
        #if it passes both test then it is a suitable neighbor and can be added to the neighbors list we made at start

        if self.row>0 and not grid[self.row-1][self.col].is_barrier():#checks if node above our current node is a suitable neighbor
            self.neighbors.append(grid[self.row-1][self.col])
        
        if self.col < self.total_rows-1 and not grid[self.row][self.col+1].is_barrier():#checks if node on the right is a suitable neighbor
            self.neighbors.append(grid[self.row][self.col+1])

        if self.col > 0 and not grid[self.row][self.col-1].is_barrier():#checks on its left
            self.neighbors.append(grid[self.row][self.col-1])

    def __lt__(self, other): #lt stands for less. we wld invoke this fn when comapring two nodes/spots as named here
        return False


def h(p1,p2): #this is the hysteric fn or the h score which will give us teh shortest dist between 2 points
    x1,y1= p1 #eg p1 is (8,10) then x1 and y1 will directly take value from it coz of python
    x2,y2,=p2
    return abs(x1-x2)+abs(y1-y2) #abs() is a default python fn it gives absolute value.

def reconstruct_path(came_from,current,draw):
    while current in came_from:
        current=came_from[current]
        current.make_path()#it simply run a for loop until it hits the start node which isnt in the list and keeps making a path until then
        draw()

def algorithm(draw,grid,start,end):
    count= 0
    open_set=PriorityQueue()
    open_set.put((0,count,start))#its the same as push but for the priorityqueue library.it basically adds the elemnt to priority queue
    came_from={}#creats an empty list/dictionary
    g_score={spot: float("inf") for row in grid for spot in row } #float("inf") initializes inifinity in python
    #for row in grid for spot in row is shorter way for nested for loops
    #we are basically just giving infinity f score to all nodes
    g_score[start]=0
    f_score={spot:float("inf")for row in grid for spot in row}
    f_score[start]=h(start.get_pos(),end.get_pos())
    
    open_set_hash={start}#this helps us check the nodes that are present in the queue and the ones that arent coz we cant check them in priority queue directly

    while not open_set.empty():#this while will run when the algo has checked all the possible paths.and if we still havent found a path then it donesnt exist
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                pygame.quit()
        
        current = open_set.get()[2]#this will get us the node we are currently looking at.
        open_set_hash.remove(current)#this is to synchronise our hash list with our open set list

        if current == end:#then we have found our shortest path
            reconstruct_path(came_from,end,draw)
            end.make_end()
            return True
        
        for neighbor in current.neighbors:#we are checking all the valid neighbors of current node
            temp_g_score=g_score[current] + 1#coz its adjacent to it so it will take only 1 to reach  the neighbor

            if temp_g_score < g_score[neighbor]:#if the temp score is lower than the actual g score of the neighbor then we actually found a better path so we will upadte the score
                came_from[neighbor]= current
                g_score[neighbor]= temp_g_score
                f_score[neighbor]=temp_g_score+h(neighbor.get_pos(),end.get_pos())
                if neighbor not in open_set_hash:#this is why we are using hash list so that we can actually check
                    count+=1#we increase the count of nodes in the original list
                    open_set.put((f_score[neighbor],count,neighbor))
                    open_set_hash.add(neighbor)#we add the same node to hash list so that both list remain same
                    neighbor.make_open()#indicates to algo that this node needs to be considered too
                
        
        draw()

        if current  != start:
            current.make_closed()#we have looked into its neighbor in above loop so now we close the current node and if we need to open this we will be able when it becomes one of the neighbor with the above loop

    return False        
        
        
        



def make_grid(rows,width):#will hold all the nodes
    grid=[]
    gap = width // rows#width / rows will give the size or dimensions of the node
    for i in range(rows):# this is for loop for row.
        grid.append([])#makes an empty list for the data of node to sit in
        for j in range(rows):#for loop for col. we are assigning nodes their place in grid
            spot = Spot(i,j,gap,rows)#giving the nodes its values
            grid[i].append(spot)#assigning them to grid
        
    return grid#if ukuk XD


def draw_grid(window,rows,width):#it draws the grid lines to separate each spot/node
    gap=width//rows
    for i in range(rows):
        pygame.draw.line(window,GREY,(0,i*gap),(width,i*gap))#for horizontal lines
        #(0,i*gap) and (width,i*gap) gives us the x and y position to draw the horizontal lines in between them
        #for eg (0,3*gap) ,(800,3*gap) this wld draw a horizontal line between those points
        for j in range(rows):
            pygame.draw.line(window,GREY,(j*gap,0),(j*gap,width))#for vertical lines


def draw(window,grid,rows,width):#this function draws the everything
    window.fill(WHITE)#this fills the whole window with one color os our choice at start of every frame
    # i.e essentially clearing the whole frame and giving us a blank frame to work with
    for row in grid:
        for spot in row:
            spot.draw(window)#we are using the draw function to draw each node using the two for loops.
            #ie black white red etc.
    draw_grid(window,rows,width)
    pygame.display.update()#it tells pygame to refresh the screen with new(this) data


def get_clicked_pos(pos,rows,width):
    gap= width//rows
    y,x=pos#directly assigns x,y of pos

    row = y//gap#this will tell us exactly which row and col and hence the actual node being clicked
    col = x//gap

    return row, col


def main(window,width):
    ROWS = 50 #defines total rows in our window
    grid=make_grid(ROWS,width)#makes an empty grid of nodes with dimensions rows and width

    start=None
    end=None

    run=True#these are our flags
    started=False

    while run:
        draw(window,grid,ROWS,width)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            if started:
                continue#this makes sure that once the algo has started the user wont be able to do anything other thaN QUIt
            if pygame.mouse.get_pressed()[0]:#left click
                pos=pygame.mouse.get_pos()#we get the pos whre mouse was clicked
                row, col=get_clicked_pos(pos,ROWS,width)
                spot=grid[row][col]
                if not start and spot != end: #assigning start node
                    start = spot
                    start.make_start()
                
                elif not end and spot != start:#assigning end node
                    end =spot
                    end.make_end()

                elif spot != start and spot != end :#assigning barriers
                    spot.make_barrier() 
            
            elif pygame.mouse.get_pressed()[2]:#right click. [1] means middle button
                pos = pygame.mouse.get_pos()
                row,col=get_clicked_pos(pos,ROWS,width)
                spot=grid[row][col]
                spot.reset()#erasing the clicked node
                if spot == start:#if start node is clicked then its flag also needs to be reset.
                    start=None
                elif spot == end:#same for end node
                    end=None

            if event.type == pygame.KEYDOWN:#KEYDOWN=key pressed    
                if event.key == pygame.K_SPACE and not started:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    algorithm(lambda: draw(window,grid,ROWS,width),grid,start,end)  #lambda is an anonymous function. 
                    #it acts a name for a function. it helps u to pass fucntions as an argument to another funciton.
                    # for eg x=lambda:print("hello") and then u call x(), will print hello.
                if event.key== pygame.K_r:#for resetting
                    start=None
                    end=None
                    grid = make_grid(ROWS,width)  


    pygame.quit()#when close button is clicked


main(WINDOW,WIDTH)#calling the main function
