
Instalation
-----------

If the SOBA package is not yet installed, we must first do so. To
install SOBA the best option is to use the package management system
PIP. For this, we execute the following command.

.. code:: bash

        $ pip install soba

In case of error, this other command should be used, ensuring to have
installed python 3 and pip 3.

.. code:: bash

        $ pip3 install soba

Introductory Tutorial
=====================

Tutorial
--------

The SOBA tool can be provided to be used directly on two scenarios:

1. Generic case with a space defined as a grid of a given square size
   (by default, half a meter on each side).
2. Simplified case with a room defined by rooms, to perform simulations
   in simplified buildings that require less consumption of resources
   and specifications.

An introductory tutorial will be presented for each case, although most
parameters are common or similar.

SOBA enables the performance of the simulations in two modes:

1. With visual representation.
2. In batch mode.

In the tutorials, the small modifications required to use each
posibility are reflected.

In addition, two added mechanisms are provided to interact with the
simulation:

1. Use an API on a REST server to obtain information and create and
   manage avatars.
2. use the external tool `RAMEN <https://github.com/gsi-upm/RAMEN>`__
   for advanced 3D-visualization on Three.js.

IMPORTANT NOTE: The .py files described in this tutorial are available
in the github repository
https://github.com/gsi-upm/soba/tree/master/projects/basicExamples

Implementing a sample model with continuous space
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once soba is installed, the implementation can be started. First we
define the generic parameters to both types of scenario.

1.- We define the characteristics of the occupants

.. code:: python

    from collections import OrderedDict
    #JSON to store all the informacion.
    jsonsOccupants = []
    
    #Number of occupants
    N = 3
    
    #Definition of the states
    states = OrderedDict([('Leaving','out'), ('Resting', 'sofa'), ('Working in my laboratory', 'wp')])
    
    #Definition of the schedule
    schedule = {'t1': "08:01:00", 't2': "08:10:00", 't3': "08:20:00"}
    
    #Possible Variation on the schedule
    variation = {'t1': "00:01:00", 't2': "00:01:00", 't3': "00:01:00"}
    
    #Probability of state change associated with the Markovian chain as a function of the temporal period
    markovActivity = {
        '-t1': [[100, 0, 0], [0, 0, 0], [0, 0, 0]],
        't1-t2': [[0, 0, 100], [0, 50, 50], [0, 50, 50]],
        't2-t3': [[100, 0, 0], [0, 50, 50], [0, 50, 50]],
        't3-': [[0, 0, 100], [0, 100, 0], [0, 100, 0]]
    }
    
    #Time associated to each state (minutes)
    timeActivity = {
        '-t1': [3, 0, 0], 't1-t2': [3, 3, 3], 't2-t3': [3, 3, 3], 't3-': [3, 3, 3]
    }
    
    
    #Time variation associated to each state (minutes)
    timeActivityVariation = {
        '-t1': [1, 0, 0], 't1-t2': [1, 1, 1], 't2-t3': [1, 1, 1], 't3-': [1, 1, 1]
    }
    
    #Store the information
    jsonOccupant = {'type': 'example' , 'N': N, 'states': states , 'schedule': schedule, 'variation': variation,
    'markovActivity': markovActivity, 'timeActivity': timeActivity, "timeActivityVariation": timeActivityVariation}
    
    jsonsOccupants.append(jsonOccupant)

2.- We define the building plan or the distribution of the space.

.. code:: python

    import soba.visualization.ramen.mapGenerator as ramen
    
    with open('labgsi.blueprint3d') as data_file:
        jsonMap = ramen.returnMap(data_file)

3.- We implement a Model inheriting a base class of SOBA.

.. code:: python

    from soba.models.continuousModel import ContinuousModel
    from time import time
    
    class ModelExample(ContinuousModel):
    
        def __init__(self, width, height, jsonMap, jsonsOccupants, seed = int(time())):
            super().__init__(width, height, jsonMap, jsonsOccupants, seed = seed, timeByStep = 60)
            self.createOccupants(jsonsOccupants)
    
        def step(self):
            if self.clock.clock.hour > 17:
                self.finishSimulation = True
            super().step()


4.- We call the execution methods.

::

    4.1-With visual representation.

.. code:: python

    import soba.run
    import sys
    from optparse import OptionParser
    
    parameters = {'width': 40, 'height': 40, 'jsonMap': jsonMap, 'jsonsOccupants': jsonsOccupants}
    
    sys.argv = []
    sys.argv.append("-1")
    sys.argv.append("-v")
    
    soba.run.run(ModelExample, parameters, visualJS="example.js")

::

    4.1- Bacth mode.

.. code:: python

    import soba.run
    import sys
    #Fixed parameters during iterations
    fixed_params = {"width": 40, "height": 40, "jsonMap": jsonMap, "jsonsOccupants": jsonsOccupants}
    #Variable parameters to each iteration
    variable_params = {"seed": range(10, 500, 10)}
    
    sys.argv = []
    sys.argv.append("-1")
    sys.argv.append("-b")
    
    soba.run.run(ModelExample, fixed_params, variable_params)

