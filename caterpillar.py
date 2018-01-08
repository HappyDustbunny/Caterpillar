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


def planet_direction(forward, upward, turn, turn_axis, on_planet, planets, body):
    """ Checking key_event value and update direction while on planet. """
    global key_event
    if key_event == 'a':
        forward = -cross(forward, upward)
        forward = forward.rotate(1/planets[on_planet].radius, -cross(forward, upward))
        turn = radians(90)
        turn_axis = norm((forward+body[0].pos)-planets[on_planet].pos)
        # The visual elements of the body aren't properly turned along the planet,
        # So they drift out of sync with the caterpillar if it turns on a planet.
    if key_event == 'd':
        forward = cross(forward, upward)
        forward = forward.rotate(1/planets[on_planet].radius, -cross(forward, upward))
        turn = radians(90)
        turn_axis = -upward
        # The visual elements of the body aren't properly turned along the planet,
        # So they drift out of sync with the caterpillar if it turns on a planet.
    if key_event == '':
        turn_axis = -cross(forward, upward)
        turn = 1/planets[on_planet].radius
        forward = forward.rotate(1/planets[on_planet].radius, -cross(forward, upward))
    if key_event == 'w':
        forward, upward = upward, -forward
        turn = radians(90)
        on_planet = -1  # -1 represents when the caterpillar isn't on a planet
        turn_axis = cross(forward, upward)
    key_event = ''
    return forward, upward, turn, turn_axis, on_planet, planets


def is_planet_reached(body, caterpillar_pos, forward, on_planet, planets, turn, turn_axis, upward, roll):
    """ Checks if a planet is reached """
    for num1, planet in enumerate(planets):
        if mag(planet.pos - body[0].pos) <= planet.radius:
            on_planet = num1
            core_to_head = norm(body[0].pos - planet.pos) * planet.radius
            body[0].pos = core_to_head + planet.pos
            caterpillar_pos[0] = body[0].pos
            new_forward = norm(forward - proj(forward, core_to_head))
            if new_forward.equals(vector(0, 0, 0)):
                # This is here to check if the approach to the planet is vertical
                print("the caterpillar entered vertically")
                new_forward = norm(upward - proj(upward, core_to_head))
                turn = radians(90)
            else:
                turn = acos(dot(forward, new_forward) / (mag(forward) * mag(new_forward)))
            roll = acos(dot(upward, core_to_head)/(mag(upward)*mag(core_to_head)))
            upward = norm(core_to_head)
            forward = norm(new_forward)
            turn_axis = cross(forward, upward)
    return body, caterpillar_pos, forward, on_planet, planets, turn, turn_axis, upward, roll


def move_caterpillar(body, caterpillar_pos, forward, suit, turn, turn_axis, roll):
    """ Moving the caterpillar"""
    old_caterpillar_pos = caterpillar_pos[:]
    caterpillar_pos[0] += forward
    body[0].rotate(angle=turn, axis=turn_axis)
    body[0].rotate(angle=roll, axis=forward)
    body[0].pos = caterpillar_pos[0]
    suit[0].rotate(angle=turn, axis=turn_axis)
    suit[0].rotate(angle=roll, axis=forward)
    suit[0].pos = caterpillar_pos[0]
    for num, segment in enumerate(body):
        if num == 0:
            continue
        segment.pos = old_caterpillar_pos[num - 1]
        suit[num].pos = old_caterpillar_pos[num - 1]
        segment.rotate(angle=turn, axis=turn_axis)
        segment.rotate(angle=roll, axis=forward)
        suit[num].rotate(angle=turn, axis=turn_axis)
        suit[num].rotate(angle=roll, axis=forward)
        caterpillar_pos[num] = old_caterpillar_pos[num - 1]
    scene.center = caterpillar_pos[0]
    turn = 0
    roll = 0
    return turn, roll


def foodcheck(planets, on_planet, body):
    """Checks if you're touching the food"""
    scorechange = 0
    for food in planets[on_planet].food:
        if not food.visible:
            continue
        if mag(body[0].pos-food.pos) <= 1:
            food.visible = False
            scorechange += 1
    return scorechange


def main():
    """ Main loop """
    scene.bind('keydown', direction)

    global key_event  # Listening for key presses

    forward = vector(1, 0, 0)
    upward = vector(0, 1, 0)
    turn = 0
    roll = 0
    turn_axis = vector(0, 1, 0)

    caterpillar_pos = []  # Initialize Caterpillar position. Head in origo
    for dummy in range(5):
        caterpillar_pos.append(vector(-dummy, 0, 0))

    head = make_head()  # Make Caterpillar head
    body = make_body(caterpillar_pos, head)  # Make Caterpillar body
    helmet = make_helmet()
    suit = make_suit(caterpillar_pos, helmet)
    planets = make_planets(10)  # Makes planets
    make_food(planets)  # Distribute food on the planets
    # score = 0
    # scoretext = text(text=str(score), billboard=True, emissive=True, color=color.green)

    # cwd = os.getcwd()

    sleep_time = 0.2  # Time between position update
    on_planet = -1  # -1 represents when the caterpillar isn't on a planet
    while True:
        if on_planet > -1:  # -1 represents when the caterpillar isn't on a planet
            if suit[0].visible:
                for segment in suit:
                    segment.visible = False
            # score += foodcheck(planets, on_planet, body)
            # scoretext.text = str(score)
            # winsound.PlaySound(os.path.join(cwd, 'CaterpillarSounds', 'futz.wav'),
            #                    winsound.SND_FILENAME)
            upward = norm(body[0].pos-planets[on_planet].pos)
            caterpillar_pos[0] += upward*(planets[on_planet].radius - mag(
                caterpillar_pos[0] - planets[on_planet].pos)) + 0.75*upward
            forward, upward, turn, turn_axis, on_planet, planets = planet_direction(
                forward, upward, turn, turn_axis, on_planet, planets, body)
        else:
            if not suit[0].visible:
                for segment in suit:
                    segment.visible = True
            forward, upward, turn, turn_axis = space_direction(forward, upward, turn, turn_axis)
            body, caterpillar_pos, forward, on_planet, planets, turn, turn_axis, upward, roll = is_planet_reached(body, caterpillar_pos, forward, on_planet, planets, turn, turn_axis, upward, roll)

        if dot(forward, upward) > 0.1:
            print(forward, upward)
            return

        turn, roll = move_caterpillar(body, caterpillar_pos, forward, suit, turn, turn_axis, roll)
        sleep(sleep_time)

# box()

main()
