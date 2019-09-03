import numpy as np
from sklearn.cluster import DBSCAN


def dbscan_clustering(visit_points, max_distance, min_points):
    clusters = []
    np_points = []
    for vp in visit_points:
        np_points.append(vp['position'].to_np_point())
    np_points = np.array(np_points)
    dbscan_res = DBSCAN(
        eps=max_distance, min_samples=min_points).fit(np_points)
    for i in range(0, max(dbscan_res.labels_) + 1):
        clusters.append([])
    for ind, v in enumerate(visit_points):
        label = int(dbscan_res.labels_[ind])
        if label == -1:
            clusters.append([ind])
        else:
            clusters[label].append(ind)
    return clusters


class BaseConverter(object):
    decimal_digits = "0123456789"

    def __init__(self, digits):
        self.digits = digits

    def from_decimal(self, i):
        return self.convert(i, self.decimal_digits, self.digits)

    def to_decimal(self, s):
        return int(self.convert(s, self.digits, self.decimal_digits))

    def convert(number, fromdigits, todigits):
        # Based on http://code.activestate.com/recipes/111286/
        if str(number)[0] == '-':
            number = str(number)[1:]
            neg = 1
        else:
            neg = 0

        # make an integer out of the number
        x = 0
        for digit in str(number):
            x = x * len(fromdigits) + fromdigits.index(digit)

        # create the result in base 'len(todigits)'
        if x == 0:
            res = todigits[0]
        else:
            res = ""
            while x > 0:
                digit = x % len(todigits)
                res = todigits[digit] + res
                x = int(x / len(todigits))
            if neg:
                res = '-' + res
        return res
    convert = staticmethod(convert)


bin = BaseConverter('01')
hexconv = BaseConverter('0123456789ABCDEF')
base62 = BaseConverter(
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz'
)
base57 = BaseConverter(
    'ABCDEFGHJKLMNPQRSTUVWXYZ23456789abcdefghijkmnopqrstuvwxyz'
    # Base57 is essentially Base62, but with five characters removed
    # (I, O, l, 1, 0) because they are often mistaken for one another.
)
