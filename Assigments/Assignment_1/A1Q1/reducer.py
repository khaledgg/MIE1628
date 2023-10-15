#!/usr/bin/env python3

import sys

total_count = 0

for line in sys.stdin:
    _, count = line.split('\t', 1)
    total_count += int(count)

print('%s\t%s' % ("line", total_count))