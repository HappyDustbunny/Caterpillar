''' Graphics for catarpillar '''

from vpython import *

def make_head():
    ''' Make caterpillar head '''
    head_ball = sphere(color=color.orange)
    left_eye = sphere(pos=vector(0.5, 0.5, -0.4), radius=0.35)
    right_eye = sphere(pos=vector(0.5, 0.5, 0.4), radius=0.35)
    left_pupil = sphere(pos=vector(0.6, 0.56, -0.42), radius=0.25, color=color.black)
    rigth_pupil = sphere(pos=vector(0.6, 0.56, 0.42), radius=0.25, color=color.black)
    head = compound([head_ball, left_eye, right_eye, left_pupil, rigth_pupil])
    return head

def make_helmet():
    ''' Make caterpillar head '''
    helmet = sphere(pos=vector(.1, 0.15, 0), radius=1.2, opacity=0.3)
    return helmet

def make_body(caterpillar_pos, head):
    ''' Make caterpillar body '''
    body = [head]
    for increment in range(1, 5):
        body_sphere = sphere(pos=caterpillar_pos[increment], color=color.blue)
        left_foot = sphere(pos=caterpillar_pos[increment] +
                           vector(0, -0.6, -0.5), radius=0.3, color=color.orange)
        right_foot = sphere(pos=caterpillar_pos[increment] +
                            vector(0, -0.6, 0.5), radius=0.3, color=color.orange)
        body_segment = compound([body_sphere, left_foot, right_foot])
        body.append(body_segment)
    return body

def make_suit(caterpillar_pos, helmet):
    ''' Make caterpillar suit '''
    suit = [helmet]
    for increment in range(1, 5):
        body_sphere = sphere(pos=caterpillar_pos[increment], radius=1.1,
                             color=color.white)
        left_foot = sphere(pos=caterpillar_pos[increment] +
                           vector(0, -0.6, -0.5), radius=0.4, color=color.black)
        right_foot = sphere(pos=caterpillar_pos[increment] +
                            vector(0, -0.6, 0.5), radius=0.4, color=color.black)
        body_segment = compound([body_sphere, left_foot, right_foot])
        suit.append(body_segment)
    return suit

def make_planets(number_of_planets):
    ''' Makes planets '''
    planets = []
    planet = sphere(pos=vector(50, -1, 0), radius=20, texture=textures.wood_old) # Test planet. Remove when reinstating all planets
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
            food_pos = norm(vector(random() - 0.5, random() - 0.5,
                                   random() - 0.5))*radius + planet.pos
            food = sphere(pos=food_pos, texture=textures.rock)
            foods.append(food)
        planet.food = foods
    return
