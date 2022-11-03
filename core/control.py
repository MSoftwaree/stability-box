from core.sfar_device import SfarModules
from config.read_configuration import ReadConfiguration
from core.get_status import TDPClient
from graphql_api.plugins import *


def check_circuit_number(function):
    def decorator(*args, **kwargs):
        if not 1 <= args[1] <= 16:
            print("Wrong circuit number!")
            return False
        return function(*args, **kwargs)
    return decorator


class StabilityControl(SfarModules):
    number_of_stations = 16

    def __init__(self):
        self.stations = {"STATION_" + str(i): {'name': None, 'status': None, 'test_plans': None,
                                               'alarm_confirmed': True}
                         for i in range(1, self.number_of_stations + 1)}
        self.thread_flag = False
        super().__init__()

    @check_circuit_number
    def stability_alarm(self, circuit: int):
        """
        If stability is in alarm, green light is off, red light is on
        :param circuit: Number of checking circuit
        """
        self.set_do_sfar_red(circuit - 1, True)
        self.set_do_sfar_green(circuit - 1, False)

    @check_circuit_number
    def stability_ok(self, circuit: int):
        """
        If stability is ok, green light is on, red light is off
        :param circuit: Number of checking circuit
        """
        self.set_do_sfar_red(circuit - 1, False)
        self.set_do_sfar_green(circuit - 1, True)

    def create_stability_stations_list(self):
        """ Reading stability_config.json file. If station is not empty it is added to stations dictionary,
        for example: {'STATION_1'}: {'name: 'RAC18'}} """
        config = ReadConfiguration(config_dir="stability_data_base/", file_path="stability_config.json").configuration

        for station_number in range(1, self.number_of_stations + 1):
            check_station = eval("config.STATIONS.STATION_" + str(station_number))
            if check_station != "EMPTY":
                self.stations['STATION_' + str(station_number)]['name'] = check_station

    def read_station_test_plans(self):
        """ Reading station json file for list of test plans """
        for station in self.stations:
            if self._check_if_station_is_empty(station) is False:
                continue

            station_file = (self.stations[station]['name']).lower() + ".json"

            config = ReadConfiguration(config_dir="stability_data_base/stations/",
                                       file_path=station_file).configuration

            station_test_plans = eval("config." + str(self.stations[station]['name']) + ".TEST_PLANS")

            self.stations[station]['test_plans'] = station_test_plans

    def update_stations_statuses(self):
        """ Update all statuses for active stations in stations_statuses dictionary """
        for station in self.stations:
            if self._check_if_station_is_empty(station) is False:
                continue

            test_plans = self.stations[station]['test_plans']

            fail_counter = 0
            for test_plan in test_plans:

                if self._verify_test_plan_status(test_plan) is False:
                    fail_counter += 1
                    break

            if fail_counter > 0 or self.stations[station]['alarm_confirmed'] is False:
                self.stations[station]['status'] = False
            else:
                self.stations[station]['status'] = True

    def activation_of_leds(self):
        """ Appropriate control of the LEDs due to the status of the station """
        for station in self.stations:
            station_number = int(station.removeprefix("STATION_"))

            if self.stations[station]['status'] is True and self.stations[station]['alarm_confirmed'] is True:
                self.stability_ok(station_number)
            elif self.stations[station]['status'] is None:
                pass
            else:
                self.stations[station]['alarm_confirmed'] = False
                self.stability_alarm(station_number)

    @staticmethod
    def _verify_test_plan_status(tdp: str) -> bool:
        """
        Verification specific test plan status
        :param tdp: Test plan number, for example: TDP-1234
        :return: True if status is Passed, False for every other status
        """
        plug = Jira_plugin("key", "components")
        client = TDPClient(plug)
        result = client.get_tdp_last_exec_status(tdp)
        if result != "PASSED":
            return False
        else:
            return True

    def _check_if_station_is_empty(self, station) -> bool:
        """ Verify empty station """
        if self.stations[station]['name'] is None:
            return False
        else:
            return True
