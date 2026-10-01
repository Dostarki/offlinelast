import math
import random
from world import free


def spawn_position(game):
    # All new lives start in the permanent central sanctuary.
    points = [(0, 0), (7, 0), (-7, 0), (0, 7), (0, -7), (5, 5), (-5, 5), (5, -5), (-5, -5)]
    random.shuffle(points)
    for x, z in points:
        if not free(x, z):
            continue
        if any(p['hp'] > 0 and math.hypot(p['x']-x, p['z']-z) < 10 for p in game.players.values()):
            continue
        if any(e['hp'] > 0 and math.hypot(e['x']-x, e['z']-z) < 20 for e in game.zombies.values()):
            continue
        if any(e['hp'] > 0 and math.hypot(e['x']-x, e['z']-z) < 65 for e in game.bosses.values()):
            continue
        return x, z
    # A crowded sanctuary can share a spawn cell; it remains enemy-free.
    return next((p for p in points if free(*p)), (0, 0))
