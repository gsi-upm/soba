
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


.. parsed-literal::

    SOBA is running
    Interface starting at http://127.0.0.1:7777


::


    ---------------------------------------------------------------------------

    OSError                                   Traceback (most recent call last)

    <ipython-input-8-f0544481815d> in <module>()
          9 sys.argv.append("-v")
         10 
    ---> 11 soba.run.run(ModelExample, parameters, visualJS="example.js")
    

    /home/merinom/anaconda3/lib/python3.5/site-packages/soba/run.py in run(model, visualJS, back, iterations, *args)
         47                 if sys.argv[1] == '-v':
         48                         process(True)
    ---> 49                         visual.run(model, visual = visualJS, back = back, parameters = args[0])
         50                 elif sys.argv[1] == '-b':
         51                         parameters = args[0]


    /home/merinom/anaconda3/lib/python3.5/site-packages/soba/launchers/visual.py in run(model, parameters, visual, back)
         40 
         41         server.port = 7777
    ---> 42         server.launch()
    

    /home/merinom/anaconda3/lib/python3.5/site-packages/mesa/visualization/ModularVisualization.py in launch(self, port)
        320         url = 'http://127.0.0.1:{PORT}'.format(PORT=self.port)
        321         print('Interface starting at {url}'.format(url=url))
    --> 322         self.listen(self.port)
        323         webbrowser.open(url)
        324         tornado.autoreload.start()


    /home/merinom/anaconda3/lib/python3.5/site-packages/tornado/web.py in listen(self, port, address, **kwargs)
       1848         from tornado.httpserver import HTTPServer
       1849         server = HTTPServer(self, **kwargs)
    -> 1850         server.listen(port, address)
       1851         return server
       1852 


    /home/merinom/anaconda3/lib/python3.5/site-packages/tornado/tcpserver.py in listen(self, port, address)
        124         the `.IOLoop`.
        125         """
    --> 126         sockets = bind_sockets(port, address=address)
        127         self.add_sockets(sockets)
        128 


    /home/merinom/anaconda3/lib/python3.5/site-packages/tornado/netutil.py in bind_sockets(port, address, family, backlog, flags, reuse_port)
        192 
        193         sock.setblocking(0)
    --> 194         sock.bind(sockaddr)
        195         bound_port = sock.getsockname()[1]
        196         sock.listen(backlog)


    OSError: [Errno 98] Address already in use


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


.. parsed-literal::

    0it [00:00, ?it/s]

.. parsed-literal::

    SOBA is running
    01:08:01:00
    01:08:02:00
    01:08:03:00
    01:08:04:00
    01:08:05:00
    01:08:06:00
    01:08:07:00
    01:08:08:00
    01:08:09:00
    01:08:10:00
    01:08:11:00
    01:08:12:00
    01:08:13:00
    01:08:14:00
    01:08:15:00
    01:08:16:00
    01:08:17:00
    01:08:18:00
    01:08:19:00
    01:08:20:00
    01:08:21:00
    01:08:22:00
    01:08:23:00
    01:08:24:00
    01:08:25:00
    01:08:26:00
    01:08:27:00
    01:08:28:00
    01:08:29:00
    01:08:30:00
    01:08:31:00
    01:08:32:00
    01:08:33:00
    01:08:34:00
    01:08:35:00
    01:08:36:00
    01:08:37:00
    01:08:38:00
    01:08:39:00
    01:08:40:00
    01:08:41:00
    01:08:42:00
    01:08:43:00
    01:08:44:00
    01:08:45:00
    01:08:46:00
    01:08:47:00
    01:08:48:00
    01:08:49:00
    01:08:50:00
    01:08:51:00
    01:08:52:00
    01:08:53:00
    01:08:54:00
    01:08:55:00
    01:08:56:00
    01:08:57:00
    01:08:58:00
    01:08:59:00
    01:09:00:00
    01:09:01:00
    01:09:02:00
    01:09:03:00
    01:09:04:00
    01:09:05:00
    01:09:06:00
    01:09:07:00
    01:09:08:00
    01:09:09:00
    01:09:10:00
    01:09:11:00
    01:09:12:00
    01:09:13:00
    01:09:14:00
    01:09:15:00
    01:09:16:00
    01:09:17:00
    01:09:18:00
    01:09:19:00
    01:09:20:00
    01:09:21:00
    01:09:22:00
    01:09:23:00
    01:09:24:00
    01:09:25:00
    01:09:26:00
    01:09:27:00
    01:09:28:00
    01:09:29:00
    01:09:30:00
    01:09:31:00
    01:09:32:00
    01:09:33:00
    01:09:34:00
    01:09:35:00
    01:09:36:00
    01:09:37:00
    01:09:38:00
    01:09:39:00
    01:09:40:00
    01:09:41:00
    01:09:42:00
    01:09:43:00
    01:09:44:00
    01:09:45:00
    01:09:46:00
    01:09:47:00
    01:09:48:00
    01:09:49:00
    01:09:50:00
    01:09:51:00
    01:09:52:00
    01:09:53:00
    01:09:54:00
    01:09:55:00
    01:09:56:00
    01:09:57:00
    01:09:58:00
    01:09:59:00
    01:10:00:00
    01:10:01:00
    01:10:02:00
    01:10:03:00
    01:10:04:00
    01:10:05:00
    01:10:06:00
    01:10:07:00
    01:10:08:00
    01:10:09:00
    01:10:10:00
    01:10:11:00
    01:10:12:00
    01:10:13:00
    01:10:14:00
    01:10:15:00
    01:10:16:00
    01:10:17:00
    01:10:18:00
    01:10:19:00
    01:10:20:00
    01:10:21:00
    01:10:22:00
    01:10:23:00
    01:10:24:00
    01:10:25:00
    01:10:26:00
    01:10:27:00
    01:10:28:00
    01:10:29:00
    01:10:30:00
    01:10:31:00
    01:10:32:00
    01:10:33:00
    01:10:34:00
    01:10:35:00
    01:10:36:00
    01:10:37:00
    01:10:38:00
    01:10:39:00
    01:10:40:00
    01:10:41:00
    01:10:42:00
    01:10:43:00
    01:10:44:00
    01:10:45:00
    01:10:46:00
    01:10:47:00
    01:10:48:00
    01:10:49:00
    01:10:50:00
    01:10:51:00
    01:10:52:00
    01:10:53:00
    01:10:54:00
    01:10:55:00
    01:10:56:00
    01:10:57:00
    01:10:58:00
    01:10:59:00
    01:11:00:00
    01:11:01:00
    01:11:02:00
    01:11:03:00
    01:11:04:00
    01:11:05:00
    01:11:06:00
    01:11:07:00
    01:11:08:00
    01:11:09:00
    01:11:10:00
    01:11:11:00
    01:11:12:00
    01:11:13:00
    01:11:14:00
    01:11:15:00
    01:11:16:00
    01:11:17:00
    01:11:18:00
    01:11:19:00
    01:11:20:00
    01:11:21:00
    01:11:22:00
    01:11:23:00
    01:11:24:00
    01:11:25:00
    01:11:26:00
    01:11:27:00
    01:11:28:00
    01:11:29:00
    01:11:30:00
    01:11:31:00
    01:11:32:00
    01:11:33:00
    01:11:34:00
    01:11:35:00
    01:11:36:00
    01:11:37:00
    01:11:38:00
    01:11:39:00
    01:11:40:00
    01:11:41:00
    01:11:42:00
    01:11:43:00
    01:11:44:00
    01:11:45:00
    01:11:46:00
    01:11:47:00
    01:11:48:00
    01:11:49:00
    01:11:50:00
    01:11:51:00
    01:11:52:00


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


::


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-12-9c31cdd5317f> in <module>()
          2 import datetime as dt
          3 
    ----> 4 class ModelExample(RoomsModel):
          5 
          6     def __init__(self, width, height, jsonMap, jsonsOccupants, seed = int(time())):


    <ipython-input-12-9c31cdd5317f> in ModelExample()
          4 class ModelExample(RoomsModel):
          5 
    ----> 6     def __init__(self, width, height, jsonMap, jsonsOccupants, seed = int(time())):
          7         super().__init__(width, height, jsonMap, jsonsOccupants, seed = seed)
          8 


    NameError: name 'time' is not defined


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


.. parsed-literal::

    SOBA is running


::


    ---------------------------------------------------------------------------

    TypeError                                 Traceback (most recent call last)

    mtrand.pyx in mtrand.RandomState.seed (numpy/random/mtrand/mtrand.c:12129)()


    TypeError: 'datetime.datetime' object cannot be interpreted as an integer

    
    During handling of the above exception, another exception occurred:


    TypeError                                 Traceback (most recent call last)

    <ipython-input-11-2565ca2f8582> in <module>()
         10 
         11 parameters = {'width': cellW, 'height': cellH, 'jsonMap': jsonMap, 'jsonsOccupants': jsonsOccupants}
    ---> 12 soba.run.run(ModelExample, parameters, visualJS="example.js")
    

    /home/merinom/anaconda3/lib/python3.5/site-packages/soba/run.py in run(model, visualJS, back, iterations, *args)
         47                 if sys.argv[1] == '-v':
         48                         process(True)
    ---> 49                         visual.run(model, visual = visualJS, back = back, parameters = args[0])
         50                 elif sys.argv[1] == '-b':
         51                         parameters = args[0]


    /home/merinom/anaconda3/lib/python3.5/site-packages/soba/launchers/visual.py in run(model, parameters, visual, back)
         37                 server = ModularServer(model, [backEndVisualization, back], name="Simulation", model_params=parameters)
         38         else:
    ---> 39                 server = ModularServer(model, [backEndVisualization], name="Simulation", model_params=parameters)
         40 
         41         server.port = 7777


    /home/merinom/anaconda3/lib/python3.5/site-packages/mesa/visualization/ModularVisualization.py in __init__(self, model_cls, visualization_elements, name, model_params)
        274 
        275         self.model_kwargs = model_params
    --> 276         self.reset_model()
        277 
        278         # Initializing the application itself:


    /home/merinom/anaconda3/lib/python3.5/site-packages/mesa/visualization/ModularVisualization.py in reset_model(self)
        300                 model_params[key] = val
        301 
    --> 302         self.model = self.model_cls(**model_params)
        303 
        304     def render_model(self):


    <ipython-input-10-1d8b7a07559a> in __init__(self, width, height, jsonMap, jsonsOccupants, seed)
          5 
          6     def __init__(self, width, height, jsonMap, jsonsOccupants, seed = dt.datetime.now()):
    ----> 7         super().__init__(width, height, jsonMap, jsonsOccupants, seed = seed)
          8 
          9     def step(self):


    /home/merinom/anaconda3/lib/python3.5/site-packages/soba/models/roomsModel.py in __init__(self, width, height, jsonRooms, jsonsOccupants, seed, timeByStep)
         46 	"""
         47         def __init__(self, width, height, jsonRooms, jsonsOccupants, seed = int(time()), timeByStep = 60):
    ---> 48                 super().__init__(width, height, seed, timeByStep)
         49 		"""
         50                 Create a new RoomsModel object.


    /home/merinom/anaconda3/lib/python3.5/site-packages/soba/models/generalModel.py in __init__(self, width, height, seed, timeByStep)
         33 
         34         def __init__(self, width, height, seed = int(time()), timeByStep = 60):
    ---> 35                 super().__init__(seed)
         36 		"""
         37                 Create a new Model object.


    /home/merinom/anaconda3/lib/python3.5/site-packages/mesa/model.py in __init__(self, seed)
         31             self.seed = seed
         32         random.seed(seed)
    ---> 33         numpy.random.seed(seed)
         34 
         35         self.running = True


    mtrand.pyx in mtrand.RandomState.seed (numpy/random/mtrand/mtrand.c:12411)()


    TypeError: Cannot cast array from dtype('O') to dtype('int64') according to the rule 'safe'


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


