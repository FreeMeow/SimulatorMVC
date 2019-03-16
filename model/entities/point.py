class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return (round(self.x) == round(other.x)) and (round(self.y) == round(other.y))

    def __ne__(self, other):
        return not (self == other)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __truediv__(self, other):
        return Point(self.x / other, self.y / other)

    def __mul__(self, other):
        return Point(self.x * other, self.y * other)

    def __str__(self):
        return "({},{})".format(self.x, self.y)

    def __hash__(self):
        return "({},{})".format(self.x, self.y).__hash__()

    def to_np_point(self):
        return [self.x, self.y]
