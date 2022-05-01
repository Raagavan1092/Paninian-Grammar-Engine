def flatten_and_set(l, ltypes=(list, tuple)):
    ltype = type(l)
    i, l, newl = 0, list(l), []
    while i < len(l):
        while isinstance(l[i], ltypes):
            if not l[i]:
                l.pop(i)
                i -= 1
                break
            else:
                l[i:i + 1] = l[i]
        i += 1

    [newl.append(j) for j in l if j not in newl]
    return ltype(newl)
