#!/usr/bin/env python
from gi.repository import Clutter
import time
import datetime
import gobject
import timer
import Xlib.display

# Colors
white    = Clutter.Color.new (255, 255, 255, 255)
black    = Clutter.Color.new (  0,   0,   0, 255)
darkgrey = Clutter.Color.new ( 80,  80,  80, 255)
green    = Clutter.Color.new (  0, 128,   0, 255)
yellow   = Clutter.Color.new (200, 200,   0, 255)
orange   = Clutter.Color.new (255, 128,   0, 255)
red      = Clutter.Color.new (255,   0,   0, 255)

# Objects
input = timer.TimeInput ()
timer = timer.Timer ()

alternate_black = False
absolute_time   = False

def finalize (Unused = None):
    Clutter.main_quit ()

def update_display (timeline = None):
    if timer.running ():
        time_elapsed.set_text (timer.elapsed () )
        time_remaining.set_text (timer.remaining () )

        progress = timer.progress ()

        if 1 <= timer.seconds_remaining () <= 60:
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
        time_remaining.set_text (input.to_string () )

        if absolute_time:
            stage.set_color (darkgrey)
            time_elapsed.set_text (time.strftime ("%H:%M:%S", time.localtime () ) )
            # Show the absolute labels?
        else:
            stage.set_color (black)
            time_elapsed.set_text (timer.elapsed () )

def parseKeyPress (self, event):
    global absolute_time
    character_key = chr (0)

    if 0 <= event.keyval <= 255:
        character_key = chr (event.keyval)

    if character_key == 'q' or character_key == 'Q':
        finalize ()
    elif character_key == ' ':
        if timer.running ():
            timer.reset ()
        else:
            if absolute_time:
                timer.set (input.duration_until () )
            else:
                timer.set (input.duration () )

            timer.start ()
    elif character_key == '@':
        absolute_time = True
    elif event.keyval == 65307: # Escape.
        if timer.running ():
            timer.reset ()
        elif absolute_time:
            absolute_time = False
            input.clear ()
        else:
            input.clear ()
    elif character_key.isdigit ():
        input.append (chr (event.keyval) )
        update_display ()
    else:
        print 'What to do with: ',  event.keyval

def redraw (fullscreen = False):
    stage.set_fullscreen (fullscreen)

    if fullscreen:
        stage.set_size (screen.width_in_pixels, screen.height_in_pixels)

    stage_width, stage_height = stage.get_size ()

    time_elapsed.set_font_name ("Sans " + str (stage_height / 4) + "px")
    time_remaining.set_font_name ("Sans " + str (stage_height / 4) + "px")

    update_display ()
    text_width, text_height = time_remaining.get_size ()

    stage.add_actor (time_elapsed)
    stage.add_actor (time_remaining)

    time_elapsed.set_position (stage_width / 2 - text_width / 2, stage_height / 3 - text_height / 2)
    time_remaining.set_position (stage_width / 2 - text_width / 2, stage_height / 3 * 2 - text_height / 2)

def redraw_fullscreen ():
    redraw (fullscreen = True)

Clutter.init(None)

stage = Clutter.Stage()
stage.set_minimum_size (600, 400)
stage.set_user_resizable (True)
stage.set_title ("Event Timer");

screen = Xlib.display.Display ().screen ()
#stage.set_size (screen.width_in_pixels, screen.height_in_pixels)

stage.set_color (black)
stage.connect_after ("key-press-event", parseKeyPress)
stage.connect ("destroy", finalize)

time_elapsed = Clutter.Text ()
time_elapsed.set_color (white)

time_remaining = Clutter.Text ()
time_remaining.set_color (white)

stage.show_all ()

t = Clutter.Timeline ()
t.set_duration (250)
t.set_loop (True)
t.connect ('completed', update_display)
t.start ()

gobject.timeout_add (10,redraw)

Clutter.main ()
