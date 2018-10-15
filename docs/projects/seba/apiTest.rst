# REST API Test 
===============

Test execution guide
--------------------

To make a test of the REST service, the first thing to do is to make sure to run the SEBA software with the server option specified (-s), providing or not (optional) the port where the service will be defined.

.. code:: bash

        $ git clone https://github.com/gsi-upm/soba

        $ cd soba/projects/seba

        $ python3 run.py -v -s


Then, once the software has run, following the previous case, selecting the start option of the interface in the browser. Once the simulation has started, run the 'apiTest.py' test script. If a port was defined in the execution, change the variable port of the file to the chosen value.

.. code:: bash

        $ cd restClient

        $ python3 apiTest.py


Tests in a notebook
-------------------
To execute the tests with greater control, it is recommended to download and use the jupyter notebook that is provided in the following address: `Notebook <https://github.com/gsi-upm/blob/master/docs/projects/apiTest.ipynb>`_ 

This notebook is also presented below.

Initialization of params
""""""""""""""""""""""""""""""""""""

.. code:: python

    from unittest import TestCase
    import json, requests
    from jsonschema import validate
    import socket
    import unittest
    
    
    ipServer = socket.gethostbyname(socket.gethostname())
    
    #Port defined when executing, 10000 default
    port = '10000'
    
    #Template of the URLs
    URLBASE = "http://127.0.0.1:"+ port
    URISOBA = "/api/v1/occupants"
    URISEBA = "/api/v1/occupants"
    URIFIRE = "/api/v1/fire"
    
    stringTemplate = {"type": "string"}
    numberTemplate = {"type": "number"}
    
    #Number of test for each pair (URI, Method) 
    N = 1

