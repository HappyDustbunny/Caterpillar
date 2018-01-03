""" Snake clone """

from math import acos
import vpython
from caterpillar_graphics import *
import winsound
import os

key_event = ''


def direction(event):
    """ Capture keyboard interrupt and choose new direction and new orientation """
    # value = event.key
    global key_event
    key_event = event.key


def space_direction(forward, upward, turn, turn_axis):
    """ Checking key_event value and update direction if key_event is not empty """
    global key_event
    if key_event == 'a':
        forward = -cross(forward, upward)
        turn = radians(90)
        turn_axis = upward
    if key_event == 'd':
        forward = cross(forward, upward)
        turn = radians(90)
        turn_axis = -upward
    if key_event == 'w':
        forward, upward = upward, -forward
        turn = radians(90)
        turn_axis = cross(forward, upward)
    if key_event == 's':
        forward, upward = -upward, forward
        turn = radians(90)
        turn_axis = -cross(forward, upward)
    key_event = ''
    return forward, upward, turn, turn_axis


def planet_direction(forward, upward, turn, turn_axis, on_planet, planets):
    """ Checking key_event value and update direction while on planet. """
    global key_event
    if key_event == 'a':
        forward = -cross(forward, upward)
        forward = forward.rotate(1/planets[on_planet].radius, -cross(forward, upward))
        turn = radians(90)
        turn_axis = upward
    if key_event == 'd':
        forward = cross(forward, upward)
        forward = forward.rotate(1/planets[on_planet].radius, -cross(forward, upward))
        turn = radians(90)
        turn_axis = -upward
    if key_event == 'w':
        forward, upward = upward, -forward
        turn = radians(90)
        on_planet = -1 # -1 represents when the caterpillar isn't on a planet
        turn_axis = cross(forward, upward)
    if key_event == '':
        turn_axis = -cross(forward, upward)
        turn = 1/planets[on_planet].radius
        forward = forward.rotate(1/planets[on_planet].radius, -cross(forward, upward))
    key_event = ''
    return forward, upward, turn, turn_axis, on_planet, planets


def is_planet_reached(body, caterpillar_pos, forward, on_planet, planets, turn, turn_axis, upward):
    """ Checks if a planet is reached """
    for num1, planet in enumerate(planets):
        if mag(planet.pos - body[0].pos) <= planet.radius:
            on_planet = num1
            core_to_head = norm(body[0].pos - planet.pos) * planet.radius
            body[0].pos = core_to_head + planet.pos  # + 0.5*norm(core_to_head)
            caterpillar_pos[0] = body[0].pos
            new_forward = norm(forward - proj(forward, core_to_head))
            if new_forward.equals(vector(0, 0, 0)):  # If incoming is vertical new_forward = 0
                print("the caterpillar entered vertically")
                new_forward = norm(upward - proj(upward, core_to_head))
                turn = radians(90)
            else:
                turn = acos(dot(forward, new_forward) / (mag(forward) * mag(new_forward)))
            upward = norm(core_to_head)
            forward = norm(new_forward)
            turn_axis = cross(forward, upward)
    return forward, on_planet, turn, turn_axis, upward


def move_caterpillar(body, caterpillar_pos, forward, suit, turn, turn_axis):
    """ Moving the caterpillar"""
    old_caterpillar_pos = caterpillar_pos[:]
    caterpillar_pos[0] += forward
    body[0].rotate(angle=turn, axis=turn_axis)
    body[0].pos = caterpillar_pos[0]
    suit[0].rotate(angle=turn, axis=turn_axis)
    suit[0].pos = caterpillar_pos[0]
    for num, segment in enumerate(body):
        if num == 0:
            continue
        segment.pos = old_caterpillar_pos[num - 1]
        suit[num].pos = old_caterpillar_pos[num - 1]
        segment.rotate(angle=turn, axis=turn_axis)
        suit[num].rotate(angle=turn, axis=turn_axis)
        caterpillar_pos[num] = old_caterpillar_pos[num - 1]
    scene.center = caterpillar_pos[0]
    turn = 0
    sleep(0.2)
    return turn


def main():
    """ Main loop """
    scene.bind('keydown', direction)

    global key_event # Listening for key presses

    forward = vector(1, 0, 0)
    upward = vector(0, 1, 0)
    turn = 0
    turn_axis = vector(0, 1, 0)

    caterpillar_pos = []  # Initialize Caterpillar position. Head in origo
    for dummy in range(5):
        caterpillar_pos.append(vector(-dummy, 0, 0))

    head = make_head()  # Make Caterpillar head
    body = make_body(caterpillar_pos, head) # Make Caterpillar body
    helmet = make_helmet()
    suit = make_suit(caterpillar_pos, helmet)
    planets = make_planets(10) # Makes planets
    make_food(planets)  # Distribute food on the planets

    cwd = os.getcwd()

    d_t = 0.2
    on_planet = -1  # -1 represents when the caterpillar isn't on a planet
    while True:
        if on_planet > -1:  # -1 represents when the caterpillar isn't on a planet
            if suit[0].visible:
                for segment in suit:
                    segment.visible = False
            winsound.PlaySound(os.path.join(cwd, 'CaterpillarSounds', 'futz.wav'), winsound.SND_FILENAME)
            upward = norm(body[0].pos-planets[on_planet].pos)
            forward, upward, turn, turn_axis, on_planet, planets = planet_direction(forward, upward, turn, turn_axis, on_planet, planets)
        else:
            if not suit[0].visible:
                for segment in suit:
                    segment.visible = True
            forward, upward, turn, turn_axis = space_direction(forward, upward, turn, turn_axis)
            forward, on_planet, turn, turn_axis, upward = is_planet_reached(body, caterpillar_pos, forward, on_planet,
                                                                            planets, turn, turn_axis, upward)

        if dot(forward, upward) > 0.1:
            print(forward, upward)
            return

        turn = move_caterpillar(body, caterpillar_pos, forward, suit, turn, turn_axis)


box()

main()
