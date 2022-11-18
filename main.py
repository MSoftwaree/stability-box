from core.control import StabilityControl
from core.web_page import PageGenerator
from core.page_request import PageRequest, Root
import cherrypy
import cherrypy_cors
import threading
import time


cherrypy.config.update({
    'global': {
        'environment': 'test_suite',
        'server.socket_host': '192.168.67.142',
        'server.socket_port': 8080,
        'cors.expose.on': True
    }
})

cherrypy_cors.install()

stab = StabilityControl()
stab.create_stability_stations_list()
stab.read_station_test_plans()
stab.update_stations_statuses()
stab.activation_of_leds()

page = PageGenerator(stab)

cherrypy.tree.mount(Root())
cherrypy.tree.mount(PageRequest(stab, page), '/api', {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}})


def start_requests():
    cherrypy.engine.start()
    cherrypy.engine.block()


requests = threading.Thread(target=start_requests)
requests.start()

while True:
    stab.update_stations_statuses()
    stab.activation_of_leds()
    page.generate_page()
    time.sleep(1800)
