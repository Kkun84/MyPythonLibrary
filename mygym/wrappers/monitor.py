import gym


class Monitor(gym.Wrapper):
    def __init__(self, env, mode):
        super().__init__(env)
        self._images = []
        self.mode = mode

    def step(self, action):
        observation, reward, done, info = self.env.step(action)
        self._record()
        return observation, reward, done, info

    def reset(self, **kwargs):
        self._flush()
        observation = self.env.reset(**kwargs)
        self._record()
        return observation

    @property
    def images(self):
        return tuple(self._images)

    def _flush(self):
        self._images = []

    def _record(self):
        image = self.env.render(self.mode)
        self._images.append(image)
