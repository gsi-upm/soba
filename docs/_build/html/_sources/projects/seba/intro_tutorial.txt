
Use Case
========

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

Tutorial
--------

SEBA enables the performance of the simulations in two modes:

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

Configuring the simulation
~~~~~~~~~~~~~~~~~~~~~~~~~~

First we define the generic parameters.

1.- We define the characteristics of the occupants

.. code:: python

    from soba.models.continuousModel import ContinuousModel
    import soba.visualization.ramen.mapGenerator as ramen
    import soba.run
    from collections import OrderedDict
    import json
    import sys
    from model import SEBAModel
    from visualization.back import Visualization
    import datetime as dt
    
    
    strategies = ['nearest', 'safest', 'uncrowded']
    
    today = dt.date.today()
    timeHazard = dt.datetime(today.year, today.month, 1, 8, 30, 0, 0)
    
    families = []
    
    family1 = {'N': 3, 'child': 1, 'adult': 2} #Only two are really neccesary 
    family2 = {'N': 3, 'child': 2, 'adult': 1}
    
    # Uncomment to consider families
    #families.append(family1)
    #families.append(family2)
    
    sebaConfiguration = {'families': families, 'hazard': timeHazard}
    
    #JSON to store all the informacion.
    jsonsOccupants = []
    
    #Number of occupants
    N = 4
    
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
    'markovActivity': markovActivity, 'timeActivity': timeActivity, 'timeActivityVariation': timeActivityVariation,
    'strategy': 'nearest'}
    
    cellW = 20
    cellH = 20
    
    jsonsOccupants.append(jsonOccupant)

2.- We define the building plan or the distribution of the space.

.. code:: python

    import soba.visualization.ramen.mapGenerator as ramen
    
    with open('auxiliarFiles/labgsi.blueprint3d') as data_file:
        jsonMap = ramen.returnMap(data_file)

3.- We call the execution methods.

::

    3.1-With visual representation.

.. code:: python

    sys.argv = []
    sys.argv.append("-1")
    sys.argv.append("-v")
    
    back = Visualization(cellW, cellH)
    parameters = {'width': cellW, 'height': cellH, 'jsonMap': jsonMap, 'jsonsOccupants': jsonsOccupants, 'sebaConfiguration': sebaConfiguration}
    soba.run.run(SEBAModel, parameters, visualJS="visualization/front.js", back=back)


