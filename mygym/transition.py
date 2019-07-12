import random

import collections
import dataclasses as dc

import torch


@dc.dataclass(frozen=True)
class Transition:
    state: torch.Tensor
    action: torch.Tensor
    next_state: torch.Tensor
    reward: torch.Tensor
    done: torch.Tensor

    def to_tuple(self):
        return dc.astuple(self)

    def to_dict(self):
        return dc.asdict(self)

    @classmethod
    def from_transitions(cls, transitions):
        """Transitionインスタンス配列をまとめたインスタンスを返す

        Args:
            transitions (list[Transition]): 要素がTransitionインスタンスの配列

        Returns:
            Transition: Transitionのインスタンス
        """
        retval = cls(*zip(*[
            [t.__dict__[key] for key in cls.__dataclass_fields__.keys()]
            for t in transitions
        ]))
        return retval


class ReplayMemory(collections.UserList):
    def __init__(self, capacity, batch_size=None):
        super().__init__()
        self._capacity = capacity
        self._batch_size = batch_size

        self._latest = 0

    @property
    def capacity(self):
        return self._capacity

    @property
    def batch_size(self):
        return self._batch_size

    @batch_size.setter
    def batch_size(self, batch_size):
        self._batch_size = batch_size

    @property
    def latest(self):
        return self[self._latest - 1]

    def append(self, data):
        if len(self) < self._capacity:
            super().append(data)
        else:
            self[self._latest] = data
        self._latest += 1
        if self._latest >= self._capacity:
            self._latest = 0

    def sample(self, batch_size=None):
        if batch_size is None:
            batch_size = self._batch_size
        if batch_size is None:
            raise ValueError('"batch_size" must be int, but It was None.')
        dst = random.sample(self, batch_size)
        return dst

    def __call__(self, batch_size=None):
        return self.sample(batch_size)
