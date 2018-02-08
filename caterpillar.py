""" Snake clone """

# from math import acos
import vpython
from math import pi
import winsound
import os
from random import random, shuffle
from caterpillar_graphics import *

key_event = ''


class CaterpillarClass:
    """ Store position data and local coordinate system """
    def __init__(self, pos, forward, upward, turn_list):
        self.pos = pos
        self.forward = forward
        self.upward = upward
        self.last_forward = forward
        self.last_upward = upward
        self.turn_list = turn_list
    
    def right(self):
        return norm(cross(self.forward, self.upward))

    def right(self):
        return norm(cross(self.forward, self.upward))

    def angle(self):
        angle = diff_angle(self.last_upward, self.upward)
        return angle

    def update_pos(self, new_pos):
        last_pos = self.pos
        self.pos = new_pos


def direction(event):
    """ Capture keyboard interrupt and choose new direction and new orientation """
    # value = event.key
    global key_event
    key_event = event.key


def space_direction(cat):
    """ Checking key_event value and update direction if key_event is not empty """
    global key_event
    if key_event == 'a':
        cat.forward = -cat.right()
    if key_event == 'd':
        cat.forward = cat.right()
    if key_event == 'w':
        cat.forward, cat.upward = cat.upward, -cat.forward
    if key_event == 's':
        cat.forward, cat.upward = -cat.upward, cat.forward
    key_event = ''
    return cat


def planet_direction(cat, body, suit, planets, target_food, score, on_planet):
    """ Checking key_event value and update direction while on planet. """
    global key_event
    if key_event == 'a':
        cat.forward = -cat.right()
        cat.forward = cat.forward.rotate(1 / (planets[on_planet].radius + 0.75), -cat.right())
    if key_event == 'd':
        cat.forward = cat.right()
        cat.forward = cat.forward.rotate(1 / (planets[on_planet].radius + 0.75), -cat.right())
    if key_event == 's':
        cat.forward = cat.forward.rotate(1 / (planets[on_planet].radius + 0.75), -cat.right())
    if key_event == 'w':  # Leaving planet
        cat.forward, cat.upward = cat.upward, cat.right()
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
            cat.pos[dummy] = cat.pos[0] - dummy * cat.forward
        for dummy in range(5):
            cat.turn_list[dummy] = [0, vector(0, 0, 0)]
        body = make_body(cat.pos, cat.forward, cat.upward)  # Make Caterpillar body
        suit = make_suit(cat.pos, cat.forward, cat.upward)
        cat.last_forward = cat.forward
        cat.last_upward = cat.upward
        scene.camera.follow(body[0])
    key_event = ''
    return cat, body, suit, target_food, score, on_planet


def is_planet_reached(cat, body, suit, planets, on_planet, target_food):
    """ Checks if a planet is reached """
    for num1, planet in enumerate(planets):
        if mag(planet.pos - body[0].pos) <= planet.radius:  # Arriving at planet
            on_planet = num1
            for segment in body:
                segment.visible = False
            for segment in suit:
                segment.visible = False
            core_to_head = norm(body[0].pos - planet.pos) * planet.radius
            # cat.pos[0] = core_to_head + planet.pos
            # body[0].pos = cat.pos[0]
            cat.forward = norm(cat.forward - proj(cat.forward, core_to_head))
            if cat.forward.equals(vector(0, 0, 0)):  # Check if the approach to the planet is vertical
                cat.forward = norm(cat.upward - proj(cat.upward, core_to_head))
            cat.upward = norm(core_to_head)
            for dummy in range(5):
                cat.pos[dummy] = cat.pos[0] - dummy * cat.forward
            for dummy in range(5):
                cat.turn_list[dummy] = [0, vector(0, 0, 0)]
            body = make_body(cat.pos, cat.forward, cat.upward)  # Make Caterpillar body
            scene.camera.follow(planets[on_planet])
            if planets[on_planet].food[-1].visible:
                for num, food in enumerate(planets[on_planet].food):
                    food.pos = foodscatter(planets, on_planet, num, body)
                    food.axis = 2 * norm(food.pos - planets[on_planet].pos)
                target_food = 0
            else:
                target_food = -1
            for segment in suit:
                segment.visible = False
    return cat, body, on_planet, target_food


