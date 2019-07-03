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


class BoxField(gym.Env):
    def __init__(self, shape=[32, 32], directions=8, reward=None, done=None, **kwargs):
        super().__init__()

        if 'kwargs' in kwargs:
            kwargs = kwargs['kwargs']
        shape = kwargs.get('shape', shape)[::-1]
        directions = kwargs.get('directions', directions)
        self._reward = kwargs.get('reward', reward)
        self._done = kwargs.get('done', done)

        if len(shape) != 2:
            raise ValueError('Set the length of "shape" to 2.')
        if directions not in [4, 8]:
            raise ValueError('The value of "directions" must be 4 or 8.')

        self._seed = None
        self._position = None
        self._position_prev = None
        self._map = np.zeros(shape, dtype=np.uint8)

        self.action_space = gym.spaces.Discrete(directions)
        self.observation_space = gym.spaces.Box(
            0, 0xff, shape=(*shape, 2), dtype=np.uint8)

    def _action(self, n):
        if not 0 <= n < self.action_space.n:
            raise ValueError('not 0 <= n < action_space.n')
        action = [[0, 1], [-1, 0], [0, -1], [1, 0],
                  [-1, 1], [-1, -1], [1, -1], [1, 1]][n]
        return action

    def _observe(self):
        position = np.zeros_like(self._map)
        position[tuple(self._position)] = 0xff
        observe = np.dstack([self._map, position]) / 0xff
        return observe

    def _get_reward(self):
        if self._reward is not None:
            reward = self._reward(self._position)
        else:
            reward = 0
        return reward

    def _is_done(self):
        if self._done is not None:
            done = self._done(self._position)
        else:
            done = False
        return done

    def reset(self):
        self._position = (
            self._map.shape * np.random.rand(2) if self._seed is None else
            np.array([self._seed // self._map.shape[1] % self._map.shape[0],
                      self._seed % self._map.shape[1]])
        ).astype(np.uint8)
        self._map = np.zeros_like(self._map, dtype=np.uint8)
        self._map[tuple(self._position)] = 0xff
        observation = self._observe()
        return observation

    def seed(self, seed=None):
        if not isinstance(seed, int):
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
        reward = self._get_reward()
        done = self._is_done()
        return observation, reward, done, {}

    def render(self, mode='human', close=False):
        if mode == 'human':
            raise ValueError('Sorry, "human" is not yet supported.')

        elif mode == 'rgb_array':
            rendered = np.dstack([0xff - self._map]*3)
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
            rendered[1:-1,  1:-1][1 <= self._map] = '[]'
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
    env = SquareField()
    print(env.reset())
    print(env.render('ansi'))
    for i in range(4):
        print(env.step(0))
        print(env.render('ansi'))

    print('#' * 20)

    env = BoxField([8, 4])
    env.seed(45)
    env.reset()
    print(env.render('ansi'))
    for i in range(4):
        print(env.step(0)[1:])
        print(env.render('ansi'))
