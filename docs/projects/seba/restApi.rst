REST API
========

SEBA provides an API defined as a REST service (Get, Post, Pull and Push) to interact with the simulation. Specifically, the following methods are defined.


This API is supported by default at http://127.0.1.1:10000

.. admonition:: GET /api/v1/soba/getmovementsoccupants
  
  Return information about the movement all occupants are performing.

    Result:
      
      .. sourcecode:: js

        {
          "id_unique1": 
            {
              "speed": speed1, 
              "orientation": "orientation1"
            }, 
          "id_unique2": 
            {
              "speed": speed2, 
              "orientation": "orientation2"
            }
        }

    

      Double speed: Speed of the occupants in meters per second.
      String orientation: Orientation of movement as a cardinal point.
      

    Example:

      .. sourcecode:: js

        {
          "1": 
            {
              "speed": 0.71428, 
              "orientation": "E"
            }, 
          "0": 
            {
              "speed": 0.71428, 
              "orientation": "E"
            }, 
          "3": 
            {
              "speed": 0.71428, 
              "orientation": "E"
            },
          "100009":
            {
            }, 
          "2": 
            {
              "speed": 0.71428, 
              "orientation": "E"
            }
        }
      


.. admonition:: GET /api/v1/soba/getpositionoccupants
  
  Returns the position of all occupants on the grid x, y.

    Result:

      .. sourcecode:: js
      
        {
          "id_unique1": [x1, y1], 
          "id_unique2": [x2, y2]
        }
      ..
      
    Example:
    
      .. sourcecode:: js

        {
          "100009": [4, 4], 
          "1": [7, 8], 
          "0": [7, 14], 
          "3": [7, 15], 
          "2": [11, 10]
        }
     
      ..

.. admonition:: GET /api/v1/soba/getstateoccupants
  
  Returns the state or activity of all occupants.

    Result:

      .. sourcecode:: js

          {
            "id_unique1": "state1", 
            id_unique1: "state2"
          }


    Example:

      .. sourcecode:: js

      {
        "100009": "walking", 
        "1": "Resting", 
        "0": "Resting", 
        "3": "Resting", 
        "2": "Resting"
      }


.. admonition:: GET /api/v1/soba/getmovementoccupant/{id}
  
  Return information about the movement one occupant is performing. The unique_id of the occupant must be provided.

    Results:

      .. sourcecode:: js

        {
        "speed": speed, 
        "orientation": "orientation"
        }

    Example:

      .. sourcecode:: js

          {
          "speed": 0.71428, 
          "orientation": "E"
          }

.. admonition:: GET /api/v1/soba/getpositionoccupant/{id}
  
  Returns the position of one occupant on the grid x, y. The unique_id of the occupant must be provided.

    Result:

      .. sourcecode:: js

      [x, y]

    Example:

      .. sourcecode:: js

      [3, 15]

.. admonition:: GET /api/v1/soba/soba/getstatesoccupant/{id}
  
  Returns the state or activity of one occupant. The unique_id of the occupant must be provided.

    Result:

      .. sourcecode:: js

        "State"

    Example:

      .. sourcecode:: js

        "Resting"


