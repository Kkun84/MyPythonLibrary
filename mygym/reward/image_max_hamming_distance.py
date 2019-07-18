import numpy as np

from .core import BaseReward


class ImageMaxHammingDistanceReward(BaseReward):

    def __init__(self, target, mode):
        self.target = target

        if mode is 'sum':
            self.func = np.sum
        elif mode is 'mean':
            self.func = np.mean
        else:
            raise ValueError('mode must be "sum" or "mean".')

    def reset(self, env, state):
        pass

    def __call__(self, env, state, done):
        reward = state[0] != self.target
        reward = self.func(reward, axis=(1, 2))
        reward = -reward.min()
        return reward
