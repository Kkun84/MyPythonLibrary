from .core import BaseReward


class FinalReward(BaseReward):

    def __init__(self, class_):
        if not isinstance(class_, BaseReward):
            raise ValueError('not isinstance(self.class_, BaseReward)')
        self.class_ = class_

    def reset(self, env, state):
        self.class_.reset(env, state)

    def __call__(self, env, state, done):
        reward = self.class_(env, state, done) if done else 0
        return reward
