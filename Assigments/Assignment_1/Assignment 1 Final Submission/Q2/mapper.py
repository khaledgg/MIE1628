#!/usr/bin/env python
"""mapper.py"""

import sys
from math import sqrt

# Load initial centroids from a text file and add them to an array
def getCentroids(filepath):
    centroids = []
    with open(filepath, 'r') as file:
        for line in file:
            fields = line.strip().split(',')
            cluster_id = int(fields[0])
            coordinates = (float(fields[1]), float(fields[2]))
            centroids.append((cluster_id, coordinates))
    return centroids

# Create clusters based on initial centroids
def createClusters(centroids):
    for line in sys.stdin:
        data_point_coords = tuple(map(float, line.strip().split(',')))
        closest_centroid_id = None
        closest_distance = float('inf')
        for centroid in centroids:
            centroid_id, centroid_coords = centroid
            distance = sqrt((data_point_coords[0] - centroid_coords[0])**2 + (data_point_coords[1] - centroid_coords[1])**2)
            if distance < closest_distance:
                closest_distance = distance
                closest_centroid_id = centroid_id
        
        # Output the closest centroid ID and the data point coordinates
        print(f'{closest_centroid_id}\t{data_point_coords[0]},{data_point_coords[1]}')

if __name__ == "__main__":
    centroids_filepath = 'centroids.txt'
    centroids = getCentroids(centroids_filepath)
    createClusters(centroids)
