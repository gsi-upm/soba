SOBA Overview
=============

`SOBA <https://github.com/gsi-upm/soba>`_ (Simulation of Occupancy Based on Agents) is a tool of simulation of occupancy in buildings implemented in `Python <http://www.python.org/>`_.

This software is useful for studies that require working with crowds, mainly in buildings. For example, SOBA has been used to carry out studies on the improvement of evacuations and for the improvement of energy efficiency in buildings.

The simulations are configured by declaring one or more types of occupants, with specific and definable behavior and a physical space. Regarding space, two different models are provided: a simplified model with a room defined by rooms, and a model with a continuous space. The simulation and results can be evaluated both in real time and post-simulation.


It is provided as open source software:

``Github repository``:
https://github.com/gsi-upm/soba

Arquitecture Description
------------------------

.. image:: images/arquitectura.png
   :width: 100%
   :scale: 100%

SEBA Components
***************

- `MESA <https://github.com/gsi-upm/soba>`_. Mesa is an Apache2 licensed agent-based modeling (or ABM) framework in Python. It allows users to create agent-based models using built-in core components (such as spatial grids and agent schedulers) or customized implementations.
- `Transitions <https://github.com/pytransitions/transitions#threading>`_. This external package is a lightweight, object-oriented state machine implementation in Python.
- `RAMEN <https://github.com/gsi-upm/RAMEN>`_. It is an agent-based social simulation visualization tool for indoor crowd analytics based on the library Three.js. It allows to visualize a social simulation in a 3D environment and also to create the floor plan of a building.
- `Browser <https://www.google.com/chrome/>`_. Using a browser a simple visualization can be made to know the performance of the simulation. This is also useful for debugging.
- `REST Service <https://www.getpostman.com/>`_. The software provide an API defined as a REST service (Get, Post, Pull and Push methods are defined) to interact with the simulation. 

SEBA Modules
************

SOBA is implemented through 5 modules which group independent components with a related function.

- *Model*.
	- **Model**. Base Class to create simulation models. It creates and manages space and agents. The model creates and manages space and agents, provides a scheduler that controls the agents activation regime, stores model-level parameters and serves as a container for the rest of components.
	- **Continuous Model**. Base Class to create simulation models on a continuous space.
	- **Rooms Model**. Base Class to create simulation models on a simplified space based on rooms.
	- **Time**. Component of time management during the simulation in sexagesimal units and controller of the scheduler during the simulation.

- *Agents*.
	- **Occupant**. An object of the Occupant class is a type of agent developed and characterized to simulate the behavior of crowds in buildings. The occupants are agents with their activity defined by markov states.
	- **Continuous Occupant**.This class enables to create occupants that are modelled with a continuous space models. based on considering a scaled grid (x, y). Cell size of 0.5m ^ 2 by default. 
	- **Rooms Occupant**. This class enables to create occupants that are modelled with a simplified models based on a discrete space associated with rooms. 
	- **Avatar**. It enables to create avatars that represent virtual occupants, that is, they are not controlled by the simulation but by an API Rest, providing a means of interaction between simulation and real human participation.
	- *Agents modules*.
		- **Markov**. Base class to models the activity of the agents by means of Markovian behavior.
		- **AStar**. Auxiliar class used by the occupants to move in the building.
		- `FOV <http://www.roguebasin.com/index.php?title=Permissive_Field_of_View>`_.This component is a permissive field of view, which is useful to define the occupant visibility.

- *Space*.
	- **Grid**. The space where the agents are situated and where they perform their actions is defined by means of a grid with coordinates (x, y).
	- **ContinuousItems**. Various classes that define the representation of physical space objects in the continuous space model.
	- **RoomsItems**. Various classes that define the representation of physical space objects in the simplificated space model based on rooms.

- *Visualization*. 
	- **Back.py** and **front js**. Two components provide a simple mechanism to represent the model in a web interface, based on HTML rendering though a server interface, implemented with web sockets. Connection between a JS file and a class py by means of parameters rendering. 
	- **ramenInterface**. Component to make the conexión with the RAMEN API.

- *Launchers*.
	- **RESTServer**. Specification of the REST service server deployment.
	- **Visual**. Manages the execution of the simulation in Browser by launch JS (front)/.py (back) files
	- **Run**. Provides the execution of the simulation from terminal.