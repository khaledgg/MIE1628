#!/usr/bin/env python
"""reducer.py"""

import sys

def calculateNewCentroids():
    current_centroid_id = None
    points_sum = (0, 0)
    points_count = 0

    for line in sys.stdin:
        centroid_id, coordinates = line.strip().split('\t')
        x, y = map(float, coordinates.split(','))

        if current_centroid_id != centroid_id:
            if current_centroid_id is not None:
                new_centroid_x = points_sum[0] / points_count
                new_centroid_y = points_sum[1] / points_count
                print(f'{current_centroid_id},{new_centroid_x},{new_centroid_y}')
            current_centroid_id = centroid_id
            points_sum = (0, 0)
            points_count = 0
        
        points_sum = (points_sum[0] + x, points_sum[1] + y)
        points_count += 1

    # Output the centroid for the last cluster
    if current_centroid_id is not None:
        new_centroid_x = points_sum[0] / points_count
        new_centroid_y = points_sum[1] / points_count
        print(f'{current_centroid_id},{new_centroid_x},{new_centroid_y}')

if __name__ == "__main__":
    calculateNewCentroids()
