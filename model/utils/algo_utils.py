import numpy as np
from sklearn.cluster import DBSCAN
from collections import defaultdict
import sys


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

# Agglomerative Hierarchical Clustering


def AHC(distance_matrix, cluster_num, original_cluster):

    clusters = [[i] for i in original_cluster]
    # find closest clusters and unify them
    while len(clusters) > cluster_num:
        min_distance = float("inf")
        chosen_one = None
        chosen_two = None
        for cluster1 in clusters:
            for cluster2 in clusters:
                if cluster1 == cluster2:
                    continue
                cluster_dist = clusterDistance(cluster1, cluster2, distance_matrix)
                if cluster_dist < min_distance:
                    min_distance = cluster_dist
                    chosen_one = cluster1
                    chosen_two = cluster2
        for number in chosen_two:
            chosen_one.append(number)
        clusters.remove(chosen_two)
    return clusters


def clusterDistance(cluster1, cluster2, matrix):
    max = 0
    for i in cluster1:
        for j in cluster2:
            if matrix[i][j] > max:
                max = matrix[i][j]
    return max

    # if condition not reached, repeat


def combinations(number, length):
    combos = []
    for i in range(0, number):
        array = [i]
        combos.append(array)
    num = length
    for j in range(0, length-1):
        new_combos = []
        for combo in combos:
            for i in range(0, number):
                new_combos.append(combo+[i])
        combos = new_combos
    return combos

# def spatial_entropy(distance_matrix):


class Heap():

    def __init__(self):
        self.array = []
        self.size = 0
        self.pos = []

    def newMinHeapNode(self, v, dist):
        minHeapNode = [v, dist]
        return minHeapNode

    # A utility function to swap two nodes of
    # min heap. Needed for min heapify
    def swapMinHeapNode(self, a, b):
        t = self.array[a]
        self.array[a] = self.array[b]
        self.array[b] = t

    # A standard function to heapify at given idx
    # This function also updates position of nodes
    # when they are swapped. Position is needed
    # for decreaseKey()
    def minHeapify(self, idx):
        smallest = idx
        left = 2 * idx + 1
        right = 2 * idx + 2

        if left < self.size and self.array[left][1] < self.array[smallest][1]:
            smallest = left

        if right < self.size and self.array[right][1] < self.array[smallest][1]:
            smallest = right

        # The nodes to be swapped in min heap
        # if idx is not smallest
        if smallest != idx:

            # Swap positions
            self.pos[self.array[smallest][0]] = idx
            self.pos[self.array[idx][0]] = smallest

            # Swap nodes
            self.swapMinHeapNode(smallest, idx)

            self.minHeapify(smallest)

    # Standard function to extract minimum node from heap
    def extractMin(self):

        # Return NULL wif heap is empty
        if self.isEmpty() == True:
            return

        # Store the root node
        root = self.array[0]

        # Replace root node with last node
        lastNode = self.array[self.size - 1]
        self.array[0] = lastNode

        # Update position of last node
        self.pos[lastNode[0]] = 0
        self.pos[root[0]] = self.size - 1

        # Reduce heap size and heapify root
        self.size -= 1
        self.minHeapify(0)

        return root

    def isEmpty(self):
        return True if self.size == 0 else False

    def decreaseKey(self, v, dist):

        # Get the index of v in  heap array

        i = self.pos[v]

        # Get the node and update its dist value
        self.array[i][1] = dist

        # Travel up while the complete tree is not
        # hepified. This is a O(Logn) loop
        while i > 0 and self.array[i][1] < self.array[int((i - 1) / 2)][1]:

            # Swap this node with its parent
            self.pos[self.array[i][0]] = int((i-1)/2)
            self.pos[self.array[int((i-1)/2)][0]] = i
            self.swapMinHeapNode(i, int((i - 1)/2))

            # move to parent index
            i = int((i - 1) / 2)

    # A utility function to check if a given vertex
    # 'v' is in min heap or not
    def isInMinHeap(self, v):

        if self.pos[v] < self.size:
            return True
        return False


class Graph():

    def __init__(self, V):
        self.V = V
        self.graph = defaultdict(list)

    # Adds an edge to an undirected graph
    def addEdge(self, src, dest, weight):

        # Add an edge from src to dest.  A new node is
        # added to the adjacency list of src. The node
        # is added at the begining. The first element of
        # the node has the destination and the second
        # elements has the weight
        newNode = [dest, weight]
        self.graph[src].insert(0, newNode)

        # Since graph is undirected, add an edge from
        # dest to src also
        newNode = [src, weight]
        self.graph[dest].insert(0, newNode)

    # The main function that prints the Minimum
    # Spanning Tree(MST) using the Prim's Algorithm.
    # It is a O(ELogV) function
    def PrimMST(self):
        # Get the number of vertices in graph
        V = self.V

        # key values used to pick minimum weight edge in cut
        key = []

        # List to store contructed MST
        parent = []

        # minHeap represents set E
        minHeap = Heap()

        # Initialize min heap with all vertices. Key values of all
        # vertices (except the 0th vertex) is is initially infinite
        for v in range(V):
            parent.append(-1)
            key.append(float("inf"))
            minHeap.array.append(minHeap.newMinHeapNode(v, key[v]))
            minHeap.pos.append(v)

        # Make key value of 0th vertex as 0 so
        # that it is extracted first
        minHeap.pos[0] = 0
        key[0] = 0
        minHeap.decreaseKey(0, key[0])

        # Initially size of min heap is equal to V
        minHeap.size = V

        # In the following loop, min heap contains all nodes
        # not yet added in the MST.
        while minHeap.isEmpty() == False:

            # Extract the vertex with minimum distance value
            newHeapNode = minHeap.extractMin()
            u = newHeapNode[0]

            # Traverse through all adjacent vertices of u
            # (the extracted vertex) and update their
            # distance values
            for pCrawl in self.graph[u]:

                v = pCrawl[0]

                # If shortest distance to v is not finalized
                # yet, and distance to v through u is less than
                # its previously calculated distance
                if minHeap.isInMinHeap(v) and pCrawl[1] < key[v]:
                    key[v] = pCrawl[1]
                    parent[v] = u

                    # update distance value in min heap also
                    minHeap.decreaseKey(v, key[v])

        return parent, V
