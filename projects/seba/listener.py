import json
import soba.launchers.listener as ltnr

global model
model = None

#Get methods without query
class getPositionsFire(tornado.web.RequestHandler):
    def get(self):
    	global model
    	data = model.getPositionsFire()
        reponse = json.dumps(data)
        self.write(response)

#Get methods with query
class getExitWayAvatar(tornado.web.RequestHandler):
    def get(self, id, strategy = 'nearest'):
    	global model
    	data = model.getExitWayAvatar(avatar_id, strategy)
        reponse = json.dumps(data)
        self.write(response)

def setModel(modelAux):
    global model
    ltnr.model = modelAux
    model = modelAux

def setHandlers(modelAux):
    ltnr.externalHandlers = [
            (r"/api/v1/soba/getpositionsfire?", getPositionFire),
            (r"/api/v1/soba/getexitwayavatar/[0-9]+?[a-z]?", getExitWayAvatar)
            ]