'''
Author: Graham Montgomery
Western State Colorado University

This file holds the Graphic objects for the library
'''

# External imports
import threading


# Internal imports
from Globals import *
from Constants import *


class GObj:

    def __init__(self, color, x, y):
        self._lock = threading.Lock()
        self.cx = 0
        self.cy = 0
        self.x = x
        self.y = y
        self.color = color
        self.visible = True
        self.collidable = False

    def move(self, xv, yv):
        self.x += xv
        self.y += yv

    def setLocation(self, x, y):
        self.x = x
        self.y = y

    def getLocation(self):
        return (self.x, self.y)

    def getX(self): #------------------------------- 7/30 added
        return self.x

    def getY(self): #------------------------------- 7/30 added
        return self.y

    def setColor(self, color):
        self.color = color
    def getColor(self):
        return self.color

    def setVisible(self, val):
        self.visible = val
    def getVisible(self):
        return self.visible

    def acquire(self):
        self._lock.acquire()
    def release(self):
        self._lock.release()
    def __setattr__(self, item, value):
        if item is "_lock":
            self.__dict__[item] = value
        else:
            self.acquire()
            self.__dict__[item] = value
            self.release()
    def __add__(self, obj):
        if type(obj) is GComp:
            return obj + self #shortened that up. GComps know how to add things to themselves anyway.
        elif isinstance(obj, GObj):
            obj.cx = obj.x
            obj.x = 0
            obj.cy = obj.y
            obj.y = 0
            self.cx = self.x
            self.x = 0
            self.cy = self.y
            self.y = 0
            return GComp(self, obj)

class GComp(GObj):

    def __init__(self, obj1, obj2):
        GObj.__init__(self, WHITE, 0, 0)
        if not isLabel(obj1) and not isLabel(obj2): #3/8/2016 added this check to make sure that only non-label objects could be turned into a GComp.
            self.objs = [obj1,obj2]
        elif not isLabel(obj1):
            self.objs = [obj1] #But, come to think of it, I have no idea how it'll react to having a reduced number of component pieces.
        elif not isLabel(obj2):
            self.objs = [obj2]
        else:
            self.objs = [] #Or being empty.

    def move(self, xv, yv):
        self.x += xv
        self.y += yv
        self.updateQualities();
    def setLocation(self, x, y):
        self.x = x
        self.y = y
        self.updateQualities();
    def setVisible(self, val):
        self.visible = val
        self.updateQualities();
    def updateQualities(self):
        for obj in self.objs:
            obj.x = self.x + obj.cx
            obj.y = self.y + obj.cy
            obj.setVisible(self.visible)

    def getWidth(self):
        maxX = 0
        minX = 0 #minimums used to be set ludicrously high. Now they're 0, so that no matter what, the origin point is included in width and height calculations.
        for obj in self.objs:
            min, max = obj._getBox()
            if max[0] >= maxX:
                maxX = max[0]
            if min[0] <= minX:
                minX = min[0]
        return maxX-minX

    def getHeight(self):
        maxY = 0
        minY = 0 #As a bonus? No more negative width/height readings from empty gcompounds.
        for obj in self.objs:
            min, max = obj._getBox()
            if max[1] >= maxY:
                maxY = max[1]
            if min[1] <= minY:
                minY = min[1]
        return maxY-minY

    def draw(self, window):
        for obj in self.objs:
            obj.draw(window);

    def __add__(self, obj):
        if isLabel(obj):
            return self #GComps now refuse to add label or button objects to themselves.
        if type(obj) is GComp:
            self.objs += obj.objs
        elif isinstance(obj, GObj):
            obj.cx = obj.x
            obj.x = 0
            obj.cy = obj.y
            obj.y = 0
            self.objs.append(obj)
        return self

    def _getBox(self):

        maxX = 0
        maxY = 0
        minX = 10000
        minY = 10000
        for obj in self.objs:
            #if type(obj) is Label or type(obj) is Button:
            #    pass
            #else:
            #no need for those. Labels and Buttons can't be in objects anymore.
                min, max = obj._getBox() #We should be checking for labels. They don't have a getBox function.
                #Check min and max X
                if max[0] >= maxX:
                    maxX = max[0]
                if min[0] <= minX:
                    minX = min[0]

                #Check min and max Y
                if max[1] >= maxY:
                    maxY = max[1]
                if min[1] <= minY:
                    minY = min[1]
        return ((minX, minY), (maxX, maxY))


