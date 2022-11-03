class PageGenerator(object):
    page_title = "Stability control"
    logo = "https://www.ismacontrolli.com/pub/media/logo/stores/2/iSMACONTROLLI-logo-hd.png"
    title_margin = "160"
    stations_margin = "170"
    file_name = "control_page.html"

    def __init__(self, stability):
        self.stab = stability

    def generate_page(self):
        """ Create html file """

        html_file = open(self.file_name, 'w')

        page = f"""
        <!DOCTYPE html>
        
        <html>
        <head>
        <title>{self.page_title}</title>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
        </head>
        <body>
            {self._script()}
            <img src={self.logo} alt="">
            <h1 style="margin-left: {self.title_margin}px">{self.page_title}</h1>
            {self._station_information()}
        </body>
        </html>"""

        html_file.write(page)
        html_file.close()

    def _station_information(self) -> str:
        """ Prepare all stations information for web page including station number, station name and station status """
        stations_information = ""

        for station in self.stab.stations:
            name = self._prepare_name_for_station(station)
            status, color = self._prepare_status_and_color_for_station(station)
            button = self._prepare_button_for_station(station, name)

            # add station to the page
            stations_information += f"""
                        <p id="{station}_ID" style='color:{color}; margin-left: {self.stations_margin}px;'>{station} -
                        {name} - {status} {button}
                        </p>"""

        return stations_information

    @staticmethod
    def _script() -> str:
        """ Prepare function in JavaScript for buttons """
        script = """<script>
                    function confirm_alarm(station, name, id){
                        const elem = document.getElementById(station + '_ID');
                        elem.innerHTML = station + " - " + name + " - OK!";
                        elem.style.color = 'green';
                        $.get("http://localhost:8080/", { station_name: id });
                    }
                    </script>"""

        return script

    def _confirm_alarm(self, station):
        """
        Change all needed data for confirm alarm. Activate the LEDs on stability board
        :param station: Station
        """
        self.stab.stations[station]['alarm_confirmed'] = True
        self.stab.stations[station]['status'] = True
        self.stab.activation_of_leds()

    def _prepare_name_for_station(self, station: str) -> str:
        """
        Prepare name for station
        :param station: Station
        :return: Station name if exist. In the other case, the name is EMPTY
        """
        if self.stab.stations[station]['name'] is None:
            name = "EMPTY"
        else:
            name = self.stab.stations[station]['name']
        return name

    def _prepare_status_and_color_for_station(self, station: str) -> tuple:
        """
        Prepare status info and correct color
        :param station: Station
        :return: Status and color in tuple
        """
        if self.stab.stations[station]['status'] is None:
            status, color = "None", "blue"
        elif self.stab.stations[station]['status'] is True:
            status, color = "OK!", "green"
        else:
            status, color = "Alarm!", "red"
        return status, color

    def _prepare_button_for_station(self, station: str, name: str) -> str:
        """
        Create a button if station is in alarm
        :param station: Station
        :param name: Station name
        :return: Script for station button if station is in alarm. In the other case return empty string
        """
        if self.stab.stations[station]['status'] is False:
            button = f"""
            <button type=\"submit\" id=\"{station}_BUTTON\" onclick=\"confirm_alarm('{station}', '{name}', this.id)\"
            >Confirm Alarm</button>"""
        else:
            button = ""
        return button
