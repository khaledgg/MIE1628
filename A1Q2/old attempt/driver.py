import os
import shutil
import subprocess

MAX_ITERATIONS = 20
CONVERGENCE_THRESHOLD = 0.01
K = 3  # Number of clusters

# 1. Initialize centroids
# We'll just pick the first K data points. Alternatively, you can choose them randomly or use other methods.
centroids = []
with open("data_points.txt", "r") as f:
    for _ in range(K):
        centroids.append(f.readline().strip())

# Write initial centroids to file
with open("centroids.txt", "w") as f:
    for centroid in centroids:
        f.write(centroid + "\n")

iteration = 0
converged = False

while not converged and iteration < MAX_ITERATIONS:
    iteration += 1
    print(f"Iteration {iteration}")

    # Prepare input and output directories
    input_dir = f'input_{iteration}'
    output_dir = f'output_{iteration}'
    
    # 2. Run MapReduce
    cmd = [
        "hadoop", "jar", "C:\\hadoop-3.3.0\\share\\hadoop\\tools\\lib\\hadoop-streaming-3.3.0.jar",
        "-file", "mapper.py", "-mapper", f"C:\\Users\\Khaled\\AppData\\Local\\Microsoft\\WindowsApps\\python3.exe mapper.py",
        "-file", "reducer.py", "-reducer", f"C:\\Users\\Khaled\\AppData\\Local\\Microsoft\\WindowsApps\\python3.exe reducer.py",
        "-input", input_dir, "-output", output_dir
    ]

    subprocess.run(cmd)

    # 3. Check for convergence and update centroids
    cat_cmd = ["hdfs", "dfs", "-cat", f"{output_dir}/part-00000"]
    cat_output = subprocess.check_output(cat_cmd).decode("utf-8")
    new_centroids = [line.split('\t')[1] for line in cat_output.strip().split('\n')]

    # A simple convergence test: check if centroids have changed
    converged = all(nc == c for nc, c in zip(new_centroids, centroids))

    # Update centroids for the next iteration
    centroids = new_centroids

    # Write updated centroids to file for next iteration
    with open("centroids.txt", "w") as f:
        for centroid in centroids:
            f.write(centroid + "\n")

    # Optionally, remove the previous iteration's output
    shutil.rmtree(f"output/iteration-{iteration-1}", ignore_errors=True)

print("K-means clustering completed!")
if converged:
    print(f"Converged after {iteration} iterations.")
else:
    print(f"Reached maximum iterations ({MAX_ITERATIONS}) without convergence.")
