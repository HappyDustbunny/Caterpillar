""" Snake clone """

# from math import acos
from vpython import *
# import winsound
# import os
from random import random, shuffle
from caterpillar_graphics import make_body, make_suit, make_food, make_planets

PI = 3.1415926536
key_event = ''


class CaterpillarClass:
    """ Store position data and local coordinate system """
    def __init__(self, pos, forward, upward, turn_list):
        self.pos = pos
        self.forward = forward
        self.upward = upward
        self.last_pos = pos
        self.last_forward = forward
        self.last_upward = upward
        self.turn_list = turn_list

    def right(self):
        """ Returns last vector in local coordinate system (forward, upward, right)"""
        value = norm(cross(self.forward, self.upward))
        return value
    #
    # def angle(self):
    #     angle = diff_angle(self.last_upward, self.upward)
    #     return angle
    #
    # def update_pos(self, new_pos):
    #     self.last_pos = self.pos
    #     self.pos = new_pos


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
        cat.turn_list[0] = [PI/2, cat.upward]
    if key_event == 'd':
        cat.forward = cat.right()
        cat.turn_list[0] = [-PI/2, cat.upward]
    if key_event == 'w':
        cat.forward, cat.upward = cat.upward, -cat.forward
        cat.turn_list[0] = [PI/2, cat.right()]
    if key_event == 's':
        cat.forward, cat.upward = -cat.upward, cat.forward
        cat.turn_list[0] = [-PI/2, cat.right()]
    key_event = ''
    return cat


def planet_direction(cat, body, suit, planets, target_food, score, on_planet):
    """ Checking key_event value and update direction while on planet. """
    global key_event
    if key_event == 'a':
        cat.forward = -cat.right()
        cat.turn_list[0] = [PI/2, cat.upward]
        # cat.turn_list.insert(0, [-PI/2, cat.upward])
        # cat.turn_list.pop()
    if key_event == 'd':
        cat.forward = cat.right()
        cat.turn_list[0] = [-PI/2, cat.upward]
        # cat.turn_list.insert(0, [PI/2, cat.upward])
        # cat.turn_list.pop()
    if key_event == 'w':  # Leaving planet
        cat.forward, cat.upward = cat.upward, -cat.forward
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
        for num in range(5):
            cat.pos[num] = cat.pos[0] - num * cat.forward
            cat.turn_list[num] = [0, vector(0, 0, 0)]
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
            cat.pos[0] = core_to_head + planet.pos + 0.75 * norm(core_to_head)
            body[0].pos = cat.pos[0]
            cat.forward = norm(cat.forward - proj(cat.forward, core_to_head))
            if cat.forward.equals(vector(0, 0, 0)):  # Check if the approach to the planet is vertical
                cat.forward = norm(cat.upward - proj(cat.upward, core_to_head))
            cat.upward = norm(core_to_head)
            for num in range(5):
                cat.pos[num] = cat.pos[0] - num * cat.forward
                cat.turn_list[num] = [0, vector(0, 0, 0)]
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


def move_caterpillar(cat, body, suit, on_planet, planets):
    """ Move the caterpillar one step"""
    # winsound.PlaySound(os.path.join(cwd, 'CaterpillarSounds', 'futz.wav'),
    #                    winsound.SND_FILENAME)
    old_caterpillar_pos = cat.pos[:]
    cat.pos[0] += cat.forward

    body[0].pos = cat.pos[0]
    suit[0].pos = cat.pos[0]

    body[0].rotate(cat.turn_list[0][0], cat.turn_list[0][1])
    suit[0].rotate(cat.turn_list[0][0], cat.turn_list[0][1])
    if on_planet != -1:
        body[0].rotate(1 / (planets[on_planet].radius + 0.75), -cat.right())
    for num, segment in enumerate(body):
        if num == 0:
            continue
        segment.pos = old_caterpillar_pos[num - 1]
        suit[num].pos = old_caterpillar_pos[num - 1]
        cat.pos[num] = old_caterpillar_pos[num - 1]

        segment.rotate(cat.turn_list[num][0], cat.turn_list[num][1])
        suit[num].rotate(cat.turn_list[num][0], cat.turn_list[num][1])
        if on_planet != -1:
            segment.rotate(1 / (planets[on_planet].radius + 0.75), -cat.right())
    cat.turn_list.insert(0, [0, vector(0, 0, 0)])
    cat.turn_list.pop()


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

    # cwd = os.getcwd()
    target_food, score = 0, 0
    scene.caption = "Score:" + str(score)

    forward, upward = vector(1, 0, 0), vector(0, 1, 0)
    caterpillar_pos = [vector(0, 0, 0)]  # Initialize Caterpillar head position. Head in origo
    turn_list = [[0, vector(0, 0, 0)]]  # Initialize a list describing how each segment turns when the caterpillar moves
    for num in range(1, 5):  # Initialize body segment positions
        caterpillar_pos.append(caterpillar_pos[0] - num * forward)
        turn_list.append([0, vector(0, 0, 0)])

    cat = CaterpillarClass(caterpillar_pos, forward, upward, turn_list)

    body = make_body(cat.pos, cat.forward, cat.upward)  # Make caterpillar body
    suit = make_suit(cat.pos, cat.forward, cat.upward)  # Make space suit
    planets = make_planets(10)  # Make planets
    make_food(planets)  # Distribute food on the planets

    scene.camera.follow(body[0])

    sleep_time = 1.2  # Time between position updates
    on_planet = -1  # on_planet being -1 represents when the caterpillar isn't on a planet
    while True:
        if on_planet == -1:  # Off planet: on_planet being -1 represents when the caterpillar isn't on a planet
            cat = space_direction(cat)
            cat, body, on_planet, target_food = is_planet_reached(cat, body, suit, planets, on_planet, target_food)
        else:  # On planet:
            target_food = foodcheck(planets, on_planet, body, target_food)
            cat.upward = norm(cat.pos[0] - planets[on_planet].pos)
            cat.pos[0] += cat.upward * (planets[on_planet].radius - mag(cat.pos[0] -
                                                                        planets[on_planet].pos)) + 0.75 * cat.upward
            cat, body, suit, target_food, score, on_planet = planet_direction(cat,
                                                                              body, suit, planets,
                                                                              target_food, score, on_planet)
            scene.caption = "Score:" + str(score + target_food)
            cat.forward = cat.forward.rotate(1 / (planets[on_planet].radius + 0.75), -cat.right())
            # for segment in body:
            #     segment.rotate(1 / (planets[on_planet].radius + 0.75), -cat.right())
# TODO Ovenstående løkke skal integreres in move_caterpillar. Her virker den kun hvis retningen ikke ændres.
# TODO Måske skal kroppen jævnligt nulstilles ligesom ved planetfall?

        move_caterpillar(cat, body, suit, on_planet, planets)
        sleep(sleep_time)


main()
