"""
Test suite for format function in "merge - 2048"
"""

import user34_fLQO0ejC6D_7 as simpletest
def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    count=0
    while 0 in line:
        count=count + 1
        line.remove(0)
    for dump_num in range(0, count):
        line.append(0)
    for looper in range(0,len(line)-1):
        if line[looper]==line[looper+1]:
            line[looper]=line[looper]+line[looper+1]
            line.remove(line[looper+1])
            line.append(0)
            looper=looper+1
    return line

simpletest.run_test(merge)