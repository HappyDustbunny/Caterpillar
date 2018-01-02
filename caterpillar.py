''' Snake clone '''

from math import acos
from vpython import *
from caterpillar_graphics import *
import winsound
import os

key_event = ''


def direction(event):
    """ Capture keyboard interupt and choose new direction and new orientation """
    # value = event.key
    global key_event
    key_event = event.key


def change_direction(forward, upward, turn, turn_axis):
    ''' Checking keyevent value and uddate direction if keyevent is not empty '''
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
    ''' Checking keyevent value and uddate direction while on planet.'''
    global key_event
    # planet planet planet planet planet planet planet
    if key_event == 'a':
        forward = -cross(forward, upward)
        forward = forward.rotate(1/planets[on_planet].radius, -cross(forward, upward))
        #turn and turn_axis not yet adapted
        #this means the caterpillar body's legs and face will get out of sync with the planet
        turn = radians(90)
        turn_axis = upward
    if key_event == 'd':
        forward = cross(forward, upward)
        forward = forward.rotate(1/planets[on_planet].radius, -cross(forward, upward))
        #turn and turn_axis not yet adapted
        #this means the caterpillar body's legs and face will get out of sync with the planet
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

def main():
    ''' Main loop '''
    scene.bind('keydown', direction)

    global key_event # Listening for key presses

    forward = vector(1, 0, 0)
    upward = vector(0, 1, 0)
    turn = 0
    turn_axis = vector(0, 1, 0)

    caterpillar_pos = []  # Initialize Caterpillar position. Head in origo
    for dummy in range(5):
        caterpillar_pos.append(vector(-dummy, 0, 0))

    head = make_head() # Make Caterpillar head
    body = make_body(caterpillar_pos, head) # Make Caterpillar body
    helmet = make_helmet()
    suit = make_suit(caterpillar_pos, helmet)
    sleep(0.01)
    planets = make_planets(10) # Makes planets
    make_food(planets) # Distribute food on the planets

    cwd = os.getcwd()
    print(cwd)  # Copy the folder CaterpillarSounds to this directory, pls

    d_t = 0.2
    on_planet = -1 # -1 represents when the caterpillar isn't on a planet
    while True:
        if on_planet > -1: # -1 represents when the caterpillar isn't on a planet
            if helmet.visible:
                helmet.visible = False
                for segment in suit:
                    segment.visible = False
            winsound.PlaySound(os.path.join(cwd, 'CaterpillarSounds', 'futz.wav'), winsound.SND_FILENAME)
            upward = norm(head.pos-planets[on_planet].pos)
            forward, upward, turn, turn_axis, on_planet, planets = planet_direction(forward, upward, turn, turn_axis, on_planet, planets)
        else:
            if not helmet.visible:
                helmet.visible = True
                for segment in suit:
                    segment.visible = True
            forward, upward, turn, turn_axis = change_direction(forward, upward, turn, turn_axis)

            for num1, planet in enumerate(planets): # Checking if a planet is reached
                if mag(planet.pos-head.pos) <= planet.radius:
                    on_planet = num1
                    core_to_head = norm(head.pos-planet.pos)*planet.radius
                    head.pos = core_to_head + planet.pos + 0.5*norm(core_to_head)
                    caterpillar_pos[0] = head.pos
                    new_forward = norm(forward - proj(forward, core_to_head))
                    if new_forward == 0: # If incoming is vertical new_forward = 0
                        new_forward = upward
                        turn = radians(90)
                    turn = acos(dot(forward, new_forward) / (mag(forward)*mag(new_forward)))
                    upward = norm(core_to_head)
                    forward = norm(new_forward)
                    turn_axis = cross(forward, upward)

        if dot(forward, upward) > 1:
            print(forward, upward)
            return

        old_caterpillar_pos = caterpillar_pos[:]  # Moving the caterpillar
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
            # if turn > 0:
            segment.rotate(angle=turn, axis=turn_axis)
            suit[num].rotate(angle=turn, axis=turn_axis)
            caterpillar_pos[num] = old_caterpillar_pos[num - 1]
        scene.center = caterpillar_pos[0]
        turn = 0
        sleep(d_t)

box()

main()
