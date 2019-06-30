def ljust(src, n, fillchar=' '):
    dst = str(src).ljust(n)[:n]
    return dst


def all_index(array, value):
    index = [-1]
    while value in array[index[-1] + 1:]:
        index.append(array.index(value, index[-1] + 1))
    index.pop(0)
    return index


def flatten(src):
    dst = []
    for s in src:
        if isinstance(s, (tuple, list)):
            for s_ in flatten(s):
                dst.append(s_)
        else:
            dst.append(s)
    dst = tuple(dst)
    return dst


def mean(x):
    x = flatten(x)
    x = sum(x) / len(x)
    return x


def multiple(src, *func):
    if hasattr(src, '__iter__'):
        dst = []
        for i in src:
            dst.append(multiple(i, *func))
    else:
        dst = src
        for f in func:
            dst = f(dst)
    return dst


def to_str(src, n=5, sep=', '):
    if hasattr(src, '__iter__') and not isinstance(src, str):
        dst = '['
        for s in src:
            dst += to_str(s, n)
            dst += sep
        if len(src) > 0:
            dst = dst[:-len(sep)]
        dst += ']'
    else:
        if isinstance(src, float):
            dst = ljust(f"{src:f}", n) if 'e' in str(
                src) else ljust(str(src), n)
        elif isinstance(src, bool):
            dst = ljust(str(src), 5)
        elif src is None:
            dst = ''
        else:
            dst = ljust(str(src), n)
    return dst
