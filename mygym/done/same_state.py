from .core import BaseDone


class SameStateDone(BaseDone):

    def __init__(self):
        self._state_list = None

    def reset(self, env, state):
        self._state_list = [state]

    def __call__(self, env, state):
        if any((state == s).all() for s in self._state_list[::-1]):
            done = True
        else:
            done = False
            self._state_list.append(state)
        return done
