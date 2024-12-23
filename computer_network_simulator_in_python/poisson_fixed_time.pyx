from libc.stdlib cimport rand, srand, RAND_MAX, malloc, free
from libc.math cimport log
import numpy as np
cimport numpy as np

# Helper function to generate random numbers between 0 and 1
cdef double random_uniform():
    return (rand() + 1) / (RAND_MAX + 2)

# Poisson fixed-time function using libc's rand
def poisson_fixed_time(double start_time, double end_time, unsigned int seed, double lam):
    cdef double avg = 1 / lam
    cdef double t = start_time
    cdef double dt
    cdef double r
    cdef int n = 0
    cdef double *inter_arrival_times
    cdef np.ndarray[np.double_t, ndim=1] result

    # Seed the random number generator
    srand(seed)

    # print("Start simulation:")
    # print(f"Start time: {start_time}, End time: {end_time}, Lambda: {lam}, Avg: {avg}")

    # First phase: count the number of events
    while True:
        r = random_uniform()
        dt = -avg * log(r)  # Generate exponential random variable
        # print(f"{r}")
        # print(f"{dt}")
        t += dt
        if t < end_time:
            n += 1
        else:
            break
        
    # print(f"Total events: {n}")

    # Allocate memory for inter-arrival times
    created_t = <double *>malloc(n * sizeof(double))
    if inter_arrival_times == NULL:
        raise MemoryError("Failed to allocate memory for inter-arrival times")

    # Second phase: generate inter-arrival times
    srand(seed)
    t = start_time
    for i in range(n):
        dt = -avg * log(random_uniform())
        created_t[i] = t + dt
        t += dt

    # Convert to NumPy array and free allocated memory
    created = np.zeros(n, dtype=np.double)
    for i in range(n):
        created[i] = created_t[i]        
    free(created_t)
    
    # print("Simulation complete!")
    return created
