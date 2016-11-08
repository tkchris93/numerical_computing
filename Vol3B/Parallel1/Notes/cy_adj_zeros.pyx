cimport cython

def adjacent_zeros(double[:] mylist):
    adjacent = []
    cdef int i = 0
    cdef int n = mylist.size
    while i < n:
        if mylist[i] != 0:
            i += 1
        else:
            while mylist[i] == 0:
                adjacent.append(i)
                i += 1
                if i == n:
                    return adjacent
    return adjacent
