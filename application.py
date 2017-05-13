import pygame
from pygame.locals import *

import branchmap3 as branchmap
import snowflakes

import math,numpy,random

class App(): #Based on my PygameBase
    def __init__(self,width,height,title="pygame window",icon=None):
        self.running = False
        self.size = (width,height)
        self.title = title
        self.icon = icon
        pygame.init()

    def init(self):
        """Commands to be processed before the application starts"""
        NUM_SNOWFLAKES = 10 #How many snowflakes to make. 1 to 5 should be fine at 100 fps, it starts to slow noticeably from there.
        
        pygame.display.set_caption(self.title)
        if self.icon != None:
            self.icon = pygame.image.load(self.icon)
            pygame.display.set_icon(self.icon)
        self.display = pygame.display.set_mode(self.size, pygame.HWSURFACE | DOUBLEBUF)

        self.font = pygame.font.SysFont("kruella",40) #Preference for Kruella. Otherwise standard pygame font should be used.

        self.snowflakes = []
        for x in range(NUM_SNOWFLAKES): 
            snowflake = snowflakes.Snowflake() #All generated snowflakes are stored here.
            for i in range(2,6):
                snowflake.branch()
            snowflake.complete()
            snowflake.position = (random.randrange(0,self.size[0]+1),-snowflake.size)
            self.snowflakes.append(snowflake)

        self.clock = pygame.time.Clock()
        return True

    def get_transform_array(self,TURN_BY):
        """Get a transformation array based on degree rotation"""
        RADIANS = math.pi/180.
        return numpy.array([[math.cos(RADIANS*TURN_BY),-math.sin(RADIANS*TURN_BY)],
                      [math.sin(RADIANS*TURN_BY),math.cos(RADIANS*TURN_BY)]])


    def __loop__(self):
        """Commands processed every frame"""
        GRAVITY = 0.75 # affects how fast snowflakes fall
        WIND_CONSTANT = 0.25 # wind = sin(time)+constant. Affects how much the snowflakes will actually be moved. 0 means they will just oscillate back and forth around a mean position.
        wind = math.sin(pygame.time.get_ticks()/1000.)+WIND_CONSTANT
        for snowflake in self.snowflakes:
            #self.snowflake = snowflake
            snowflake.transform(self.get_transform_array(snowflake.rotate*((self.clock.get_time()/1000.)*60)))
            if snowflake.position[1] <= snowflake.size + self.size[1]:
                snowflake.position = (snowflake.position[0]+(wind/snowflake.weight),snowflake.position[1]+GRAVITY*snowflake.weight*((self.clock.get_time()/1000.)*60))
            else:
                self.snowflakes.remove(snowflake) #Destroy the snowflake and make a new one
                snowflake = snowflakes.Snowflake()
                for i in range(2,6):
                    snowflake.branch()
                snowflake.complete()
                snowflake.position = (random.randrange(0,self.size[0]+1),-snowflake.size)
                self.snowflakes.append(snowflake)
            

    def __events__(self, event):
        """Event Handling"""
        if event.type == pygame.QUIT:
            self.running = False

    def adjust_coords(self,coord):
        """Redundant"""
        return (self.size[0]/2.+coord[0],self.size[1]/2.-coord[1]) 

    def __render__(self):
        """Rendering"""
        self.display.fill((0,0,0))
        self.display.blit(self.font.render(str(round(self.clock.get_fps(),1)),1,(255,255,255)),(0,0))
        for snowflake in self.snowflakes:
            for branch in snowflake:
                for c in branch[1]:
                    pygame.draw.aaline(self.display,(255,255,255),snowflake.render_coordinates(branch[0]),snowflake.render_coordinates(c))
        pygame.display.flip()
        self.clock.tick(self.fps_limit)

    def __cleanup__(self,e=None):
        """Commands to be processed when quiiting"""
        pygame.quit()
        if e != None:
            raise e

    def start(self,fps_limit=0):
        """Start the application"""
        self.fps_limit = fps_limit
        ex = None
        try:
            self.running = self.init()
        except Exception,e:
            ex = e
        
        while self.running == True:
            try:
                for event in pygame.event.get():
                    self.__events__(event)

                self.__loop__()
                self.__render__()
            except Exception,e:
                self.running = False
                ex = e
    

        self.__cleanup__(ex)

a = App(800,800,"Snowstorm")
a.start(30) #framelimit of 30 - change this as you like, movement is frame independent but it probably won't look as smooth
