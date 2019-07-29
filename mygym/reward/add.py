from .core import BaseReward


class Add(BaseReward):

    def __init__(self, class_, value):
        if not isinstance(class_, BaseReward):
            raise ValueError('not isinstance(self.class_, BaseReward)')
        self.class_ = class_
        self.value = value

    def reset(self, env, state):
        self.class_.reset(env, state)

    def __call__(self, env, state, done):
        reward = self.class_(env, state, done) + self.value
        return reward
