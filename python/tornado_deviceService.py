import tornado.web
import tornado.ioloop
import json
from NetworkManagement.Service.DeviceService import NetworkDeviceService
from NetworkManagement.Service.ConfigService import ConfigService

nds = NetworkDeviceService()
cs = ConfigService()

class DeviceHandler(tornado.web.RequestHandler):
    def get(self):
        devices = nds.getAllDevices()
        devices = [d.items() for d in devices]
        self.set_header("Content-Type", "application/json")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(json.dumps(devices))
        self.finish()

class ConfigHandler(tornado.web.RequestHandler):
    def get(self, device):
        nds.getDeviceByIP('')
        cs.get()

def make_app():
    return tornado.web.Application(
        [
            (r"/networkDevice", MainHandler),
            (r"/deviceConfig/(.+)", MainHandler),
        ]
    )

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
