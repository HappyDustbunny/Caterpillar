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

    def __init__(self, position):
        bodyorb = sphere(pos=position, radius=1, color=color.blue)
        bodyrod = cylinder(pos=position+vector(0, 0, 1.1), radius=0.2, axis=vector(0, 0, -2.2))
        self.segment = compound([bodyorb, bodyrod])
        self.next_segment = None
        self.last_segment = None
        self.last_turn_axis = vector(0, 1, 0)
        self.last_turn_angle = 0
        self.on_planet = None
        self.fresh_environment = False
        # fresh_environment is used to check if the segment has just landed on a planet or it has just left a planet.
        self.right = vector(0, 0, 1)

    def link_with(self, other_segment):
        self.next_segment = other_segment
        other_segment.last_segment = self

    def move_turn_space(self, moveto, turn_angle, turn_axis):
        self.segment.rotate(turn_angle, turn_axis)
        if self.next_segment is not None:
            self.next_segment.move_turn_space(self.segment.pos, self.last_turn_angle, self.last_turn_axis)
        self.last_turn_angle = turn_angle
        self.last_turn_axis = turn_axis
        self.segment.pos = moveto

    def planet_approach(self, moveto, turn_angle, turn_axis, right, planet):
        self.segment.rotate(turn_angle, turn_axis)
        if self.next_segment is not None:
            self.next_segment.move_turn_space(self.segment.pos, self.last_turn_angle, self.last_turn_axis)
        self.last_turn_angle = turn_angle
        self.last_turn_axis = turn_axis
        self.right = right
        self.on_planet = planet
        self.segment.pos = moveto
        self.fresh_environment = True

    def move_turn_planet(self, moveto, turn_angle, turn_axis):
        self.segment.rotate(turn_angle, turn_axis)
        self.right.rotate(turn_angle, turn_axis)
        self.segment.rotate(1/self.on_planet.radius, self.right)
        if self.next_segment is not None:
            if self.fresh_environment:
                self.planet_approach(self.segment.pos, self.last_turn_angle,
                                     self.last_turn_axis, self.right, self.on_planet)
                self.fresh_environment = False
            else:
                self.next_segment.move_turn_planet(self.segment.pos, self.last_turn_angle, self.last_turn_axis)
        self.last_turn_angle = turn_angle
        self.last_turn_axis = turn_axis
        self.segment.pos = moveto


class HeadClass(SegmentsClass):
    def __init__(self):
        SegmentsClass.__init__(self, position=vector(0, 0, 0))
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
        self.last_turn_angle = turn_angle
        self.last_turn_axis = turn_axis
        self.segment.pos += self.forward
        self.for_guide.pos = self.segment.pos+self.forward
        self.up_guide.pos = self.segment.pos+self.upward

    def head_turn_planet(self, keystroke):
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
            pass
            #TODO Leaving the planet needs to be implemented.
        self.segment.rotate(turn_angle, turn_axis)
        self.segment.rotate(1/self.on_planet.radius, cross(self.forward, self.upward))


class PlanetClass:
    def __init__(self):
        pass


def main():
    global key_event
    scene.bind('keydown', direction)
    box()
    head = HeadClass()
    segment1 = SegmentsClass(vector(0, 0, 0))
    head.link_with(segment1)
    segment2 = SegmentsClass(vector(0, 0, 0))
    segment1.link_with(segment2)
    segment3 = SegmentsClass(vector(0, 0, 0))
    segment2.link_with(segment3)
    scene.camera.follow(head.segment)
    while True:
        sleep(0.3)
        head.head_turn_space(key_event)
        key_event = ''

main()