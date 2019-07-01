REST API Definition
===================


SEBA provides an API defined as a REST service (Get, Post, Pull and Push) to interact with the simulation. Specifically, the following methods are defined.


This API is supported by default at http://127.0.0.1:10000



+-------------+----------------------------------------------+----------------------------------+
| HTTP Method | URI                                          | Action                           |
+=============+==============================================+==================================+
| GET         | /api/v1/occupants                            | List with all occupants          |
+-------------+----------------------------------------------+----------------------------------+
| GET         | /api/v1/occupants/movements                  | Movement of all occupants        |
+-------------+----------------------------------------------+----------------------------------+
| GET         | /api/v1/occupants/positions                  | Position of all occupants        |
+-------------+----------------------------------------------+----------------------------------+
| GET         | /api/v1/occupants/states                     | States of all occupants          |
+-------------+----------------------------------------------+----------------------------------+
| GET         | /api/v1/occupants/{id}                       | Information about one occupant   |
+-------------+----------------------------------------------+----------------------------------+
| GET         | /api/v1/occupants/{id}/movement              | Movement of one occupant         |
+-------------+----------------------------------------------+----------------------------------+
| GET         | /api/v1/occupants/{id}/position              | Position of one occupant         |
+-------------+----------------------------------------------+----------------------------------+
| GET         | /api/v1/occupants/{id}/state                 | State of one occupant            |
+-------------+----------------------------------------------+----------------------------------+
| GET         | /api/v1/occupants/{id}/fov                   | FOV of one occupant              |
+-------------+----------------------------------------------+----------------------------------+
| GET         | /api/v1/occupants/{id}/route/{route_id}      | Evacuation route of one occupant |
+-------------+----------------------------------------------+----------------------------------+
| GET         | /api/v1/occupants/{id}/fire                  | Fire in the one occupant's FOV   |
+-------------+----------------------------------------------+----------------------------------+
| PUT         | /api/v1/occupants/{id}                       | Create an emergency occupant     |
+-------------+----------------------------------------------+----------------------------------+
| POST        | /api/v1/occupants/{id}/position              | Move an occupant                 |
+-------------+----------------------------------------------+----------------------------------+
| GET         | /api/v1/fire                                 | Positions with fire              |
+-------------+----------------------------------------------+----------------------------------+




.. admonition:: GET /api/v1/occupants
  
  Return a list with all the occupants in the simulations.

    Result:
      
      .. sourcecode:: js

        {
          "occupants": 
            [
              unique_id1, unique_id2, ..., unique_idN
            ]
        }   
      

    Example:

      .. sourcecode:: js

        {
          "occupants": 
            [
              100001, 1, 0, 3, 2
            ]
        }
      


.. admonition:: GET /api/v1/occupants/movements
  
  Return information about the movement all occupants are performing.

    Result:
      
      .. sourcecode:: js

        {
          "unique_id1": 
            {
              "orientation": "orientation1",
              "speed": speed1 
            }, 
          "unique_id2": 
            {
              "orientation": "orientation2",
              "speed": speed2
            }
        }

    

      *Double speed: Speed of the occupants in meters per second.*
      
      *String orientation: Orientation of movement as a cardinal point.*
      

    Example:

      .. sourcecode:: js

        {
          "1":
            {
              "orientation": "E",
              "speed": 0.71428
            }, 
          "0":
            {
              "orientation": "W", 
              "speed": 0.71428
            }, 
          "3":
            {
              "orientation": "N", 
              "speed": 0.71428
            }, 
          "2": 
            {
              "orientation": "E",
              "speed": 0.71428
            }
        }
      


.. admonition:: GET /api/v1/occupants/positions
  
  Returns the position of all occupants on the grid x, y.

    Result:

      .. sourcecode:: js
      
        {
          "unique_id1": 
            {
              "x": x1, 
              "y": y1
            }, 
          "unique_id2": 
            {
              "x": x2,
              "y": y2
            },
          ...
            ,
          "unique_idN": 
            {
              "x": xN,
              "y": yN
            }
        }
      
    Example:
    
      .. sourcecode:: js

        {
          "100001": 
            {
              "x": 3, 
              "y": 5
            }, 
          "1": 
            {
              "x": 0,
              "y": 6
            }, 
          "0": 
            {
              "x": 11,
              "y": 10
            }, 
          "3": 
            {
              "x": 12,
              "y": 4
            }, 
          "2": 
            {
              "x": 7, 
              "y": 11
            }
        }

