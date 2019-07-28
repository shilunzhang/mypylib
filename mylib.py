import math
import numpy as np

def mean(seq):
    if not len(seq):
        return None
    return sum(seq)/float(len(seq))


def std(seq):
    if not len(seq):
        return None
    m = sum(seq)/float(len(seq))
    return math.sqrt(sum([(e-m)**2 for e in seq])/float(len(seq)-1))


def sem(seq):
    if not len(seq):
        return None
    m = sum(seq)/float(len(seq))
    return math.sqrt(sum([(e-m)**2 for e in seq])/float(len(seq)-1))/math.sqrt(float(len(seq)))


def pearsonr(seq1, seq2):
    mu1, mu2 = mean(seq1), mean(seq2)
    r = mean([(e1-mu1)*(e2-mu2) for e1, e2 in zip(seq1, seq2)])/(std(seq1)*std(seq2))
    return r


def herfindahl_index(seq):
    total = sum(seq)
    return sum([(e/float(total))**2 for e in seq])


def precision(seq1, seq2, num):
    s1 = sorted(enumerate(seq1, 1), key=lambda x: x[1], reverse=True)[:num]
    s2 = sorted(enumerate(seq2, 1), key=lambda x: x[1], reverse=True)[:num]
    s1 = set([e[0] for e in s1])
    s2 = set([e[0] for e in s2])
    return len(s1&s2)/float(num)


def average_over_logbin(l):
# 'average_over_logbin(l)' average the elements in list 'l' in each 'log10' bin
#
# return: tuple list 'avged_l', i.e. elements are like '(mean, population)',
#
# 'mean' is the mean of elements fall in a bin,
#
# 'population' is the average number of elements fall in 1 unit length interval of a bin,
# i.e. total number of elements fall in the bin devided by the interval length.
    import statistics # new in python3.4

    # sort list l
    l = sorted(l[:])
    interv_power = 0
    interv1, interv2 = 1., 2.
    p1, p2 = 0, 0
    avged_l = []
    for _ in l:
        if l[p2]<interv2 and l[p1]>interv1:
            p2 += 1
        else:
            if p2>p1:
                avged_l.append((statistics.mean(l[p1:p2]), (p2-p1)/10**(interv_power)))
            p1 = p2
            p2 += 1
            interv_power = math.floor(math.log10(l[p1]))
            interv1 = math.floor(l[p1]/(10**interv_power))*(10**interv_power)
            interv2 = (math.floor(l[p1]/(10**interv_power))+1)*(10**interv_power)
    return avged_l


def average_over_xbins(x, y, bins_edge):
    assert len(x) == len(y), 'x and y have different dimension.'
    x_in_each_bin, y_in_each_bin = [], []
    for i in range(len(bins_edge) - 1):
        x_in_each_bin.append([])
        y_in_each_bin.append([])
    bin_index = np.digitize(x, bins_edge) - 1
    for i in range(len(x)):
        x_in_each_bin[bin_index[i]].append(x[i])
        y_in_each_bin[bin_index[i]].append(y[i])
    meanx_in_each_bin, meany_in_each_bin, yerr_in_each_bin = [], [], []
    for i in range(len(x_in_each_bin)):
        assert len(x_in_each_bin[i]) == len(y_in_each_bin[i]), 'x and y have different length in bin {0}'.format(i)
        if len(x_in_each_bin[i]) > 1:
            meanx_in_each_bin.append(np.mean(x_in_each_bin[i]))
            meany_in_each_bin.append(np.mean(y_in_each_bin[i]))
            yerr_in_each_bin.append(sem(y_in_each_bin[i]))

    return meanx_in_each_bin, meany_in_each_bin, yerr_in_each_bin