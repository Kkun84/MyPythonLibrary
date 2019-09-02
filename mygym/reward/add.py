from .core import BaseReward


class Add(BaseReward):

    def __init__(self, *reward_class):
        for c in reward_class:
            if not isinstance(c, BaseReward):
                raise ValueError(
                    f'{c} is not an instance of a subclass of BaseReward.')
        self.reward_class = reward_class

    def reset(self, env, state):
        for c in self.reward_class:
            c.reset(env, state)

    def __call__(self, env, state, done):
        reward = 0
        for c in self.reward_class:
            reward += c(env, state, done)
        return reward