.. admonition:: GET /api/v1/soba/getfovoccupant/{id}
  
  Returns the position of the FOV (field of vision) of one occupant. The unique_id of the occupant must be provided.

    Result:

      .. sourcecode:: js

        [
          [x1, y1], [x2, y2], [x3, y3], [x4, y4], ... , [xn, yn]
        ]

    Example:

      .. sourcecode:: js

        [
          [0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], 
          [7, 0], [8, 0], [9, 0], [0, 1], [1, 1], [2, 1], [3, 1], 
          [4, 1], [5, 1], [6, 1], [7, 1], [8, 1], [9, 1], [0, 2], 
          [1, 2], [2, 2], [3, 2], [4, 2], [5, 2], [6, 2], [7, 2], 
          [8, 2], [9, 2], [0, 3], [1, 3], [2, 3], [3, 3], [4, 3], 
          [5, 3], [6, 3], [7, 3], [8, 3], [9, 3], [0, 4], [1, 4], [2, 4], [3, 4], [4, 4], [5, 4], [6, 4], [7, 4], [8, 4], [9, 4], [0, 5], [1, 5], [2, 5], [3, 5], [4, 5], [5, 5], [6, 5], [7, 5], [8, 5], [9, 5], [0, 6], [1, 6], [2, 6], [3, 6], [4, 6], [5, 6], [6, 6], [7, 6], [8, 6], [9, 6], 
          [0, 7], [1, 7], [2, 7], [3, 7], [4, 7], [6, 7], [7, 7], [8, 7], [9, 7], [0, 8], [1, 8], [2, 8], [3, 8], [4, 8], [5, 8], [6, 8], [7, 8], [8, 8], [9, 8], [0, 9], [1, 9], [2, 9], [3, 9], [4, 9], [5, 9], [6, 9], [7, 9], [8, 9], [9, 9], [0, 10], [1, 10], [2, 10], [3, 10], [4, 10], 
          [5, 10], [6, 10], [7, 10], [8, 10], [9, 10], [10, 10], 
          [8, 11], [9, 11], [10, 11], [11, 11], [9, 12], [10, 12], [11, 12], [12, 12], [13, 12], [10, 13], [11, 13], 
          [12, 13], [13, 13], [14, 13], [11, 14], [12, 14], 
          [13, 14], [14, 14], [15, 14], [16, 14], [12, 15], 
          [13, 15], [14, 15], [15, 15], [16, 15], [17, 15], 
          [13, 16], [14, 16], [15, 16], [16, 16], [17, 16], 
          [18, 16], [14, 17], [15, 17], [16, 17], [17, 17], 
          [18, 17], [15, 18], [16, 18], [17, 18], [18, 18]
        ]



.. admonition:: GET /api/v1/soba/getinfooccupant/{id}
  
    Returns general information (unique_id, state, FOV, position and movement) of one occupant. The unique_id of the occupant must be provided.

      Result:

        .. sourcecode:: js

          {
            "state": "state", 
            "fov": [
              [x1, y1], [x2, y2], [x3, y3], [x4, y4], ... , [xn, yn]
            ], 
            "movement": {
              "orientation": "orientation", 
              "speed": speed
            }, 
            "position": [x0, y0], 
            "unique_id": unique_id
          }
    
         .. code-block:: json
            double unique_id: Unique identifier of an occupant.
            string state: State or activity of an occupant.
            double fov: Fielf of vision of an occupant.
            double position: Position on the grid as (x, y) of an occupant.
            double movement: Movement of an occupant.
            double speed: Speed of the occupants in meters per second.
            string orientation: Orientation of movement as a cardinal point.

      Example:

        .. sourcecode:: js

          {
            "state": "Resting", 
            "fov": [
                  [5, 0], [6, 0], [7, 0], [8, 0], [9, 0], [15, 0], [16, 0], [17, 0], [18, 0], [6, 1], [7, 1], [8, 1], [9, 1], [14, 1], [15, 1], [16, 1], [17, 1], [18, 1], [6, 2], [7, 2], [8, 2], [9, 2], [14, 2], [15, 2], [16, 2], [17, 2], [18, 2], [6, 3], [7, 3], [8, 3], [9, 3], [13, 3], [14, 3], [15, 3], [16, 3], [17, 3], [18, 3], [6, 4], [7, 4], [8, 4], [9, 4], [12, 4], [13, 4], [14, 4], [15, 4], [16, 4], [17, 4], [18, 4], [19, 4], [6, 5], [7, 5], [8, 5], [9, 5], [12, 5], [13, 5], [14, 5], [15, 5], [16, 5], [17, 5], [18, 5], [19, 5], [7, 6], [8, 6], [9, 6], [11, 6], [12, 6], [13, 6], [14, 6], [15, 6], [16, 6], [17, 6], [7, 7], [8, 7], [9, 7], [11, 7], [12, 7], [13, 7], [14, 7], [15, 7], [16, 7], [7, 8], [8, 8], [9, 8], [10, 8], [11, 8], [12, 8], [13, 8], [14, 8], [7, 9], [8, 9], [9, 9], [10, 9], [11, 9], [12, 9], [13, 9], [0, 10], [1, 10], [2, 10], [3, 10], [4, 10], [5, 10], [6, 10], [7, 10], [8, 10], [9, 10], [10, 10], [11, 10], [12, 10], [13, 10], [14, 10], [15, 10], [16, 10], [17, 10], [18, 10], [0, 11], [1, 11], [2, 11], [3, 11], [4, 11], [5, 11], [6, 11], [7, 11], [8, 11], [9, 11], [10, 11], [11, 11], [12, 11], [13, 11], [14, 11], [15, 11], [16, 11], [17, 11], [18, 11], [0, 12], [1, 12], [2, 12], [3, 12], [4, 12], [5, 12], [6, 12], [7, 12], [9, 12], [10, 12], [11, 12], [12, 12], [13, 12], [14, 12], [15, 12], [16, 12], [17, 12], [18, 12], [0, 13], [1, 13], [2, 13], [3, 13], [4, 13], [5, 13], [6, 13], [7, 13], [8, 13], [9, 13], [10, 13], [11, 13], [12, 13], [13, 13], [14, 13], [15, 13], [16, 13], [17, 13], [18, 13], [0, 14], [1, 14], [2, 14], [3, 14], [4, 14], [5, 14], [6, 14], [7, 14], [8, 14], [9, 14], [10, 14], [11, 14], [12, 14], [13, 14], [14, 14], [15, 14], [16, 14], [17, 14], [18, 14], [0, 15], [1, 15], [2, 15], [3, 15], [4, 15], [5, 15], [6, 15], [7, 15], [8, 15], [9, 15], [10, 15], [11, 15], [12, 15], [13, 15], [14, 15], [15, 15], [16, 15], [17, 15], [18, 15], [0, 16], [1, 16], [2, 16], [3, 16], [4, 16], [5, 16], [6, 16], [7, 16], [8, 16], [9, 16], [10, 16], [11, 16], [12, 16], [13, 16], [14, 16], [15, 16], [16, 16], [17, 16], [18, 16], [0, 17], [1, 17], [2, 17], [3, 17], [4, 17], [5, 17], [6, 17], [7, 17], [8, 17], [9, 17], [10, 17], [11, 17], [12, 17], [13, 17], [14, 17], [15, 17], [16, 17], [17, 17], [18, 17], [0, 18], [1, 18], [2, 18], [3, 18], [4, 18], [5, 18], [6, 18], [7, 18], [8, 18], [9, 18], [10, 18], [11, 18], [12, 18], [13, 18], [14, 18], [15, 18], [16, 18], [17, 18], [18, 18]
              ], 
            "movement": {
              "orientation": "E", 
              "speed": 0.71428
            }, 
            "position": [8, 12], 
            "unique_id": 1
        }


