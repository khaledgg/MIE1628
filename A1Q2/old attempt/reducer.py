#!C:\Users\khale\AppData\Local\Microsoft\WindowsApps\python3.exe 

import sys
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler()])

current_cluster = None
points = []

for line in sys.stdin:
    # logging.info(f'Processing line: {line.strip()}')

    items = line.strip().split(',')
    
    try:
        cluster = int(items[0])
        x = float(items[1])
        y = float(items[2])
    except ValueError as e:
        logging.error(f'ValueError: {e} on line: {line.strip()}')
        continue
    
    if current_cluster == cluster:
        points.append((x, y))
    else:
        if current_cluster is not None:
            centroid_x = sum(p[0] for p in points) / len(points)
            centroid_y = sum(p[1] for p in points) / len(points)
            print(f"{current_cluster},{centroid_x},{centroid_y}")
        points = [(x, y)]
        current_cluster = cluster

if current_cluster == cluster:
    centroid_x = sum(p[0] for p in points) / len(points)
    centroid_y = sum(p[1] for p in points) / len(points)
    print(f"{current_cluster},{centroid_x},{centroid_y}")