class Exponential:
    def __init__(self, *, start, end, decay):
        self.start = start
        self.end = end
        self.decay = decay
        self.step = 0

    def __call__(self):
        epsilon = self.end + (
            self.start - self.end) * 2**(-self.step / self.decay)
        self.step += 1
        return epsilon

    def reset(self, step=0):
        self.step = step
