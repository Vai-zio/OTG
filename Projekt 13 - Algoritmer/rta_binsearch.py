from binsearch import binsearch
import time
import random
from statistics import mean

times = []

for size in [10,100,500,1E3,1E4,1E5,4E5,7E5,1E6]:
    for i in range(100):
        target = 80085*10
        numbers = [target]
        for i in range(int(size)):
            r = random.randint(-100000,100000)
            numbers.append(r)
        numbers = sorted(numbers)

        time_start = time.perf_counter_ns()
        idx = binsearch(target, numbers)
        time_end = time.perf_counter_ns()
        #print(f"Size: {size} | Time: {time_end-time_start}")
        times.append(time_end-time_start)
    print(f"{size} ; {mean(times)}")
    #print(f"Average time spent: {mean(times)}")