.. admonition:: GET /api/v1/occupants/states
  
  Returns the state or activity of all occupants.

    Result:

      .. sourcecode:: js

          {
            "unique_id1": "state1", 
            unique_id2: "state2"
          }


    Example:

      .. sourcecode:: js

        {
          "100001": "walking", 
          "1": "Resting", 
          "0": "Working in my laboratory", 
          "3": "Working in my laboratory", 
          "2": "Outside of building"
        }


.. admonition:: GET /api/v1/occupants/{id}
  
    Returns general information (unique_id, state, `FOV <http://www.roguebasin.com/index.php?title=Permissive_Field_of_View>`_ (field of vision), position and movement) of one occupant. The unique_id of the occupant must be provided.

      Result:

        .. sourcecode:: js

          {
            "occupant": 
              {
                "movement": 
                  {
                    "orientation": "orientation",
                    "speed": speed
                  }, 
                "unique_id": "unique_id", 
                "position": 
                  {
                    "x": x, 
                    "y": y
                  }, 
                        {
                "fov": 
                  [
                    {
                      "x": x1, 
                      "y": y1
                    }, 
                    {
                      "x": x2, 
                      "y": y2
                    }, 
                    {
                      "x": x3, 
                      "y": y3
                    }, 
                    ...
                    {
                      "x": xN, 
                      "y": yN
                    }
                  ],
                "state": "state"
              }
          }
    
      *double unique_id: Unique identifier of an occupant.*
      
      *string state: State or activity of an occupant.*
      
      *double fov: Fielf of vision of an occupant.*
      
      *double position: Position on the grid as (x, y) of an occupant.*
      
      *double movement: Movement of an occupant.*
      
      *double speed: Speed of the occupants in meters per second.*
      
      *string orientation: Orientation of movement as a cardinal point.*

      Example:

        .. sourcecode:: js

          {
            "occupant": 
              {
                "movement": 
                  {
                    "orientation": "E",
                    "speed": 0.71428
                  }, 
                "unique_id": "1", 
                "position": 
                  {
                    "x": 0, 
                    "y": 6
                  }, 
                "fov": 
                  [
                    {"x": 5, "y": 0}, {"x": 6, "y": 0}, {"x": 7, "y": 0}, {"x": 8, "y": 0}, {"x": 9, "y": 0}, {"x": 4, "y": 1}, {"x": 5, "y": 1}, {"x": 6, "y": 1}, {"x": 7, "y": 1}, {"x": 8, "y": 1}, {"x": 9, "y": 1}, {"x": 3, "y": 2}, {"x": 4, "y": 2}, {"x": 5, "y": 2}, {"x": 6, "y": 2}, {"x": 7, "y": 2}, {"x": 8, "y": 2}, {"x": 9, "y": 2}, {"x": 2, "y": 3}, {"x": 3, "y": 3}, {"x": 4, "y": 3}, {"x": 5, "y": 3}, {"x": 6, "y": 3}, {"x": 7, "y": 3}, {"x": 8, "y": 3}, {"x": 9, "y": 3}, {"x": 1, "y": 4}, {"x": 2, "y": 4}, {"x": 3, "y": 4}, {"x": 4, "y": 4}, {"x": 5, "y": 4}, {"x": 6, "y": 4}, {"x": 7, "y": 4}, {"x": 8, "y": 4}, {"x": 9, "y": 4}, {"x": 0, "y": 5}, {"x": 1, "y": 5}, {"x": 2, "y": 5}, {"x": 3, "y": 5}, {"x": 4, "y": 5}, {"x": 5, "y": 5}, {"x": 6, "y": 5}, {"x": 7, "y": 5}, {"x": 8, "y": 5}, {"x": 9, "y": 5}, {"x": 1, "y": 6}, {"x": 2, "y": 6}, {"x": 3, "y": 6}, {"x": 4, "y": 6}, {"x": 5, "y": 6}, {"x": 6, "y": 6}, {"x": 7, "y": 6}, {"x": 8, "y": 6}, {"x": 9, "y": 6}, {"x": 0, "y": 7}, {"x": 1, "y": 7}, {"x": 2, "y": 7}, {"x": 3, "y": 7}, {"x": 4, "y": 7}, {"x": 5, "y": 7}, {"x": 6, "y": 7}, {"x": 7, "y": 7}, {"x": 8, "y": 7}, {"x": 9, "y": 7}, {"x": 0, "y": 8}, {"x": 1, "y": 8}, {"x": 2, "y": 8}, {"x": 3, "y": 8}, {"x": 4, "y": 8}, {"x": 5, "y": 8}, {"x": 6, "y": 8}, {"x": 7, "y": 8}, {"x": 8, "y": 8}, {"x": 9, "y": 8}, {"x": 1, "y": 9}, {"x": 2, "y": 9}, {"x": 3, "y": 9}, {"x": 4, "y": 9}, {"x": 5, "y": 9}, {"x": 6, "y": 9}, {"x": 7, "y": 9}, {"x": 8, "y": 9}, {"x": 9, "y": 9}, {"x": 1, "y": 10}, {"x": 2, "y": 10}, {"x": 3, "y": 10}, {"x": 4, "y": 10}, {"x": 5, "y": 10}, {"x": 6, "y": 10}, {"x": 7, "y": 10}, {"x": 8, "y": 10}, {"x": 9, "y": 10}, {"x": 10, "y": 10}, {"x": 11, "y": 10}, {"x": 10, "y": 11}, {"x": 11, "y": 11}, {"x": 12, "y": 11}, {"x": 13, "y": 11}, {"x": 12, "y": 12}, {"x": 13, "y": 12}, {"x": 14, "y": 12}, {"x": 15, "y": 12}, {"x": 16, "y": 12}, {"x": 14, "y": 13}, {"x": 15, "y": 13}, {"x": 16, "y": 13}, {"x": 17, "y": 13}, {"x": 18, "y": 13}, {"x": 16, "y": 14}, {"x": 17, "y": 14}, {"x": 18, "y": 14}, {"x": 18, "y": 15}
                  ], 
                "state": "Working in my laboratory"
              }
          }


.. admonition:: GET /api/v1/occupants/{id}/movement
  
  Return information about the movement one occupant is performing. The unique_id of the occupant must be provided.

    Results:

      .. sourcecode:: js

          {
            "movement": 
              {
                "orientation": "orientation", 
                "speed": speed
              }
          }

      *Double speed: Speed of the occupants in meters per second.*
      
      *String orientation: Orientation of movement as a cardinal point.*
    Example:

      .. sourcecode:: js

          {
            "movement": 
              {
                "orientation": "E", 
                "speed": 0.71428
              }
          }

.. admonition:: GET /api/v1/occupants/{id}/position
  
  Returns the position of one occupant on the grid x, y. The unique_id of the occupant must be provided.

    Result:

      .. sourcecode:: js

        {
          "position" : 
            {
              "x": x, 
              "y": y
            }
        }

    Example:

      .. sourcecode:: js

        {
          "position" : 
            {
              "x": 4, 
              "y": 7
            }
        }

.. admonition:: GET /api/v1/occupants/{id}/state
  
  Returns the state or activity of one occupant. The unique_id of the occupant must be provided.

    Result:

      .. sourcecode:: js

        {"state": "state"}

    Example:

      .. sourcecode:: js

        {"state": "Working in my laboratory"}


.. admonition:: GET /api/v1/occupants/{id}/fov 
  
  Returns the position of the `FOV <http://www.roguebasin.com/index.php?title=Permissive_Field_of_View>`_ (field of vision) of one occupant. The unique_id of the occupant must be provided.

    Result:

      .. sourcecode:: js

        {
          "fov": 
            [
              {
                "x": x1, 
                "y": y1
              }, 
              {
                "x": x2, 
                "y": y2
              }, 
              {
                "x": x3, 
                "y": y3
              }, 
              ...
              {
                "x": xN, 
                "y": yN
              }
            ]
        }

    Example:

      .. sourcecode:: js

        {
          "fov": 
            [
              {"x": 5, "y": 0}, {"x": 6, "y": 0}, {"x": 7, "y": 0}, {"x": 8, "y": 0}, {"x": 9, "y": 0}, {"x": 4, "y": 1}, {"x": 5, "y": 1}, {"x": 6, "y": 1}, {"x": 7, "y": 1}, {"x": 8, "y": 1}, {"x": 9, "y": 1}, {"x": 3, "y": 2}, {"x": 4, "y": 2}, {"x": 5, "y": 2}, {"x": 6, "y": 2}, {"x": 7, "y": 2}, {"x": 8, "y": 2}, {"x": 9, "y": 2}, {"x": 2, "y": 3}, {"x": 3, "y": 3}, {"x": 4, "y": 3}, {"x": 5, "y": 3}, {"x": 6, "y": 3}, {"x": 7, "y": 3}, {"x": 8, "y": 3}, {"x": 9, "y": 3}, {"x": 1, "y": 4}, {"x": 2, "y": 4}, {"x": 3, "y": 4}, {"x": 4, "y": 4}, {"x": 5, "y": 4}, {"x": 6, "y": 4}, {"x": 7, "y": 4}, {"x": 8, "y": 4}, {"x": 9, "y": 4}, {"x": 0, "y": 5}, {"x": 1, "y": 5}, {"x": 2, "y": 5}, {"x": 3, "y": 5}, {"x": 4, "y": 5}, {"x": 5, "y": 5}, {"x": 6, "y": 5}, {"x": 7, "y": 5}, {"x": 8, "y": 5}, {"x": 9, "y": 5}, {"x": 1, "y": 6}, {"x": 2, "y": 6}, {"x": 3, "y": 6}, {"x": 4, "y": 6}, {"x": 5, "y": 6}, {"x": 6, "y": 6}, {"x": 7, "y": 6}, {"x": 8, "y": 6}, {"x": 9, "y": 6}, {"x": 0, "y": 7}, {"x": 1, "y": 7}, {"x": 2, "y": 7}, {"x": 3, "y": 7}, {"x": 4, "y": 7}, {"x": 5, "y": 7}, {"x": 6, "y": 7}, {"x": 7, "y": 7}, {"x": 8, "y": 7}, {"x": 9, "y": 7}, {"x": 0, "y": 8}, {"x": 1, "y": 8}, {"x": 2, "y": 8}, {"x": 3, "y": 8}, {"x": 4, "y": 8}, {"x": 5, "y": 8}, {"x": 6, "y": 8}, {"x": 7, "y": 8}, {"x": 8, "y": 8}, {"x": 9, "y": 8}, {"x": 1, "y": 9}, {"x": 2, "y": 9}, {"x": 3, "y": 9}, {"x": 4, "y": 9}, {"x": 5, "y": 9}, {"x": 6, "y": 9}, {"x": 7, "y": 9}, {"x": 8, "y": 9}, {"x": 9, "y": 9}, {"x": 1, "y": 10}, {"x": 2, "y": 10}, {"x": 3, "y": 10}, {"x": 4, "y": 10}, {"x": 5, "y": 10}, {"x": 6, "y": 10}, {"x": 7, "y": 10}, {"x": 8, "y": 10}, {"x": 9, "y": 10}, {"x": 10, "y": 10}, {"x": 11, "y": 10}, {"x": 10, "y": 11}, {"x": 11, "y": 11}, {"x": 12, "y": 11}, {"x": 13, "y": 11}, {"x": 12, "y": 12}, {"x": 13, "y": 12}, {"x": 14, "y": 12}, {"x": 15, "y": 12}, {"x": 16, "y": 12}, {"x": 14, "y": 13}, {"x": 15, "y": 13}, {"x": 16, "y": 13}, {"x": 17, "y": 13}, {"x": 18, "y": 13}, {"x": 16, "y": 14}, {"x": 17, "y": 14}, {"x": 18, "y": 14}, {"x": 18, "y": 15}
            ]
        }



.. admonition:: PUT /api/v1/occupants/{id}
  
  Create an avatar object in a given position to be part of the simulation. The unique_id and the position (x, y) of the avatar must be provided.

    Args:

      .. sourcecode:: js

        {
          "x": x, 
          "y": y
        }

    Results:

      .. sourcecode:: js

        {
          "avatar": 
            {
              "position": 
                {
                  "x": x, 
                  "y": y
                }, 
              "id": unique_id
            }
        }

    Example:

      .. sourcecode:: js

        {
          "x": 4, 
          "y": 5
        }

      .. sourcecode:: js

        {
          "avatar": 
            {
              "position": 
                {
                  "x": 3, 
                  "y": 5
                }, 
              "id": 100010
            }
        }


.. admonition:: POST /api/v1/occupants/{id}/position
  
  Move an avatar object to a given position. The unique_id and the new position (x, y) of the avatar must be provided.

    Args:

      .. sourcecode:: js

        {
          "x": x, 
          "y": y
        }

    Result:

      .. sourcecode:: js

        {
          "avatar": 
            {
              "position": 
                {
                  "x": x, 
                  "y": y
                }, 
              "id": unique_id
            }
        }

    Example:

      .. sourcecode:: js

        {
          "x": 4, 
          "y": 5
        }

      .. sourcecode:: js

        {
          "avatar": 
            {
              "position": 
                {
                  "x": 4, 
                  "y": 5
                }, 
              "id": 100010
            }
        }



.. admonition:: GET /api/v1/occupants/{id}/route/{route_id}
  
  Returns the path that an avatar must follow to evacuate the building based on a strategy. The unique_id of the avatar and the strategy used must be provided.

    Result:

      .. sourcecode:: js

        {
          "positions": 
            [
              {
                "x": x1,
                "y": y1
              }, 
              {
                "x": x2,
                "y": y2
              }, 
              ...
              {
                "x": xN,
                "y": yN
              }
            ]
        }

    Example:

      .. sourcecode:: js

        {
          "positions": 
            [
              {
                "y": 14,
                "x": 2
              }, 
              {
                "y": 14,
                "x": 1
              }, 
              {
                "y": 14,
                "x": 0
              }
            ]
        }

.. admonition:: GET /api/v1/occupants/{id}/fire
  
  Returns the positions in the field of vision of the agent where there is fire. 

    Result:

      .. sourcecode:: js

        {
          "positions": 
            [
              {
                "x": x1,
                "y": y1
              }, 
              {
                "x": x2,
                "y": y2
              }, 
              ...
              {
                "x": xN,
                "y": yN
              }
            ]
        }

    Example:

      .. sourcecode:: js

        {
          "positions": 
            [
              {
                "y": 10,
                "x": 9
              }, 
              {
                "y": 11,
                "x": 8
              }, 
              {
                "y": 10,
                "x": 10
              }
            ]
        }


.. admonition:: PUT /api/v1/occupants/{id}
  
   Create an EmergencyAvatar object in a given position to be part of the simulation. The unique_id and the position (x, y) of the avatar must be provided.
    
    Args:

      .. sourcecode:: js

        {
          "x": x, 
          "y": y
        }

    Result:

      .. sourcecode:: js

        {
          "avatar": 
            {
              "position": 
                {
                  "x": x, 
                  "y": y
                }, 
              "id": unique_id
            }
        }

    Example:
      
      .. sourcecode:: js

        {
          "x": 3, 
          "y": 2
        }

      .. sourcecode:: js

        {
          "avatar": 
            {
              "position": 
                {
                  "x": 3, 
                  "y": 2
                }, 
              "id": 100001
            }
        }

.. admonition:: GET /api/v1/fire
  
   Returns the positions where there is fire.

    Result:

      .. sourcecode:: js

        {
          "positions": 
            [
              {
                "x": x1,
                "y": y1
              }, 
              {
                "x": x2,
                "y": y2
              },
              ...
              {
                "x": xN,
                "y": yN
              }
            ]
        }

    Example:

      .. sourcecode:: js

        {
          "positions": 
            [
              {"x": 7, "y": 9}, {"x": 8, "y": 10}, {"x": 8, "y": 9}, {"x": 6, "y": 9}, {"x": 6, "y": 8}, {"x": 7, "y": 10}, {"x": 7, "y": 8}, {"x": 6, "y": 10}, {"x": 8, "y": 8}
            ]
        }