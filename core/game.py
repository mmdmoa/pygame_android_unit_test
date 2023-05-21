from core.common.names import *
import core.common.resources as cr

class Game:
    def __init__(self):
        ...

    def render( self ):
        w,h = cr.screen.get_width() * 0.3, cr.screen.get_width() * 0.3
        for finger in cr.event_holder.fingers.values():
            rect = Rect(0,0,w,h)
            rect.center = (finger.x,finger.y)

            pg.draw.rect(cr.screen,"black",rect)