REST API Client
===============

.. code:: python

    from unittest import TestCase
    import json, requests
    from jsonschema import validate
    import socket
    import unittest
    
    
    ipServer = socket.gethostbyname(socket.gethostname())
    
    
    URLBASE = "http://127.0.1.1:10000"
    URISOBA = "/api/soba/v1/occupants"
    URISEBA = "/api/seba/v1/occupants"
    URIFIRE = "/api/seba/v1/fire"
    stringTemplate = {"type": "string"}
    numberTemplate = {"type": "number"}
    
    N = 1


.. code:: python

    print(str('Testing {}').format('GET /api/soba/v1/occupants'))
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

    Testing GET /api/soba/v1/occupants
    Response:  {'occupants': [2, 0, 1]}


.. code:: python

    print(str('Testing {}').format('GET /api/soba/v1/occupants/movements'))
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

    Testing GET /api/soba/v1/occupants/movements
    Response:  {'0': {'speed': 0.71428, 'orientation': 'out'}, '2': {'speed': 0.71428, 'orientation': 'out'}, '1': {'speed': 0.71428, 'orientation': 'out'}}


.. code:: python

    print(str('Testing {}').format('GET /api/soba/v1/occupants/positions'))
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

    Testing GET /api/soba/v1/occupants/positions
    Response:  {'0': {'y': 14, 'x': 0}, '2': {'y': 14, 'x': 0}, '1': {'y': 14, 'x': 0}}


.. code:: python

    print(str('Testing {}').format('GET /api/soba/v1/occupants/states'))
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

    Testing GET /api/soba/v1/occupants/states
    Response:  {'0': 'Leaving', '2': 'Leaving', '1': 'Leaving'}


.. code:: python

    print(str('Testing {}').format('GET /api/soba/v1/occupants/{id}'))
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

    Testing GET /api/soba/v1/occupants/{id}
    Response:  {'occupant': {'unique_id': '0', 'movement': {'speed': 0.71428, 'orientation': 'out'}, 'fov': [], 'position': {'y': 14, 'x': 0}, 'state': 'Leaving'}}
    {'type': 'object', 'required': ['occupant'], 'properties': {'occupant': {'type': 'object', 'required': ['state', 'fov', 'unique_id', 'movement', 'position'], 'properties': {'unique_id': {'type': 'string'}, 'position': {'type': 'object', 'required': ['x', 'y'], 'properties': {'y': {'type': 'number'}, 'x': {'type': 'number'}}}, 'fov': {'type': 'array'}, 'movement': {'type': 'object', 'required': ['orientation', 'speed'], 'properties': {'speed': {'type': 'number'}, 'orientation': {'type': 'string'}}}, 'state': {'type': 'string'}}}}}


.. code:: python

    print(str('Testing {}').format('GET /api/soba/v1/occupants/{id}/movement'))
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

    Testing GET /api/soba/v1/occupants/{id}/movement
    Response:  {'movement': {'speed': 0.71428, 'orientation': 'out'}}


.. code:: python

    print(str('Testing {}').format('GET /api/soba/v1/occupants/{id}/position'))
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

    Testing GET /api/soba/v1/occupants/{id}/position
    Response:  {'position': {'y': 14, 'x': 0}}


.. code:: python

    print(str('Testing {}').format('GET /api/soba/v1/occupants/{id}/state'))
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

    Testing GET /api/soba/v1/occupants/{id}/state
    Response:  {'state': 'Leaving'}


.. code:: python

    print(str('Testing {}').format('GET /api/soba/v1/occupants/{id}/fov'))
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

    Testing GET /api/soba/v1/occupants/{id}/fov
    Response:  {'fov': []}


.. code:: python

    print(str('Testing {}').format('PUT /api/soba/v1/occupants/{id}'))
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

    Testing PUT /api/soba/v1/occupants/{id}
    Response:  {'avatar': {'id': 100000, 'position': {'y': 10, 'x': 10}}}


.. code:: python

    print(str('Testing {}').format('POST /api/soba/v1/occupants/{id}/position'))
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
    
    dataBody = {"x": 5, "y": 5}
    
    for i in range(N):
        url = URLBASE + URISOBA + "/" + str(100000) + "/position"
        data = requests.post(url, json=dataBody, headers={'Content-Type': "application/json", 'Accept': "application/json"})
        datajson = data.json()
        print("Response: ", datajson)
        validate(datajson, template)


.. parsed-literal::

    Testing POST /api/soba/v1/occupants/{id}/position
    Response:  {'avatar': {'id': 100000, 'position': {'y': 5, 'x': 5}}}


.. code:: python

    print(str('Testing {}').format('GET /api/seba/v1/occupants/{id}/route/{route_id}'))
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

    Testing GET /api/seba/v1/occupants/{id}/route/{route_id}
    Response:  {'positions': [{'y': 10, 'x': 11}, {'y': 9, 'x': 12}, {'y': 8, 'x': 13}, {'y': 8, 'x': 14}, {'y': 8, 'x': 15}, {'y': 7, 'x': 16}, {'y': 6, 'x': 17}, {'y': 5, 'x': 18}]}


