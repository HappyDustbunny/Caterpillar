"""An alternative way of writing caterpillar"""

from vpython import *
from random import random, shuffle
from caterpillar_graphics import make_body, make_suit, make_food, make_planets

class SegmentsClass:
    """Each segment of the caterpillar is an instance of the SegmentClass"""

    def __init__(self, position, next_segment, last_segment):
        self.position = position
        self.next_segment = next_segment
        self.last_segment = last_segment

    def link_with(self, other_segment):
        self.next_segment = other_segment
        other_segment.last_segment = self

    def move_turn_space(self, moveto, turn_axis, turn_angle):
        pass

    def move_turn_planet(self):
        pass


class HeadClass(SegmentsClass):
    def __init__(self):
        SegmentsClass.__init__(self, position=vector(0, 0, 0), next_segment=None, last_segment=None)
        self.segment.color = orange
        self.forward = vector(1, 0, 0)
        self.for_guide = sphere(pos=self.pos+2*self.forward, radius=0.1, color=color.blue)
        self.upward = vector(0, 1, 0)
        self.up_guide = sphere(pos=self.pos+2*self.upward, radius=0.1, color=color.cyan)
        self.right = norm(cross(self.forward, self.upward))

        def move_turn_space(self, keystroke):
            pass

        def move_turn_planet(self, keystroke):
            pass


def direction(event):
    """ Capture keyboard interrupt and choose new direction and new orientation """
    global key_event
    key_event = event.key

def main():
    global key_event

    while true:
        sleep(0.3)
        head.move_turn_space(key_event)