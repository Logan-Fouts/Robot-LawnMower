import math
import random


class Robot:
    """
    Basic Robot with direction, postition, and velocity.
    """

    def __init__(self, velocity=0.3):
        self.px = 0
        self.py = 0
        self.vx = 0.0
        self.vy = 0.0
        self.velocity = velocity

    def gen_rand_vector(self, scale):
        """
        Generates random direction as defined in the assignment.
        """
        angle = random.uniform(0, 2 * math.pi)
        vx = (self.velocity * scale) * math.cos(angle)
        vy = (self.velocity * scale) * math.sin(angle)
        return vx, vy
