def ljust(src, n, fillchar=' '):
    dst = str(src).ljust(n)[:n]
    return dst


def all_index(array, value):
    index = [-1]
    while value in array[index[-1] + 1:]:
        index.append(array.index(value, index[-1] + 1))
    index.pop(0)
    return index
