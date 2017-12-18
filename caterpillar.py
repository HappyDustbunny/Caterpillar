''' Snake clone '''

from math import acos
from vpython import *

keyevent = ''

def make_head():
    ''' Make caterpillar head '''
    head_ball = sphere(color=color.orange)
    helmet = sphere(pos=vector(.1, 0.15, 0), radius=1.2, opacity=0.3)
    left_eye = sphere(pos=vector(0.5, 0.5, -0.4), radius=0.35)
    right_eye = sphere(pos=vector(0.5, 0.5, 0.4), radius=0.35)
    left_pupil = sphere(pos=vector(0.6, 0.56, -0.42), radius=0.25, color=color.black)
    rigth_pupil = sphere(pos=vector(0.6, 0.56, 0.42), radius=0.25, color=color.black)
    head = compound([head_ball, helmet, left_eye, right_eye, left_pupil, rigth_pupil])
    return head

def make_body(caterpillar_pos):
    ''' Make caterpillar body '''
    body = []
    for increment in range(1, 5):
        body_sphere = sphere(pos=caterpillar_pos[increment], color=color.blue)
        left_foot = sphere(pos=caterpillar_pos[increment] +
                           vector(0, -0.6, -0.5), radius=0.3, color=color.orange)
        right_foot = sphere(pos=caterpillar_pos[increment] +
                            vector(0, -0.6, 0.5), radius=0.3, color=color.orange)
        body_segment = compound([body_sphere, left_foot, right_foot])
        body.append(body_segment)
    return body

def make_planets(number_of_planets):
    ''' Makes planets '''
    planets = []
    planet = sphere(pos=vector(50, -1, 0), radius=20, texture=textures.wood_old) # Testplanet. Remove when reinstating all planets
    planets.append(planet) # Testplanet. Remove when reinstating all planets
    # for _ in range(number_of_planets):
    #     planet = sphere(pos=vector(int(150*random() - 50), int(150*random() - 50),
    #                                int(150*random()) - 50), radius=int(20*random()),
    #                     texture=textures.wood_old)
    #     planets.append(planet)
    return planets

def make_food(planets):
    ''' Distribute food on planets '''
    for planet in planets:
        radius = planet.radius
        foods = []
        for _ in range(int(5*random() + 5)): # makes 5-10 pellets
            food_pos = norm(vector(random() - 0.5, random() - 0.5, random() - 0.5))*radius + planet.pos
            food = sphere(pos=food_pos, texture=textures.rock)
            foods.append(food)
        planet.food = foods
    return

def direction(event):
    ''' Capture keyboard interupt and choose new direction and new orientation '''
    # value = event.key
    global keyevent
    keyevent = event.key

def change_direction(forward, upward, turn, turn_axis):
    ''' Checking keyevent value and uddate direction if keyevent is not empty '''
    global keyevent
    if keyevent == 'a':
        forward = -cross(forward, upward)
        turn = radians(90)
        turn_axis = upward
    if keyevent == 'd':
        forward = cross(forward, upward)
        turn = radians(90)
        turn_axis = -upward
    if keyevent == 'w':
        forward, upward = upward, -forward
        turn = radians(90)
        turn_axis = cross(forward, upward)
    if keyevent == 's':
        forward, upward = -upward, forward
        turn = radians(90)
        turn_axis = -cross(forward, upward)
    keyevent = ''
    return forward, upward, turn, turn_axis

def main():
    ''' Main loop '''
    scene.bind('keydown', direction)

    global keyevent # Listening for key presses

    forward = vector(1, 0, 0)
    upward = vector(0, 1, 0)
    turn = 0
    turn_axis = vector(0, 1, 0)

    caterpillar_pos = []  # Initialize Caterpillar position. Head in origo
    for dummy in range(5):
        caterpillar_pos.append(vector(-dummy, 0, 0))

    head = make_head() # Make Caterpillar head
    body = make_body(caterpillar_pos) # Make Caterpillar body
    planets = make_planets(10) # Makes planets
    make_food(planets) # Distribute food on the planets

    d_t = 0.2
    on_planet = False
    while True:
        if on_planet:
            pass
        else:
            forward, upward, turn, turn_axis = change_direction(forward, upward, turn, turn_axis)

            old_caterpillar_pos = caterpillar_pos[:]  # Moving the caterpillar
            caterpillar_pos[0] += forward
            head.pos = caterpillar_pos[0]
            scene.center = caterpillar_pos[0]
            for planet in planets:
                if mag(planet.pos-head.pos) <= planet.radius:
                    core_to_head = norm(head.pos-planet.pos)*planet.radius
                    head.pos = core_to_head + planet.pos + 0.5*norm(core_to_head)
                    new_forward = norm(forward - proj(forward, core_to_head))
                    if new_forward == 0: # If incomming is vertical new_forward = 0
                        new_forward = upward
                    turn = acos(dot(forward, new_forward) / (mag(forward)*mag(new_forward)))
                    upward = norm(core_to_head)
                    forward = norm(new_forward)
                    if dot(forward, upward) > 0.001:
                        print(forward)
                        print(upward)
                        return
                    turn_axis = cross(forward, upward)
            # scene.up = upward    # Gives hard turning camera
            for num, segment in enumerate(body):
                segment.pos = old_caterpillar_pos[num]
                if turn > 0:
                    segment.rotate(angle=turn, axis=turn_axis)
                caterpillar_pos[num + 1] = old_caterpillar_pos[num]
            turn = False
            sleep(d_t)
    # for _ in range(20):
    #     for segment in body:
    #         for _ in range(5):
    #             segment.pos.x += .1
    #             sleep(0.001)

box()

main()