Implementing a sample model with simplified space
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once soba is installed, the implementation can be started. First we
define the generic parameters to both types of scenario.

1.- We define the characteristics of the occupants

.. code:: python

    from collections import OrderedDict
    #JSON to store all the informacion.
    jsonsOccupants = []
    
    #Number of occupants
    N = 3
    
    #Definition of the states
    states = OrderedDict([('out','Pos1'), ('Working in my laboratory', {'Pos2': 1, 'Pos3': 2})])
    
    #Definition of the schedule
    schedule = {'t1': "08:01:00", 't2': "08:10:00", 't3': "08:20:00"}
    
    #Possible Variation on the schedule
    variation = {'t1': "00:01:00", 't2': "00:01:00", 't3': "00:01:00"}
    
    #Probability of state change associated with the Markovian chain as a function of the temporal period
    markovActivity = {
        '-t1': [[100, 0, 0], [0, 0, 0], [0, 0, 0]],
        't1-t2': [[0, 0, 100], [0, 50, 50], [0, 50, 50]],
        't2-t3': [[100, 0, 0], [0, 50, 50], [0, 50, 50]],
        't3-': [[0, 0, 100], [0, 100, 0], [0, 100, 0]]
    }
    
    #Time associated to each state (minutes)
    timeActivity = {
        '-t1': [3, 0, 0], 't1-t2': [3, 3, 3], 't2-t3': [3, 3, 3], 't3-': [3, 3, 3]
    }
    
    
    #Time variation associated to each state (minutes)
    timeActivityVariation = {
        '-t1': [1, 0, 0], 't1-t2': [1, 1, 1], 't2-t3': [1, 1, 1], 't3-': [1, 1, 1]
    }
    
    #Store the information
    jsonOccupant = {'type': 'example' , 'N': N, 'states': states , 'schedule': schedule, 'variation': variation, 
                    'markovActivity': markovActivity, 'timeActivity': timeActivity}
    jsonsOccupants.append(jsonOccupant)

2.- We define the building plan or the distribution of the space.

.. code:: python

    jsonMap = {
      'Pos1': {'entrance':'', 'conectedTo': {'U':'Pos2'}, 'measures': {'dx':2, 'dy':2}},
      'Pos2': {'measures': {'dx':3, 'dy':3.5}, 'conectedTo': {'R':'Pos3'}},
      'Pos3': {'measures': {'dx':3, 'dy':3.5}}
    }

3.- We implement a Model inheriting a base class of SOBA.

.. code:: python

    from soba.models.roomsModel import RoomsModel
    import datetime as dt
    
    class ModelExample(RoomsModel):
    
        def __init__(self, width, height, jsonMap, jsonsOccupants, seed = int(time())):
            super().__init__(width, height, jsonMap, jsonsOccupants, seed = seed)
    
        def step(self):
            if self.clock.clock.day > 3:
                self.finishSimulation = True
            super().step()

4.- We call the execution methods. 4.1- With visual representation.

.. code:: python

    import soba.run
    import sys
    
    cellW = 4
    cellH = 4
    
    sys.argv = []
    sys.argv.append("-1")
    sys.argv.append("-v")
    
    parameters = {'width': cellW, 'height': cellH, 'jsonMap': jsonMap, 'jsonsOccupants': jsonsOccupants}
    soba.run.run(ModelExample, parameters, visualJS="example.js")

::

    4.1- Bacth mode.

.. code:: python

    #Fixed parameters during iterations
    fixed_params = {"width": cellW, "height": cellH, "jsonMap": jsonMap, "jsonsOccupants": jsonsOccupants}
    #Variable parameters to each iteration
    variable_params = {"seed": range(10, 500, 10)}
    
    sys.argv = []
    sys.argv.append("-1")
    sys.argv.append("-b")
    
    soba.run.run(ModelExample, fixed_params, variable_params)

Running the simulation using the terminal
-----------------------------------------

.. code:: bash


            $ git clone https://github.com/gsi-upm/soba

            $ cd soba/projects/examples

Then, execute the run file.

.. code:: bash


            $ python continuousExample.py

or

.. code:: bash


            $ python3 continuousExample.py

Different options are provided for execution:

1. Visual mode

.. code:: bash


            $ python3 continuousExample.py -v

1.1 Launching REST Server

.. code:: bash


            $ python3 continuousExample.py -v -s

1.2 Using RAMEN tool

.. code:: bash


            $ python3 continuousExample.py -v -r

2. Batch mode

.. code:: bash


            $ python3 continuousExample.py -b

2.1 Launching REST Server

.. code:: bash


            $ python3 continuousExample.py -b -s

2.2 Using RAMEN tool

.. code:: bash


            $ python3 continuousExample.py -b -r

