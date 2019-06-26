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

