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

def setModel(modelAux):
    global model
    ltnr.model = modelAux
    model = modelAux
    ltnr.externalHandlers = [
            (r"/api/v1/soba/getpositionsfire?", getPositionsFire),
            (r"/api/v1/soba/getexitwayavatar/([0-9]+)?&([n-z]+)?", getExitWayAvatar)
            ]