def move_caterpillar(cat, body, suit):
    """ Moving the caterpillar"""
    # winsound.PlaySound(os.path.join(cwd, 'CaterpillarSounds', 'futz.wav'),
    #                    winsound.SND_FILENAME)
    old_caterpillar_pos = cat.pos[:]
    cat.pos[0] += cat.forward
    body[0].pos = cat.pos[0]
    suit[0].pos = cat.pos[0]
    for num, segment in enumerate(body):
        if num == 0:
            continue
        segment.pos = old_caterpillar_pos[num - 1]
        suit[num].pos = old_caterpillar_pos[num - 1]
        cat.pos[num] = old_caterpillar_pos[num - 1]
    body[0].rotate(cat.turn_list[0][0], cat.turn_list[0][1])  # Rotate segments and suit
    suit[0].rotate(cat.turn_list[0][0], cat.turn_list[0][1])
    for num, segment in enumerate(body):
        if num == 0:
            continue
        segment.rotate(cat.turn_list[num][0], cat.turn_list[num][1])
        suit[num].rotate(cat.turn_list[num][0], cat.turn_list[num][1])


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

    target_food = 0
    forward, upward = vector(1, 0, 0), vector(0, 1, 0)
    caterpillar_pos = [vector(0, 0, 0)]  # Initialize Caterpillar head position. Head in origo
    for dummy in range(1, 5):  # Initialize body segment positions
        caterpillar_pos.append(caterpillar_pos[0] - dummy * forward)
    turn_list = []  # Initialize the list describing how each segment turns when the caterpillar moves
    for dummy in range(5):
        turn_list.append([0, vector(0, 0, 0)])

    cat = CaterpillarClass(caterpillar_pos, forward, upward, turn_list)

    body = make_body(cat.pos, cat.forward, cat.upward)  # Make caterpillar body
    suit = make_suit(cat.pos, cat.forward, cat.upward)  # Make space suit
    planets = make_planets(10)  # Make planets
    make_food(planets)  # Distribute food on the planets
    
    # cwd = os.getcwd()
    score = 0
    scene.caption = "Score:" + str(score)
    scene.camera.follow(body[0])

    scene.caption = "Score:" + str(score)
    scene.camera.follow(body[0])

    sleep_time = 0.2  # Time between position update
    on_planet = -1  # on_planet being -1 represents when the caterpillar isn't on a planet
    while True:
        if on_planet == -1:  # Off planet: on_planet being -1 represents when the caterpillar isn't on a planet
            cat = space_direction(cat)
            # cat.forward, cat.upward = space_direction(cat.forward, cat.upward)
            cat, body, on_planet, target_food = is_planet_reached(cat, body, suit, planets, on_planet, target_food)
        else:  # On planet:
            target_food = foodcheck(planets, on_planet, body, target_food)
            cat.upward = norm(cat.pos[0] - planets[on_planet].pos)
            cat.pos[0] += cat.upward * (planets[on_planet].radius - mag(cat.pos[0] - planets[on_planet].pos)) + 0.75 * cat.upward
            cat, body, suit, target_food, score, on_planet = planet_direction(cat, body, suit, planets, target_food,\
                score, on_planet)
            scene.caption = "Score:" + str(score + target_food)

        if not cat.last_forward.equals(cat.forward):
            cat.turn_list.insert(0, [diff_angle(cat.last_forward, cat.forward),
                                     norm(cross(cat.last_forward, cat.forward))])
            cat.turn_list.pop()

        cat.last_forward = cat.last_forward.rotate(cat.turn_list[0][0], cat.turn_list[0][1])
        cat.last_upward = cat.last_upward.rotate(cat.turn_list[0][0], cat.turn_list[0][1])
        move_caterpillar(cat, body, suit)
        sleep(sleep_time)

    # cat.upward = vector(0, 0, 1)
    # print(cat.upward, cat.last_upward, cat.angle())
    # body[2].up = cat.upward


main()

# def main():
#     """ Main loop """
#     scene.bind('keydown', direction)
#
#     # global key_event  # Listening for key presses
#     target_food = 0
#
#     forward, upward = vector(1, 0, 0), vector(0, 1, 0)
#     v_forward, v_upward = vector(1, 0, 0), vector(0, 1, 0)
#
#     turn_list = []  # Initialize the list describing how each segment turns when the caterpillar moves
#     for dummy in range(5):
#         turn_list.append([0, vector(0, 0, 0)])
#
#     caterpillar_pos = [vector(0, 0, 0)]  # Initialize Caterpillar position. Head in origo
#     for dummy in range(1, 5):
#         caterpillar_pos.append(caterpillar_pos[0] - dummy * forward)
#
#     body = make_body(caterpillar_pos, forward, upward)  # Make Caterpillar body
#     suit = make_suit(caterpillar_pos, forward, upward)  # Make space suit
#     planets = make_planets(10)  # Make planets
#     make_food(planets)  # Distribute food on the planets
#
#     # cwd = os.getcwd()
#     score = 0
#     scene.caption = "Score:" + str(score)
#     scene.camera.follow(body[0])
#
#     sleep_time = 0.2  # Time between position update
#     on_planet = -1  # on_planet being -1 represents when the caterpillar isn't on a planet
#     while True:
#         if on_planet == -1:  # Off planet: on_planet being -1 represents when the caterpillar isn't on a planet
#             forward, upward = space_direction(forward, upward)
#             body, caterpillar_pos, forward, on_planet, upward, turn_list, target_food = is_planet_reached(
#                 body, caterpillar_pos, forward, on_planet, planets, upward, suit, turn_list, target_food)
#         else:  # On planet:
#             target_food = foodcheck(planets, on_planet, body, target_food)
#             upward = norm(caterpillar_pos[0] - planets[on_planet].pos)
#             caterpillar_pos[0] += upward * (planets[on_planet].radius - mag(
#                 caterpillar_pos[0] - planets[on_planet].pos)) + 0.75 * upward
#             forward, upward, target_food, score, on_planet, head, body, helmet, suit, caterpillar_pos, \
#                 turn_list, v_forward, v_upward = planet_direction(forward, upward, planets, target_food,\
#                 score, on_planet, head, body, helmet, suit, caterpillar_pos, turn_list, v_forward, v_upward)
#             scene.caption = "Score:" + str(score + target_food)
#
#         if v_forward != forward:
#             turn_list.insert(0, [diff_angle(v_forward, forward), norm(cross(v_forward, forward))])
#             turn_list.pop()
#
#         if dot(forward, upward) > 0.1:
#             print('forward and upward is not perpendicular', forward, upward)
#             return
#
#         v_forward = v_forward.rotate(turn_list[0][0], turn_list[0][1])
#         v_upward = v_upward.rotate(turn_list[0][0], turn_list[0][1])
#         move_caterpillar(body, caterpillar_pos, forward, suit, turn_list)
#         sleep(sleep_time)