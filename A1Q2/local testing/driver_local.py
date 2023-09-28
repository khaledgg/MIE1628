import os
import subprocess
import time  # Import the time module
start_time = time.time()


MAX_ITERATIONS = 20
CONVERGENCE_THRESHOLD = 0.01
K = 6  # Number of clusters

print("For K = ", K)

# 1. Initialize centroids
# We'll just pick the first K data points. Alternatively, you can choose them randomly or use other methods.
centroids = []
with open("data_points.txt", "r") as f:
    for i, line in enumerate(f):
        if i < K:
            x, y = line.strip().split(",")
            centroids.append(f"{i},{x},{y}")

# Write initial centroids to file
with open("centroids.txt", "w") as f:
    f.write('\n'.join(centroids) + '\n')

iteration = 0
converged = False

while not converged and iteration < MAX_ITERATIONS:
    iteration += 1
    print(f"Iteration {iteration}")

    # 2. Run MapReduce-like pipeline
    pipeline_cmd = f"type data_points.txt | python3 mapper.py | sort | python3 reducer.py"
    process = subprocess.Popen(pipeline_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    # Error handling
    if process.returncode != 0:
        print(f"Pipeline failed with error code {process.returncode}: {stderr.decode('utf-8')}")
        break

    # 3. Check for convergence and update centroids
    new_centroids = stdout.decode('utf-8').strip().split('\n')


    # A simple convergence test: check if centroids have changed
    converged = all(nc == c for nc, c in zip(new_centroids, centroids))

    # Update centroids for the next iteration
    centroids = new_centroids

    # Write updated centroids to file for next iteration
    with open("centroids.txt", "w") as f:
        for centroid in centroids:
            f.write(centroid)

print("K-means clustering completed!")
if converged:
    print(f"Converged after {iteration} iterations.")
else:
    print(f"Reached maximum iterations ({MAX_ITERATIONS}) without convergence.")

print(centroids)

# Stop the timer
end_time = time.time()

# Calculate and print the elapsed time
elapsed_time = end_time - start_time
print(f"Time taken: {elapsed_time:.2f} seconds")