.. parsed-literal::

    SOBA is running
    {'t1': datetime.datetime(2017, 10, 1, 8, 1, 0, 291422), 't2': datetime.datetime(2017, 10, 1, 8, 9, 45, 947140), 't3': datetime.datetime(2017, 10, 1, 8, 20, 5, 813700)}
    {'t1': datetime.datetime(2017, 10, 1, 8, 1, 5, 873230), 't2': datetime.datetime(2017, 10, 1, 8, 9, 40, 597876), 't3': datetime.datetime(2017, 10, 1, 8, 20, 18, 968479)}
    {'t1': datetime.datetime(2017, 10, 1, 8, 0, 35, 656475), 't2': datetime.datetime(2017, 10, 1, 8, 9, 46, 200526), 't3': datetime.datetime(2017, 10, 1, 8, 20, 45, 775966)}
    {'t1': datetime.datetime(2017, 10, 1, 8, 1, 12, 804713), 't2': datetime.datetime(2017, 10, 1, 8, 10, 12, 223587), 't3': datetime.datetime(2017, 10, 1, 8, 20, 8, 565048)}
    Interface starting at http://127.0.0.1:7777
    Socket opened!
    {"type":"get_params"}
    {"type":"reset"}
    {'t1': datetime.datetime(2017, 10, 1, 8, 1, 0, 291422), 't2': datetime.datetime(2017, 10, 1, 8, 9, 45, 947140), 't3': datetime.datetime(2017, 10, 1, 8, 20, 5, 813700)}
    {'t1': datetime.datetime(2017, 10, 1, 8, 1, 5, 873230), 't2': datetime.datetime(2017, 10, 1, 8, 9, 40, 597876), 't3': datetime.datetime(2017, 10, 1, 8, 20, 18, 968479)}
    {'t1': datetime.datetime(2017, 10, 1, 8, 0, 35, 656475), 't2': datetime.datetime(2017, 10, 1, 8, 9, 46, 200526), 't3': datetime.datetime(2017, 10, 1, 8, 20, 45, 775966)}
    {'t1': datetime.datetime(2017, 10, 1, 8, 1, 12, 804713), 't2': datetime.datetime(2017, 10, 1, 8, 10, 12, 223587), 't3': datetime.datetime(2017, 10, 1, 8, 20, 8, 565048)}
    {"type":"get_step","step":1}
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:07:51:00
    {"type":"get_step","step":2}
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:07:52:00
    {"type":"get_step","step":3}
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:07:53:00
    {"type":"get_step","step":4}
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:07:54:00
    {"type":"get_step","step":5}
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:07:55:00
    {"type":"get_step","step":6}
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:07:56:00
    {"type":"get_step","step":7}
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:07:57:00
    {"type":"get_step","step":8}
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:07:58:00
    {"type":"get_step","step":9}
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:07:59:00
    {"type":"get_step","step":10}
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:00:00
    {"type":"get_step","step":11}
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:01:00
    {"type":"get_step","step":12}
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:02:00
    {"type":"get_step","step":13}
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:03:00
    {"type":"get_step","step":14}
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:04:00
    {"type":"get_step","step":15}
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:05:00
    {"type":"get_step","step":16}
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:06:00
    {"type":"get_step","step":17}
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:07:00
    {"type":"get_step","step":18}
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:08:00
    {"type":"get_step","step":19}
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:09:00
    {"type":"get_step","step":20}
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:10:00
    {"type":"get_step","step":21}
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:11:00
    {"type":"get_step","step":22}
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:12:00
    {"type":"get_step","step":23}
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:13:00
    {"type":"get_step","step":24}
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:14:00
    {"type":"get_step","step":25}
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:15:00
    {"type":"get_step","step":26}
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:16:00
    {"type":"get_step","step":27}
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:17:00
    {"type":"get_step","step":28}
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:18:00
    {"type":"get_step","step":29}
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:19:00
    {"type":"get_step","step":30}
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:20:00
    {"type":"get_step","step":31}
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:21:00
    {"type":"get_step","step":32}
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:22:00
    {"type":"get_step","step":33}
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:23:00
    {"type":"get_step","step":34}
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:24:00
    {"type":"get_step","step":35}
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:25:00
    {"type":"get_step","step":36}
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:26:00
    {"type":"get_step","step":37}
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:27:00
    {"type":"get_step","step":38}
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:28:00
    {"type":"get_step","step":39}
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:29:00
    {"type":"get_step","step":40}
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:30:00
    {"type":"get_step","step":41}
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:31:00
    {"type":"get_step","step":42}
    Situation:  Emergency , Occupants dead:  0 , Occupants alive:  4
    01:08:32:00
    {"type":"get_step","step":43}
    Situation:  Emergency , Occupants dead:  0 , Occupants alive:  4
    01:08:33:00
    {"type":"get_step","step":44}
    Situation:  Emergency , Occupants dead:  0 , Occupants alive:  4
    01:08:34:00
    {"type":"get_step","step":45}
    Situation:  Emergency , Occupants dead:  0 , Occupants alive:  4
    01:08:35:00
    {"type":"get_step","step":46}
    Situation:  Emergency , Occupants dead:  0 , Occupants alive:  4
    01:08:36:00
    {"type":"get_step","step":47}
    Situation:  Emergency , Occupants dead:  0 , Occupants alive:  4
    01:08:37:00
    {"type":"get_step","step":48}
    Situation:  Emergency , Occupants dead:  0 , Occupants alive:  4
    01:08:38:00
    {"type":"get_step","step":49}
    Situation:  Emergency , Occupants dead:  1 , Occupants alive:  3
    01:08:39:00
    {"type":"get_step","step":50}
    Situation:  Emergency , Occupants dead:  1 , Occupants alive:  3
    01:08:40:00
    {"type":"get_step","step":51}
    Situation:  Emergency , Occupants dead:  2 , Occupants alive:  2
    01:08:41:00
    {"type":"get_step","step":52}
    Situation:  Emergency , Occupants dead:  2 , Occupants alive:  2
    01:08:42:00
    {"type":"get_step","step":53}
    Situation:  Emergency , Occupants dead:  2 , Occupants alive:  2
    01:08:43:00
    {"type":"get_step","step":54}
    Situation:  Emergency , Occupants dead:  2 , Occupants alive:  2
    Simulation terminated.


