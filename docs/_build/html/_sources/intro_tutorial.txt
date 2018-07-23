
Introductory Tutorial
=====================

Instalation
~~~~~~~~~~~

If the SOBA package is not yet installed, we must first do so. To
install SOBA the best option is to use the package management system
PIP. For this, we execute the following command.

.. code:: bash

        $ pip install soba

In case of error, this other command should be used, ensuring to have
installed python 3 and pip 3.

.. code:: bash

        $ pip3 install soba

Tutorial
~~~~~~~~

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
        't3-': [[0, 0, 100], [100, 0, 0], [0, 0, 100]]
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


.. parsed-literal::

    SOBA is running
    Interface starting at http://127.0.0.1:7777
    Socket opened!
    {"type":"get_params"}
    {"type":"reset"}
    {"type":"get_step","step":1}
    01:08:01:00
    {"type":"get_step","step":2}
    01:08:02:00
    {"type":"get_step","step":3}
    01:08:03:00
    {"type":"get_step","step":4}
    01:08:04:00
    {"type":"get_step","step":5}
    01:08:05:00
    {"type":"get_step","step":6}
    01:08:06:00
    {"type":"get_step","step":7}
    01:08:07:00
    {"type":"get_step","step":8}
    01:08:08:00
    {"type":"get_step","step":9}
    01:08:09:00
    {"type":"get_step","step":10}
    01:08:10:00
    {"type":"get_step","step":11}
    01:08:11:00
    {"type":"get_step","step":12}
    01:08:12:00
    {"type":"get_step","step":13}
    01:08:13:00
    {"type":"get_step","step":14}
    01:08:14:00
    {"type":"get_step","step":15}
    01:08:15:00
    {"type":"get_step","step":16}
    01:08:16:00
    {"type":"get_step","step":17}
    01:08:17:00
    {"type":"get_step","step":18}
    01:08:18:00
    {"type":"get_step","step":19}
    01:08:19:00
    {"type":"get_step","step":20}
    01:08:20:00
    {"type":"get_step","step":21}
    01:08:21:00
    {"type":"get_step","step":22}
    01:08:22:00
    {"type":"get_step","step":23}
    01:08:23:00
    {"type":"get_step","step":24}
    01:08:24:00
    {"type":"get_step","step":25}
    01:08:25:00
    {"type":"get_step","step":26}
    01:08:26:00
    {"type":"get_step","step":27}
    01:08:27:00
    {"type":"get_step","step":28}
    01:08:28:00
    {"type":"get_step","step":29}
    01:08:29:00
    {"type":"get_step","step":30}
    01:08:30:00
    {"type":"get_step","step":31}
    01:08:31:00
    {"type":"get_step","step":32}
    01:08:32:00
    {"type":"get_step","step":33}
    01:08:33:00
    {"type":"get_step","step":34}
    01:08:34:00
    {"type":"get_step","step":35}
    01:08:35:00
    {"type":"get_step","step":36}
    01:08:36:00
    {"type":"get_step","step":37}
    01:08:37:00
    {"type":"get_step","step":38}
    01:08:38:00
    {"type":"get_step","step":39}
    01:08:39:00
    {"type":"get_step","step":40}
    01:08:40:00
    {"type":"get_step","step":41}
    01:08:41:00
    {"type":"get_step","step":42}
    01:08:42:00
    {"type":"get_step","step":43}
    01:08:43:00
    {"type":"get_step","step":44}
    01:08:44:00
    {"type":"get_step","step":45}
    01:08:45:00
    {"type":"get_step","step":46}
    01:08:46:00
    {"type":"get_step","step":47}
    01:08:47:00
    {"type":"get_step","step":48}
    01:08:48:00
    {"type":"get_step","step":49}
    01:08:49:00
    {"type":"get_step","step":50}
    01:08:50:00
    {"type":"get_step","step":51}
    01:08:51:00
    {"type":"get_step","step":52}
    01:08:52:00
    {"type":"get_step","step":53}
    01:08:53:00
    {"type":"get_step","step":54}
    01:08:54:00
    {"type":"get_step","step":55}
    01:08:55:00
    {"type":"get_step","step":56}
    01:08:56:00
    {"type":"get_step","step":57}
    01:08:57:00
    {"type":"get_step","step":58}
    01:08:58:00


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
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

