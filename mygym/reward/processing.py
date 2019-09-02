from .core import BaseReward


class Processing(BaseReward):

    def __init__(self, class_, func):
        if not isinstance(class_, BaseReward):
            raise ValueError('not isinstance(self.class_, BaseReward)')
        self.class_ = class_
        self.func = func

    def reset(self, env, state):
        self.class_.reset(env, state)

    def __call__(self, env, state, done):
        reward = self.class_(env, state, done)
        reward = self.func(reward)
        return reward
