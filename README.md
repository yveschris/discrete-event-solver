# World's First Discrete Event Solver

I became a researcher on telecom/computer network performance when I did my PhD in 2008. During my research, I always find existing network simulators hard to use in terms of code readability and runtime performance. In September 2021, I decided to develop a simulator (that I love to use) based on Lindley's equation (a core math equation in queueing theory); and I call this type of simulation **discrete event solver**.

Such a solver is new (i.e., no such solvers exist in the world before), and more importantly, it has two **BIG** advantages comparing to the conventional discrete event simulation:
1. super fast: it's supposed to be at least 100x faster than the conventional network simulators;
2. super easy to read and super simple to develop your own ideas: the codes are written in Python and the total line number is less than 1k.

I'm committed to this simulator to make sure that it will be a real computer network simulator and other types of simulators based on this discrete-event simulator. 

## TO DO:
1. to improve the server side's response performance (est. 2025 First quarter)
2. https
3. scaling law problem
4. tcp capability
5. dynamic routing
6. animation

## How to use this computer network simulator?
1. the Cython codes are compiled using Python 3.11.9. Therefore, in order to run the simulation properly, you may have to use Python 3.11.9, which can be downloaded on https://www.python.org/downloads/release/python-3119/
2. install the required modules using pip (only numpy, matplotlib, networkx and requests modules are required).
3. run netsim_client.py in the computer_network_simulator_in_python folder
4. that's it! Enjoy!
