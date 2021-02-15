#
# this code calculates percentage of files still found in the cache after one server failure
# it implements 3 different algorithms to distribute files over servers
# algo 1. simple filehash % nservers
# algo 2. divides all hash space by number of servers.
# algo 3. each server gets equal fraction but chunks are not continuous in hash space
#         eg.
# nservers: 4     will have  5 pieces
# serv: 1, 1/4,
# serv: 3, 1/6,
# serv: 2, 1/4,
# serv: 3, 1/12,
# serv: 0, 1/4
#
# Results are:
# algo1: 49927, 33690, 25267, 20038, 16862, 14315, 12409, 11171, 10045 - more servers worse it is
# algo2: 50136, 50023, 50144, 50248, 49966, 50317, 49967, 50066, 50039 - recovers half independently how many servers
# algo3: 50020, 66644, 75118, 79996, 83030, 85846, 87653, 88849, 90042 - fraction of lost files is 1-1/nservers.

import random
# for fractional numbers arithmetics
from fractions import Fraction

MAX_HASH = pow(2, 32)
FILES_TO_SIMULATE = 100000
MAX_SERVERS = 10

# needed only for algo3


def generate_fraction(servs):
    res = [[(0, Fraction(1, 1))]]  # server index, fraction
    for i in range(1, servs):
        rn = []
        fraction_to_subtract = {}
        for si in range(0, i):
            fraction_to_subtract[si] = Fraction(1, i * (i + 1))
        # print('to subtract per server:', fraction_to_subtract)
        # take a part from each previous server.
        for piece in res[i - 1]:

            # print('starting:', piece, end='\t')
            si = piece[0]
            fr = piece[1]

            if (not fr > fraction_to_subtract[si]):
                # print('giving it all to nfew server')
                rn.append([i, fr])
                fraction_to_subtract[si] -= fr
            else:
                if si % 2:  # makes similar parts sit together
                    # rewriting old one but now its fraction decreases
                    rn.append([si, fr - fraction_to_subtract[si]])
                    # adding new one
                    rn.append([i, fraction_to_subtract[si]])
                else:
                    rn.append([i, fraction_to_subtract[si]])
                    rn.append([si, fr - fraction_to_subtract[si]])
                fraction_to_subtract[si] = Fraction(0, 1)

        # connect pieces siting next to each other
        r = []
        p = [-1, Fraction(1, 1)]
        # print('rn:', rn)
        for j in rn:
            if j[0] != p[0]:
                r.append(j)
            else:
                r[-1] = ([j[0], j[1] + p[1]])
            p = j
        # print(r)
        res.append(r)
    return res


fractions = generate_fraction(MAX_SERVERS)
ranges = []
for s, f in enumerate(fractions):
    ul = 0
    rang = []
    for i in f:
        ul += i[1]
        rang.append([i[0], ul])
    # print(rang)
    ranges.append(rang)
    print('servers:', s + 1, '\tpieces:', len(f),
          '\nfractions:', f, '\nranges:', rang)


def algo1(fm, servers):
    return fm % (servers+1)


def algo2(fm, servers):
    fr = (MAX_HASH - 1) / (servers+1)
    return int(fm / fr)


def algo3(fm, servers):
    ff = Fraction(fm, MAX_HASH)
    # print(ranges[servers])
    for i in ranges[servers]:
        if ff < i[1]:
            # print(ff, i, float(ff))
            return i[0]


print('-' * 50)

# this will be our result. For how many of the files initial and after adding one more server
# will be the same
matches = [0] * (MAX_SERVERS - 1)

# loop over files
for files in range(FILES_TO_SIMULATE):
    fm = random.randint(0, MAX_HASH)

    # loop over all possible numers of servers and find on which of them file will finish.
    endup = []
    for servers in range(0, MAX_SERVERS):
        s = algo3(fm, servers)
        endup.append(s)
    # print('-' * 30)
    # print(fm, endup)

    # summ up situations where n-th+1 server == n-th server
    l = endup[0]
    for i, e in enumerate(endup[1:]):
        if e == l:
            matches[i] += 1
        l = e

print('=' * 50)
print('reused from total of', FILES_TO_SIMULATE, 'files')
print(matches)
