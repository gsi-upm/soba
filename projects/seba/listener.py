import json
import soba.launchers.listener as ltnr
from tornado import httpserver
from tornado.ioloop import IOLoop
import tornado.web

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
    def get(self, avatar_id, strategy = 'nearest'):
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
            (r"/api/v1/soba/getpositionsfire?", getPositionsFire),
            (r"/api/v1/soba/getexitwayavatar/([0-9]+)?&([n-z]+)?", getExitWayAvatar),
            (r"/api/v1/soba/putcreateemergencyavatar/([0-9]+)?&([0-9]+)?,([0-9]+)?", putCreateEmergencyAvatar)
            ]