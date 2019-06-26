from .mygym import Transition, History, ReplayMemory, Epsilon
from . import wrappers
from . import envs

import os
import sys


path = os.path.dirname(__file__) + '/envs'
for p in sys.path:
    if not (p and path.startswith(p)):
        continue
    path = path[len(p) + 1:].replace('/', '.')

    from gym.envs.registration import register

    register(
        id='SquareField-v0',
        entry_point=path + ':SquareField'
    )

    del register
    break
