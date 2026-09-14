from search import search, searchall
import time
import random
from statistics import mean
##import matplotlib

times = []

for size in [10,100,500,1E3,5E3,1E4,5E4,1E5,4E5,7E5]:
    for i in range(100):
        target = 1337
        listwan = [target]
        for i in range(int(size)):
            r = random.randint(-100000,100000)
            listwan.append(r)
        listwan = sorted(listwan)

        time_start = time.perf_counter_ns()
        idx = search(target, listwan)
        time_end = time.perf_counter_ns()
        #print(size, ",", time_end-time_start)
        #print(f"Size: {size} | Time: {time_end-time_start}")
        times.append(time_end-time_start)
    print(f"{size} ; {mean(times)}")
    #print(f"Average time spent: {mean(times)}")

