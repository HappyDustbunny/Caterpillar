''' Snake clone '''

from vpython import box, sphere, color, scene, vector, compound, sleep, cross, radians

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

def direction(event):
    ''' Capture keyboard inupt and choose new direction and new orientation '''
    # value = event.key
    global keyevent
    keyevent = event.key



def main():
    ''' Main loop '''
    scene.bind('keydown', direction)

    caterpillar_pos = []
    for dummy in range(5):
        caterpillar_pos.append(vector(-dummy, 0, 0))

    head = make_head()
    body = make_body(caterpillar_pos)

    forward = vector(1, 0, 0)
    up = vector(0, 1, 0)
    turn = False
    turn_axis = vector(0, 1, 0)

    '''Listening for key presses'''
    global keyevent

    
    d_t = 0.4

    while True:
        if keyevent == 'a':
            forward = -cross(forward, up)
            turn = True
            turn_axis = up
        if keyevent == 'd':
            forward = cross(forward, up)
            turn = True
            turn_axis = -up
        if keyevent == 'w':
            forward, up = up, -forward
            turn = True
            turn_axis = cross(forward, up)
        if keyevent == 's':
            forward, up = -up, forward
            turn = True
            turn_axis = -cross(forward, up)
        keyevent = ''

        old_caterpillar_pos = caterpillar_pos[:]
        caterpillar_pos[0] += forward
        head.pos = caterpillar_pos[0]
        # sleep(d_t)
        if turn:
            head.rotate(angle=radians(90), axis=turn_axis)
        for num, segment in enumerate(body):
            segment.pos = old_caterpillar_pos[num]
            if turn:
                segment.rotate(angle=radians(90), axis=turn_axis)
            caterpillar_pos[num + 1] = old_caterpillar_pos[num]
            # sleep(d_t)
        turn = False
        sleep(d_t)
    # for _ in range(20):
    #     for segment in body:
    #         for _ in range(5):
    #             segment.pos.x += .1
    #             sleep(0.001)


kasse = box()

main()
