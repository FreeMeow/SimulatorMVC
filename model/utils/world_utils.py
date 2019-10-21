import math


def calc_entropy(world):
    count_matrix = [[0 for _ in range(0, 4)] for _ in range(0, 4)]
    for vertex in world['visit_points']:
        count_matrix[int(vertex['position'].x/150)][int(vertex['position'].y/150)] += 1
    entropy = 0
    for row in count_matrix:
        for tile in row:
            if tile != 0:
                dls = tile/len(world['visit_points'])
                entropy += -dls*math.log2(dls) / math.log2(len(world['visit_points']))
    return entropy

def standard_deviation(world):
    p_sum = 0
    st_sum = 0
    for vertex in world['visit_points']:
        p_sum += vertex['probability']
        st_sum += vertex['starvation']
    p_average = p_sum / len(world['visit_points'])
    st_average = st_sum / len(world['visit_points'])
    p_deviation = 0
    st_deviation = 0
    for vertex in world['visit_points']:
        p_deviation += (vertex['probability'] - p_average)**2
        st_deviation += (vertex['starvation'] - st_average)**2
    return (p_deviation/len(world['visit_points']))**0.5, (st_deviation/len(world['visit_points']))**0.5


