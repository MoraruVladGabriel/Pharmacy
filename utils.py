def mySort(iterable, *, key=lambda x: x, reverse=False):
    swapped = True
    while swapped:
        swapped = False
        for i in range(len(iterable) - 1):
            if key(iterable[i]) > key(iterable[i + 1]):
                iterable[i], iterable[i + 1] = iterable[i + 1], iterable[i]
                swapped = True

    if not reverse:
        return iterable
    else:
        return list(reversed(iterable))
