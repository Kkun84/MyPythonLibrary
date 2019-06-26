import itertools
import numpy as np

import gym


class SquareField(gym.Env):
    def __init__(self, size=3, render_size=40, **kwargs):
        super().__init__()

        if 'kwargs' in kwargs:
            kwargs = kwargs['kwargs']

        self.__size = kwargs['size'] if 'size' in kwargs else size
        self.__render_size = kwargs['render_size'] if 'render_size' in kwargs else render_size
        self.__seed = None
        self.__position = None

        self.action_space = gym.spaces.Discrete(4)
        self.observation_space = gym.spaces.Discrete(2)
        self.reward_range = [-1.0, 1.0]

    def __observe(self):
        return self.__position.copy()

    def __is_done(self):
        return (self.__position < 0).any() or (self.__size <= self.__position).any()

    def __is_in_field(self):
        return (-1 <= self.__position).all() and (self.__position <= self.__size).all()

    def __get_reward(self):
        return 1.0 if not self.__is_done() else -1.0

    def reset(self):
        self.__position = np.array(
            [0, 0] if self.__seed is None else divmod(self.__seed, self.__size), dtype=int)
        observation = self.__observe()
        return observation

    def seed(self, seed=None):
        if not isinstance(seed, int):
            raise ValueError('not isinstance(seed, int).')
        self.__seed = seed

    def step(self, action):
        self.__position += [[1, 0], [0, -1], [-1, 0], [0, 1]][action]
        observation = self.__observe()
        reward = self.__get_reward()
        done = self.__is_done()
        return observation, reward, done, {}

    def render(self, mode='human', close=False):
        if mode == 'human':
            raise ValueError('Sorry, "human" is not yet supported.')

        elif mode == 'rgb_array':
            dst = np.zeros([self.__size + 2] * 2 + [3])
            for i in [0]:
                dst[[0, -1], :, i] = dst[:, [0, -1], i] = 0.5
            if self.__is_in_field():
                for i in [0, 1, 2]:
            for i in range(2):
                dst = dst.repeat(self.__render_size, axis=i)

        elif mode == 'ansi':
            dst = [['+'] * (self.__size + 2) for i in range(self.__size + 2)]
            for i, j in itertools.product(range(1, self.__size + 1), repeat=2):
                dst[i][j] = '0'
            if self.__is_in_field():
                dst[self.__position[1] + 1][self.__position[0] + 1] = '1'
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
