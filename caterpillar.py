""" Snake clone """

# from math import acos
import vpython
from math import pi
import winsound
import os
from random import random, shuffle
from caterpillar_graphics import *

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
    p_shift = False
    if key_event == 'a':
        forward = -cross(forward, upward)
        forward = forward.rotate(1 / (planets[on_planet].radius + 0.75), -cross(forward, upward))
    if key_event == 'd':
        forward = cross(forward, upward)
        forward = forward.rotate(1 / (planets[on_planet].radius + 0.75), -cross(forward, upward))
    if key_event == '':
        forward = forward.rotate(1 / (planets[on_planet].radius + 0.75), -cross(forward, upward))
    if key_event == 'w':  # Leaving planet
        right = cross(forward, upward)
        forward, upward = upward, cross(right, upward)
        p_shift = True
    key_event = ''
    return forward, upward, p_shift


def is_planet_reached(body, caterpillar_pos, forward, on_planet, planets, upward, suit, turn_list):
    """ Checks if a planet is reached """
    for num1, planet in enumerate(planets):
        if mag(planet.pos - body[0].pos) <= planet.radius:  # Arriving at planet
            on_planet = num1
            for segment in body:
                segment.visible = False
            for segment in suit:
                segment.visible = False
            core_to_head = norm(body[0].pos - planet.pos) * planet.radius
            # caterpillar_pos[0] = core_to_head + planet.pos
            # body[0].pos = caterpillar_pos[0]
            forward = norm(forward - proj(forward, core_to_head))
            if forward.equals(vector(0, 0, 0)):  # Check if the approach to the planet is vertical
                forward = norm(upward - proj(upward, core_to_head))
            upward = norm(core_to_head)
            for dummy in range(5):
                caterpillar_pos[dummy] = caterpillar_pos[0] - dummy * forward
            for dummy in range(5):
                turn_list[dummy] = [0, vector(0, 0, 0)]
            head = make_head(caterpillar_pos, forward, upward)  # Make Caterpillar head
            body = make_body(caterpillar_pos, head, forward, upward)  # Make Caterpillar body
            scene.camera.follow(planets[on_planet])
    return body, caterpillar_pos, forward, on_planet, upward, turn_list


def rotate_caterpillar(body, suit, turn_list):
    """ Rotating the caterpillarsegments  and the suit"""
    body[0].rotate(turn_list[0][0], turn_list[0][1])
    suit[0].rotate(turn_list[0][0], turn_list[0][1])
    for num, segment in enumerate(body):
        if num == 0:
            continue
        segment.rotate(turn_list[num][0], turn_list[num][1])
        suit[num].rotate(turn_list[num][0], turn_list[num][1])


def move_caterpillar(body, caterpillar_pos, forward, suit, turn_list):
    """ Moving the caterpillar"""
    old_caterpillar_pos = caterpillar_pos[:]
    caterpillar_pos[0] += forward
    body[0].pos = caterpillar_pos[0]
    suit[0].pos = caterpillar_pos[0]
    for num, segment in enumerate(body):
        if num == 0:
            continue
        segment.pos = old_caterpillar_pos[num - 1]
        suit[num].pos = old_caterpillar_pos[num - 1]
        caterpillar_pos[num] = old_caterpillar_pos[num - 1]
    rotate_caterpillar(body, suit, turn_list)
    # scene.center = caterpillar_pos[0]


def foodscatter(planets, on_planet, foodnum, body):
    """Moves all food pieces to randdom places on the planet after landing"""
    food_pos = norm(vector(random() - 0.5, random() - 0.5, random() - 0.5)
                    ) * planets[on_planet].radius + planets[on_planet].pos
    if mag(food_pos - body[0].pos) <= 3:
        food_pos = foodscatter(planets, on_planet, foodnum, body)
    for num in range(foodnum):
        if mag(food_pos - planets[on_planet].food[num].pos) <= 3:
            food_pos = foodscatter(planets, on_planet, foodnum, body)
    return food_pos


def foodorder(planets, on_planet):
    """Puts all the food back in its place after leaving a planet
    without having picked up all the food in the correct order"""
    toward_zero = norm(-planets[on_planet].pos) * planets[on_planet].radius
    perp_to_zero = norm(cross(toward_zero, vector(0, -1, 0)))
    color_list = [color.blue, color.cyan, color.green, color.magenta,
                 color.orange, color.red, color.yellow, color.white]
    for num, food in enumerate(planets[on_planet].food):
        shuffle(color_list)
        food.pos = norm(toward_zero + perp_to_zero * (num * 2 - len(planets[on_planet].food))) \
                        * (planets[on_planet].radius + 0.5) + planets[on_planet].pos
        food.axis = perp_to_zero * 2
        food.color = color_list.pop()
        food.visible = True


