import abc


class BaseDone(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def reset(self, env, state):
        raise NotImplementedError()

    @abc.abstractmethod
    def __call__(self, env, state):
        raise NotImplementedError()


class BaseReward(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def reset(self, env, state):
        raise NotImplementedError()

    @abc.abstractmethod
    def __call__(self, env, state, done):
        raise NotImplementedError()
