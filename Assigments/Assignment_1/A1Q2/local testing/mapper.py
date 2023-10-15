#!C:\Users\Khaled\AppData\Local\Microsoft\WindowsApps\python3.exe 

import sys

def dist(x1, y1, x2, y2):
    # using straight line heuristic (instead of Manhattan, etc)
    distance = ((x1-x2)**2 + (y1-y2)**2)**0.5
    return distance

# get centroids from
def read_centroids():
    # store centroid in a dictionary: n: [x, y]
    centroids = {}
    # read centroids from a file
    with open("centroids.txt", "r") as f:
        for line in f:
            items = line.strip().split(',')
    
            c_number = int(items[0])
            x = float(items[1])
            y = float(items[2])

            centroids[c_number] = [float(x),float(y)]

    return centroids

centroids = read_centroids()

for line in sys.stdin:
    # for each line get the x, y value split by comma
    x, y = line.split(",")
    x = float(x)
    y = float(y)

    cluster = None
    min_dist = float('inf')  # max_float

    # get nearest centroid
    for centroid_id in centroids:
        temp_dist = dist(x, y, centroids[centroid_id][0], centroids[centroid_id][1])
        if temp_dist < min_dist:
            cluster = centroid_id
            min_dist = temp_dist
    
    output = f"{cluster},{x},{y}"
    # print(f"Mapper output: {output}", file=sys.stderr)
    print(output)

