import numpy as np
from sklearn.cluster import DBSCAN

def dbscan_clustering(visit_points, max_distance, min_points):
    clusters = []
    np_points = []
    for vp in visit_points:
        np_points.append(vp['position'].to_np_point())
    np_points = np.array(np_points)
    dbscan_res = DBSCAN(eps=max_distance, min_samples=min_points).fit(np_points)
    for i in range(0, max(dbscan_res.labels_) + 1):
        clusters.append([])
    for ind, v in enumerate(visit_points):
        label = int(dbscan_res.labels_[ind])
        if label == -1:
            clusters.append([ind])
        else:
            clusters[label].append(ind)
    return clusters