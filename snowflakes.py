##Snowflake generator

import math, random, branchmap3
import numpy
from copy import deepcopy

class Snowflake(object):
    def __init__(self):
        self.HEX_GRAD = math.tan(30*math.pi/180.)
        self.map = branchmap3.BranchMap((0,0))
        self.position = (0,0)
        self.size = 0
        self.weight = 0 #Used in gravity and wind calculations

        RANDOM_RANGE = [-1.5,1.5] #Range for rotation speed
        a,b = RANDOM_RANGE
        self.rotate = a + (random.random()*(b-a))

    def __iter__(self):
        return self.map.__iter__()

    def transform(self,matrix):
        self.map.transform(matrix)

    def render_coordinates(self,coord):
        """Converts relative coordinates to absolute"""
        return (coord[0]+self.position[0],coord[1]+self.position[1])

    def get_size(self):
        for c in self.map:
            if c[0][1] > self.size:
                self.size = c[0][1]

    def complete(self):
        """Rotates around 360 degrees to make a full snowflake"""
        self.get_size()
        start = deepcopy(self.map)
        for TURN_BY in range(60,360,60):
            original = deepcopy(start)
            #TURN_BY = 60
            RADIANS = math.pi/180.
            ROTATE = numpy.array([[math.cos(RADIANS*TURN_BY),-math.sin(RADIANS*TURN_BY)],
                                  [math.sin(RADIANS*TURN_BY),math.cos(RADIANS*TURN_BY)]])
            original.transform(ROTATE)
            self.map.map += original.map
            self.map.update_raw()

    def branch(self):
        """Generates one "branch" of the vertcal tree"""
        TYPES = ["single"] #Expandable to add more types

        if len(self.map) == 1: #Make the first line to branch from
            coord = (0,random.randrange(5,11))
            self.map.add_branch(coord)
            self.map.select_coordinate(coord)
            self.weight += coord[1]/100.
        
        random.shuffle(TYPES)
        out = eval("self."+TYPES[0]+"()") #Execute the function randomly chosen from TYPES
        #I know using exec/eval can be dangerous, but this is not coming from user input. Anything to be executed is hard-coded, unless someone really wants to go to the hassle of editing __code__ or something.

        return out
    
    def single(self):
        ROOT3 = 3.**0.5
        length = random.randrange(7,26)

        diameter = length/(2*math.sin(math.pi/6))
        #print length,diameter

        alpha = diameter/2.
        beta = ROOT3*alpha

        x = beta
        y = alpha+self.map.current_coordinate.coord[1]
        #Method of calculating points of a hexagon. Only using the bottom two sides of the hexagon to produce a 120 degree angle between them.

        #print (y-self.map.current_coordinate.coord[1])/(x-self.map.current_coordinate.coord[0])
        self.weight += (((x**2)+(y**2))**0.5)/100. #weight based on line length
        self.map.add_branch((x,y))
        self.map.add_branch((-x,y))
        
        coord = (0,random.randrange(5,11)+self.map.current_coordinate.coord[1])
        self.map.add_branch(coord)
        self.map.select_coordinate(coord)
        self.weight += coord[1]/100.
