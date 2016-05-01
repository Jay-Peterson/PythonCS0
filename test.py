from cs0 import *

setColor(BLUE)
setCaption("hello")

charlie = Circle(10, RED, 0,0) + Circle(10, YELLOW, 5,5) + Rectangle(10,15, makeColorHex(990033),0, 10)
#print(type(charlie))
#add(sam, 326, 119)
#charlie += sam
a = Label(30, WHITE, "Testing!", 100, 100)
b = Rectangle(10,15, AQUA, 5, 10)
c = Rectangle(10, 15, BROWN, 5, 15)
add(charlie, 321, 114)
d = Button("This is a button", 30, BLACK, WHITE, 0, 0)
add(a)
add(b)
add(c)
add(d)

#s = SoundClip('pacman_beginning.wav')
#s.setVolume(0.1)

def clicky(evt):
    #d.setVisible(not d.getVisible())
    #print (str(b.getColor()))
    #d.setFontSize(d.getFontSize() + 10)
    #print (str(d.getFontSize()))
    a.setColor(BLACK)
    if d.isClicked(evt):
        d.setText("CLICK!")

def printEvent(evt):
    print(str(evt))

def mouseDrag(evt):
    charlie.setLocation(evt.pos[0], evt.pos[1])

def mouseClick(evt):
    o = objectAt(evt.pos)
    if(o is not None):
        print("Object at " +  str(evt.pos[0]) + ", " + str(evt.pos[1]) +  " is a " + str(type(o)))

def key(evt):
    if evt.key == KEY_A:
        sendForward(b)
    if evt.key == KEY_B:
        sendBackward(b)
    if evt.key == KEY_K:
        removeAll()
    if evt.key == KEY_D:
        remove(d)
        

mouseClickedEvent(mouseClick)

mouseReleasedEvent(clicky)
#mouseMovedEvent(mouseClick)
mouseDraggedEvent(mouseDrag)
keyPressedEvent(key)
keyReleasedEvent(printEvent)

start()
#start()

waitForClick()
count = 0
while(count < 500):
    #print(charlie._getBox())
    if charlie.x > 300:
        charlie.setLocation(0,0)
        sendForward(charlie)
        #waitForClick()
    charlie.move(2, 2)
    #print (charlie._getBox())
    pause(25)
    #s.play()
    pause(200)
    #s.stop()
    count = count + 1
    #print(count)

stop()
