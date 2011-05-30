#!/usr/bin/env python
import clutter
import time
import datetime
import gobject
import timer
import Xlib.display

# Colors
white  = clutter.Color (255, 255, 255, 255)
black  = clutter.Color (  0,   0,   0, 255)
green  = clutter.Color (  0, 128,   0, 255)
yellow = clutter.Color (200, 200,   0, 255)
orange = clutter.Color (255, 128,   0, 255)
red    = clutter.Color (255,   0,   0, 255)

# Objects
input = timer.TimeInput ()
timer = timer.Timer ()

alternate_black = False
absolute_time   = False

def update_timer (timeline = None):
    if timer.running ():
        time_elapsed.set_text (timer.elapsed () )
        time_remaining.set_text (timer.remaining () )

        progress = timer.progress ()

        if timer.seconds_remaining () <= 60:
            global alternate_black
            alternate_black = not alternate_black

            if alternate_black:
                stage.set_color (black)
            else:
                stage.set_color (red)
        elif timer.duration <= datetime.timedelta (minutes = 20):
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
        stage.set_color (black)
        time_remaining.set_text (input.to_string () )

        if absolute_time:
            time_elapsed.set_text (time.strftime ("%H:%M:%S", time.localtime () ) )
            # Show the absolute labels?
        else:
            time_elapsed.set_text (timer.elapsed () )

def parseKeyPress (self, event):
    global absolute_time
    character_key = chr (0)

    if 0 <= event.keyval <= 255:
        character_key = chr (event.keyval)

    if event.keyval == clutter.keysyms.q or event.keyval == clutter.keysyms.Q:
        clutter.main_quit ()
    elif event.keyval == clutter.keysyms.space:
        if timer.running ():
            timer.reset ()
        else:
            if absolute_time:
                timer.set (input.durationUntil () )
            else:
                timer.set (input.duration () )

            timer.start ()
    elif event.keyval == clutter.keysyms.at:
        absolute_time = True
    elif event.keyval == clutter.keysyms.Escape:
        if timer.running ():
            timer.reset ()
        if absolute_time:
            absolute_time = False
            input.clear ()
    elif character_key.isdigit ():
        input.append (chr (event.keyval) )
        update_timer ()
    else:
        print 'What to do with: ',  event.keyval

def redraw (fullscreen = False):
    stage.set_fullscreen (fullscreen)
    stage_width, stage_height = stage.get_size ()

    update_timer ()
    text_width, text_height = time_remaining.get_size ()

    stage.add (time_elapsed)
    stage.add (time_remaining)

    time_elapsed.set_position (stage_width / 2 - text_width / 2, stage_height / 3 - text_height / 2)
    time_remaining.set_position (stage_width / 2 - text_width / 2, stage_height / 3 * 2 - text_height / 2)

def redraw_fullscreen ():
    redraw (fullscreen = True)

stage = clutter.Stage ()

screen = Xlib.display.Display ().screen ()
stage.set_size (screen.width_in_pixels, screen.height_in_pixels)

stage.set_color (black)
stage.connect ('key-press-event', parseKeyPress)
time_elapsed = clutter.Text ()

time_elapsed.set_font_name ("Sans " + str (screen.height_in_pixels / 4) + "px")
time_elapsed.set_color (white)


time_remaining = clutter.Text ()
time_remaining.set_font_name ("Sans " + str (screen.height_in_pixels / 4) + "px")
time_remaining.set_color (white)

stage.show_all ()

t=clutter.Timeline ()
t.set_duration (250)
t.set_loop (True)
t.connect ('completed', update_timer)
t.start ()

gobject.timeout_add (10,redraw)
clutter.main ()