.. admonition:: PUT /api/v1/soba/putcreateavatar/{id}&{x},{y}
  
  Create an avatar object in a given position to be part of the simulation. The unique_id and the position (x, y) of the avatar must be provided.

    Results:

      .. sourcecode:: js

        Avatar with id: unique_id, created in pos: (x, y)

    Example:

      .. sourcecode:: js

        Avatar with id: 100009, created in pos: (3, 3)


.. admonition:: POST /api/v1/soba/postposavatar/{id}&{x},{y}
  
  Move an avatar object to a given position. The unique_id and the new position (x, y) of the avatar must be provided.

    Result:

      .. sourcecode:: js

        Avatar with id: unique_id, moved to pos: (x, y)

    Example:

      .. sourcecode:: js

        Avatar with id: 100009, moved to pos: (3, 4)


.. admonition:: GET /api/v1/seba/getpositionsfire
  
   Returns the positions where there is fire.

    Result:

      .. sourcecode:: js

        [
          [x1, y1], [x2, y2], ..., [xn, yn]
        ]

    Example:

      .. sourcecode:: js

        [
          [13, 15], [14, 15], [13, 16], [14, 16]
        ]


.. admonition:: PUT /api/v1/seba/putcreateemergencyavatar/{id}&{x},{y}
  
   Create an EmergencyAvatar object in a given position to be part of the simulation. The unique_id and the position (x, y) of the avatar must be provided.

    Result:

      .. sourcecode:: js

        Avatar with id: unique_id, created in pos: (x, y)

    Example:

      .. sourcecode:: js

        Avatar with id: 200009, created in pos: (4, 4)


.. admonition:: GET /api/v1/seba/getexitwayavatar/{id}&{strategy}
  
  Returns the path that an avatar must follow to evacuate the building based on a strategy. The unique_id of the avatar and the strategy used must be provided.

    Result:

      .. sourcecode:: js

        [
          [x1, y1], [x2, y2], [x3, y3], ..., [xn, yn]
        ]

    Example:

      .. sourcecode:: js

        [
          [3, 4], [2, 5], [1, 6], [0, 6]
        ]
