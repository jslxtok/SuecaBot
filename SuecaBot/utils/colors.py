import hikari
import random


def get_color():
    color = hikari.Colour.of((random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)))
    return color