from tornado import httpserver
from tornado.ioloop import IOLoop
import tornado.web
import json

# Simulation model
global model
model = None

global externalHandlers
externalHandlers = []

def setModel(modelAux):
    global model
    model = modelAux

# Defining Server Handlers
class getPresentation(tornado.web.RequestHandler):
    def get(self):
        global model
        reponse = ' Welcome to SOBA API¡ \n Simulation in step: {}'.format(model.NStep)
        self.write(response)

#Get methods without query
class getMovementsOccupants(tornado.web.RequestHandler):
    def get(self):
        global model
        data = model.getMovementsOccupants()
        reponse = json.dumps(data)
        self.write(response)

class getPositionOccupants(tornado.web.RequestHandler):
    def get(self):
        global model
        data = model.getPositionOccupants()
        reponse = json.dumps(data)
        self.write(response)

class getStatesOccupants(tornado.web.RequestHandler):
    def get(self):
        global model
        data = model.getStatesOccupants()
        reponse = json.dumps(data)
        self.write(response)

#Get methods with query
class getMovementsOccupant(tornado.web.RequestHandler):
    def get(self, occupant_id):
        global model
        data = model.getMovementsOccupant(occupant_id)
        reponse = json.dumps(data)
        self.write(response)

class getPositionOccupant(tornado.web.RequestHandler):
    def get(self, occupant_id):
        global model
        data = model.getPositionOccupant(occupant_id)
        reponse = json.dumps(data)
        self.write(response)

class getStateOccupant(tornado.web.RequestHandler):
    def get(self, occupant_id):
        global model
        data = model.getStateOccupant(occupant_id)
        reponse = json.dumps(data)
        self.write(response)

class getFOVOccupant(tornado.web.RequestHandler):
    def get(self, occupant_id):
        global model
        data = model.getFOVOccupant(occupant_id)
        reponse = json.dumps(data)
        self.write(response)

class getInfoOccupant(tornado.web.RequestHandler):
    def get(self, occupant_id):
        global model
        data = model.getInfoOccupant(occupant_id)
        reponse = json.dumps(data)
        self.write(response)

#Put methods with query
class putCreateAvatar(tornado.web.RequestHandler):
    def put(self, avatar_id, pos):
        global model
        a = model.putCreateAvatar(avatar_id, pos)
        self.write('Avatar with id: {}, created in pos: {}'.format(a.unique_id, a.pos))

#Post methods with query
class postPosAvatar(tornado.web.RequestHandler):
    def post(self, avatar_id, pos):
        global model
        a = model.postPosAvatar(avatar_id, pos)
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
            (r"/api/v1/soba/getmovementsoccupant?", getMovementsOccupant),
            (r"/api/v1/soba/getpositionoccupant/[0-9]+?", getPositionOccupant),
            (r"/api/v1/soba/getstatesoccupant/[0-9]+?", getStatesOccupant),
            (r"/api/v1/soba/getfovoccupant/[0-9]+?", getFOVOccupant),
            (r"/api/v1/soba/getinfooccupant/[0-9]+?", getInfoOccupant),
            (r"/api/v1/soba/putcreateavatar/[0-9]+?\([0-9]\,[0-9]\)?", putCreateAvatar),
            (r"/api/v1/soba/postposavatar/[0-9]+?\([0-9]\,[0-9]\)?", postPosAvatar),
        ]
        handlers = internalHandlers + externalHandlers
        tornado.web.Application.__init__(self, handlers)

'''
def divide():
    global counter
    global model
    while True:
        counter = counter + 1
        model.step()
'''

#Run server method
def runServer(host='127.0.0.1', port=7771):
    global app
    print('server ON')
    app = Application()
    app.listen(port, address=host)
    '''
    thread = threading.Thread(target=divide, args=())
    thread.start()
    '''
    tornado.autoreload.start()
    IOLoop.current().start()