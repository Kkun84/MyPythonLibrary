from .core import BaseReward


class DifferenceReward(BaseReward):

    def __init__(self, class_):
        if not isinstance(class_, BaseReward):
            raise ValueError('not isinstance(self.class_, BaseReward)')
        self.class_ = class_
        self._pre_value = None

    def reset(self, env, state):
        self.class_.reset(env, state)
        self._pre_value = self.class_(env, state, False)

    def __call__(self, env, state, done):
        reward = self.class_(env, state, done)
        reward, self._pre_value = reward - self._pre_value, reward
        return reward
