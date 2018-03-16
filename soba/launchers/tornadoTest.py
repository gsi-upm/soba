from tornado import httpserver
from tornado import gen
from tornado.ioloop import IOLoop
import tornado.web

# Simulation model
global model
model = None

def setModel(modelAux):
    global model
    model = modelAux

# Defining Server


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello, world')

class CarHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('GET - Welcome to the CarHandler!\n')

    def post(self):
        self.write('POST - Welcome to the CarHandler!\n')

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/?", MainHandler),
            (r"/api/v1/cars/?", CarHandler),
            (r"/api/v1/cars/[0-9][0-9][0-9][0-9]/?", CarHandler)
        ]
        tornado.web.Application.__init__(self, handlers)

def runServer(host='127.0.0.1', port=7777):
    app = Application()
    app.listen(8000)
    IOLoop.instance().start()

runServer()