.. code:: python

    print(str('Testing {}').format('PUT /api/seba/v1/occupants/{id}'))
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

    Testing PUT /api/seba/v1/occupants/{id}
    Response:  {'avatar': {'id': 100001, 'position': {'y': 13, 'x': 13}}}


.. code:: python

    print(str('Testing {}').format('GET /api/seba/v1/occupants/{id}/fire'))
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
        url = URLBASE + URISEBA + "/" + str(100000) + "/fire"
        data = requests.get(url)
        datajson = data.json()
        print("Response: ", datajson)
        validate(datajson, template)
        for m in datajson["positions"]:
            validate(m, template2)
    



.. parsed-literal::

    Testing GET /api/seba/v1/occupants/{id}/fire
    Response:  {'positions': [{'y': 1, 'x': 10}, {'y': 1, 'x': 11}, {'y': 1, 'x': 12}, {'y': 1, 'x': 13}, {'y': 1, 'x': 14}, {'y': 1, 'x': 15}, {'y': 1, 'x': 16}, {'y': 2, 'x': 10}, {'y': 2, 'x': 11}, {'y': 2, 'x': 12}, {'y': 2, 'x': 13}, {'y': 2, 'x': 14}, {'y': 2, 'x': 15}, {'y': 2, 'x': 16}, {'y': 3, 'x': 10}, {'y': 3, 'x': 11}, {'y': 3, 'x': 12}, {'y': 3, 'x': 13}, {'y': 3, 'x': 14}, {'y': 3, 'x': 15}, {'y': 3, 'x': 16}, {'y': 4, 'x': 10}, {'y': 4, 'x': 11}, {'y': 4, 'x': 12}, {'y': 4, 'x': 13}, {'y': 4, 'x': 14}, {'y': 4, 'x': 15}, {'y': 4, 'x': 16}, {'y': 5, 'x': 10}, {'y': 5, 'x': 11}, {'y': 5, 'x': 12}, {'y': 5, 'x': 13}, {'y': 5, 'x': 14}, {'y': 5, 'x': 15}, {'y': 5, 'x': 16}, {'y': 6, 'x': 10}, {'y': 6, 'x': 11}, {'y': 6, 'x': 12}, {'y': 6, 'x': 13}, {'y': 6, 'x': 14}, {'y': 6, 'x': 15}, {'y': 6, 'x': 16}, {'y': 7, 'x': 10}, {'y': 7, 'x': 11}, {'y': 7, 'x': 12}, {'y': 7, 'x': 13}, {'y': 7, 'x': 14}, {'y': 7, 'x': 15}, {'y': 7, 'x': 16}, {'y': 8, 'x': 10}, {'y': 8, 'x': 11}, {'y': 8, 'x': 12}, {'y': 8, 'x': 13}, {'y': 8, 'x': 14}, {'y': 8, 'x': 15}, {'y': 8, 'x': 16}]}


.. code:: python

    
    print(str('Testing {}').format('GET /api/seba/v1/fire'))
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

    Testing GET /api/seba/v1/fire
    Response:  {'positions': [{'y': 4, 'x': 12}, {'y': 5, 'x': 13}, {'y': 4, 'x': 13}, {'y': 4, 'x': 11}, {'y': 3, 'x': 11}, {'y': 5, 'x': 12}, {'y': 3, 'x': 12}, {'y': 5, 'x': 11}, {'y': 3, 'x': 13}, {'y': 6, 'x': 14}, {'y': 5, 'x': 14}, {'y': 6, 'x': 13}, {'y': 6, 'x': 12}, {'y': 4, 'x': 14}, {'y': 3, 'x': 14}, {'y': 4, 'x': 10}, {'y': 3, 'x': 10}, {'y': 5, 'x': 10}, {'y': 2, 'x': 10}, {'y': 2, 'x': 11}, {'y': 2, 'x': 12}, {'y': 6, 'x': 11}, {'y': 2, 'x': 13}, {'y': 6, 'x': 10}, {'y': 2, 'x': 14}, {'y': 7, 'x': 15}, {'y': 6, 'x': 15}, {'y': 7, 'x': 14}, {'y': 7, 'x': 13}, {'y': 5, 'x': 15}, {'y': 4, 'x': 15}, {'y': 7, 'x': 12}, {'y': 7, 'x': 11}, {'y': 3, 'x': 15}, {'y': 2, 'x': 15}, {'y': 1, 'x': 10}, {'y': 1, 'x': 11}, {'y': 1, 'x': 12}, {'y': 1, 'x': 13}, {'y': 7, 'x': 10}, {'y': 1, 'x': 14}, {'y': 1, 'x': 15}, {'y': 8, 'x': 16}, {'y': 7, 'x': 16}, {'y': 8, 'x': 15}, {'y': 8, 'x': 14}, {'y': 6, 'x': 16}, {'y': 5, 'x': 16}, {'y': 8, 'x': 13}, {'y': 8, 'x': 12}, {'y': 4, 'x': 16}, {'y': 3, 'x': 16}, {'y': 8, 'x': 11}, {'y': 8, 'x': 10}, {'y': 2, 'x': 16}, {'y': 1, 'x': 16}]}

