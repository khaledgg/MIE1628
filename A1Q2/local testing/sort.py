import sys

def sort_input():
    lines = [line.strip() for line in sys.stdin if line.strip()]
    lines.sort(key=lambda x: x.split('\t', 1)[0])
    for line in lines:
        print(line)

if __name__ == "__main__":
    sort_input()