::

    3.1- Bacth mode.

.. code:: python

    import soba.run
    import sys
    
    #Fixed parameters during iterations
    fixed_params = {"width": cellW, "height": cellH, "jsonMap": jsonMap, "jsonsOccupants": jsonsOccupants, 'sebaConfiguration': sebaConfiguration}
    
    #Variable parameters to each iteration
    variable_params = {"seed": range(10, 500, 10)}
    
    
    sys.argv = []
    sys.argv.append("-1")
    sys.argv.append("-b")
    
    
    soba.run.run(SEBAModel, fixed_params, variable_params)


.. parsed-literal::

    0it [00:00, ?it/s]

.. parsed-literal::

    SOBA is running
    {'t1': datetime.datetime(2017, 10, 1, 8, 1, 26, 631730), 't2': datetime.datetime(2017, 10, 1, 8, 10, 14, 305579), 't3': datetime.datetime(2017, 10, 1, 8, 19, 29, 91994)}
    {'t1': datetime.datetime(2017, 10, 1, 8, 0, 59, 832323), 't2': datetime.datetime(2017, 10, 1, 8, 10, 12, 426719), 't3': datetime.datetime(2017, 10, 1, 8, 19, 45, 598289)}
    {'t1': datetime.datetime(2017, 10, 1, 8, 1, 5, 310232), 't2': datetime.datetime(2017, 10, 1, 8, 10, 2, 170971), 't3': datetime.datetime(2017, 10, 1, 8, 20, 0, 85829)}
    {'t1': datetime.datetime(2017, 10, 1, 8, 0, 56, 507996), 't2': datetime.datetime(2017, 10, 1, 8, 10, 8, 660524), 't3': datetime.datetime(2017, 10, 1, 8, 20, 24, 60747)}
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:07:51:00
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:07:52:00
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:07:53:00
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:07:54:00
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:07:55:00
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:07:56:00
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:07:57:00
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:07:58:00
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:07:59:00
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:00:00
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:01:00
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:02:00
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:03:00
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:04:00
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:05:00
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:06:00
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:07:00
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:08:00
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:09:00
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:10:00
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:11:00
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:12:00
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:13:00
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:14:00
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:15:00
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:16:00
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:17:00
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:18:00
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:19:00
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:20:00
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:21:00
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:22:00
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:23:00
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:24:00
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:25:00
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:26:00
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:27:00
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:28:00
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:29:00
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:30:00
    Situation:  Normal , Occupants dead:  0 , Occupants alive:  4
    01:08:31:00
    Situation:  Emergency , Occupants dead:  0 , Occupants alive:  4
    01:08:32:00
    Situation:  Emergency , Occupants dead:  0 , Occupants alive:  4
    01:08:33:00
    Situation:  Emergency , Occupants dead:  0 , Occupants alive:  4
    01:08:34:00
    Situation:  Emergency , Occupants dead:  0 , Occupants alive:  4
    01:08:35:00
    Situation:  Emergency , Occupants dead:  0 , Occupants alive:  4
    01:08:36:00
    Situation:  Emergency , Occupants dead:  0 , Occupants alive:  4
    01:08:37:00
    Situation:  Emergency , Occupants dead:  0 , Occupants alive:  4
    01:08:38:00
    Situation:  Emergency , Occupants dead:  0 , Occupants alive:  4
    01:08:39:00
    Situation:  Emergency , Occupants dead:  1 , Occupants alive:  3
    01:08:40:00
    Situation:  Emergency , Occupants dead:  1 , Occupants alive:  3
    Simulation terminated.


