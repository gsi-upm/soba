import os
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.escape
import tornado.gen
import webbrowser


class VisualizationElement:
    package_includes = []
    local_includes = []
    js_code = ''
    render_args = {}

    def __init__(self):
        pass

    def render(self, model):
        return "<b>VisualizationElement goes here</b>."

class PageHandler(tornado.web.RequestHandler):

    def get(self):
        elements = self.application.visualization_elements
        for i, element in enumerate(elements):
            element.index = i
        self.render("template.html", port=self.application.port,
                    model_name=self.application.model_name,
                    package_includes=self.application.package_includes,
                    local_includes=self.application.local_includes,
                    scripts=self.application.js_code)


class SocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        if self.application.verbose:
            print("Socket opened!")

    def check_origin(self, origin):
        return True

    def on_message(self, message):
        if self.application.verbose:
            print(message)
        msg = tornado.escape.json_decode(message)

        if msg["type"] == "get_step":
            self.application.model.step()
            self.write_message({"type": "viz_state",
                    "data": self.application.render_model()})

        elif msg["type"] == "reset":
            self.application.resetModel()
            self.write_message({"type": "viz_state",
                    "data": self.application.render_model()})

        else:
            if self.application.verbose:
                print("Unexpected message!")


class ModularServer(tornado.web.Application):
    verbose = True
    model_name = "SOBA Model"
    model_cls = None
    port = 7777
    canvas_width = 500
    canvas_height = 500
    grid_height = 0
    grid_width = 0
    max_steps = 1000000
    model_args = ()
    model_kwargs = {}
    page_handler = (r'/', PageHandler)
    socket_handler = (r'/ws', SocketHandler)
    static_handler = (r'/static/(.*)', tornado.web.StaticFileHandler,
                      {"path": os.path.dirname(__file__)})
    local_handler = (r'/local/(.*)', tornado.web.StaticFileHandler,
                     {"path": ''})

    handlers = [page_handler, socket_handler, static_handler, local_handler]
    settings = {"debug": True,
                "template_path": os.path.dirname(__file__)}

    def __init__(self, model_cls, visualization_elements, name="SOBA Model",
                 *args, **kwargs):
        self.visualization_elements = visualization_elements
        self.package_includes = set()
        self.local_includes = set()
        self.js_code = []
        for element in self.visualization_elements:
            for include_file in element.package_includes:
                self.package_includes.add(include_file)
            for include_file in element.local_includes:
                self.local_includes.add(include_file)
            self.js_code.append(element.js_code)
        self.model_name = name
        self.model_cls = model_cls
        self.model_args = args
        self.model_kwargs = kwargs
        self.resetModel()
        super().__init__(self.handlers, **self.settings)

    def resetModel(self):
        self.model = self.model_cls(*self.model_args, **self.model_kwargs)

    def render_model(self):
        visualization_state = []
        for element in self.visualization_elements:
            element_state = element.render(self.model)
            visualization_state.append(element_state)
        return visualization_state

    def launch(self, port=None):
        if port is not None:
            self.port = port
        url = 'http://127.0.0.1:{PORT}'.format(PORT=self.port)
        print('Interface starting at {url}'.format(url=url))
        self.listen(self.port)
        webbrowser.open(url)
        tornado.ioloop.IOLoop.instance().start()