Tests
"""""

.. code:: python

    print(str('Testing {}').format('GET /api/v1/occupants'))
    template = {
        "type": "object",
        "properties": {
            "occupants": {
                "type": "array"
                }
        },
        "required": ["occupants"]
    }
    
    for i in range(N):
        url = URLBASE + URISOBA
        data = requests.get(url)
        datajson = data.json()
        print("Response: ", datajson)
        validate(datajson, template)
        for o in datajson["occupants"]:
            validate(o, numberTemplate)


.. parsed-literal::

    Testing GET /api/v1/occupants
    Response:  {'occupants': [1, 0, 3, 100000, 2]}


.. code:: python

    print(str('Testing {}').format('GET /api/v1/occupants/movements'))
    template = {
        "type": "object",
        "properties": {
            "orientation": {
                "type": "string"
                },
            "speed": {
                "type": "number"
                }
        },
        "required": ["orientation", "speed"]
    }
    
    template2 = {
        "type": "object"
    }
    
    for i in range(N):
        url = URLBASE + URISOBA + "/movements"
        data = requests.get(url)
        datajson = data.json()
        print("Response: ", datajson)
        validate(datajson, template2)
        for k, v  in datajson.items():
            validate(k, stringTemplate)
            validate(int(k), numberTemplate)
            validate(v, template)


.. parsed-literal::

    Testing GET /api/v1/occupants/movements
    Response:  {'0': {'speed': 1.38, 'orientation': 'SE'}, '1': {'speed': 1.38, 'orientation': 'W'}, '2': {'speed': 1.38, 'orientation': 'SE'}, '3': {'speed': 1.38, 'orientation': 'E'}}


.. code:: python

    print(str('Testing {}').format('GET /api/v1/occupants/positions'))
    template = {
        "type": "object",
        "properties": {
            "x": {
                "type": "number"
                },
            "y": {
                "type": "number"
                }
        },
        "required": ["x", "y"]
    }
    
    for i in range(N):
        url = URLBASE + URISOBA + "/positions"
        data = requests.get(url)
        datajson = data.json()
        print("Response: ", datajson)
        for k, v in datajson.items():
            validate(k, stringTemplate)
            validate(int(k), numberTemplate)
            validate(v, template)


.. parsed-literal::

    Testing GET /api/v1/occupants/positions
    Response:  {'0': {'y': 8, 'x': 12}, '1': {'y': 6, 'x': 0}, '2': {'y': 8, 'x': 13}, '100000': {'y': 7, 'x': 5}, '3': {'y': 6, 'x': 14}}


.. code:: python

    print(str('Testing {}').format('GET /api/v1/occupants/states'))
    for i in range(N):
        url = URLBASE + URISOBA + "/states"
        data = requests.get(url)
        datajson = data.json()
        print("Response: ", datajson)
        for k,v in datajson.items():
            validate(v, stringTemplate)
            validate(k, stringTemplate)
            validate(int(k), numberTemplate)


.. parsed-literal::

    Testing GET /api/v1/occupants/states
    Response:  {'0': 'Working in my laboratory', '1': 'Working in my laboratory', '2': 'Working in my laboratory', '100000': 'walking', '3': 'Working in my laboratory'}


.. code:: python

    print(str('Testing {}').format('GET /api/v1/occupants/{id}'))
    template = {
        "type": "object",
        "properties": {
            "occupant":{
                "type": "object",
                "properties": {
                        "state":{
                            "type": "string"
                        },
                        "fov": {
                            "type": "array"
                        },
                        "unique_id":{
                            "type": "string"
                        },
                        "movement": {
                            "type": "object",
                            "properties": {
                                "orientation":{
                                    "type": "string"
                                },
                                "speed":{
                                    "type": "number"
                                },
                            },
                            "required": ["orientation", "speed"]
                        },
                        "position": {
                            "type": "object",
                            "properties": {
                                "x":{
                                    "type": "number"
                                },
                                "y":{
                                    "type": "number"
                                }
                            },
                            "required": ["x", "y"]
                        }
                },
        "required": ["state", "fov", "unique_id", "movement", "position"]
            }
        },
        "required": ["occupant"]
    }
    
    template2 = {
        "type": "object",
        "properties": {
            "x": {
                "type": "number"
                },
            "y": {
                "type": "number"
            }
        },
        "required": ["x", "y"]
    }
    
    for i in range(N):
        url = URLBASE + URISOBA + "/" + str(0)
        data = requests.get(url)
        datajson = data.json()
        print("Response: ", datajson)
        validate(datajson, template)
        validate(int(datajson['occupant']['unique_id']), numberTemplate)
        print(template)
        for p in datajson['occupant']['fov']:
            validate(p, template2)


.. parsed-literal::

    Testing GET /api/v1/occupants/{id}
    Response:  {'occupant': {'unique_id': '0', 'fov': [{'y': 0, 'x': 9}, {'y': 0, 'x': 10}, {'y': 0, 'x': 11}, {'y': 0, 'x': 12}, {'y': 0, 'x': 13}, {'y': 0, 'x': 14}, {'y': 0, 'x': 15}, {'y': 0, 'x': 16}, {'y': 0, 'x': 17}, {'y': 0, 'x': 18}, {'y': 1, 'x': 9}, {'y': 1, 'x': 10}, {'y': 1, 'x': 11}, {'y': 1, 'x': 12}, {'y': 1, 'x': 13}, {'y': 1, 'x': 14}, {'y': 1, 'x': 15}, {'y': 1, 'x': 16}, {'y': 1, 'x': 17}, {'y': 1, 'x': 18}, {'y': 2, 'x': 9}, {'y': 2, 'x': 10}, {'y': 2, 'x': 11}, {'y': 2, 'x': 12}, {'y': 2, 'x': 13}, {'y': 2, 'x': 14}, {'y': 2, 'x': 15}, {'y': 2, 'x': 16}, {'y': 2, 'x': 17}, {'y': 2, 'x': 18}, {'y': 3, 'x': 9}, {'y': 3, 'x': 10}, {'y': 3, 'x': 11}, {'y': 3, 'x': 12}, {'y': 3, 'x': 13}, {'y': 3, 'x': 14}, {'y': 3, 'x': 15}, {'y': 3, 'x': 16}, {'y': 3, 'x': 17}, {'y': 3, 'x': 18}, {'y': 4, 'x': 9}, {'y': 4, 'x': 10}, {'y': 4, 'x': 11}, {'y': 4, 'x': 12}, {'y': 4, 'x': 13}, {'y': 4, 'x': 14}, {'y': 4, 'x': 15}, {'y': 4, 'x': 16}, {'y': 4, 'x': 17}, {'y': 4, 'x': 18}, {'y': 4, 'x': 19}, {'y': 5, 'x': 9}, {'y': 5, 'x': 10}, {'y': 5, 'x': 11}, {'y': 5, 'x': 12}, {'y': 5, 'x': 13}, {'y': 5, 'x': 14}, {'y': 5, 'x': 15}, {'y': 5, 'x': 16}, {'y': 5, 'x': 17}, {'y': 5, 'x': 18}, {'y': 5, 'x': 19}, {'y': 6, 'x': 9}, {'y': 6, 'x': 10}, {'y': 6, 'x': 11}, {'y': 6, 'x': 12}, {'y': 6, 'x': 13}, {'y': 6, 'x': 14}, {'y': 6, 'x': 15}, {'y': 6, 'x': 16}, {'y': 6, 'x': 17}, {'y': 6, 'x': 18}, {'y': 6, 'x': 19}, {'y': 7, 'x': 9}, {'y': 7, 'x': 10}, {'y': 7, 'x': 11}, {'y': 7, 'x': 12}, {'y': 7, 'x': 13}, {'y': 7, 'x': 14}, {'y': 7, 'x': 15}, {'y': 7, 'x': 16}, {'y': 7, 'x': 17}, {'y': 7, 'x': 18}, {'y': 8, 'x': 9}, {'y': 8, 'x': 10}, {'y': 8, 'x': 11}, {'y': 8, 'x': 13}, {'y': 8, 'x': 14}, {'y': 8, 'x': 15}, {'y': 8, 'x': 16}, {'y': 8, 'x': 17}, {'y': 8, 'x': 18}, {'y': 9, 'x': 9}, {'y': 9, 'x': 10}, {'y': 9, 'x': 11}, {'y': 9, 'x': 12}, {'y': 9, 'x': 13}, {'y': 9, 'x': 14}, {'y': 9, 'x': 15}, {'y': 9, 'x': 16}, {'y': 9, 'x': 17}, {'y': 9, 'x': 18}, {'y': 10, 'x': 8}, {'y': 10, 'x': 9}, {'y': 10, 'x': 10}, {'y': 10, 'x': 11}, {'y': 10, 'x': 12}, {'y': 10, 'x': 13}, {'y': 10, 'x': 14}, {'y': 10, 'x': 15}, {'y': 10, 'x': 16}, {'y': 10, 'x': 17}, {'y': 10, 'x': 18}, {'y': 11, 'x': 6}, {'y': 11, 'x': 7}, {'y': 11, 'x': 8}, {'y': 11, 'x': 9}, {'y': 11, 'x': 10}, {'y': 11, 'x': 11}, {'y': 12, 'x': 4}, {'y': 12, 'x': 5}, {'y': 12, 'x': 6}, {'y': 12, 'x': 7}, {'y': 12, 'x': 8}, {'y': 12, 'x': 9}, {'y': 12, 'x': 10}, {'y': 12, 'x': 11}, {'y': 13, 'x': 3}, {'y': 13, 'x': 4}, {'y': 13, 'x': 5}, {'y': 13, 'x': 6}, {'y': 13, 'x': 7}, {'y': 13, 'x': 8}, {'y': 13, 'x': 9}, {'y': 13, 'x': 10}, {'y': 13, 'x': 11}, {'y': 14, 'x': 1}, {'y': 14, 'x': 2}, {'y': 14, 'x': 3}, {'y': 14, 'x': 4}, {'y': 14, 'x': 5}, {'y': 14, 'x': 6}, {'y': 14, 'x': 7}, {'y': 14, 'x': 8}, {'y': 14, 'x': 9}, {'y': 14, 'x': 10}, {'y': 15, 'x': 0}, {'y': 15, 'x': 1}, {'y': 15, 'x': 2}, {'y': 15, 'x': 3}, {'y': 15, 'x': 4}, {'y': 15, 'x': 5}, {'y': 15, 'x': 6}, {'y': 15, 'x': 7}, {'y': 15, 'x': 8}, {'y': 15, 'x': 9}, {'y': 15, 'x': 10}, {'y': 16, 'x': 0}, {'y': 16, 'x': 1}, {'y': 16, 'x': 2}, {'y': 16, 'x': 3}, {'y': 16, 'x': 4}, {'y': 16, 'x': 5}, {'y': 16, 'x': 6}, {'y': 16, 'x': 7}, {'y': 16, 'x': 8}, {'y': 16, 'x': 9}, {'y': 16, 'x': 10}, {'y': 17, 'x': 0}, {'y': 17, 'x': 1}, {'y': 17, 'x': 2}, {'y': 17, 'x': 3}, {'y': 17, 'x': 4}, {'y': 17, 'x': 5}, {'y': 17, 'x': 6}, {'y': 17, 'x': 7}, {'y': 17, 'x': 8}, {'y': 17, 'x': 9}, {'y': 18, 'x': 0}, {'y': 18, 'x': 1}, {'y': 18, 'x': 2}, {'y': 18, 'x': 3}, {'y': 18, 'x': 4}, {'y': 18, 'x': 5}, {'y': 18, 'x': 6}, {'y': 18, 'x': 7}, {'y': 18, 'x': 8}, {'y': 18, 'x': 9}], 'state': 'Working in my laboratory', 'position': {'y': 8, 'x': 12}, 'movement': {'speed': 1.38, 'orientation': 'SE'}}}
    {'type': 'object', 'required': ['occupant'], 'properties': {'occupant': {'type': 'object', 'required': ['state', 'fov', 'unique_id', 'movement', 'position'], 'properties': {'unique_id': {'type': 'string'}, 'fov': {'type': 'array'}, 'position': {'type': 'object', 'required': ['x', 'y'], 'properties': {'y': {'type': 'number'}, 'x': {'type': 'number'}}}, 'state': {'type': 'string'}, 'movement': {'type': 'object', 'required': ['orientation', 'speed'], 'properties': {'speed': {'type': 'number'}, 'orientation': {'type': 'string'}}}}}}}


.. code:: python

    print(str('Testing {}').format('GET /api/v1/occupants/{id}/movement'))
    template = {
        "type": "object",
        "properties": {
            "movement":{
                "type": "object",
                "properties": {
                        "orientation": {
                            "type": "string"
                        },
                        "speed": {
                            "type": "number"
                        }
                },
            "required": ["orientation", "speed"]
            }
        },
        "required": ["movement"]
    }
    
    for i in range(N):
        url = URLBASE + URISOBA + "/" + str(0) + "/movement"
        data = requests.get(url)
        datajson = data.json()
        print("Response: ", datajson)
        validate(datajson, template)


.. parsed-literal::

    Testing GET /api/v1/occupants/{id}/movement
    Response:  {'movement': {'speed': 1.38, 'orientation': 'SE'}}


.. code:: python

    print(str('Testing {}').format('GET /api/v1/occupants/{id}/position'))
    template = {
        "type": "object",
        "properties": {
            "position":{
                "type": "object",
                "properties": {
                    "x": {
                        "type": "number"
                        },
                    "y": {
                        "type": "number"
                    }
                },
                "required": ["x", "y"]
            }
        },
        "required": ["position"]
    }
    
    for i in range(N):
        url = URLBASE + URISOBA + "/" + str(0) + "/position"
        data = requests.get(url)
        datajson = data.json()
        print("Response: ", datajson)
        validate(datajson, template)


.. parsed-literal::

    Testing GET /api/v1/occupants/{id}/position
    Response:  {'position': {'y': 8, 'x': 12}}


.. code:: python

    print(str('Testing {}').format('GET /api/v1/occupants/{id}/state'))
    template = {
        "type": "object",
        "properties":{
            "state": {
                "type": "string"
            }
        },
        "required": ["state"]
    }
    
    for i in range(N):
        url = URLBASE + URISOBA + "/" + str(0) + "/state"
        data = requests.get(url)
        datajson = data.json()
        print("Response: ", datajson)
        validate(datajson, template)



.. parsed-literal::

    Testing GET /api/v1/occupants/{id}/state
    Response:  {'state': 'Working in my laboratory'}


.. code:: python

    print(str('Testing {}').format('GET /api/v1/occupants/{id}/fov'))
    template = {
        "type": "object",
        "properties": {
            "fov": {
                "type": "array"
                }
        },
        "required": ["fov"]
    }
    
    
    template2 = {
        "type": "object",
        "properties": {
            "x": {
                "type": "number"
                },
            "y": {
                "type": "number"
            }
        },
        "required": ["x", "y"]
    }
    
    for i in range(N):
        url = URLBASE + URISOBA + "/" + str(0) + "/fov"
        data = requests.get(url)
        datajson = data.json()
        print("Response: ", datajson)
        validate(datajson, template)
        for p in datajson['fov']:
            validate(p, template2)



.. parsed-literal::

    Testing GET /api/v1/occupants/{id}/fov
    Response:  {'fov': [{'y': 0, 'x': 9}, {'y': 0, 'x': 10}, {'y': 0, 'x': 11}, {'y': 0, 'x': 12}, {'y': 0, 'x': 13}, {'y': 0, 'x': 14}, {'y': 0, 'x': 15}, {'y': 0, 'x': 16}, {'y': 0, 'x': 17}, {'y': 0, 'x': 18}, {'y': 1, 'x': 9}, {'y': 1, 'x': 10}, {'y': 1, 'x': 11}, {'y': 1, 'x': 12}, {'y': 1, 'x': 13}, {'y': 1, 'x': 14}, {'y': 1, 'x': 15}, {'y': 1, 'x': 16}, {'y': 1, 'x': 17}, {'y': 1, 'x': 18}, {'y': 2, 'x': 9}, {'y': 2, 'x': 10}, {'y': 2, 'x': 11}, {'y': 2, 'x': 12}, {'y': 2, 'x': 13}, {'y': 2, 'x': 14}, {'y': 2, 'x': 15}, {'y': 2, 'x': 16}, {'y': 2, 'x': 17}, {'y': 2, 'x': 18}, {'y': 3, 'x': 9}, {'y': 3, 'x': 10}, {'y': 3, 'x': 11}, {'y': 3, 'x': 12}, {'y': 3, 'x': 13}, {'y': 3, 'x': 14}, {'y': 3, 'x': 15}, {'y': 3, 'x': 16}, {'y': 3, 'x': 17}, {'y': 3, 'x': 18}, {'y': 4, 'x': 9}, {'y': 4, 'x': 10}, {'y': 4, 'x': 11}, {'y': 4, 'x': 12}, {'y': 4, 'x': 13}, {'y': 4, 'x': 14}, {'y': 4, 'x': 15}, {'y': 4, 'x': 16}, {'y': 4, 'x': 17}, {'y': 4, 'x': 18}, {'y': 4, 'x': 19}, {'y': 5, 'x': 9}, {'y': 5, 'x': 10}, {'y': 5, 'x': 11}, {'y': 5, 'x': 12}, {'y': 5, 'x': 13}, {'y': 5, 'x': 14}, {'y': 5, 'x': 15}, {'y': 5, 'x': 16}, {'y': 5, 'x': 17}, {'y': 5, 'x': 18}, {'y': 5, 'x': 19}, {'y': 6, 'x': 9}, {'y': 6, 'x': 10}, {'y': 6, 'x': 11}, {'y': 6, 'x': 12}, {'y': 6, 'x': 13}, {'y': 6, 'x': 14}, {'y': 6, 'x': 15}, {'y': 6, 'x': 16}, {'y': 6, 'x': 17}, {'y': 6, 'x': 18}, {'y': 6, 'x': 19}, {'y': 7, 'x': 9}, {'y': 7, 'x': 10}, {'y': 7, 'x': 11}, {'y': 7, 'x': 12}, {'y': 7, 'x': 13}, {'y': 7, 'x': 14}, {'y': 7, 'x': 15}, {'y': 7, 'x': 16}, {'y': 7, 'x': 17}, {'y': 7, 'x': 18}, {'y': 8, 'x': 9}, {'y': 8, 'x': 10}, {'y': 8, 'x': 11}, {'y': 8, 'x': 13}, {'y': 8, 'x': 14}, {'y': 8, 'x': 15}, {'y': 8, 'x': 16}, {'y': 8, 'x': 17}, {'y': 8, 'x': 18}, {'y': 9, 'x': 9}, {'y': 9, 'x': 10}, {'y': 9, 'x': 11}, {'y': 9, 'x': 12}, {'y': 9, 'x': 13}, {'y': 9, 'x': 14}, {'y': 9, 'x': 15}, {'y': 9, 'x': 16}, {'y': 9, 'x': 17}, {'y': 9, 'x': 18}, {'y': 10, 'x': 8}, {'y': 10, 'x': 9}, {'y': 10, 'x': 10}, {'y': 10, 'x': 11}, {'y': 10, 'x': 12}, {'y': 10, 'x': 13}, {'y': 10, 'x': 14}, {'y': 10, 'x': 15}, {'y': 10, 'x': 16}, {'y': 10, 'x': 17}, {'y': 10, 'x': 18}, {'y': 11, 'x': 6}, {'y': 11, 'x': 7}, {'y': 11, 'x': 8}, {'y': 11, 'x': 9}, {'y': 11, 'x': 10}, {'y': 11, 'x': 11}, {'y': 12, 'x': 4}, {'y': 12, 'x': 5}, {'y': 12, 'x': 6}, {'y': 12, 'x': 7}, {'y': 12, 'x': 8}, {'y': 12, 'x': 9}, {'y': 12, 'x': 10}, {'y': 12, 'x': 11}, {'y': 13, 'x': 3}, {'y': 13, 'x': 4}, {'y': 13, 'x': 5}, {'y': 13, 'x': 6}, {'y': 13, 'x': 7}, {'y': 13, 'x': 8}, {'y': 13, 'x': 9}, {'y': 13, 'x': 10}, {'y': 13, 'x': 11}, {'y': 14, 'x': 1}, {'y': 14, 'x': 2}, {'y': 14, 'x': 3}, {'y': 14, 'x': 4}, {'y': 14, 'x': 5}, {'y': 14, 'x': 6}, {'y': 14, 'x': 7}, {'y': 14, 'x': 8}, {'y': 14, 'x': 9}, {'y': 14, 'x': 10}, {'y': 15, 'x': 0}, {'y': 15, 'x': 1}, {'y': 15, 'x': 2}, {'y': 15, 'x': 3}, {'y': 15, 'x': 4}, {'y': 15, 'x': 5}, {'y': 15, 'x': 6}, {'y': 15, 'x': 7}, {'y': 15, 'x': 8}, {'y': 15, 'x': 9}, {'y': 15, 'x': 10}, {'y': 16, 'x': 0}, {'y': 16, 'x': 1}, {'y': 16, 'x': 2}, {'y': 16, 'x': 3}, {'y': 16, 'x': 4}, {'y': 16, 'x': 5}, {'y': 16, 'x': 6}, {'y': 16, 'x': 7}, {'y': 16, 'x': 8}, {'y': 16, 'x': 9}, {'y': 16, 'x': 10}, {'y': 17, 'x': 0}, {'y': 17, 'x': 1}, {'y': 17, 'x': 2}, {'y': 17, 'x': 3}, {'y': 17, 'x': 4}, {'y': 17, 'x': 5}, {'y': 17, 'x': 6}, {'y': 17, 'x': 7}, {'y': 17, 'x': 8}, {'y': 17, 'x': 9}, {'y': 18, 'x': 0}, {'y': 18, 'x': 1}, {'y': 18, 'x': 2}, {'y': 18, 'x': 3}, {'y': 18, 'x': 4}, {'y': 18, 'x': 5}, {'y': 18, 'x': 6}, {'y': 18, 'x': 7}, {'y': 18, 'x': 8}, {'y': 18, 'x': 9}]}


.. code:: python

    print(str('Testing {}').format('PUT /api/v1/occupants/{id}'))
    template = {
        "type": "object",
            "properties": {
                "avatar":{
                    "type": "object",
                    "properties": {
                        "position":{
                            "type": "object",
                            "properties": {
                                "x": {
                                    "type": "number",
                                },
                                "y": {
                                    "type": "number"
                                }
                            },
                            "required": ["x", "y"]
                        },
                        "id":{
                            "type": "number"
                        }
                },
                "required": ["position", "id"]
            }
        },
        "required": ["avatar"]
    }
    
    dataBody = {"x": 10, "y": 10}
    
    for i in range(N):
        url = URLBASE + URISOBA + "/" + str(0)
        data = requests.put(url, json=dataBody, headers={'Content-Type': "application/json", 'Accept': "application/json"})
        datajson = data.json()
        print("Response: ", datajson)
        validate(datajson, template)



.. parsed-literal::

    Testing PUT /api/v1/occupants/{id}
    Response:  {'avatar': {'position': {'y': 10, 'x': 10}, 'id': 100000}}


.. code:: python

    print(str('Testing {}').format('POST /api/v1/occupants/{id}/position'))
    template = {
        "type": "object",
            "properties": {
                "avatar":{
                    "type": "object",
                    "properties": {
                        "position":{
                            "type": "object",
                            "properties": {
                                "x": {
                                    "type": "number",
                                },
                                "y": {
                                    "type": "number"
                                }
                            },
                            "required": ["x", "y"]
                        },
                        "id":{
                            "type": "number"
                        }
                },
                "required": ["position", "id"]
            }
        },
        "required": ["avatar"]
    }
    
    dataBody = {"x": 5, "y": 7}
    
    for i in range(N):
        url = URLBASE + URISOBA + "/" + str(100000) + "/position"
        data = requests.post(url, json=dataBody, headers={'Content-Type': "application/json", 'Accept': "application/json"})
        datajson = data.json()
        print("Response: ", datajson)
        validate(datajson, template)


.. parsed-literal::

    Testing POST /api/v1/occupants/{id}/position
    Response:  {'avatar': {'position': {'y': 7, 'x': 5}, 'id': 100000}}


.. code:: python

    print(str('Testing {}').format('GET /api/v1/occupants/{id}/route/{route_id}'))
    template = {
        "type": "object",
        "properties": {
            "positions": {
                "type": "array"
                }
        }
    }
    
    template2 = {
        "type": "object",
        "properties": {
            "x": {
                "type": "number"
                },
            "y": {
                "type": "number"
                }
        },
        "required": ["x", "y"]
    }
    
    for i in range(N):
        url = URLBASE + URISEBA + "/" + str(100000) + "/route/1"
        data = requests.get(url)
        datajson = data.json()
        print("Response: ", datajson)
        validate(datajson, template)
        for m in datajson["positions"]:
            validate(m, template2)


.. parsed-literal::

    Testing GET /api/v1/occupants/{id}/route/{route_id}
    Response:  {'positions': [{'y': 7, 'x': 4}, {'y': 7, 'x': 3}, {'y': 7, 'x': 2}, {'y': 6, 'x': 1}, {'y': 6, 'x': 0}]}


.. code:: python

    print(str('Testing {}').format('PUT /api/v1/occupants/{id}'))
    template = {
        "type": "object",
        "properties": {
            "avatar": {
                "type": "object",
                "properties":{
                    "position":{
                        "type": "object",
                        "properties":{
                            "x": {
                                "type": "number"
                            },
                            "y": {
                                "type": "number"
                            }
                        },
                        "required": ["x", "y"]
                    },
                    "id": {
                        "type": "number"
                    }
                },
                "required": ["position", "id"]
            }
        },
        "required": ["avatar"]
    }
    
    dataBody = {"x": 13, "y": 13}
    
    for i in range(N):
        url = URLBASE + URISEBA + "/" + str(1)
        data = requests.put(url, json=dataBody, headers={'Content-Type': "application/json", 'Accept': "application/json"})
        datajson = data.json()
        print("Response: ", datajson)
        validate(datajson, template)


.. parsed-literal::

    Testing PUT /api/v1/occupants/{id}
    Response:  {'avatar': {'id': 100001, 'position': {'y': 13, 'x': 13}}}


.. code:: python

    print(str('Testing {}').format('GET /api/v1/occupants/{id}/fire'))
    template = {
        "type": "object",
        "properties": {
            "positions": {
                "type": "array"
                }
        },
        "required": ["positions"]
    }
    
    template2 = {
        "type": "object",
        "properties": {
            "x": {
                "type": "number"
                },
            "y": {
                "type": "number"
                }
        },
        "required": ["x", "y"]
    }
    
    for i in range(N):
        url = URLBASE + URISEBA + "/" + str(2) + "/fire"
        data = requests.get(url)
        datajson = data.json()
        print("Response: ", datajson)
        validate(datajson, template)
        for m in datajson["positions"]:
            validate(m, template2)
    



.. parsed-literal::

    Testing GET /api/v1/occupants/{id}/fire
    Response:  {'positions': [{'y': 4, 'x': 12}, {'y': 5, 'x': 13}, {'y': 4, 'x': 13}, {'y': 4, 'x': 11}, {'y': 3, 'x': 11}, {'y': 5, 'x': 12}, {'y': 3, 'x': 12}, {'y': 5, 'x': 11}, {'y': 3, 'x': 13}, {'y': 6, 'x': 14}, {'y': 5, 'x': 14}, {'y': 6, 'x': 13}, {'y': 6, 'x': 12}, {'y': 4, 'x': 14}, {'y': 3, 'x': 14}, {'y': 4, 'x': 10}, {'y': 3, 'x': 10}, {'y': 5, 'x': 10}, {'y': 2, 'x': 10}, {'y': 2, 'x': 11}, {'y': 2, 'x': 12}, {'y': 6, 'x': 11}, {'y': 2, 'x': 13}, {'y': 6, 'x': 10}, {'y': 2, 'x': 14}, {'y': 7, 'x': 15}, {'y': 6, 'x': 15}, {'y': 7, 'x': 14}, {'y': 7, 'x': 13}, {'y': 5, 'x': 15}, {'y': 4, 'x': 15}, {'y': 7, 'x': 12}, {'y': 7, 'x': 11}, {'y': 3, 'x': 15}, {'y': 2, 'x': 15}, {'y': 1, 'x': 10}, {'y': 1, 'x': 11}, {'y': 1, 'x': 12}, {'y': 1, 'x': 13}, {'y': 7, 'x': 10}, {'y': 1, 'x': 14}, {'y': 1, 'x': 15}, {'y': 8, 'x': 16}, {'y': 7, 'x': 16}, {'y': 8, 'x': 15}, {'y': 8, 'x': 14}, {'y': 6, 'x': 16}, {'y': 5, 'x': 16}, {'y': 8, 'x': 13}, {'y': 8, 'x': 12}, {'y': 4, 'x': 16}, {'y': 3, 'x': 16}, {'y': 8, 'x': 11}, {'y': 8, 'x': 10}, {'y': 2, 'x': 16}, {'y': 1, 'x': 16}]}


.. code:: python

    
    print(str('Testing {}').format('GET /api/v1/fire'))
    template = {
        "type": "object",
        "properties": {
            "positions": {
                "type": "array"
                }
        },
        "required": ["positions"]
    }
    
    template2 = {
        "type": "object",
        "properties": {
            "x": {
                "type": "number"
                },
            "y": {
                "type": "number"
                }
        },
        "required": ["x", "y"]
    }
    
    for i in range(N):
        url = URLBASE + URIFIRE
        data = requests.get(url)
        datajson = data.json()
        print("Response: ", datajson)
        validate(datajson, template)
        for m in datajson["positions"]:
            validate(m, template2)


.. parsed-literal::

    Testing GET /api/v1/fire
    Response:  {'positions': [{'y': 4, 'x': 12}, {'y': 5, 'x': 13}, {'y': 4, 'x': 13}, {'y': 4, 'x': 11}, {'y': 3, 'x': 11}, {'y': 5, 'x': 12}, {'y': 3, 'x': 12}, {'y': 5, 'x': 11}, {'y': 3, 'x': 13}, {'y': 6, 'x': 14}, {'y': 5, 'x': 14}, {'y': 6, 'x': 13}, {'y': 6, 'x': 12}, {'y': 4, 'x': 14}, {'y': 3, 'x': 14}, {'y': 4, 'x': 10}, {'y': 3, 'x': 10}, {'y': 5, 'x': 10}, {'y': 2, 'x': 10}, {'y': 2, 'x': 11}, {'y': 2, 'x': 12}, {'y': 6, 'x': 11}, {'y': 2, 'x': 13}, {'y': 6, 'x': 10}, {'y': 2, 'x': 14}, {'y': 7, 'x': 15}, {'y': 6, 'x': 15}, {'y': 7, 'x': 14}, {'y': 7, 'x': 13}, {'y': 5, 'x': 15}, {'y': 4, 'x': 15}, {'y': 7, 'x': 12}, {'y': 7, 'x': 11}, {'y': 3, 'x': 15}, {'y': 2, 'x': 15}, {'y': 1, 'x': 10}, {'y': 1, 'x': 11}, {'y': 1, 'x': 12}, {'y': 1, 'x': 13}, {'y': 7, 'x': 10}, {'y': 1, 'x': 14}, {'y': 1, 'x': 15}, {'y': 8, 'x': 16}, {'y': 7, 'x': 16}, {'y': 8, 'x': 15}, {'y': 8, 'x': 14}, {'y': 6, 'x': 16}, {'y': 5, 'x': 16}, {'y': 8, 'x': 13}, {'y': 8, 'x': 12}, {'y': 4, 'x': 16}, {'y': 3, 'x': 16}, {'y': 8, 'x': 11}, {'y': 8, 'x': 10}, {'y': 2, 'x': 16}, {'y': 1, 'x': 16}]}

