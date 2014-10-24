
"""
albumart.py

Using Cairo to draw album art. Software by Michiel Overtoom, motoom@xs4all.nl
"""

import cairo # On Ubuntu: sudo apt-get install python-cairo
import jumpcity
from jumpcity import rnd
import rotate
from rotate import Rectangle, Point
import random


def randomcolor():
    return jumpcity.rnd(1), jumpcity.rnd(1), jumpcity.rnd(1)


def randomrectangle_candidate(w, h):
    center = Point(rnd(w), rnd(h))
    rw = max(rnd(w / 2), 20) # Not too thin: minimum width and height 20 pixels.
    rh = max(rnd(h / 2), 20)
    r = Rectangle(
        Point(center.x - rw / 2, center.y + rh / 2),
        Point(center.x + rw / 2, center.y + rh / 2),
        Point(center.x + rw / 2, center.y - rh / 2),
        Point(center.x - rw / 2, center.y - rh / 2))
    # Now rotate it randomly.
    r = rotate.rotatedrectangle(r, rnd(360))
    # Check whether every coordinate of the rectangle lies within (0,0)-(w,h) (with a 5% margin)
    topmargin, rightmargin, bottommargin, leftmargin = w * 0.05, w * 0.95, h * 0.95, h * 0.05 
    for p in r:
        if p.x < leftmargin or p.x > rightmargin: return None
        if p.y < topmargin or p.y > bottommargin: return None
    return r


def randomrectangle(w, h):
    r = None
    while not r:
        r = randomrectangle_candidate(w, h)
    return r


def drawrectangle(cr, r):
    for p in r:
        cr.line_to(p.x, p.y)
    cr.fill()
    

def render(cr, w, h):
    splith = h * 0.8
    # Colored background.
    # IDEA: use H,S,L color model with constraints on all components.
    cr.set_source_rgb(*randomcolor())
    cr.rectangle(0, 0, w, splith)
    cr.fill()
    # Backdrop for album title.
    cr.set_source_rgb(1, 1, 1) # White.
    cr.rectangle(0, splith, w, h - splith)
    cr.fill()
    # Figure.
    cr.set_line_width(0)
    if w > 100 and h > 100: # Refuse to draw in too small a space.
        for i in xrange(2): # Draw two rectangles.
            cr.set_source_rgb(*randomcolor())
            r = randomrectangle(w, splith)
            drawrectangle(cr, r)
            cr.fill()
    # Album title.
    cr.set_source_rgb(0.12, 0.12, 0.12) # Almost black.
    cr.select_font_face("DejaVu Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    cr.set_font_size(h * 0.065)
    albumtitle_baseline = h * 0.894
    albumtitle_left = w * 0.0275
    cr.move_to(albumtitle_left, albumtitle_baseline)
    title = jumpcity.randomname()
    cr.show_text(title)
    # Recordlabel name.
    cr.set_source_rgb(0.5, 0.5, 0.5) # Gray.
    cr.select_font_face("Courier New", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    cr.set_font_size(h * 0.03)
    recordlabelname_baseline = h * 0.95
    cr.move_to(albumtitle_left, recordlabelname_baseline)
    cr.show_text("jump city records")
    # Release number.
    releasenumber_left = w * 0.897
    cr.move_to(releasenumber_left, recordlabelname_baseline)
    cr.show_text("%04d" % int(random.uniform(0, 10000)))