.. parsed-literal::

    0it [00:00, ?it/s]

.. parsed-literal::

    SOBA is running
    01:08:01:00
    01:08:02:00
    01:08:03:00
    01:08:04:00
    01:08:05:00
    01:08:06:00
    01:08:07:00
    01:08:08:00
    01:08:09:00
    01:08:10:00
    01:08:11:00
    01:08:12:00
    01:08:13:00
    01:08:14:00
    01:08:15:00
    01:08:16:00
    01:08:17:00
    01:08:18:00
    01:08:19:00
    01:08:20:00
    01:08:21:00
    01:08:22:00
    01:08:23:00
    01:08:24:00
    01:08:25:00
    01:08:26:00
    01:08:27:00
    01:08:28:00
    01:08:29:00
    01:08:30:00
    01:08:31:00
    01:08:32:00
    01:08:33:00
    01:08:34:00
    01:08:35:00
    01:08:36:00
    01:08:37:00
    01:08:38:00
    01:08:39:00
    01:08:40:00
    01:08:41:00
    01:08:42:00
    01:08:43:00
    01:08:44:00
    01:08:45:00
    01:08:46:00
    01:08:47:00
    01:08:48:00
    01:08:49:00
    01:08:50:00
    01:08:51:00
    01:08:52:00
    01:08:53:00
    01:08:54:00
    01:08:55:00
    01:08:56:00
    01:08:57:00
    01:08:58:00
    01:08:59:00
    01:09:00:00
    01:09:01:00
    01:09:02:00
    01:09:03:00
    01:09:04:00
    01:09:05:00
    01:09:06:00
    01:09:07:00
    01:09:08:00
    01:09:09:00
    01:09:10:00
    01:09:11:00
    01:09:12:00
    01:09:13:00
    01:09:14:00
    01:09:15:00
    01:09:16:00
    01:09:17:00
    01:09:18:00
    01:09:19:00
    01:09:20:00
    01:09:21:00
    01:09:22:00
    01:09:23:00
    01:09:24:00
    01:09:25:00
    01:09:26:00
    01:09:27:00
    01:09:28:00
    01:09:29:00
    01:09:30:00
    01:09:31:00
    01:09:32:00
    01:09:33:00
    01:09:34:00
    01:09:35:00
    01:09:36:00
    01:09:37:00
    01:09:38:00
    01:09:39:00
    01:09:40:00
    01:09:41:00
    01:09:42:00
    01:09:43:00
    01:09:44:00
    01:09:45:00
    01:09:46:00
    01:09:47:00
    01:09:48:00
    01:09:49:00
    01:09:50:00
    01:09:51:00
    01:09:52:00
    01:09:53:00
    01:09:54:00
    01:09:55:00
    01:09:56:00
    01:09:57:00
    01:09:58:00
    01:09:59:00
    01:10:00:00
    01:10:01:00
    01:10:02:00
    01:10:03:00
    01:10:04:00
    01:10:05:00
    01:10:06:00
    01:10:07:00
    01:10:08:00
    01:10:09:00
    01:10:10:00
    01:10:11:00
    01:10:12:00
    01:10:13:00
    01:10:14:00
    01:10:15:00
    01:10:16:00
    01:10:17:00
    01:10:18:00
    01:10:19:00
    01:10:20:00
    01:10:21:00
    01:10:22:00
    01:10:23:00
    01:10:24:00
    01:10:25:00
    01:10:26:00
    01:10:27:00
    01:10:28:00
    01:10:29:00
    01:10:30:00
    01:10:31:00
    01:10:32:00
    01:10:33:00
    01:10:34:00
    01:10:35:00
    01:10:36:00
    01:10:37:00
    01:10:38:00
    01:10:39:00
    01:10:40:00
    01:10:41:00
    01:10:42:00
    01:10:43:00
    01:10:44:00
    01:10:45:00
    01:10:46:00
    01:10:47:00
    01:10:48:00
    01:10:49:00
    01:10:50:00
    01:10:51:00
    01:10:52:00
    01:10:53:00
    01:10:54:00
    01:10:55:00
    01:10:56:00
    01:10:57:00
    01:10:58:00
    01:10:59:00
    01:11:00:00
    01:11:01:00
    01:11:02:00
    01:11:03:00
    01:11:04:00
    01:11:05:00
    01:11:06:00
    01:11:07:00
    01:11:08:00
    01:11:09:00
    01:11:10:00
    01:11:11:00
    01:11:12:00
    01:11:13:00
    01:11:14:00
    01:11:15:00
    01:11:16:00
    01:11:17:00
    01:11:18:00
    01:11:19:00
    01:11:20:00
    01:11:21:00
    01:11:22:00
    01:11:23:00
    01:11:24:00
    01:11:25:00
    01:11:26:00
    01:11:27:00
    01:11:28:00
    01:11:29:00
    01:11:30:00
    01:11:31:00
    01:11:32:00
    01:11:33:00
    01:11:34:00
    01:11:35:00
    01:11:36:00
    01:11:37:00
    01:11:38:00
    01:11:39:00
    01:11:40:00
    01:11:41:00
    01:11:42:00
    01:11:43:00
    01:11:44:00
    01:11:45:00
    01:11:46:00
    01:11:47:00
    01:11:48:00
    01:11:49:00
    01:11:50:00
    01:11:51:00
    01:11:52:00
    01:11:53:00
    01:11:54:00
    01:11:55:00
    01:11:56:00
    01:11:57:00
    01:11:58:00
    01:11:59:00
    01:12:00:00
    01:12:01:00
    01:12:02:00
    01:12:03:00
    01:12:04:00
    01:12:05:00
    01:12:06:00
    01:12:07:00
    01:12:08:00
    01:12:09:00
    01:12:10:00
    01:12:11:00
    01:12:12:00
    01:12:13:00
    01:12:14:00
    01:12:15:00
    01:12:16:00
    01:12:17:00
    01:12:18:00
    01:12:19:00
    01:12:20:00
    01:12:21:00
    01:12:22:00
    01:12:23:00
    01:12:24:00
    01:12:25:00
    01:12:26:00
    01:12:27:00
    01:12:28:00
    01:12:29:00
    01:12:30:00
    01:12:31:00
    01:12:32:00
    01:12:33:00
    01:12:34:00
    01:12:35:00
    01:12:36:00
    01:12:37:00
    01:12:38:00
    01:12:39:00
    01:12:40:00
    01:12:41:00
    01:12:42:00
    01:12:43:00
    01:12:44:00
    01:12:45:00
    01:12:46:00
    01:12:47:00
    01:12:48:00
    01:12:49:00
    01:12:50:00
    01:12:51:00
    01:12:52:00
    01:12:53:00
    01:12:54:00
    01:12:55:00
    01:12:56:00
    01:12:57:00
    01:12:58:00
    01:12:59:00
    01:13:00:00
    01:13:01:00
    01:13:02:00
    01:13:03:00
    01:13:04:00
    01:13:05:00
    01:13:06:00
    01:13:07:00
    01:13:08:00
    01:13:09:00
    01:13:10:00
    01:13:11:00
    01:13:12:00
    01:13:13:00
    01:13:14:00
    01:13:15:00
    01:13:16:00
    01:13:17:00
    01:13:18:00
    01:13:19:00
    01:13:20:00
    01:13:21:00
    01:13:22:00
    01:13:23:00
    01:13:24:00
    01:13:25:00
    01:13:26:00
    01:13:27:00
    01:13:28:00
    01:13:29:00
    01:13:30:00
    01:13:31:00
    01:13:32:00
    01:13:33:00
    01:13:34:00
    01:13:35:00
    01:13:36:00
    01:13:37:00
    01:13:38:00
    01:13:39:00
    01:13:40:00
    01:13:41:00
    01:13:42:00
    01:13:43:00
    01:13:44:00
    01:13:45:00
    01:13:46:00
    01:13:47:00
    01:13:48:00
    01:13:49:00
    01:13:50:00
    01:13:51:00
    01:13:52:00
    01:13:53:00
    01:13:54:00
    01:13:55:00
    01:13:56:00
    01:13:57:00
    01:13:58:00
    01:13:59:00
    01:14:00:00
    01:14:01:00
    01:14:02:00
    01:14:03:00
    01:14:04:00
    01:14:05:00
    01:14:06:00
    01:14:07:00
    01:14:08:00
    01:14:09:00
    01:14:10:00
    01:14:11:00
    01:14:12:00
    01:14:13:00
    01:14:14:00
    01:14:15:00
    01:14:16:00
    01:14:17:00
    01:14:18:00
    01:14:19:00
    01:14:20:00
    01:14:21:00
    01:14:22:00
    01:14:23:00
    01:14:24:00
    01:14:25:00
    01:14:26:00
    01:14:27:00
    01:14:28:00
    01:14:29:00
    01:14:30:00
    01:14:31:00
    01:14:32:00
    01:14:33:00
    01:14:34:00
    01:14:35:00
    01:14:36:00
    01:14:37:00
    01:14:38:00
    01:14:39:00
    01:14:40:00
    01:14:41:00
    01:14:42:00
    01:14:43:00
    01:14:44:00
    01:14:45:00
    01:14:46:00
    01:14:47:00
    01:14:48:00
    01:14:49:00
    01:14:50:00
    01:14:51:00
    01:14:52:00
    01:14:53:00
    01:14:54:00
    01:14:55:00
    01:14:56:00
    01:14:57:00
    01:14:58:00
    01:14:59:00
    01:15:00:00
    01:15:01:00
    01:15:02:00
    01:15:03:00
    01:15:04:00
    01:15:05:00
    01:15:06:00
    01:15:07:00
    01:15:08:00
    01:15:09:00
    01:15:10:00
    01:15:11:00
    01:15:12:00
    01:15:13:00
    01:15:14:00
    01:15:15:00
    01:15:16:00
    01:15:17:00
    01:15:18:00
    01:15:19:00
    01:15:20:00
    01:15:21:00
    01:15:22:00
    01:15:23:00
    01:15:24:00
    01:15:25:00
    01:15:26:00
    01:15:27:00
    01:15:28:00
    01:15:29:00
    01:15:30:00
    01:15:31:00
    01:15:32:00
    01:15:33:00
    01:15:34:00
    01:15:35:00
    01:15:36:00
    01:15:37:00
    01:15:38:00
    01:15:39:00
    01:15:40:00
    01:15:41:00
    01:15:42:00
    01:15:43:00
    01:15:44:00
    01:15:45:00
    01:15:46:00
    01:15:47:00
    01:15:48:00
    01:15:49:00
    01:15:50:00
    01:15:51:00
    01:15:52:00
    01:15:53:00
    01:15:54:00
    01:15:55:00
    01:15:56:00
    01:15:57:00
    01:15:58:00
    01:15:59:00
    01:16:00:00
    01:16:01:00
    01:16:02:00
    01:16:03:00
    01:16:04:00
    01:16:05:00
    01:16:06:00
    01:16:07:00
    01:16:08:00
    01:16:09:00
    01:16:10:00
    01:16:11:00
    01:16:12:00
    01:16:13:00
    01:16:14:00
    01:16:15:00
    01:16:16:00
    01:16:17:00
    01:16:18:00
    01:16:19:00
    01:16:20:00
    01:16:21:00
    01:16:22:00
    01:16:23:00
    01:16:24:00
    01:16:25:00
    01:16:26:00
    01:16:27:00
    01:16:28:00
    01:16:29:00
    01:16:30:00
    01:16:31:00
    01:16:32:00
    01:16:33:00
    01:16:34:00
    01:16:35:00
    01:16:36:00
    01:16:37:00
    01:16:38:00
    01:16:39:00
    01:16:40:00
    01:16:41:00
    01:16:42:00
    01:16:43:00
    01:16:44:00
    01:16:45:00
    01:16:46:00
    01:16:47:00
    01:16:48:00
    01:16:49:00
    01:16:50:00
    01:16:51:00
    01:16:52:00
    01:16:53:00
    01:16:54:00
    01:16:55:00
    01:16:56:00
    01:16:57:00
    01:16:58:00
    01:16:59:00
    01:17:00:00
    01:17:01:00
    01:17:02:00
    01:17:03:00
    01:17:04:00
    01:17:05:00
    01:17:06:00
    01:17:07:00
    01:17:08:00
    01:17:09:00
    01:17:10:00
    01:17:11:00
    01:17:12:00
    01:17:13:00
    01:17:14:00
    01:17:15:00
    01:17:16:00
    01:17:17:00
    01:17:18:00
    01:17:19:00
    01:17:20:00
    01:17:21:00
    01:17:22:00
    01:17:23:00
    01:17:24:00
    01:17:25:00
    01:17:26:00
    01:17:27:00
    01:17:28:00
    01:17:29:00
    01:17:30:00
    01:17:31:00
    01:17:32:00
    01:17:33:00
    01:17:34:00
    01:17:35:00
    01:17:36:00
    01:17:37:00
    01:17:38:00
    01:17:39:00
    01:17:40:00
    01:17:41:00
    01:17:42:00
    01:17:43:00
    01:17:44:00
    01:17:45:00
    01:17:46:00
    01:17:47:00
    01:17:48:00
    01:17:49:00
    01:17:50:00
    01:17:51:00
    01:17:52:00
    01:17:53:00
    01:17:54:00
    01:17:55:00
    01:17:56:00
    01:17:57:00
    01:17:58:00
    01:17:59:00
    01:18:00:00
    01:18:01:00
    01:18:02:00
    01:18:03:00
    01:18:04:00
    01:18:05:00
    01:18:06:00
    01:18:07:00
    01:18:08:00
    01:18:09:00
    01:18:10:00
    01:18:11:00
    01:18:12:00
    01:18:13:00
    01:18:14:00
    01:18:15:00
    01:18:16:00
    01:18:17:00
    01:18:18:00
    01:18:19:00
    01:18:20:00
    01:18:21:00
    01:18:22:00
    01:18:23:00
    01:18:24:00
    01:18:25:00
    01:18:26:00
    01:18:27:00
    01:18:28:00
    01:18:29:00
    01:18:30:00
    01:18:31:00
    01:18:32:00
    01:18:33:00
    01:18:34:00
    01:18:35:00
    01:18:36:00
    01:18:37:00
    01:18:38:00
    01:18:39:00
    01:18:40:00
    01:18:41:00
    01:18:42:00
    01:18:43:00
    01:18:44:00
    01:18:45:00
    01:18:46:00
    01:18:47:00
    01:18:48:00
    01:18:49:00
    01:18:50:00
    01:18:51:00
    01:18:52:00
    01:18:53:00
    01:18:54:00
    01:18:55:00
    01:18:56:00
    01:18:57:00
    01:18:58:00
    01:18:59:00
    01:19:00:00
    01:19:01:00
    01:19:02:00
    01:19:03:00
    01:19:04:00
    01:19:05:00
    01:19:06:00
    01:19:07:00
    01:19:08:00
    01:19:09:00
    01:19:10:00
    01:19:11:00
    01:19:12:00
    01:19:13:00
    01:19:14:00
    01:19:15:00
    01:19:16:00
    01:19:17:00
    01:19:18:00
    01:19:19:00
    01:19:20:00
    01:19:21:00
    01:19:22:00
    01:19:23:00
    01:19:24:00
    01:19:25:00
    01:19:26:00
    01:19:27:00
    01:19:28:00
    01:19:29:00
    01:19:30:00
    01:19:31:00
    01:19:32:00
    01:19:33:00
    01:19:34:00
    01:19:35:00
    01:19:36:00
    01:19:37:00
    01:19:38:00
    01:19:39:00
    01:19:40:00
    01:19:41:00
    01:19:42:00
    01:19:43:00
    01:19:44:00
    01:19:45:00
    01:19:46:00
    01:19:47:00
    01:19:48:00
    01:19:49:00
    01:19:50:00
    01:19:51:00
    01:19:52:00
    01:19:53:00
    01:19:54:00
    01:19:55:00
    01:19:56:00
    01:19:57:00
    01:19:58:00
    01:19:59:00
    01:20:00:00
    02:08:00:00
    02:08:01:00
    02:08:02:00
    02:08:03:00
    02:08:04:00
    02:08:05:00
    02:08:06:00
    02:08:07:00
    02:08:08:00
    02:08:09:00
    02:08:10:00
    02:08:11:00
    02:08:12:00
    02:08:13:00
    02:08:14:00
    02:08:15:00
    02:08:16:00
    02:08:17:00
    02:08:18:00
    02:08:19:00
    02:08:20:00
    02:08:21:00
    02:08:22:00
    02:08:23:00
    02:08:24:00
    02:08:25:00
    02:08:26:00
    02:08:27:00
    02:08:28:00
    02:08:29:00
    02:08:30:00
    02:08:31:00
    02:08:32:00
    02:08:33:00
    02:08:34:00
    02:08:35:00
    02:08:36:00
    02:08:37:00
    02:08:38:00
    02:08:39:00
    02:08:40:00
    02:08:41:00
    02:08:42:00
    02:08:43:00
    02:08:44:00
    02:08:45:00
    02:08:46:00
    02:08:47:00
    02:08:48:00
    02:08:49:00
    02:08:50:00
    02:08:51:00
    02:08:52:00
    02:08:53:00
    02:08:54:00
    02:08:55:00
    02:08:56:00
    02:08:57:00
    02:08:58:00
    02:08:59:00
    02:09:00:00
    02:09:01:00
    02:09:02:00
    02:09:03:00
    02:09:04:00
    02:09:05:00
    02:09:06:00
    02:09:07:00
    02:09:08:00
    02:09:09:00
    02:09:10:00
    02:09:11:00
    02:09:12:00
    02:09:13:00
    02:09:14:00
    02:09:15:00
    02:09:16:00
    02:09:17:00
    02:09:18:00
    02:09:19:00
    02:09:20:00
    02:09:21:00
    02:09:22:00
    02:09:23:00
    02:09:24:00
    02:09:25:00
    02:09:26:00
    02:09:27:00
    02:09:28:00
    02:09:29:00
    02:09:30:00
    02:09:31:00
    02:09:32:00
    02:09:33:00
    02:09:34:00
    02:09:35:00
    02:09:36:00
    02:09:37:00
    02:09:38:00
    02:09:39:00
    02:09:40:00
    02:09:41:00
    02:09:42:00
    02:09:43:00
    02:09:44:00
    02:09:45:00
    02:09:46:00
    02:09:47:00
    02:09:48:00
    02:09:49:00
    02:09:50:00
    02:09:51:00
    02:09:52:00
    02:09:53:00
    02:09:54:00
    02:09:55:00
    02:09:56:00
    02:09:57:00
    02:09:58:00
    02:09:59:00
    02:10:00:00
    02:10:01:00
    02:10:02:00
    02:10:03:00
    02:10:04:00
    02:10:05:00
    02:10:06:00
    02:10:07:00
    02:10:08:00
    02:10:09:00
    02:10:10:00
    02:10:11:00
    02:10:12:00
    02:10:13:00
    02:10:14:00
    02:10:15:00
    02:10:16:00
    02:10:17:00
    02:10:18:00
    02:10:19:00
    02:10:20:00
    02:10:21:00
    02:10:22:00
    02:10:23:00
    02:10:24:00
    02:10:25:00
    02:10:26:00
    02:10:27:00
    02:10:28:00
    02:10:29:00
    02:10:30:00
    02:10:31:00
    02:10:32:00
    02:10:33:00
    02:10:34:00
    02:10:35:00
    02:10:36:00
    02:10:37:00
    02:10:38:00
    02:10:39:00
    02:10:40:00
    02:10:41:00
    02:10:42:00
    02:10:43:00
    02:10:44:00
    02:10:45:00
    02:10:46:00
    02:10:47:00
    02:10:48:00
    02:10:49:00
    02:10:50:00
    02:10:51:00
    02:10:52:00
    02:10:53:00
    02:10:54:00
    02:10:55:00
    02:10:56:00
    02:10:57:00
    02:10:58:00
    02:10:59:00
    02:11:00:00
    02:11:01:00
    02:11:02:00
    02:11:03:00
    02:11:04:00
    02:11:05:00
    02:11:06:00
    02:11:07:00
    02:11:08:00
    02:11:09:00
    02:11:10:00
    02:11:11:00
    02:11:12:00
    02:11:13:00
    02:11:14:00
    02:11:15:00
    02:11:16:00
    02:11:17:00
    02:11:18:00
    02:11:19:00
    02:11:20:00
    02:11:21:00
    02:11:22:00
    02:11:23:00
    02:11:24:00
    02:11:25:00
    02:11:26:00
    02:11:27:00
    02:11:28:00
    02:11:29:00
    02:11:30:00
    02:11:31:00
    02:11:32:00
    02:11:33:00
    02:11:34:00
    02:11:35:00
    02:11:36:00
    02:11:37:00
    02:11:38:00
    02:11:39:00
    02:11:40:00
    02:11:41:00
    02:11:42:00
    02:11:43:00
    02:11:44:00
    02:11:45:00
    02:11:46:00
    02:11:47:00
    02:11:48:00
    02:11:49:00
    02:11:50:00
    02:11:51:00
    02:11:52:00
    02:11:53:00
    02:11:54:00
    02:11:55:00
    02:11:56:00
    02:11:57:00
    02:11:58:00
    02:11:59:00
    02:12:00:00
    02:12:01:00
    02:12:02:00
    02:12:03:00
    02:12:04:00
    02:12:05:00
    02:12:06:00
    02:12:07:00
    02:12:08:00
    02:12:09:00
    02:12:10:00
    02:12:11:00
    02:12:12:00
    02:12:13:00
    02:12:14:00
    02:12:15:00
    02:12:16:00
    02:12:17:00
    02:12:18:00
    02:12:19:00
    02:12:20:00
    02:12:21:00
    02:12:22:00
    02:12:23:00
    02:12:24:00
    02:12:25:00
    02:12:26:00
    02:12:27:00
    02:12:28:00
    02:12:29:00
    02:12:30:00
    02:12:31:00
    02:12:32:00
    02:12:33:00
    02:12:34:00
    02:12:35:00
    02:12:36:00
    02:12:37:00
    02:12:38:00
    02:12:39:00
    02:12:40:00
    02:12:41:00
    02:12:42:00
    02:12:43:00
    02:12:44:00
    02:12:45:00
    02:12:46:00
    02:12:47:00
    02:12:48:00
    02:12:49:00
    02:12:50:00
    02:12:51:00
    02:12:52:00
    02:12:53:00
    02:12:54:00
    02:12:55:00
    02:12:56:00
    02:12:57:00
    02:12:58:00
    02:12:59:00
    02:13:00:00
    02:13:01:00
    02:13:02:00
    02:13:03:00
    02:13:04:00
    02:13:05:00
    02:13:06:00
    02:13:07:00
    02:13:08:00
    02:13:09:00
    02:13:10:00
    02:13:11:00
    02:13:12:00
    02:13:13:00
    02:13:14:00
    02:13:15:00
    02:13:16:00
    02:13:17:00
    02:13:18:00
    02:13:19:00
    02:13:20:00
    02:13:21:00
    02:13:22:00
    02:13:23:00
    02:13:24:00
    02:13:25:00
    02:13:26:00
    02:13:27:00
    02:13:28:00
    02:13:29:00
    02:13:30:00
    02:13:31:00
    02:13:32:00
    02:13:33:00
    02:13:34:00
    02:13:35:00
    02:13:36:00
    02:13:37:00
    02:13:38:00
    02:13:39:00
    02:13:40:00
    02:13:41:00
    02:13:42:00
    02:13:43:00
    02:13:44:00
    02:13:45:00
    02:13:46:00
    02:13:47:00
    02:13:48:00
    02:13:49:00
    02:13:50:00
    02:13:51:00
    02:13:52:00
    02:13:53:00
    02:13:54:00
    02:13:55:00
    02:13:56:00
    02:13:57:00
    02:13:58:00
    02:13:59:00
    02:14:00:00
    02:14:01:00
    02:14:02:00
    02:14:03:00
    02:14:04:00
    02:14:05:00
    02:14:06:00
    02:14:07:00
    02:14:08:00
    02:14:09:00
    02:14:10:00
    02:14:11:00
    02:14:12:00
    02:14:13:00
    02:14:14:00
    02:14:15:00
    02:14:16:00
    02:14:17:00
    02:14:18:00
    02:14:19:00
    02:14:20:00
    02:14:21:00
    02:14:22:00
    02:14:23:00
    02:14:24:00
    02:14:25:00
    02:14:26:00
    02:14:27:00
    02:14:28:00
    02:14:29:00
    02:14:30:00
    02:14:31:00
    02:14:32:00
    02:14:33:00
    02:14:34:00
    02:14:35:00
    02:14:36:00
    02:14:37:00
    02:14:38:00
    02:14:39:00
    02:14:40:00
    02:14:41:00
    02:14:42:00
    02:14:43:00
    02:14:44:00
    02:14:45:00
    02:14:46:00
    02:14:47:00
    02:14:48:00
    02:14:49:00
    02:14:50:00
    02:14:51:00
    02:14:52:00
    02:14:53:00
    02:14:54:00
    02:14:55:00
    02:14:56:00
    02:14:57:00
    02:14:58:00
    02:14:59:00
    02:15:00:00
    02:15:01:00
    02:15:02:00
    02:15:03:00
    02:15:04:00
    02:15:05:00
    02:15:06:00
    02:15:07:00
    02:15:08:00
    02:15:09:00
    02:15:10:00
    02:15:11:00
    02:15:12:00
    02:15:13:00
    02:15:14:00
    02:15:15:00
    02:15:16:00
    02:15:17:00
    02:15:18:00
    02:15:19:00
    02:15:20:00
    02:15:21:00
    02:15:22:00
    02:15:23:00
    02:15:24:00
    02:15:25:00
    02:15:26:00
    02:15:27:00
    02:15:28:00
    02:15:29:00
    02:15:30:00
    02:15:31:00
    02:15:32:00
    02:15:33:00
    02:15:34:00
    02:15:35:00
    02:15:36:00
    02:15:37:00
    02:15:38:00
    02:15:39:00
    02:15:40:00
    02:15:41:00
    02:15:42:00
    02:15:43:00
    02:15:44:00
    02:15:45:00
    02:15:46:00
    02:15:47:00
    02:15:48:00
    02:15:49:00
    02:15:50:00
    02:15:51:00
    02:15:52:00
    02:15:53:00
    02:15:54:00
    02:15:55:00
    02:15:56:00
    02:15:57:00
    02:15:58:00
    02:15:59:00
    02:16:00:00
    02:16:01:00
    02:16:02:00
    02:16:03:00
    02:16:04:00
    02:16:05:00
    02:16:06:00
    02:16:07:00
    02:16:08:00
    02:16:09:00
    02:16:10:00
    02:16:11:00
    02:16:12:00
    02:16:13:00
    02:16:14:00
    02:16:15:00
    02:16:16:00
    02:16:17:00
    02:16:18:00
    02:16:19:00
    02:16:20:00
    02:16:21:00
    02:16:22:00
    02:16:23:00
    02:16:24:00
    02:16:25:00
    02:16:26:00
    02:16:27:00
    02:16:28:00
    02:16:29:00
    02:16:30:00
    02:16:31:00
    02:16:32:00
    02:16:33:00
    02:16:34:00
    02:16:35:00
    02:16:36:00
    02:16:37:00
    02:16:38:00
    02:16:39:00
    02:16:40:00
    02:16:41:00
    02:16:42:00
    02:16:43:00
    02:16:44:00
    02:16:45:00
    02:16:46:00
    02:16:47:00
    02:16:48:00
    02:16:49:00
    02:16:50:00
    02:16:51:00
    02:16:52:00
    02:16:53:00
    02:16:54:00
    02:16:55:00
    02:16:56:00
    02:16:57:00
    02:16:58:00
    02:16:59:00
    02:17:00:00
    02:17:01:00
    02:17:02:00
    02:17:03:00
    02:17:04:00
    02:17:05:00
    02:17:06:00
    02:17:07:00
    02:17:08:00
    02:17:09:00
    02:17:10:00
    02:17:11:00
    02:17:12:00
    02:17:13:00
    02:17:14:00
    02:17:15:00
    02:17:16:00
    02:17:17:00
    02:17:18:00
    02:17:19:00
    02:17:20:00
    02:17:21:00
    02:17:22:00
    02:17:23:00
    02:17:24:00
    02:17:25:00
    02:17:26:00
    02:17:27:00
    02:17:28:00
    02:17:29:00
    02:17:30:00
    02:17:31:00
    02:17:32:00
    02:17:33:00
    02:17:34:00
    02:17:35:00
    02:17:36:00
    02:17:37:00
    02:17:38:00
    02:17:39:00
    02:17:40:00
    02:17:41:00
    02:17:42:00
    02:17:43:00
    02:17:44:00
    02:17:45:00
    02:17:46:00
    02:17:47:00
    02:17:48:00
    02:17:49:00
    02:17:50:00
    02:17:51:00
    02:17:52:00
    02:17:53:00
    02:17:54:00
    02:17:55:00
    02:17:56:00
    02:17:57:00
    02:17:58:00
    02:17:59:00
    02:18:00:00
    02:18:01:00
    02:18:02:00
    02:18:03:00
    02:18:04:00
    02:18:05:00
    02:18:06:00
    02:18:07:00
    02:18:08:00
    02:18:09:00
    02:18:10:00
    02:18:11:00
    02:18:12:00
    02:18:13:00
    02:18:14:00
    02:18:15:00
    02:18:16:00
    02:18:17:00
    02:18:18:00
    02:18:19:00
    02:18:20:00
    02:18:21:00
    02:18:22:00
    02:18:23:00
    02:18:24:00
    02:18:25:00
    02:18:26:00
    02:18:27:00
    02:18:28:00
    02:18:29:00
    02:18:30:00
    02:18:31:00
    02:18:32:00
    02:18:33:00
    02:18:34:00
    02:18:35:00
    02:18:36:00
    02:18:37:00
    02:18:38:00
    02:18:39:00
    02:18:40:00
    02:18:41:00
    02:18:42:00
    02:18:43:00
    02:18:44:00
    02:18:45:00
    02:18:46:00
    02:18:47:00
    02:18:48:00
    02:18:49:00
    02:18:50:00
    02:18:51:00
    02:18:52:00
    02:18:53:00
    02:18:54:00
    02:18:55:00
    02:18:56:00
    02:18:57:00
    02:18:58:00
    02:18:59:00
    02:19:00:00
    02:19:01:00
    02:19:02:00
    02:19:03:00
    02:19:04:00
    02:19:05:00
    02:19:06:00
    02:19:07:00
    02:19:08:00
    02:19:09:00
    02:19:10:00
    02:19:11:00
    02:19:12:00
    02:19:13:00
    02:19:14:00
    02:19:15:00
    02:19:16:00
    02:19:17:00
    02:19:18:00
    02:19:19:00
    02:19:20:00
    02:19:21:00
    02:19:22:00
    02:19:23:00
    02:19:24:00
    02:19:25:00
    02:19:26:00
    02:19:27:00
    02:19:28:00
    02:19:29:00
    02:19:30:00
    02:19:31:00
    02:19:32:00
    02:19:33:00
    02:19:34:00
    02:19:35:00
    02:19:36:00
    02:19:37:00
    02:19:38:00
    02:19:39:00
    02:19:40:00
    02:19:41:00
    02:19:42:00
    02:19:43:00
    02:19:44:00
    02:19:45:00
    02:19:46:00
    02:19:47:00
    02:19:48:00
    02:19:49:00
    02:19:50:00
    02:19:51:00
    02:19:52:00
    02:19:53:00
    02:19:54:00
    02:19:55:00
    02:19:56:00
    02:19:57:00
    02:19:58:00
    02:19:59:00
    02:20:00:00
    03:08:00:00
    03:08:01:00
    03:08:02:00
    03:08:03:00
    03:08:04:00
    03:08:05:00
    03:08:06:00
    03:08:07:00
    03:08:08:00
    03:08:09:00
    03:08:10:00
    03:08:11:00
    03:08:12:00
    03:08:13:00
    03:08:14:00
    03:08:15:00
    03:08:16:00
    03:08:17:00
    03:08:18:00
    03:08:19:00
    03:08:20:00
    03:08:21:00
    03:08:22:00
    03:08:23:00
    03:08:24:00
    03:08:25:00
    03:08:26:00
    03:08:27:00
    03:08:28:00
    03:08:29:00
    03:08:30:00
    03:08:31:00
    03:08:32:00
    03:08:33:00
    03:08:34:00
    03:08:35:00
    03:08:36:00
    03:08:37:00
    03:08:38:00
    03:08:39:00
    03:08:40:00
    03:08:41:00
    03:08:42:00
    03:08:43:00
    03:08:44:00
    03:08:45:00
    03:08:46:00
    03:08:47:00
    03:08:48:00
    03:08:49:00
    03:08:50:00
    03:08:51:00
    03:08:52:00
    03:08:53:00
    03:08:54:00
    03:08:55:00
    03:08:56:00
    03:08:57:00
    03:08:58:00
    03:08:59:00
    03:09:00:00
    03:09:01:00
    03:09:02:00
    03:09:03:00
    03:09:04:00
    03:09:05:00
    03:09:06:00
    03:09:07:00
    03:09:08:00
    03:09:09:00
    03:09:10:00
    03:09:11:00
    03:09:12:00
    03:09:13:00
    03:09:14:00
    03:09:15:00
    03:09:16:00
    03:09:17:00
    03:09:18:00
    03:09:19:00
    03:09:20:00
    03:09:21:00
    03:09:22:00
    03:09:23:00
    03:09:24:00
    03:09:25:00
    03:09:26:00
    03:09:27:00
    03:09:28:00
    03:09:29:00
    03:09:30:00
    03:09:31:00
    03:09:32:00
    03:09:33:00
    03:09:34:00
    03:09:35:00
    03:09:36:00
    03:09:37:00
    03:09:38:00
    03:09:39:00
    03:09:40:00
    03:09:41:00
    03:09:42:00
    03:09:43:00
    03:09:44:00
    03:09:45:00
    03:09:46:00
    03:09:47:00
    03:09:48:00
    03:09:49:00
    03:09:50:00
    03:09:51:00
    03:09:52:00
    03:09:53:00
    03:09:54:00
    03:09:55:00
    03:09:56:00
    03:09:57:00
    03:09:58:00
    03:09:59:00
    03:10:00:00
    03:10:01:00
    03:10:02:00
    03:10:03:00
    03:10:04:00
    03:10:05:00
    03:10:06:00
    03:10:07:00
    03:10:08:00
    03:10:09:00
    03:10:10:00
    03:10:11:00
    03:10:12:00
    03:10:13:00
    03:10:14:00
    03:10:15:00
    03:10:16:00
    03:10:17:00
    03:10:18:00
    03:10:19:00
    03:10:20:00
    03:10:21:00
    03:10:22:00
    03:10:23:00
    03:10:24:00
    03:10:25:00
    03:10:26:00
    03:10:27:00
    03:10:28:00
    03:10:29:00
    03:10:30:00
    03:10:31:00
    03:10:32:00
    03:10:33:00
    03:10:34:00
    03:10:35:00
    03:10:36:00
    03:10:37:00
    03:10:38:00
    03:10:39:00
    03:10:40:00
    03:10:41:00
    03:10:42:00
    03:10:43:00
    03:10:44:00
    03:10:45:00
    03:10:46:00
    03:10:47:00
    03:10:48:00
    03:10:49:00
    03:10:50:00
    03:10:51:00
    03:10:52:00
    03:10:53:00
    03:10:54:00
    03:10:55:00
    03:10:56:00
    03:10:57:00
    03:10:58:00
    03:10:59:00
    03:11:00:00
    03:11:01:00
    03:11:02:00
    03:11:03:00
    03:11:04:00
    03:11:05:00
    03:11:06:00
    03:11:07:00
    03:11:08:00
    03:11:09:00
    03:11:10:00
    03:11:11:00
    03:11:12:00
    03:11:13:00
    03:11:14:00
    03:11:15:00
    03:11:16:00
    03:11:17:00
    03:11:18:00
    03:11:19:00
    03:11:20:00
    03:11:21:00
    03:11:22:00
    03:11:23:00
    03:11:24:00
    03:11:25:00
    03:11:26:00
    03:11:27:00
    03:11:28:00
    03:11:29:00
    03:11:30:00
    03:11:31:00
    03:11:32:00
    03:11:33:00
    03:11:34:00
    03:11:35:00
    03:11:36:00
    03:11:37:00
    03:11:38:00
    03:11:39:00
    03:11:40:00
    03:11:41:00
    03:11:42:00
    03:11:43:00
    03:11:44:00
    03:11:45:00
    03:11:46:00
    03:11:47:00
    03:11:48:00
    03:11:49:00
    03:11:50:00
    03:11:51:00
    03:11:52:00
    03:11:53:00
    03:11:54:00
    03:11:55:00
    03:11:56:00
    03:11:57:00
    03:11:58:00
    03:11:59:00
    03:12:00:00
    03:12:01:00
    03:12:02:00
    03:12:03:00
    03:12:04:00
    03:12:05:00
    03:12:06:00
    03:12:07:00
    03:12:08:00
    03:12:09:00
    03:12:10:00
    03:12:11:00
    03:12:12:00
    03:12:13:00
    03:12:14:00
    03:12:15:00
    03:12:16:00
    03:12:17:00
    03:12:18:00
    03:12:19:00
    03:12:20:00
    03:12:21:00
    03:12:22:00
    03:12:23:00
    03:12:24:00
    03:12:25:00
    03:12:26:00
    03:12:27:00
    03:12:28:00
    03:12:29:00
    03:12:30:00
    03:12:31:00
    03:12:32:00
    03:12:33:00
    03:12:34:00
    03:12:35:00
    03:12:36:00
    03:12:37:00
    03:12:38:00
    03:12:39:00
    03:12:40:00
    03:12:41:00
    03:12:42:00
    03:12:43:00
    03:12:44:00
    03:12:45:00
    03:12:46:00
    03:12:47:00
    03:12:48:00
    03:12:49:00
    03:12:50:00
    03:12:51:00
    03:12:52:00
    03:12:53:00
    03:12:54:00
    03:12:55:00
    03:12:56:00
    03:12:57:00
    03:12:58:00
    03:12:59:00
    03:13:00:00
    03:13:01:00
    03:13:02:00
    03:13:03:00
    03:13:04:00
    03:13:05:00
    03:13:06:00
    03:13:07:00
    03:13:08:00
    03:13:09:00
    03:13:10:00
    03:13:11:00
    03:13:12:00
    03:13:13:00
    03:13:14:00
    03:13:15:00
    03:13:16:00
    03:13:17:00
    03:13:18:00
    03:13:19:00
    03:13:20:00
    03:13:21:00
    03:13:22:00
    03:13:23:00
    03:13:24:00
    03:13:25:00
    03:13:26:00
    03:13:27:00
    03:13:28:00
    03:13:29:00
    03:13:30:00
    03:13:31:00
    03:13:32:00
    03:13:33:00
    03:13:34:00
    03:13:35:00
    03:13:36:00
    03:13:37:00
    03:13:38:00
    03:13:39:00
    03:13:40:00
    03:13:41:00
    03:13:42:00
    03:13:43:00
    03:13:44:00
    03:13:45:00
    03:13:46:00
    03:13:47:00
    03:13:48:00
    03:13:49:00
    03:13:50:00
    03:13:51:00
    03:13:52:00
    03:13:53:00
    03:13:54:00
    03:13:55:00
    03:13:56:00
    03:13:57:00
    03:13:58:00
    03:13:59:00
    03:14:00:00
    03:14:01:00
    03:14:02:00
    03:14:03:00
    03:14:04:00
    03:14:05:00
    03:14:06:00
    03:14:07:00
    03:14:08:00
    03:14:09:00
    03:14:10:00
    03:14:11:00
    03:14:12:00
    03:14:13:00
    03:14:14:00
    03:14:15:00
    03:14:16:00
    03:14:17:00
    03:14:18:00
    03:14:19:00
    03:14:20:00
    03:14:21:00
    03:14:22:00
    03:14:23:00
    03:14:24:00
    03:14:25:00
    03:14:26:00
    03:14:27:00
    03:14:28:00
    03:14:29:00
    03:14:30:00
    03:14:31:00
    03:14:32:00
    03:14:33:00
    03:14:34:00
    03:14:35:00
    03:14:36:00
    03:14:37:00
    03:14:38:00
    03:14:39:00
    03:14:40:00
    03:14:41:00
    03:14:42:00
    03:14:43:00
    03:14:44:00
    03:14:45:00
    03:14:46:00
    03:14:47:00
    03:14:48:00
    03:14:49:00
    03:14:50:00
    03:14:51:00
    03:14:52:00
    03:14:53:00
    03:14:54:00
    03:14:55:00
    03:14:56:00
    03:14:57:00
    03:14:58:00
    03:14:59:00
    03:15:00:00
    03:15:01:00
    03:15:02:00
    03:15:03:00
    03:15:04:00
    03:15:05:00
    03:15:06:00
    03:15:07:00
    03:15:08:00
    03:15:09:00
    03:15:10:00
    03:15:11:00
    03:15:12:00
    03:15:13:00
    03:15:14:00
    03:15:15:00
    03:15:16:00
    03:15:17:00
    03:15:18:00
    03:15:19:00
    03:15:20:00
    03:15:21:00
    03:15:22:00
    03:15:23:00
    03:15:24:00
    03:15:25:00
    03:15:26:00
    03:15:27:00
    03:15:28:00
    03:15:29:00
    03:15:30:00
    03:15:31:00
    03:15:32:00
    03:15:33:00
    03:15:34:00
    03:15:35:00
    03:15:36:00
    03:15:37:00
    03:15:38:00
    03:15:39:00
    03:15:40:00
    03:15:41:00
    03:15:42:00
    03:15:43:00
    03:15:44:00
    03:15:45:00
    03:15:46:00
    03:15:47:00
    03:15:48:00
    03:15:49:00
    03:15:50:00
    03:15:51:00
    03:15:52:00
    03:15:53:00
    03:15:54:00
    03:15:55:00
    03:15:56:00
    03:15:57:00
    03:15:58:00
    03:15:59:00
    03:16:00:00
    03:16:01:00
    03:16:02:00
    03:16:03:00
    03:16:04:00
    03:16:05:00
    03:16:06:00
    03:16:07:00
    03:16:08:00
    03:16:09:00
    03:16:10:00
    03:16:11:00
    03:16:12:00
    03:16:13:00
    03:16:14:00
    03:16:15:00
    03:16:16:00
    03:16:17:00
    03:16:18:00
    03:16:19:00
    03:16:20:00
    03:16:21:00
    03:16:22:00
    03:16:23:00
    03:16:24:00
    03:16:25:00
    03:16:26:00
    03:16:27:00
    03:16:28:00
    03:16:29:00
    03:16:30:00
    03:16:31:00
    03:16:32:00
    03:16:33:00
    03:16:34:00
    03:16:35:00
    03:16:36:00
    03:16:37:00
    03:16:38:00
    03:16:39:00
    03:16:40:00
    03:16:41:00
    03:16:42:00
    03:16:43:00
    03:16:44:00
    03:16:45:00
    03:16:46:00
    03:16:47:00
    03:16:48:00
    03:16:49:00
    03:16:50:00
    03:16:51:00
    03:16:52:00
    03:16:53:00
    03:16:54:00


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