class Circle(GObj):

    def __init__(self, diam, color, x = 0, y = 0):
        GObj.__init__(self, color, x, y)
        self.diam = diam
        self._type = "Circle"

    def setDiameter(self, diam):
        self.diam = diam
    def getDiameter(self):
        return self.diam

    def draw(self, window):
        if self.visible:
            pygame.draw.circle(window, self.color, (int(self.x+self.diam/2), int(self.y+self.diam/2)), int(self.diam/2), 0)

    def _getBox(self):
        x = self.x
        y = self.y
        r = self.diam/2
        return ((x, y),(x+2*r, y+2*r))

class Square(GObj): #----------------------------- 7/30 add this class
                    #----------------------------- haven't checked it thoroughly
    def __init__(self, width, color, x = 0, y = 0):
        GObj.__init__(self, color, x, y)
        self.width = width
        self.height = width
        self._type = "Square"

    def setWidth(self, width):
        self.width = width

    def getWidth(self):
        return self.width

    def draw(self, window):
        if self.visible:
            pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height), 0)

    def _getBox(self):
        x = self.x
        y = self.y
        w = self.width
        return ((x, y),(x+w, y+w))

class Oval(GObj):

    def __init__(self, width, height, color, x = 0, y = 0):
        GObj.__init__(self, color, x, y)
        self.width = width
        self.height = height
        self._type = "Oval"

    def setSize(self, width, height):
        self.width = width
        self.height = height
    def setWidth(self, width): #----------------- 7/30
        self.width = width
    def setHeight(self, height): #---------------- 7/30
        self.height = height
    def getWidth(self):
        return self.width
    def getHeight(self):
        return self.height

    def draw(self, window):
        if self.visible:
            pygame.draw.ellipse(window, self.color, (self.x, self.y, self.width, self.height), 0)

    def _getBox(self):
        x = self.x
        y = self.y
        w = self.width
        h = self.height
        return ((x, y),(x+w, y+h))


class Rectangle(GObj):

    def __init__(self, width, height, color, x = 0, y = 0):
        GObj.__init__(self, color, x, y)
        self.width = width
        self.height = height
        self._type = "Rectangle"

    def setSize(self, width, height):
        self.width = width
        self.height = height
    def setHeight(self, height): #-------------- 7/30
        self.height = height
    def setWidth(self, width): #---------------- 7/30
        self.width = width
    def getWidth(self):
        return self.width
    def getHeight(self):
        return self.height

    def draw(self, window):
        if self.visible:
            pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height), 0)

    def _getBox(self):
        x = self.x
        y = self.y
        w = self.width
        h = self.height
        return ((x, y),(x+w, y+h))

class Label(GObj):

    def __init__(self, size, color, message, x = 0, y = 0):
        GObj.__init__(self, color, x, y)
        self.message = message
        self.fontSize = size
        self.fontType = None

    def setFontSize(self, fontSize): #-------- 7/30 changed name
        self.fontSize = fontSize
    def getFontSize(self):              #---------- 7/30 changed name
        return self.fontSize

    def setText(self, message):
        self.message = message
    def getText(self): #------------------ 7/30 added
        return self.message

    def draw(self, window):
        if self.visible:
            window.blit(pygame.font.Font(self.fontType, self.fontSize).render(self.message, 1, self.color), (self.x, self.y))

