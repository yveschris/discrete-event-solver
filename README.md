# World's First Discrete Event Solver

The world's first **discrete event solver** is a new type of discrete-event simulation (No such solvers exist in the world before) that is based on Lindley's equation (a core math equation in queueing theory). It has the following advantages comparing to the conventional discrete event simulation:

1. no installation required;
2. super easy to read: the codes are written in Python and the total line number is less than 1k;
3. super fast: it's supposed to be at least 100x faster than the conventional network simulators;
4. super simple to develop your own ideas: life is short, code Python.

The **computer network simulator** is an application of the discrete event solver and will be continuously improved to be a ready computer network simulator for everyone. More importantly, other types of simulation based on this solver will be invented in the near future, like hospital simulation, road traffic simulation and so on.

## TO DO:
1. to improve the server side's response performance (est. 2025 First quarter)
2. https
3. scaling law problem
4. tcp capability
5. dynamic routing
6. animation
7. GPU-enabled, which may speed up the performance by 100x (in experimental stage)
8. optimization

## How to use this computer network simulator?
0. only work on Windows platform
1. the Cython codes are compiled using Python 3.11.9. Therefore, in order to run the simulation properly, you may have to use Python 3.11.9, which can be downloaded on https://www.python.org/downloads/release/python-3119/
2. install the required modules using pip (only numpy, matplotlib, networkx and requests modules are required).
3. download the repo (don't be panic, only 408 KBytes) and then run netsim_client.py in the computer_network_simulator_in_python folder
4. that's it! Enjoy!
