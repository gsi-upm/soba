from tornado import httpserver
from tornado import gen
from tornado.ioloop import IOLoop
import tornado.web
from time import sleep
import threading

# Simulation model
global model
global counter
model = None
counter = 0

def setModel(modelAux):
    global model
    model = modelAux

# Defining Server
class getMovements(tornado.web.RequestHandler):
    def get(self):
        global model
        self.write('Movements given: {}¡'.format(counter))
       # return model.agentsMovement

class CarHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('GET - Welcome to the CarHandler {}!\n'.format(counter))

    def post(self):
        self.write('POST - Welcome to the CarHandler!\n')

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/?", getMovements),
            (r"/api/v1/cars/?", CarHandler),
            (r"/api/v1/cars/[0-9][0-9][0-9][0-9]/?", CarHandler)
        ]
        tornado.web.Application.__init__(self, handlers)

def divide():
    global counter
    global model
    while True:
        counter = counter + 1
        model.step()

def runServer(host='127.0.0.1', port=7771):
    print('server ON')
    app = Application()
    app.listen(port)
    thread = threading.Thread(target=divide, args=())
    thread.start()
    tornado.autoreload.start()
    IOLoop.current().start()