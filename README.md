# World's First Discrete Event Solver

I became a researcher on telecom/computer network performance when I did my PhD in 2008. During my research, I always find existing network simulators hard to use in terms of 
1. installation procedures: compiling a big C++ project is a nightmare for me (I don't have a computer science background);
2. code readability: just too many C++ codes;
3. runtime performance: based on my definition, I consider the runtime performance to be poor;
4. customization of the codes: I have to debug the codes and then compile the C++ project again and again.

In September 2021, I decided to develop a simulator (that I love to use) based on Lindley's equation (a core math equation in queueing theory); and I call this type of simulation **discrete event solver**.

Such a solver is new (i.e., no such solvers exist in the world before), and more importantly, it completely relieves the pains for me comparing to the conventional discrete event simulation:
1. no installation required;
2. super easy to read: the codes are written in Python and the total line number is less than 1k;
3. super fast: it's supposed to be at least 100x faster than the conventional network simulators;
4. super simple to develop your own ideas: life is short, code Python.

I'm committed to this simulator to make sure that it will be a ready computer network simulator for everyone and will transform to other types of simulators based on this discrete-event simulator, like hospital simulation, road traffic simulation and so on.

## TO DO:
1. to improve the server side's response performance (est. 2025 First quarter)
2. https
3. scaling law problem
4. tcp capability
5. dynamic routing
6. animation
7. GPU-enabled, which may speed up the performance by 100x (in experimental stage).

## How to use this computer network simulator?
1. the Cython codes are compiled using Python 3.11.9. Therefore, in order to run the simulation properly, you may have to use Python 3.11.9, which can be downloaded on https://www.python.org/downloads/release/python-3119/
2. install the required modules using pip (only numpy, matplotlib, networkx and requests modules are required).
3. run netsim_client.py in the computer_network_simulator_in_python folder
4. that's it! Enjoy!
