import typing
import dataclasses as dc

import pandas as pd


@dc.dataclass
class History:
    step: typing.List[int] = dc.field(
        default_factory=list)
    lr: typing.List[float] = dc.field(
        default_factory=list)
    epsilon: typing.List[float] = dc.field(
        default_factory=list)
    reward: typing.List[float] = dc.field(
        default_factory=list)
    loss: typing.List[float] = dc.field(
        default_factory=list)
    update: typing.List[bool] = dc.field(
        default_factory=list)
    report: typing.List[str] = dc.field(
        default_factory=list)

    def append(self, **kwargs):
        for key in kwargs.keys():
            self.__dict__[key].append(kwargs[key])

    def to_dict(self):
        return dc.asdict(self)

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
        replaced = dc.replace(cls(), **changes)
        return replaced
