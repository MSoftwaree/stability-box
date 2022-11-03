from core.control import StabilityControl
from core.web_page import PageGenerator
from core.page_request import PageRequest
import cherrypy
import cherrypy_cors
import threading
import time

conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
            'cors.expose.on': True
        }
    }

cherrypy_cors.install()


stab = StabilityControl()
stab.create_stability_stations_list()
stab.read_station_test_plans()
stab.update_stations_statuses()
stab.activation_of_leds()

page = PageGenerator(stab)


def start_requests():
    cherrypy.quickstart(PageRequest(stab, page), '/', conf)


requests = threading.Thread(target=start_requests)
requests.start()

while True:
    stab.update_stations_statuses()
    stab.activation_of_leds()
    page.generate_page()
    time.sleep(1800)
