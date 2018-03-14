"""An alternative way of writing caterpillar"""

from vpython import *
from random import random, shuffle
from caterpillar_graphics import make_body, make_suit, make_food, make_planets


key_event = ''


def direction(event):
    """ Capture keyboard interrupt and choose new direction and new orientation """
    global key_event
    key_event = event.key


class SegmentsClass:
    """Each segment of the caterpillar is an instance of the SegmentClass"""

    def __init__(self, position, next_segment, last_segment):
        self.segment = sphere(pos=position, radius=1, color=color.blue)
        self.next_segment = next_segment
        self.last_segment = last_segment
        self.last_turn_axis = vector(0, 1, 0)
        self.last_turn_angle = 0

    def link_with(self, other_segment):
        self.next_segment = other_segment
        other_segment.last_segment = self

    def move_turn_space(self, moveto, turn_angle, turn_axis):
        self.segment.rotate(turn_angle, turn_axis)
        if self.next_segment is not None:
            self.next_segment.move_turn_space(self.segment.pos, self.last_turn_angle, self.last_turn_axis)
        self.segment.pos = moveto

    def move_turn_planet(self):
        pass


class HeadClass(SegmentsClass):
    def __init__(self):
        SegmentsClass.__init__(self, position=vector(0, 0, 0), next_segment=None, last_segment=None)
        self.segment.color = color.orange
        self.forward = vector(1, 0, 0)
        self.for_guide = sphere(pos=self.segment.pos+self.forward, radius=0.1, color=color.blue)
        self.upward = vector(0, 1, 0)
        self.up_guide = sphere(pos=self.segment.pos+self.upward, radius=0.1, color=color.cyan)

    def right(self):
        return norm(cross(self.forward, self.upward))

    def head_turn_space(self, keystroke):
        turn_axis = self.upward
        turn_angle = 0
        if keystroke == 'a':
            turn_axis = self.upward
            turn_angle = radians(90)
            self.forward = -self.right()
        if keystroke == 'd':
            turn_axis = -self.upward
            turn_angle = radians(90)
            self.forward = self.right()
        if keystroke == 'w':
            turn_axis = self.right()
            turn_angle = radians(90)
            self.forward, self.upward = self.upward, -self.forward
        if keystroke == 's':
            turn_axis = -self.right()
            turn_angle = radians(90)
            self.forward, self.upward = -self.upward, self.forward
        self.segment.rotate(turn_angle, turn_axis)
        self.next_segment.move_turn_space(self.segment.pos, self.last_turn_angle, self.last_turn_axis)
        self.segment.pos += self.forward
        self.for_guide.pos = self.segment.pos+self.forward
        self.up_guide.pos = self.segment.pos+self.upward

    def head_turn_planet(self, keystroke):
        pass


def main():
    global key_event
    box()
    head = HeadClass()
    segment1 = SegmentsClass(vector(-1, 0, 0), None, None)
    head.link_with(segment1)
    while True:
        sleep(0.3)
        head.head_turn_space(key_event)
        key_event = ''

main()