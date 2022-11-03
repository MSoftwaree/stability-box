import cherrypy


@cherrypy.expose
class PageRequest:

    def __init__(self, stab, page):
        self.page = page
        self.stab = stab

    def GET(self, station_name):
        """ Get response from web site and control the LEDs accordingly """
        station_name = station_name.removesuffix("_BUTTON")
        self.stab.stations[station_name]['alarm_confirmed'] = True
        self.stab.stations[station_name]['status'] = True
        self.stab.activation_of_leds()
        self.page.generate_page()
        return station_name
