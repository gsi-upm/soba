import json
import soba.launchers.listener as ltnr
from tornado import httpserver
from tornado.ioloop import IOLoop
import tornado.web


"""

    In this file, the API is defined to obtain information about the simulation and control of avatars.
    Specifically, the API provide the next requests:

        /api/v1/seba/getpositionsfire
            Returns all the position where there is fire as a list of [x, y].

        /api/v1/seba/getexitwayavatar/id&strategy
            Return the best way to be exit of the building in function of a given strategy.
            The way is given as a list of [x, y].

        /api/v1/seba/putcreateemergencyavatar/id&x,y
            Create an avatar on the position (x, y) on the grid.
            
        Where:
            id is a number with the unique_id of an occupant.
            x and y are the two numbers with the grid coordinates.
            strategy is one string of the next options: uncrowded, safest, nearest or lessassigned

"""

# Simulation model
global model
model = None

#Get methods without query
class getPositionsFire(tornado.web.RequestHandler):
    def get(self):
        global model
        data = model.getPositionsFire()
        response = json.dumps(data)
        self.write(response)

#Get methods with query
class getExitWayAvatar(tornado.web.RequestHandler):
    def get(self, avatar_id, strategy = 1):
        global model
        data = model.getExitWayAvatar(avatar_id, strategy)
        response = json.dumps(data)
        self.write(response)

class getFireInFOVAvatar(tornado.web.RequestHandler):
    def get(self, avatar_id):
        global model
        data = model.getFireInFOVAvatar(avatar_id)
        response = json.dumps(data)
        self.write(response)

#Put methods with query
class putCreateEmergencyAvatar(tornado.web.RequestHandler):
    def put(self, avatar_id, x, y):
        global model
        pos = (int(x), int(y))
        a = model.putCreateEmergencyAvatar(avatar_id, pos)
        self.write('Avatar with id: {}, created in pos: {}'.format(a.unique_id, a.pos))

def setModel(modelAux):
    global model
    ltnr.model = modelAux
    model = modelAux
    ltnr.externalHandlers = [
            (r"/api/v1/seba/getpositionsfire?", getPositionsFire),
            (r"/api/v1/seba/getexitwayavatar/([0-9]+)?&([0-9]+)?", getExitWayAvatar),
            (r"/api/v1/seba/putcreateemergencyavatar/([0-9]+)?&([0-9]+)?,([0-9]+)?", putCreateEmergencyAvatar)
            ]