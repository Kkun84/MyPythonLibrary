class Linear:
    def __init__(self, start=1, end=0, end_step=10):
        self.start = start
        self.end = end
        self.end_step = end_step

        self.m = (end - start) / end_step
        self.count = 0
        self._set_epsilon()

    def _set_epsilon(self):
        self.epsilon = self.start + self.m * \
            self.count if self.count < self.end_step else self.end

    def step(self):
        self.count += 1
        self._set_epsilon()
        return self.epsilon

    def reset(self, count=0):
        self.count = count
        self._set_epsilon()
