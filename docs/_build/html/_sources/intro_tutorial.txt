
Introductory Tutorial
=====================

Instalation
-----------

First of all, you need to install the package using pip.

.. code:: bash

        $ pip install soba

In case of error, this other command should be used, ensuring to have
installed python 3 and pip 3.

.. code:: bash

        $ pip3 install soba

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
    N = 12
    
    #Definition of the states
    states = OrderedDict([('Leaving','out'), ('Resting', 'sofa'), ('Working in my laboratory', 'wp')])
    
    #Definition of the schedule
    schedule = {'t1': "09:00:00", 't2': "13:00:00", 't3': "14:10:00"}
    
    #Possible Variation on the schedule
    variation = {'t1': "00:10:00", 't2': "01:20:00", 't3': "00:20:00"}
    
    #Probability of state change associated with the Markovian chain as a function of the temporal period.
    markovActivity = {
        '-t1': [[100, 0, 0], [0, 0, 0], [0, 0, 0]],
        't1-t2': [[30, 40, 30], [0, 50, 50], [0, 50, 50]],
        't2-t3': [[0, 0, 0], [50, 50, 0], [0, 0, 0]],
        't3-': [[0, 50, 50], [10, 90, 0], [0, 0, 0]]
    }
    
    #Time associated to each state (minutes)
    timeActivity = {
        '-t1': [60, 0, 0], 't1-t2': [2, 60, 15], 't2-t3': [60, 10, 15], 't3-': [60, 20, 15]
    }
    
    #Store the information
    jsonOccupant = {'type': 'example' , 'N': N, 'states': states , 'schedule': schedule, 'variation': variation, 'markovActivity': markovActivity, 'timeActivity': timeActivity}
    jsonsOccupants.append(jsonOccupant)

2.- We define the building plan or the distribution of the space.

.. code:: python

    import soba.visualization.ramen.mapGenerator as ramen
    
    with open('labgsi.blueprint3d') as data_file:
        jsonMap = ramen.returnMap(data_file)

3.- We implement a Model inheriting a base class of SOBA.

.. code:: python

    from soba.model.model import ContinuousModel
    import datetime as dt
    
    class ModelExample(ContinuousModel):
    
        def __init__(self, width, height, jsonMap, jsonsOccupants, seed = dt.datetime.now()):
            super().__init__(width, height, jsonMap, jsonsOccupants, seed = seed)
    
        def step(self):
            if self.clock.clock.day > 3:
                self.finishSimulation = True
            super().step()

4.- We call the execution methods.

::

    4.1-With visual representation.

.. code:: python

    import soba.run
    
    soba.run.run(ModelExample, [], cellW, cellH, jsonMap, jsonsOccupants)

::

    4.1- Bacth mode.

.. code:: python

    #Fixed parameters during iterations
    fixed_params = {"width": cellW, "height": cellH, "jsonMap": jsonMap, "jsonsOccupants": jsonsOccupants}
    #Variable parameters to each iteration
    variable_params = {"seed": range(10, 500, 10)}
    
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
    schedule = {'t1': "09:00:00", 't2': "13:00:00", 't3': "14:10:00"}
    
    #Possible Variation on the schedule
    variation = {'t1': "00:10:00", 't2': "01:20:00", 't3': "00:20:00"}
    
    #Probability of state change associated with the Markovian chain as a function of the temporal period.
    markovActivity = {
        '-t1': [[100, 0], [0, 0]],
        't1-t2': [[50, 50], [0, 0]],
        't2-t3': [[0, 0], [50, 0]],
        't3-': [[0, 50], [10, 90]]
    }
    
    #Time associated to each state (minutes)
    timeActivity = {
        '-t1': [60, 0],
        't1-t2': [2, 60],
        't2-t3': [60, 10],
        't3-': [60, 20]
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

    from soba.model.model import ContinuousModel
    import datetime as dt
    
    class ModelExample(RoomsModel):
    
        def __init__(self, width, height, jsonMap, jsonsOccupants, seed = dt.datetime.now()):
            super().__init__(width, height, jsonMap, jsonsOccupants, seed = seed)
    
        def step(self):
            if self.clock.clock.day > 3:
                self.finishSimulation = True
            super().step()

4.- We call the execution methods. 4.1- With visual representation.

.. code:: python

    cellW = 4
    cellH = 4
    
    soba.run.run(ModelExample, [], cellW, cellH, jsonMap, jsonsOccupants)

::

    4.1- Bacth mode.

.. code:: python

    #Fixed parameters during iterations
    fixed_params = {"width": cellW, "height": cellH, "jsonMap": jsonMap, "jsonsOccupants": jsonsOccupants}
    #Variable parameters to each iteration
    variable_params = {"seed": range(10, 500, 10)}
    
    soba.run.run(ModelExample, fixed_params, variable_params)

Running the simulation using the terminal
-----------------------------------------

.. code:: bash

        $ python exampleContinuous.py -v

Options:

::

    -v,     Visual option on browser

    -b,     Background option

    -r,     Ramen option