class Button(GObj):

    def __init__(self, text, fontSize, fontColor, bkgColor, x, y, fontType = None): 
        GObj.__init__(self, bkgColor, x, y)
        self.text = text
        self.fontSize = fontSize #Some silly person forgot to camelcaps these variables. THAT caused a bit of confusion.
        self.fontType = fontType
        self.fontColor = fontColor
        self.bkgColor = bkgColor
        self._update()

    def _update(self):
        """
        Renders the text and changes the width and height if set to auto
        gets called when any sets are called.
        Direct manipulation of the variables will not cause the update to happen (yet?)
        """
        self.drawn_font = pygame.font.Font(None, self.fontSize)
        self.drawn_text = self.drawn_font.render(self.text, 1, self.fontColor)

        self.drawn_width = self.drawn_text.get_width()
        self.drawn_height = self.drawn_text.get_height()

        self.back = Rectangle(self.drawn_width, self.drawn_height, self.bkgColor, x=self.x, y=self.y)

    def draw(self, window):
        if self.visible:
            self.back.draw(window)
            window.blit(self.drawn_text, (self.x, self.y))

    def setText(self, text):
        self.text = text
        self._update()

    def setFontType(self, type): #Why do buttons have a font type but not labels?
        self.fontType = type
        self._update()

    def setFontSize(self, size):
        self.fontSize = size
        self._update()
        
    def getFontSize(self):  #why wasn't this in the button code to begin with?
        return self.fontSize

    def isClicked(self, evt):
        x = evt.pos[0]
        y = evt.pos[1]
        if x > self.x and x < self.x + self.drawn_width:
            if y > self.y and y < self.y + self.drawn_height:
                return True
        return False
    
    #So, Buttons don't have a getBox function because they're text, like Labels.
    #Which means that we have to throw in ANOTHER clause for the objectAt() function, to exclude Buttons as well.


def collides(obj1, obj2):
    """
    Commenting out because checking if the object is in the world
    is breaking objectAt(). Will just check for None instead.

    Saving just incase - Lucas 3/30/15

    if obj1 is None or obj2 is None or not world.inWorld(obj1) or not world.inWorld(obj2):
        print "Given none obj or not in world"
        return False
        
    New plan. GObjects have an Alive boolean, which is defaulted to false. 
    When added, this boolean is set to true. When removed, it becomes False.
    This way, objects USUALLY, but not ALWAYS, have to be in the world in order for hit detection to work.
    This'll help with clicking on objects.
    
    If you're looking for objectAt(), look in cs0.
    
    Jay Peterson 2/16/16
    
    --
    
    More stuff. The Alive boolean is now keeping track of whether or not objects can collide at all.
    There's some new logic in Add (World.py) that checks to see whether a GObj is a label or button when putting it into the world.
    Because Alive implies collision, and we already have all the tests, Labels and Buttons (which can't collide) will never be set to Alive.
    Easy Peasy.
    
    Jay Peterson 3/8/16
    """
    if obj1 is None or obj2 is None or not obj1.collidable or not obj2.collidable:
        return False

    box1 = obj1._getBox()
    box2 = obj2._getBox()
    xmin = 0
    xmax = 0
    ymin = 0
    ymax = 0
    w = 0
    h = 0
    if box1[0][0] < box2[0][0]:
        xmin = box1[0][0]
        xmax = box2[0][0]
        w = box1[1][0] - box1[0][0]
    else:
        xmin = box2[0][0]
        xmax = box1[0][0]
        w = box2[1][0] - box2[0][0]
    if box1[0][1] < box2[0][1]:
        ymin = box1[0][1]
        ymax = box2[0][1]
        h = box1[1][1] - box1[0][1]
    else:
        ymin = box2[0][1]
        ymax = box1[0][1]
        h = box2[1][1] - box2[0][1]
    return xmax - xmin < w and ymax - ymin < h

#Added this function so that type checking could be streamlined.
def isLabel(obj):
    return (type(obj) is Label) or (type(obj) is Button)

#Added these functions to make colors easy to change. Colors are threeples, with int values from 0 to 255.
def makeColorRGB(r,g,b):
    c = (r,g,b)
    return c
def makeColorHex(hexValue):
    hexValue = str(hexValue) + "000000" #Conversion and buffer so it doesn't error out if it gets weird inputs.
    r = int(hexValue[:2], 16)
    g = int(hexValue[2:4], 16)
    b = int(hexValue[4:6], 16)
    print (str(r) + ", " + str(g) + ", " + str(b))
    return (r,g,b)
    
