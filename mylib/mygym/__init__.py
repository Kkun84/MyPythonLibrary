from .mygym import Transition, History, ReplayMemory, Epsilon
from . import wrappers
from . import envs

from gym.envs.registration import register


register(
    id='SquareField-v0',
    entry_point='envs:SquareField',
)
