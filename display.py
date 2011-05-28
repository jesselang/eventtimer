#!/usr/bin/env python
import clutter
import datetime
import gobject
import timer
import Xlib.display

white = clutter.Color (255, 255, 255, 255)
black = clutter.Color(0,0,0,255)
green = clutter.Color (0, 128, 0, 255)
yellow = clutter.Color (200, 200, 0, 255)
orange = clutter.Color (255, 128, 0, 255)
red = clutter.Color(255, 0, 0, 255)

input = timer.TimeInput ()
timer = timer.Timer ()

alternate_black = False

def update_timer (timeline=None):
    time_elapsed.set_text (timer.timeelapsed () )

    if timer.running ():
        time_remaining.set_text (timer.timeremaining () )

        progress = timer.progress ()

        if timer.secondsremaining () <= 60:
            global alternate_black
            alternate_black = not alternate_black

            if alternate_black:
                stage.set_color (black)
            else:
                stage.set_color (red)
        elif timer.duration <= datetime.timedelta (minutes=20):
            if 0.0 <= progress <= 0.4:
                stage.set_color (green)
            elif 0.4 <= progress <= 0.6:
                stage.set_color (yellow)
            elif 0.6 <= progress <= 0.7:
                stage.set_color (orange)
            else:
                stage.set_color (red)
        else:
            if 0.0 <= progress <= 0.5:
                stage.set_color (green)
            elif 0.5 <= progress <= 0.75:
                stage.set_color (yellow)
            elif 0.75 <= progress <= 0.95:
                stage.set_color (orange)
            else:
                stage.set_color (red)
    else:
        time_remaining.set_text (input.durationstring () )
        stage.set_color (black)

def parseKeyPress(self, event):
    character_key = chr(0)

    if 0 <= event.keyval <= 255:
        character_key = chr(event.keyval)
    if event.keyval == clutter.keysyms.q:
        clutter.main_quit()
    elif event.keyval == clutter.keysyms.space:
        if timer.running ():
            timer.reset ()
        else:
            timer.setduration (input.getduration ())
            timer.start ()
    elif character_key.isdigit():
        input.append (chr (event.keyval) )
        update_timer ()
    else:
        print 'What to do with: ',  event.keyval

def redraw (fullscreen=False):
    stage.set_fullscreen (fullscreen)
    stage_width, stage_height = stage.get_size ()

    update_timer ()
    text_width, text_height = time_remaining.get_size ()

    stage.add(time_elapsed)
    stage.add(time_remaining)

    time_elapsed.set_position (stage_width / 2 - text_width / 2, stage_height / 3 - text_height / 2)
    time_remaining.set_position (stage_width / 2 - text_width / 2, stage_height / 3 * 2 - text_height / 2)

def redraw_fullscreen ():
    redraw (fullscreen=True)

stage = clutter.Stage()

screen = Xlib.display.Display ().screen ()
stage.set_size (screen.width_in_pixels, screen.height_in_pixels)

stage.set_color(black)
stage.connect('key-press-event', parseKeyPress)
time_elapsed = clutter.Text()
# Dynamically set the font size based on screen size?
time_elapsed.set_font_name("Sans " + str (screen.height_in_pixels / 4) + "px")
time_elapsed.set_color(white)


time_remaining = clutter.Text()
# Dynamically set the font size based on screen size?
time_remaining.set_font_name("Sans " + str (screen.height_in_pixels / 4) + "px")
time_remaining.set_color(white)

stage.show_all ()

t=clutter.Timeline()
t.set_duration(250)
t.set_loop(True)
t.connect('completed', update_timer)
t.start()

gobject.timeout_add(10,redraw_fullscreen)
clutter.main()
