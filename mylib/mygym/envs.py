import itertools
import numpy as np

import gym


class SquareField(gym.Env):
    def __init__(self, size=3, render_size=40, **kwargs):
        super().__init__()

        if 'kwargs' in kwargs:
            kwargs = kwargs['kwargs']

        self._size = kwargs['size'] if 'size' in kwargs else size
        self._render_size = kwargs['render_size'] if 'render_size' in kwargs else render_size
        self._seed = None
        self._position = None

        self.action_space = gym.spaces.Discrete(4)
        self.observation_space = gym.spaces.Discrete(2)
        self.reward_range = [-1.0, 1.0]

    def _observe(self):
        return self._position.copy()

    def _is_done(self):
        return (self._position < 0).any() or (self._size <= self._position).any()

    def _is_in_field(self):
        return (-1 <= self._position).all() and (self._position <= self._size).all()

    def _get_reward(self):
        return 1.0 if not self._is_done() else -1.0

    def reset(self):
        self._position = (
            np.random.randint(self._size, size=2) if self._seed is None else
            np.array(divmod(self._seed, self._size), dtype=int)
        )
        observation = self._observe()
        return observation

    def seed(self, seed=None):
        if not isinstance(seed, int):
            raise ValueError('not isinstance(seed, int).')
        self._seed = seed

    def step(self, action):
        self._position += [[1, 0], [0, -1], [-1, 0], [0, 1]][action]
        observation = self._observe()
        reward = self._get_reward()
        done = self._is_done()
        return observation, reward, done, {}

    def render(self, mode='human', close=False):
        if mode == 'human':
            raise ValueError('Sorry, "human" is not yet supported.')

        elif mode == 'rgb_array':
            dst = np.zeros([self._size + 2] * 2 + [3], dtype=int)
            for i in [0]:
                dst[[0, -1], :, i] = dst[:, [0, -1], i] = 0x80
            if self._is_in_field():
                for i in [0, 1, 2]:
                    dst[self._position[1] + 1, self._position[0] + 1, i] = 0xff

            for i in range(2):
                dst = dst.repeat(self._render_size, axis=i)

        elif mode == 'ansi':
            dst = [['+'] * (self._size + 2) for i in range(self._size + 2)]
            for i, j in itertools.product(range(1, self._size + 1), repeat=2):
                dst[i][j] = '0'
            if self._is_in_field():
                dst[self._position[1] + 1][self._position[0] + 1] = '1'
            dst = '\n'.join([''.join(d) for d in dst])

        else:
            raise ValueError(
                'The value of "mode" is invalid. '
                'Must be "human", "rgb_array" or "ansi".'
            )

        return dst

    def close(self):
        return


if __name__ == "__main__":
    env = SquareField()
    print(env.reset())
    print(env.render('ansi'))
    for i in range(4):
        print(env.step(0))
        print(env.render('ansi'))
