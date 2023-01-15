from typing import List
from collections import namedtuple
import time


class Point(namedtuple("Point", "x y")):
    def __repr__(self) -> str:
        return f'Point{tuple(self)!r}'


class Rectangle(namedtuple("Rectangle", "lower upper")):
    def __repr__(self) -> str:
        return f'Rectangle{tuple(self)!r}'

    def is_contains(self, p: Point) -> bool:
        return self.lower.x <= p.x <= self.upper.x and self.lower.y <= p.y <= self.upper.y

class Node:
    def __init__(self, location, left=None, right=None):
        self.location = location
        self.left = left
        self.right = right
    def __repr__(self):
        return f'{tuple(self)!r}'


class KDTree:
    """k-d tree"""

    def __init__(self):
        self._root = None
        self._n = 0

    def insert(self, p: List[Point]):
        for point in p:
            if self._root is None:
                self._root = Node(location=point, left=None, right=None)
                self._n += 1
                continue
            current = self._root
            depth = 0
            while current:
                axis = depth % 2
                if axis == 0:
                    if point.x < current.location.x:
                        if current.left is None:
                            current.left = Node(location=point, left=None, right=None)
                            self._n += 1
                            break
                        current = current.left
                    else:
                        if current.right is None:
                            current.right = Node(location=point, left=None, right=None)
                            self._n += 1
                            break
                        current = current.right
                else:
                    if point.y < current.location.y:
                        if current.left is None:
                            current.left = Node(location=point, left=None, right=None)
                            self._n += 1
                            break
                        current = current.left
                    else:
                        if current.right is None:
                            current.right = Node(location=point, left=None, right=None)
                            self._n += 1
                            break
                        current = current.right
                depth += 1


    def range(self, rectangle: Rectangle) -> List[Point]:
        """range query"""
        result = []
        def _range(node: Node, rectangle: Rectangle, depth: int):
            if node is None:
                return
            if rectangle.is_contains(node.location):
                result.append(node.location)
            axis = depth % 2
            if axis == 0:
                if rectangle.lower.x <= node.location.x:
                    _range(node.left, rectangle, depth + 1)
                if rectangle.upper.x >= node.location.x:
                    _range(node.right, rectangle, depth + 1)
            else:
                if rectangle.lower.y <= node.location.y:
                    _range(node.left, rectangle, depth + 1)
                if rectangle.upper.y >= node.location.y:
                    _range(node.right, rectangle, depth + 1)
        _range(self._root, rectangle, 0)
        return result


def range_test():
    points = [Point(7, 2), Point(5, 4), Point(9, 6), Point(4, 7), Point(8, 1), Point(2, 3)]
    kd = KDTree()
    kd.insert(points)
    result = kd.range(Rectangle(Point(0, 0), Point(6, 6)))
    assert sorted(result) == sorted([Point(2, 3), Point(5, 4)])


def performance_test():
    points = [Point(x, y) for x in range(1000) for y in range(1000)]

    lower = Point(500, 500)
    upper = Point(504, 504)
    rectangle = Rectangle(lower, upper)
    #  naive method
    start = int(round(time.time() * 1000))
    result1 = [p for p in points if rectangle.is_contains(p)]
    end = int(round(time.time() * 1000))
    print(f'Naive method: {end - start}ms')

    kd = KDTree()
    kd.insert(points)
    # k-d tree
    start = int(round(time.time() * 1000))
    result2 = kd.range(Rectangle(Point(500, 500),Point(504, 504)))
    end = int(round(time.time() * 1000))
    print(f'K-D tree: {end - start}ms')

    assert sorted(result1) == sorted(result2)


if __name__ == '__main__':
    range_test()
    performance_test()