def foodcheck(planets, on_planet, body, targetfood):
    """Checks your status compared to the food on the current planet"""
    global key_event
    collection_range = 1.5
    if targetfood >= len(planets[on_planet].food) or targetfood == -1:
        # targetfood being -1 represents returning to a planet 
        # where you have already collected all the food
        print("All food collected on this planet.")
        key_event = "w"
    elif not planets[on_planet].food[targetfood].visible:
        print("If you see this error message, something went wrong, but not catastrophically so.")
        key_event = "w"
    elif mag(planets[on_planet].food[targetfood].pos - body[0].pos) <= collection_range:
        planets[on_planet].food[targetfood].visible = False
        targetfood += 1
        if targetfood >= len(planets[on_planet].food):
            print("All food collected on this planet.")
            key_event = "w"
    else:
        for nontargetfood in planets[on_planet].food:
            if nontargetfood.visible and mag(body[0].pos - nontargetfood.pos) <= collection_range:
                print("Food collected in wrong order.")
                key_event = "w"
    # for food in planets[on_planet].food:
    #     if food.visible and mag(body[0].pos-food.pos) <= 1:
    #         food.visible = False
    return targetfood


def main():
    """ Main loop """
    scene.bind('keydown', direction)

    # global key_event  # Listening for key presses

    forward = vector(1, 0, 0)
    upward = vector(0, 1, 0)

    v_forward = vector(1, 0, 0)
    v_upward = vector(0, 1, 0)
    turn_list = []
    p_shift = False
    target_food = 0

    for dummy in range(5):
        turn_list.append([0, vector(0, 0, 0)])

    caterpillar_pos = [vector(0, 0, 0)]  # Initialize Caterpillar position. Head in origo
    for dummy in range(1, 5):
        caterpillar_pos.append(caterpillar_pos[0] - dummy * forward)

    head = make_head(caterpillar_pos, forward, upward)  # Make Caterpillar head
    body = make_body(caterpillar_pos, head, forward, upward)  # Make Caterpillar body
    helmet = make_helmet(caterpillar_pos, forward, upward)  # Make space helmet
    suit = make_suit(caterpillar_pos, helmet, forward, upward)  # Make space suit
    planets = make_planets(10)  # Makes planets
    make_food(planets)  # Distribute food on the planets

    score = 0

    # cwd = os.getcwd()

    scene.caption = "Score:" + str(score)
    scene.camera.follow(body[0])

    sleep_time = 0.2  # Time between position update
    on_planet = -1  # on_planet being -1 represents when the caterpillar isn't on a planet
    while True:
        if on_planet == -1:  # on_planet being -1 represents when the caterpillar isn't on a planet
            forward, upward = space_direction(forward, upward)
            body, caterpillar_pos, forward, on_planet, upward, turn_list = is_planet_reached(
                body, caterpillar_pos, forward, on_planet, planets, upward, suit, turn_list)
            if on_planet >= 0:
                for segment in suit:
                    segment.visible = False
                if planets[on_planet].food[-1].visible:
                    for num, food in enumerate(planets[on_planet].food):
                        food.pos = foodscatter(planets, on_planet, num, body)
                        food.axis = 2 * norm(food.pos - planets[on_planet].pos)
                    target_food = 0
                else:
                    target_food = -1
                for segment in suit:
                    segment.visible = False
                p_shift = True
        else:
            target_food = foodcheck(planets, on_planet, body, target_food)
            # winsound.PlaySound(os.path.join(cwd, 'CaterpillarSounds', 'futz.wav'),
            #                    winsound.SND_FILENAME)
            upward = norm(caterpillar_pos[0] - planets[on_planet].pos)
            caterpillar_pos[0] += upward * (planets[on_planet].radius - mag(
                caterpillar_pos[0] - planets[on_planet].pos)) + 0.75 * upward
            forward, upward, p_shift = planet_direction(forward, upward, on_planet, planets)
            scene.caption = "Score:" + str(score + target_food)
            if p_shift:
                if target_food >= len(planets[on_planet].food):
                    score += target_food
                elif target_food != -1:
                    # target_food being -1 represents having returned to a planet
                    # where you have already collected all the food.
                    foodorder(planets, on_planet)
                target_food = 0
                scene.caption = "Score:" + str(score)
                on_planet = -1  # -1 represents when the caterpillar isn't on a planet
                for segment in body:
                    segment.visible = False
                for dummy in range(5):
                    caterpillar_pos[dummy] = caterpillar_pos[0] - dummy * forward
                for dummy in range(5):
                    turn_list[dummy] = [0, vector(0, 0, 0)]
                head = make_head(caterpillar_pos, forward, upward)  # Make Caterpillar head
                body = make_body(caterpillar_pos, head, forward, upward)  # Make Caterpillar body
                helmet = make_helmet(caterpillar_pos, forward, upward)
                suit = make_suit(caterpillar_pos, helmet, forward, upward)
                scene.camera.follow(body[0])

        if dot(forward, upward) > 0.1:
            print('forward and upward is not perpendicular', forward, upward)
            return
        if p_shift:
            v_forward = forward
            v_upward = upward
            p_shift = False
        else:
            turn_list.insert(0, [diff_angle(v_forward, forward),
                                 norm(cross(v_forward, forward))])
            turn_list.pop()

        v_forward = v_forward.rotate(turn_list[0][0], turn_list[0][1])
        v_upward = v_upward.rotate(turn_list[0][0], turn_list[0][1])
        move_caterpillar(body, caterpillar_pos, forward, suit, turn_list)
        sleep(sleep_time)


main()
