import subprocess
import time

def run_command(command):
    process = subprocess.Popen(command, shell=True)
    process.wait()

def check_convergence(old_centroids, new_centroids):
    #simple absolute convergence, maybe add a tolerence?
    print("Convergence: ", old_centroids == new_centroids)

    return old_centroids == new_centroids

def parse_centroids(output):
    centroids = []
    for line in output.split('\n'):
        if line:  # check if line is not empty
            fields = line.split(',')
            if len(fields) != 3:
                print(f'Unexpected line format: {line}', file=sys.stderr)
                continue  # skip to next line
            try:
                centroid_id, x, y = fields[0], float(fields[1]), float(fields[2])
                centroids.append((centroid_id, (x, y)))
            except ValueError as e:
                print(f'Error parsing line: {line} - {e}', file=sys.stderr)
    return centroids

def main():
    print("Starting Main()")
    max_iterations = 20
    k_values = [6]
    total_start_time = time.time()

    print("uploading the data_points.txt file")
    command = "hdfs dfs -put data_points.txt /input/kmeans/data_points.txt"
    subprocess.run(command, shell=True, check=True)

    for k in k_values:
        iteration = 0
        converged = False
        old_centroids = None

        # Load input data and initial centroids into HDFS
        print("initializing initial centroid values")
        centroids = []
        with open("data_points.txt", "r") as f:
            for i, line in enumerate(f):
                if i < k:
                    x, y = line.strip().split(",")
                    centroids.append(f"{i},{x},{y}")

        # Write initial centroids to file
        with open("centroids.txt", "w") as f:
            f.write('\n'.join(centroids) + '\n')

        #delete the old results file
        print("Deleting old results file")
        command = f"hdfs dfs -rm -r /output/kmeans/results"
        subprocess.run(command, shell=True, check=True)

        print("uploading the centroids.txt file")
        command = f"hdfs dfs -put centroids.txt /input/kmeans/centroids.txt"
        subprocess.run(command, shell=True, check=True)

        while not converged and iteration < max_iterations:
            iteration += 1
            print(f"Starting iteration {iteration} for k = {k}")

            start_time = time.time()

            # Run Hadoop job
            command = (
                "hadoop jar C:\\hadoop-3.3.0\\share\\hadoop\\tools\\lib\\hadoop-streaming-3.3.0.jar "
                "-mapper \"C:\\Users\\khale\\AppData\\Local\\Microsoft\\WindowsApps\\python3.exe C:\\MIE1628\\A1Q2\\mapper.py\" "
                "-reducer \"C:\\Users\\khale\\AppData\\Local\\Microsoft\\WindowsApps\\python3.exe C:\\MIE1628\\A1Q2\\reducer.py\" "
                "-input /input/kmeans/* "
                f"-output /output/kmeans/results"
            )

            run_command(command)

            # Retrieve new centroids from HDFS and compare to old centroids
            command = f"hdfs dfs -cat /output/kmeans/results/part-00000"
            try:
                new_centroids_output = subprocess.check_output(command, shell=True).decode()
            except subprocess.CalledProcessError as e: #was getting weird errors, brute force ooga booga catch
                print(f"Error: {e.output.decode()}")
                continue  # Skip to the next iteration if an error occurs

            print("New_centroids_output: ", new_centroids_output)
            new_centroids = parse_centroids(new_centroids_output) 
            print("New_centroids: ", new_centroids)

            # Check convergence
            converged = check_convergence(old_centroids, new_centroids)
            old_centroids = new_centroids

            duration = time.time() - start_time
            print(f"Iteration {iteration} completed in {duration} seconds")

   

            if converged or iteration == max_iterations:
                 #Save output file
                print("Saving Output file")
                command = "hdfs dfs -get /output/kmeans/results/* C:\MIE1628\A1Q2\Final_Results\k6"
                subprocess.run(command, shell=True, check=True)

            if not converged and iteration < max_iterations:

                print("Deleting Old centroid")
                command = f"hdfs dfs -rm /input/kmeans/centroids.txt"
                subprocess.run(command, shell=True, check=True)

                print("Adding new Centroids")
                new_centroids_str = '\n'.join(f'{id},{x},{y}' for id, (x, y) in new_centroids)
                
                #Write new centroid flie
                local_new_centroids_path = 'centroids.txt'
                with open(local_new_centroids_path, 'w') as file:
                    file.write(new_centroids_str)
                
                # Upload new centroid file
                command = "hdfs dfs -put centroids.txt /input/kmeans/centroids.txt"
                subprocess.run(command, shell=True, check=True)


                #delete the old results file
                print("Deleting old results file")
                command = f"hdfs dfs -rm -r /output/kmeans/results"
                subprocess.run(command, shell=True, check=True)



    total_duration = time.time() - total_start_time
    print(f"{iteration} Iterations in: {total_duration} seconds")

    print(f"The Final Centroids are: {new_centroids}")

if __name__ == "__main__":
    main()
