from .SquareField import SquareField
from .BoxField import BoxField


def _register_myenvs():
    import os
    import sys
    from gym.envs.registration import register

    path = os.path.dirname(__file__)
    for p in sys.path:
        if not (p and path.startswith(p)):
            continue
        path = path[len(p) + 1:].replace('/', '.')

        register(
            id='SquareField-v0',
            entry_point=path + ':SquareField'
        )

        register(
            id='BoxField-v0',
            entry_point=path + ':BoxField'
        )


_register_myenvs()
del _register_myenvs
