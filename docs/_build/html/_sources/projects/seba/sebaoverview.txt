SEBA Overview
=============

`SEBA <https://github.com/gsi-upm/soba/tree/master/projects/seba>`_ (Simulation of Evacuations Based on SOBA) is a useful simulation tool for studies related to emergencies and evacuations in buildings. It is implemented in `Python <http://www.python.org/>`_. on `SOBA <https://github.com/gsi-upm/soba>`_ software.

Simulations can be defined in three different ways. First, using behavioral modeling and strategies already implemented, by defining the space and specific characteristics of the occupants. Second, through inheritance and modification of the models defined in the classes already implemented. Third, by modifying the current software implementation.

It is provided as open source software:

``Github repository``:
https://github.com/gsi-upm/soba/tree/master/projects/seba

Arquitecture Description
------------------------

.. image:: ../../images/SEBAarquitectura.png
   :width: 80%
   :scale: 80%


SEBA Components
***************

`SOBA <https://github.com/gsi-upm/soba>`_. Software tool base for the implementation of SEBA.
`RAMEN <https://github.com/gsi-upm/RAMEN>`_. It is an agent-based social simulation visualization tool for indoor crowd analytics based on the library Three.js. It allows to visualize a social simulation in a 3D environment and also to create the floor plan of a building.
`Browser <https://www.google.com/chrome/>`_. Using a browser a simple visualization can be made to know the performance of the simulation. This is also useful for debugging.
`REST Service <https://www.getpostman.com/>`_. The software provide an API defined as a REST service (Get, Post, Pull and Push methods are defined) to interact with the simulation. 

SEBA Modules
************

SEBA is implemented through 4 modules with classes with related functionalities. 

- **Model**. This component is the center of the simulations. In the model class, the simulation starts, creating the variables and defining the conditions. During execution, it manages and functions as an intermediary between instances. In this class the strategies of the models are specified.
- *Agents*.
	- **Occupant**. Component to implement the people who are in the building, their activity and behavior.
	- **Avatar**. It is interesting to provide a means of interaction between simulation and real human participation. This functionality is provided through this component.
	- **Fire**. Through this component the threat of the emergency is modeled, specifically a fire that spreads through the building.
- *Visualization*.
	- **Back.py** and **front js**. Definition of visualization elements in browser. Connection between a JS file and a class p by means of parameter rendering.
- *Launchers*.
	- **RESTServer**. Specification of the REST service server deployment.
	- **Run**. Provides the execution of the simulation from terminal.
