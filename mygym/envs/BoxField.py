import numpy as np

import gym
import gym.spaces

from mygym.done import BaseDone
from mygym.reward import BaseReward


class Done(BaseDone):

    def reset(self, env, state):
        pass

    def __call__(self, env, state):
        return False


class Reward(BaseReward):

    def reset(self, env, state):
        pass

    def __call__(self, env, state, done):
        return 0


class BoxField(gym.Env):
    def __init__(self, shape=[32, 32], directions=8, reward=None, done=None, **kwargs):
        super().__init__()

        if 'kwargs' in kwargs:
            kwargs = kwargs['kwargs']
        shape = kwargs.get('shape', shape)
        directions = kwargs.get('directions', directions)

        self._reward = kwargs.get('reward', reward)
        if self._reward is None:
            self._reward = Reward()
        elif not isinstance(self._reward, BaseReward):
            raise ''

        self._done = kwargs.get('done', done)
        if self._done is None:
            self._done = Done()
        elif not isinstance(self._done, BaseDone):
            raise ''

        if len(shape) != 2:
            raise ValueError('Set the length of "shape" to 2.')
        if directions not in [4, 5, 8, 9]:
            raise ValueError(
                'The value of "directions" must be 4 or 5 or 8 or 9.')

        self._seed = None
        self._start = None
        self._position = None
        self._position_prev = None
        self._map = np.zeros(shape, dtype=np.uint8)

        self.action_space = gym.spaces.Discrete(directions)
        self.observation_space = gym.spaces.Box(
            0, 0xff, shape=(*shape, 2), dtype=np.uint8)

    def _action(self, n):
        if not 0 <= n < self.action_space.n:
            raise ValueError('not 0 <= n < action_space.n')
        action = {
            4: [[0, 1], [-1, 0], [0, -1], [1, 0]],
            5: [[0, 1], [-1, 0], [0, -1], [1, 0], [0, 0]],
            8: [[0, 1], [-1, 1], [-1, 0], [-1, -1],
                [0, -1], [1, -1], [1, 0], [1, 1]],
            9: [[0, 1], [-1, 1], [-1, 0], [-1, -1],
                [0, -1], [1, -1], [1, 0], [1, 1], [0, 0]],
        }[self.action_space.n][n]
        return action

    def _observe(self):
        position = np.zeros_like(self._map)
        position[tuple(self._position)] = 0xff
        observe = np.array([self._map, position]) / 0xff
        return observe

    def reset(self):
        if self._seed is None:
            self._position = (
                self._map.shape * np.random.rand(2)).astype(np.uint8)
        elif hasattr(self._seed, '__iter__'):
            self._position = np.array(self._seed).astype(np.uint8)
        elif not isinstance(self._seed, int):
            self._position = np.array([
                self._seed // self._map.shape[1] % self._map.shape[0],
                self._seed % self._map.shape[1]]).astype(np.uint8)

        self._start = self._position
        self._map = np.zeros_like(self._map, dtype=np.uint8)
        self._map[tuple(self._position)] = 0xff

        observation = self._observe()
        self._done.reset(self, observation)
        self._reward.reset(self, observation)

        return observation

    def seed(self, seed=None):
        if hasattr(seed, '__iter__'):
            if not len(seed) == 2:
                raise ValueError('not len(seed) == 2.')
        elif not isinstance(seed, int):
            raise ValueError('not isinstance(seed, int).')
        self._seed = seed

    def step(self, action):
        self._position_prev = self._position
        self._position = self._position + self._action(action)
        if (0 <= self._position).all() and (self._position < self._map.shape).all():
            self._map[tuple(self._position)] = 0xff
        else:
            self._position = self._position_prev
        observation = self._observe()
        done = self._done(self, observation)
        reward = self._reward(self, observation, done)
        return observation, reward, done, {}

    def render(self, mode='human', close=False):
        if mode == 'human':
            raise ValueError('Sorry, "human" is not yet supported.')

        elif mode == 'rgb_array':
            rendered = np.full([*self._map.shape, 3], 0xff)
            x, y = np.meshgrid(*[np.arange(i) for i in rendered.shape[:2]])
            rendered[x % 4 == 3] = 0xe0
            rendered[y % 4 == 3] = 0xe0
            rendered[self._map > 0] = [0] * 3
            rendered[tuple(self._start)] = [0, 0, 0xff]
            rendered[tuple(self._position)] = [0xff, 0, 0]

        elif mode == 'ansi':
            y, x = self._map.shape
            rendered = np.full([y + 2, x + 2], '  ')
            rendered[[0, -1], 1:-1] = '──'
            rendered[1:-1, [0, -1]] = '│'
            rendered[0, 0] = '┌'
            rendered[0, -1] = '┐'
            rendered[-1, 0] = '└'
            rendered[-1, -1] = '┘'
            rendered[1:-1, 1:-1][1 <= self._map] = '[]'
            rendered[1:-1, 1:-1][tuple(self._position)] = '<>'
            rendered = '\n'.join([''.join(i) for i in rendered])

        else:
            raise ValueError(
                'The value of "mode" is invalid. '
                'Must be "human", "rgb_array" or "ansi".'
            )

        return rendered

    def close(self):
        return


if __name__ == "__main__":
    env = BoxField([6, 8], 9)
    env.seed(34)
    env.reset()
    print(env.render('ansi'))
    for i in range(9):
        print(env.step(i)[1:])
        print(env.render('ansi'))
