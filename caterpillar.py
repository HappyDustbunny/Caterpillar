""" Snake clone """

# from math import acos
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


def space_direction(forward, upward):
    """ Checking key_event value and update direction if key_event is not empty """
    global key_event
    if key_event == 'a':
        forward = -cross(forward, upward)
    if key_event == 'd':
        forward = cross(forward, upward)
    if key_event == 'w':
        forward, upward = upward, -forward
    if key_event == 's':
        forward, upward = -upward, forward
    key_event = ''
    return forward, upward


def planet_direction(forward, upward, on_planet, planets):
    """ Checking key_event value and update direction while on planet. """
    global key_event
    if key_event == 'a':
        forward = -cross(forward, upward)
        forward = forward.rotate(1/planets[on_planet].radius, -cross(forward, upward))
    if key_event == 'd':
        forward = cross(forward, upward)
        forward = forward.rotate(1/planets[on_planet].radius, -cross(forward, upward))
    if key_event == '':
        forward = forward.rotate(1/planets[on_planet].radius, -cross(forward, upward))
    if key_event == 'w':
        forward, upward = upward, -forward
        on_planet = -1  # -1 represents when the caterpillar isn't on a planet
    key_event = ''
    return forward, upward, on_planet


def is_planet_reached(body, caterpillar_pos, forward, on_planet, planets, upward):
    """ Checks if a planet is reached """
    for num1, planet in enumerate(planets):
        if mag(planet.pos - body[0].pos) <= planet.radius:
            on_planet = num1
            core_to_head = norm(body[0].pos - planet.pos) * planet.radius
            caterpillar_pos[0] = core_to_head + planet.pos
            body[0].pos = caterpillar_pos[0]
            new_forward = norm(forward - proj(forward, core_to_head))
            if new_forward.equals(vector(0, 0, 0)):
                # This is here to check if the approach to the planet is vertical
                new_forward = norm(upward - proj(upward, core_to_head))
            upward = norm(core_to_head)
            forward = new_forward
    return body, caterpillar_pos, forward, on_planet, upward


def move_caterpillar(body, caterpillar_pos, forward, suit, turn_list):
    """ Moving the caterpillar"""
    old_caterpillar_pos = caterpillar_pos[:]
    caterpillar_pos[0] += forward
    body[0].rotate(turn_list[0][0], turn_list[0][1])
    body[0].pos = caterpillar_pos[0]
    suit[0].rotate(turn_list[0][0], turn_list[0][1])
    suit[0].pos = caterpillar_pos[0]
    for num, segment in enumerate(body):
        if num == 0:
            continue
        segment.pos = old_caterpillar_pos[num - 1]
        suit[num].pos = old_caterpillar_pos[num - 1]
        segment.rotate(turn_list[num][0], turn_list[num][1])
        suit[num].rotate(turn_list[num][0], turn_list[num][1])
        caterpillar_pos[num] = old_caterpillar_pos[num - 1]
    scene.center = caterpillar_pos[0]


def foodcheck(planets, on_planet, body):
    """Checks if you're touching the food"""
    for food in planets[on_planet].food:
        if not food.visible:
            continue
        if mag(body[0].pos-food.pos) <= 1:
            food.visible = False
    return


def main():
    """ Main loop """
    scene.bind('keydown', direction)

    global key_event  # Listening for key presses

    forward = vector(1, 0, 0)
    upward = vector(0, 1, 0)

    v_forward = vector(1, 0, 0)
    v_upward = vector(0, 1, 0)
    turn_list = []
    p_shift = False

    for dummy in range(5):
        turn_list.append([0, vector(0, 0, 0)])

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

    # cwd = os.getcwd()

    sleep_time = 0.2  # Time between position update
    on_planet = -1  # -1 represents when the caterpillar isn't on a planet
    while True:
        if on_planet > -1:  # -1 represents when the caterpillar isn't on a planet
            if suit[0].visible:
                for segment in suit:
                    segment.visible = False
            foodcheck(planets, on_planet, body)
            # scoretext.text = str(score)
            # winsound.PlaySound(os.path.join(cwd, 'CaterpillarSounds', 'futz.wav'),
            #                    winsound.SND_FILENAME)
            upward = norm(body[0].pos-planets[on_planet].pos)
            caterpillar_pos[0] += upward*(planets[on_planet].radius - mag(
                caterpillar_pos[0] - planets[on_planet].pos)) + 0.75*upward
            forward, upward, on_planet = planet_direction(forward, upward, on_planet, planets)
        else:
            if not suit[0].visible:
                for segment in suit:
                    segment.visible = True
            forward, upward = space_direction(forward, upward)
            body, caterpillar_pos, forward, on_planet, upward = is_planet_reached(
                body, caterpillar_pos, forward, on_planet, planets, upward)
            if on_planet >= 0:
                p_shift = True

        if dot(forward, upward) > 0.1:
            print(forward, upward)
            return
        if p_shift:
            # Comment the text below out after a solution is found.
            turn_list.insert(0, [diff_angle(v_forward, forward),
                                 norm(cross(v_forward, forward))])
            turn_list.pop()
            # Comment the text above out after a solution is found.
            p_shift = False
        else:
            turn_list.insert(0, [diff_angle(v_forward, forward),
                                 norm(cross(v_forward, forward))])
            turn_list.pop()

        v_forward = v_forward.rotate(turn_list[0][0], turn_list[0][1])
        v_upward = v_upward.rotate(turn_list[0][0], turn_list[0][1])
        if mag(v_forward-forward) > 0.1:# or mag(v_upward-upward) > 0.1:
            print("v_forward:", v_forward)
            print("forward:", forward)
            print("v_upward:", v_upward)
            print("upward:", upward)
            print("turning stats:", turn_list[0][0], turn_list[0][1])
            print("turning error")
            return

        move_caterpillar(body, caterpillar_pos, forward, suit, turn_list)
        sleep(sleep_time)

main()
