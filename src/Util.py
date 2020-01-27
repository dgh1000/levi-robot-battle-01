import math
import random
from PyQt5.QtCore import QPointF

ARENA_SIZE = 600
BALL_RADIUS = 50
AMOUNT_OF_BALLS = 10

def length(a):
    return math.sqrt(a.x() * a.x() + a.y() * a.y() )

def component(a, b):
    "component of a in the direction of b"
    dp = dotProduct(a, b)   
    return dp * b / (length(b) ** 2)

def dotProduct(a, b):
    return a.x() * b.x() + a.y() * b.y()

def bouncing(p1, v1, p2, v2):
    l1 = p2 - p1
    l2 = p1 - p2
    v1_p = component(v1, l1)
    v1_o = v1 - v1_p
    v2_p = component(v2, l2)
    v2_o = v2 - v2_p
    v1_new = v2_p + v1_o
    v2_new = v1_p + v2_o
    if dotProduct(v1_p - v2_p, l1) < 0:
        return v1, v2
    return v1_new, v2_new

def randomPos():
    def r():
        a = ARENA_SIZE/2
        return random.uniform(-a + 50, a - 50)
    return QPointF(r(), r())

