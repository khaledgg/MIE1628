""" for one iteration manually ran:



"""
import subprocess
import os
import shutil

def run_iteration(input_file, centroids_file):
    # Run mapper
    mapper_cmd = f'python mapper.py < {input_file}'
    map_output = subprocess.check_output(mapper_cmd, shell=True).decode('utf-8')

    # Sort mapped output (assuming mapped output is in the format: cluster_id<TAB>x,y)
    sorted_output = '\n'.join(sorted(map_output.strip().split('\n'), key=lambda x: x.split('\t')[0]))

    # Write sorted output to a temporary file
    with open('sorted_output.txt', 'w') as f:
        f.write(sorted_output)

    # Run reducer
    reducer_cmd = f'python reducer.py < sorted_output.txt'
    new_centroids_output = subprocess.check_output(reducer_cmd, shell=True).decode('utf-8')

    # Update centroids file
    with open(centroids_file, 'w') as f:
        f.write(new_centroids_output)

def has_converged(old_centroids_file, new_centroids_file):
    with open(old_centroids_file, 'r') as f:
        old_centroids = f.read().strip()

    with open(new_centroids_file, 'r') as f:
        new_centroids = f.read().strip()

    return old_centroids == new_centroids

def main():
    input_file = 'data_points.txt'
    centroids_file = 'centroids.txt'
    max_iterations = 20

    for i in range(max_iterations):
        print(f'Iteration {i + 1}')

        # Backup old centroids
        shutil.copy(centroids_file, f'old_{centroids_file}')

        # Run MapReduce iteration
        run_iteration(input_file, centroids_file)

        # Check convergence
        if has_converged(f'old_{centroids_file}', centroids_file):
            print('Converged!')
            break
    else:
        print(f'Maximum iterations ({max_iterations}) reached.')

    # Clean up temporary files
    os.remove('sorted_output.txt')
    os.remove(f'old_{centroids_file}')

if __name__ == '__main__':
    main()
