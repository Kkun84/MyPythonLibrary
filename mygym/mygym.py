import typing
import dataclasses
import collections

import random
import pandas as pd

import torch


@dataclasses.dataclass(frozen=True)
class Transition:
    state: torch.Tensor
    action: torch.Tensor
    next_state: torch.Tensor
    reward: torch.Tensor
    done: torch.Tensor

    def to_tuple(self):
        return dataclasses.astuple(self)

    def to_dict(self):
        return dataclasses.asdict(self)

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


@dataclasses.dataclass
class History:
    step: typing.List[int] = dataclasses.field(
        default_factory=list)
    lr: typing.List[float] = dataclasses.field(
        default_factory=list)
    epsilon: typing.List[float] = dataclasses.field(
        default_factory=list)
    reward: typing.List[float] = dataclasses.field(
        default_factory=list)
    loss: typing.List[float] = dataclasses.field(
        default_factory=list)
    update: typing.List[bool] = dataclasses.field(
        default_factory=list)
    report: typing.List[str] = dataclasses.field(
        default_factory=list)

    def append(self, **kwargs):
        for key in kwargs.keys():
            self.__dict__[key].append(kwargs[key])

    def to_dict(self):
        return dataclasses.asdict(self)

    def save_csv(self, path):
        src = pd.DataFrame(self.__dict__)
        src.to_csv(path, index=False)

    @staticmethod
    def load_csv(path):
        dst = pd.read_csv(path)
        dst = History(**dst.to_dict('list'))
        return dst

    @classmethod
    def buffer(cls):
        changes = {key: value.__args__[0]() for key, value in
                   cls.__annotations__.items()}
        replaced = dataclasses.replace(cls(), **changes)
        return replaced


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