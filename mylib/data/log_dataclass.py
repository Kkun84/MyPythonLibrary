import typing
import dataclasses as dc
import pandas as pd


def log_dataclass(_cls=None, *, init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False):

    def _log_dataclass(cls):

        def make_history(cls):

            def save_csv(self, path):
                data = pd.DataFrame(self.__dict__)
                data.to_csv(path, index=False)

            def load_csv(self, path):
                csv = pd.read_csv(path)
                assert set(self.__dict__.keys()) == set(csv.keys())
                for key, value in csv.items():
                    self.__dict__[key] = value.to_list()

            def append(self, **kwargs):
                for key in kwargs.keys():
                    self.__dict__[key].append(kwargs[key])

            namespace = dict(
                save_csv=save_csv,
                load_csv=load_csv,
                append=append,
            )
            return dc.make_dataclass(
                'History',
                [(i.name, typing.List[i.type], dc.field(default_factory=list))
                 for i in dc.fields(cls)],
                namespace=namespace
            )

        def push(self, init=True):
            assert all(type(i) != dc._MISSING_TYPE for i in dc.astuple(self))
            self.history.append(**dc.asdict(self))
            if init:
                self.init()

        def init(self, **kwarg):
            for key, value in self.__dataclass_fields__.items():
                if key in kwarg:
                    self.__dict__[key] = kwarg[key]
                elif type(value.default) != dc._MISSING_TYPE:
                    self.__dict__[key] = value.default
                elif type(value.default_factory) != dc._MISSING_TYPE:
                    self.__dict__[key] = value.default_factory()

        def wrap(*args, **kwargs):
            retval = cls(*args, **kwargs)
            retval.history = cls.History()
            return retval

        cls = dc.dataclass(cls, init=init, repr=repr, eq=eq,
                           order=order, unsafe_hash=unsafe_hash, frozen=frozen)
        cls.History = make_history(cls)
        cls.push = push
        cls.init = init
        return wrap

    if _cls is None:
        return _log_dataclass
    else:
        return _log_dataclass(_cls)


if __name__ == "__main__":
    @log_dataclass()
    class C:
        a: int
        b: int = 20
        c: typing.List[float] = dc.field(default_factory=list)

    y = C(-1)

    x = C(1)
    x.push()
    x.a = 2
    x.c.append(100)
    x.c.append(200)
    x.push()
    x.a = 4
    x.b = 4

    y.push()

    x.c.append(300)
    x.c.append(400)
    x.c.append(500)
    x.push()
    x.a = 8

    print(x)
    print(x.history)
    print(x.history.__class__)
    print()

    print(y)
    print(y.history)
    print(y.history.__class__)
    print()
