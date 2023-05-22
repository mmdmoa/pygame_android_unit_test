import math
import sys
import re
import traceback

import core.assets
from core.game import Game

try:
    from core.common.names import *
    import core.common.resources as cr
    import gui.common.resources as gui_cr
    from core.common.functions import *
    from core.assets import *

    from core.event_holder import EventHolder
    from gui.menu import Menu
    from gui.drawables.page import Page
    from core.common.enums import *

    import asyncio


    active_game: Games = Games.ClownBlit
    def set_active_game(to:Games):
        def onclick():
            global active_game
            active_game = to
            cr.event_holder.should_run_game = True

        return onclick


    pg.init()
    flags = SCALED | FULLSCREEN
    if IS_WEB:
        flags = 0

    gui_cr.screen = cr.screen = make_screen([9,18],25,flags)
    cr.game = Game()
    gui_cr.menu = Menu(cr.screen,cr.event_holder)
    gui_cr.event_holder = cr.event_holder = EventHolder()
    core.assets.load_assets()


    # cr.window = Window.from_display_module()
    # cr.renderer = Renderer(cr.window)


    w,h = cr.screen.get_size()
    text_table = ["blit;ClownBlit","rotate;ClownRotate","party;ClownParty"]

    page = Page(Rect(w*0.1,h*0.1,w*0.8,h*0.8),text_table,fonts['medium'])
    gui_cr.menu.add_page(page)
    gui_cr.menu.active_page = 0
    page.text_box_dict['blit'].onclick_action = set_active_game(ClownBlit)
    page.text_box_dict['rotate'].onclick_action = set_active_game(ClownRotate)

    cr.event_holder.determined_fps = 0





    def get_fps_text() -> Surface:
        fps = cr.event_holder.final_fps
        if math.isinf(fps):
            fps = "Infinite"
            print("fps is infinite!")
        else:
            fps = int(fps)

        # print(fps)
        return fonts['small'].render(f"FPS: {fps}",True,'black')

    async def main_loop():
        pic = pics['clown'].copy()
        rotated_pic = pic.copy()
        angle = 0

        while not cr.event_holder.should_quit:

            cr.screen.fill("gray")

            cr.event_holder.get_events()


            if cr.event_holder.should_run_game:
                if K_AC_BACK in cr.event_holder.pressed_keys :
                    cr.event_holder.should_run_game = False

                if K_F1 in cr.event_holder.pressed_keys:
                    cr.event_holder.should_run_game = False

                if active_game == ClownRotate:
                    angle += cr.event_holder.dt * 10
                    rotated_pic = pg.transform.rotate(pic,angle)
                if active_game in [ClownBlit,ClownRotate]:
                    rect = rotated_pic.get_rect()
                    rect.center = cr.screen.get_rect().center
                    cr.screen.blit(rotated_pic,rect)
                    cr.game.render()
            else:
                if K_AC_BACK in cr.event_holder.pressed_keys:
                    cr.event_holder.should_quit = True

                gui_cr.menu.check_events()
                gui_cr.menu.render()



            text = get_fps_text()
            rect = text.get_rect()
            rect.x = cr.screen.get_width() - rect.w
            rect.y = cr.screen.get_height() - rect.h
            cr.screen.blit(text,rect)


            pg.display.update()
            await asyncio.sleep(0)

    asyncio.run(main_loop())




except Exception as e:
    error_message = re.sub(r'\s+', ' ', traceback.format_exc())
    print("[Checkpoint:Error]", error_message.strip())
    print("[Checkpoint:Error]", traceback.format_exc())