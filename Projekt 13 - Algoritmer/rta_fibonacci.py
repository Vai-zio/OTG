from fibonacci import fibit, fib
import time
import random
from statistics import mean

times = []

for size in [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]:
    for i in range(100):
        time_start = time.perf_counter_ns()
        idx = fibit(size)
        time_end = time.perf_counter_ns()
        #print(f"Size: {size} | Time: {time_end-time_start}")
        times.append(time_end-time_start)
    print(f"{size} ; {idx} ; {mean(times)}")
    #print(f"Average time spent: {mean(times)}")

for size in [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]:
    for i in range(100):
        time_start = time.perf_counter_ns()
        idx = fib(size)
        time_end = time.perf_counter_ns()
        #print(f"Size: {size} | Time: {time_end-time_start}")
        times.append(time_end-time_start)
    print(f"{size} ; {idx} ; {mean(times)}")
    #print(f"Average time spent: {mean(times)}")
