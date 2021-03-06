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
        body_orb = sphere(pos=position, radius=1, color=color.blue)
        body_rod = cylinder(pos=position+vector(0, 0, 1.1), radius=0.2, axis=vector(0, 0, -2.2))
        self.segment = compound([body_orb, body_rod])
        self.next_segment = None
        self.last_segment = None
        self.last_turn_axis = vector(0, 1, 0)
        self.last_turn_angle = 0
        self.on_planet = None
        self.fresh_environment = None
        # fresh_environment is used to check if the segment has just landed on a planet or it has just left a planet.
        self.right = vector(0, 0, 1)

    def link_with(self, other_segment):
        self.next_segment = other_segment
        other_segment.last_segment = self

    def move_turn(self, moveto, turn_angle, turn_axis):
        self.segment.rotate(turn_angle, turn_axis)
        if self.on_planet is not None:
            self.segment.rotate(1/self.on_planet.radius, self.right)
        if self.next_segment is not None:
            if self.fresh_environment:
                if self.on_planet is None:
                    self.next_segment.planet_escape(self.pos, self.last_turn_angle, self.last_turn_axis)
                else:
                    self.next_segment.planet_approach(self.segment.pos, self.last_turn_angle,
                                         self.last_turn_axis, self.right, self.on_planet)
                    self.fresh_environment = None
            else:
                self.next_segment.move_turn(self.segment.pos, self.last_turn_angle, self.last_turn_axis)
        self.right.rotate(turn_angle, turn_axis)
        self.last_turn_angle = turn_angle
        self.last_turn_axis = turn_axis
        self.segment.pos = moveto

    def planet_approach(self, moveto, turn_angle, turn_axis, right, planet):
        # TODO 1 Implementing fresh_environment as holding the planet-approaching turn angles
        self.segment.rotate(turn_angle, turn_axis)
        if self.next_segment is not None:
            self.next_segment.move_turn(self.segment.pos, self.last_turn_angle, self.last_turn_axis)
        self.last_turn_angle = turn_angle
        self.last_turn_axis = turn_axis
        self.right = right
        self.on_planet = planet
        self.segment.pos = moveto
        self.fresh_environment = True

    def planet_escape(self, moveto, turn_angle, turn_axis):
        pass
        # TODO 3 Leaving the planet needs to be implemented.


class HeadClass(SegmentsClass):
    def __init__(self, planets):
        SegmentsClass.__init__(self, position=vector(0, 0, 0))
        self.segment.color = color.orange
        self.forward = vector(1, 0, 0)
        self.for_guide = sphere(pos=self.segment.pos+self.forward, radius=0.1, color=color.blue)
        self.upward = vector(0, 1, 0)
        self.up_guide = sphere(pos=self.segment.pos+self.upward, radius=0.1, color=color.cyan)
        self.planets = planets

    def __head_landing(self, planet):
        self.on_planet = planet
        core_to_head = norm(self.segment.pos - planet.pos)
        # core_to_head also acts as a new_upward
        self.segment.pos = core_to_head * planet.radius
        if self.forward.equals(-core_to_head):
            new_forward = norm(self.upward)
        else:
            new_forward = norm(self.forward - proj(self.forward, core_to_head))
        first_turn_angle = diff_angle(self.forward, new_forward)
        first_turn_axis = cross(self.forward, new_forward)
        self.forward.rotate(first_turn_angle, first_turn_axis)
        self.upward.rotate(first_turn_angle, first_turn_axis)
        self.segment.rotate(first_turn_angle, first_turn_axis)
        second_turn_angle = diff_angle(self.upward, core_to_head)
        # new_forward acts a second_turn_axis
        self.upward.rotate(second_turn_angle, new_forward)
        self.segment.rotate(second_turn_angle, new_forward)
        self.fresh_environment = [[first_turn_angle, first_turn_axis], [second_turn_angle, new_forward]]
        # TODO 2 check if second_turn_angle's arguments need to be swapped.

    def head_turn(self, keystroke):
        turn_axis = self.upward
        turn_angle = 0
        head_right = norm(cross(self.forward, self.upward))
        # head_right is separate from normal right, because the head has forward and upward,
        # and head_right can therefore be defined more accurately
        if keystroke == 'a':
            turn_axis = self.upward
            turn_angle = radians(90)
            self.forward = -head_right
        if keystroke == 'd':
            turn_axis = -self.upward
            turn_angle = radians(90)
            self.forward = head_right

        if self.on_planet is None:
            if keystroke == 'w':
                turn_axis = head_right
                turn_angle = radians(90)
                self.forward, self.upward = self.upward, -self.forward
            if keystroke == 's':
                turn_axis = -head_right
                turn_angle = radians(90)
                self.forward, self.upward = -self.upward, self.forward
            self.segment.rotate(turn_angle, turn_axis)
            if self.fresh_environment is not None:
                pass
            else:
                self.next_segment.move_turn(self.segment.pos, self.last_turn_angle, self.last_turn_axis)
            self.last_turn_angle = turn_angle
            self.last_turn_axis = turn_axis
            self.segment.pos += self.forward
            self.for_guide.pos = self.segment.pos+self.forward
            self.up_guide.pos = self.segment.pos+self.upward

            for planet in self.planets:
                if mag(planet.orb.pos - self.segment.pos):
                    self.__head_landing(planet)
        else:
            if keystroke == 'w':
                pass
                # TODO 3 Leaving the planet needs to be implemented.
            head_right = cross(self.forward, self.upward)
            self.segment.rotate(turn_angle, turn_axis)
            self.segment.rotate(1/self.on_planet.radius, head_right)
            if self.fresh_environment is not None:
                self.next_segment.planet_approach(self.segment.pos, self.last_turn_angle, self.last_turn_axis,
                                                  head_right, self.on_planet)
                # TODO 1 Implementing fresh_environment as holding the planet-approaching turn angles
            else:
                self.next_segment.move_turn(self.segment.pos, self.last_turn_angle, self.last_turn_axis)
            self.forward.rotate(1/self.on_planet.radius, head_right)
            self.upward.rotate(1/self.on_planet.radius, head_right)
            self.last_turn_angle = turn_angle
            self.last_turn_axis = turn_axis
            self.segment.pos += self.forward
            self.for_guide.pos = self.segment.pos+self.forward
            self.up_guide.pos = self.segment.pos+self.upward


class PlanetClass:
    def __init__(self, position, input_radius, food_count):
        self.orb = sphere(pos=position, radius=input_radius, texture=textures.wood_old)
        self.food = self.__first_food_distribution(food_count)

    def __first_food_distribution(self, food_count):
        if food_count == 0:
            return "There is no food"
        # TODO 4 implementing food.


def main():
    global key_event
    scene.bind('keydown', direction)
    box()
    planets = []
    planet1 = PlanetClass(vector(40, -10, 0), 20, 0)
    planets.append(planet1)

    head = HeadClass(planets)
    segment1 = SegmentsClass(vector(0, 0, 0))
    head.link_with(segment1)
    segment2 = SegmentsClass(vector(0, 0, 0))
    segment1.link_with(segment2)
    segment3 = SegmentsClass(vector(0, 0, 0))
    segment2.link_with(segment3)

    scene.camera.follow(head.segment)
    while True:
        sleep(0.3)
        head.head_turn(key_event)
        key_event = ''

main()