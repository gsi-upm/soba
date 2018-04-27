from tornado import httpserver
from tornado.ioloop import IOLoop
import tornado.web
import json



"""
    In this file, the API is defined to obtain information about the simulation and control of avatars.
    Specifically, the API provide the next requests:

        /api/v1/soba/getmovementsoccupants
            Returns the movement of all occupants as a list of positions [x, y].

        /api/v1/soba/getpositionoccupants
            Returns the position of all occupants as a list of positions [x, y].

        /api/v1/soba/getstateoccupants
            Returns the state of all occupants as a String.

        /api/v1/soba/getmovementoccupant/id
            Returns the movement of one occupant given as orientation and speed.

        /api/v1/soba/getpositionoccupant/id
            Returns the position of one occupant as position [x, y].

        /api/v1/soba/getstatesoccupant/id
            Returns the state of one occupant as a String.

        /api/v1/soba/getfovoccupant/id
            Returns the FOV (field of view) of one occupant as a list of positiions [x, y].

        /api/v1/soba/getinfooccupant/id
            Returns the state, movement, position and FOV of one occupant.

        /api/v1/soba/putcreateavatar/id&x,y
            Creates an avatar with an id in an (x, y) position in the grid.

        /api/v1/soba/postposavatar/id&x,y
            Moves an avatar to the position (x, y) in the grid.
            
        Where:
            id is a number with the unique_id of an occupant.
            x and y are the two numbers with the grid coordinates.

"""
# Simulation model
global model
model = None

# External handlers to expand the API. 
global externalHandlers
externalHandlers = []

def setModel(modelAux):
    global model
    if not model:
        model = modelAux

# Defining Server Handlers
class getPresentation(tornado.web.RequestHandler):
    def get(self):
        global model
        response = ' Welcome to SOBA API! \n Simulation in step: {}'.format(model.NStep)
        self.write(response)

#Get methods without query
class getMovementsOccupants(tornado.web.RequestHandler):
    def get(self):
        global model
        data = model.getMovementsOccupants()
        response = json.dumps(data)
        self.write(response)

class getPositionOccupants(tornado.web.RequestHandler):
    def get(self):
        global model
        data = model.getPositionOccupants()
        response = json.dumps(data)
        self.write(response)

class getStatesOccupants(tornado.web.RequestHandler):
    def get(self):
        global model
        data = model.getStatesOccupants()
        response = json.dumps(data)
        self.write(response)

#Get methods with query
class getMovementOccupant(tornado.web.RequestHandler):
    def get(self, occupant_id):
        global model
        data = model.getMovementOccupant(occupant_id)
        response = json.dumps(data)
        self.write(response)

class getPositionOccupant(tornado.web.RequestHandler):
    def get(self, occupant_id):
        global model
        data = model.getPositionOccupant(occupant_id)
        response = json.dumps(data)
        self.write(response)

class getStateOccupant(tornado.web.RequestHandler):
    def get(self, occupant_id):
        global model
        data = model.getStateOccupant(occupant_id)
        response = json.dumps(data)
        self.write(response)

class getFOVOccupant(tornado.web.RequestHandler):
    def get(self, occupant_id):
        global model
        data = model.getFOVOccupant(occupant_id)
        response = json.dumps(data)
        self.write(response)

class getInfoOccupant(tornado.web.RequestHandler):
    def get(self, occupant_id):
        global model
        data = model.getInfoOccupant(occupant_id)
        response = json.dumps(data)
        self.write(response)

#Put methods with query
class putCreateAvatar(tornado.web.RequestHandler):
    def put(self, avatar_id, x, y):
        global model
        pos = (int(x), int(y))
        a = model.putCreateAvatar(avatar_id, pos)
        self.write('Avatar with id: {}, created in pos: {}'.format(a.unique_id, a.pos))

#Post methods with query
class postPosAvatar(tornado.web.RequestHandler):
    def post(self, avatar_id, x, y):
        global model
        pos = (int(x), int(y))
        a = model.postPosAvatar(avatar_id, pos)
        if not a:
            self.write('Error Avatar ID')
        else:
            self.write('Avatar with id: {}, moved to pos: {}'.format(a.unique_id, a.pos))

#Defining application
class Application(tornado.web.Application):
    global externalHandlers
    def __init__(self):
        internalHandlers = [
            (r"/?", getPresentation),
            (r"/api/v1/soba/getmovementsoccupants?", getMovementsOccupants),
            (r"/api/v1/soba/getpositionoccupants?", getPositionOccupants),
            (r"/api/v1/soba/getstateoccupants?", getStatesOccupants),
            (r"/api/v1/soba/getmovementoccupant/([0-9]+)?", getMovementOccupant),
            (r"/api/v1/soba/getpositionoccupant/([0-9]+)?", getPositionOccupant),
            (r"/api/v1/soba/getstatesoccupant/([0-9]+)?", getStateOccupant),
            (r"/api/v1/soba/getfovoccupant/([0-9]+)?", getFOVOccupant),
            (r"/api/v1/soba/getinfooccupant/([0-9]+)?", getInfoOccupant),
            (r"/api/v1/soba/putcreateavatar/([0-9]+)?&([0-9]+)?,([0-9]+)?", putCreateAvatar),
            (r"/api/v1/soba/postposavatar/([0-9]+)?&([0-9]+)?,([0-9]+)?", postPosAvatar),
        ]
        handlers = internalHandlers + externalHandlers
        tornado.web.Application.__init__(self, handlers)

#Run server method
def runServer(host='127.0.1.1', port=10000):
    global app
    print('server launched in port: {}.\n'.format(port))
    app = Application()
    app.listen(port, address=host)
    tornado.autoreload.start()
    IOLoop.current().start()