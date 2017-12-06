

from vpython import box, sphere, color, scene, vector, compound, sleep, cross, radians, text

box(pos=vector(0, 2, 0))

class Segment:
    def __init__(self, position=vector(0, 0, 0)):
        sphere(color=color.blue)
        sphere.pos = position
    # def move(self, displace=vector(1, 0, 0)):
    #     print(displace)
    #     print(type(self))
    #     print(type(self).pos)
    #     type(self).pos = displace


def main():
    ''' Main loop '''
    bodypart = Segment(vector(1, 0, 0))
    bodypart.pos = vector(3, 0, 0)
    # bodypart.pos = vector(1, 0, 0)
    # for dummy in range(5):
    #     bodypart = Segment(vector(dummy, 0, 0))
    #     larve.append(bodypart)
    # Segment.move(vector(1, 0, 0))

main()
