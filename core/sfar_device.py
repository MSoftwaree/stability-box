from config.read_configuration import ReadConfiguration
from pymodbus.client.sync import ModbusSerialClient
from core.modbus_communication import ModbusLibrary


class SfarModules(ModbusLibrary):
    do_register = 51

    def __init__(self):
        self.config = ReadConfiguration(
            config_dir="config/",
            file_path="configuration.json").configuration
        self.client_modbus = ModbusSerialClient(port=self.config.RS485.PORT_COM,
                                                method=self.config.RS485.PROTOCOL,
                                                baudrate=self.config.RS485.BAUDRATE,
                                                parity=self.config.RS485.PARITY_BITS,
                                                stopbits=self.config.RS485.STOP_BITS,
                                                bytesize=self.config.RS485.DATA_BITS,
                                                timeout=self.config.RS485.TIMEOUT)
        self.modbus_id = 1
        self.modbus_init(self.client_modbus, self.modbus_id)
        super().__init__()

    def set_do_sfar_green(self, bit: int, value: bool) -> None:
        """
        Turn on/off the green LED
        :param bit: Number of LED
        :param value: True/False
        """
        self.modbus_id = self.config.SFAR_MODULES.SFAR_GREEN
        self.write_coils(self.do_register, bit, value)

    def read_do_sfar_green(self, bit: int) -> bool:
        """
        Read state of the specific green LED
        :param bit: Number of LED
        :return: True when LED is on, False when LED is off
        """
        self.modbus_id = self.config.SFAR_MODULES.SFAR_GREEN
        return self.read_coil(self.do_register, bit)

    def set_do_sfar_red(self, bit: int, value: bool) -> None:
        """
        Turn on/off the red LED
        :param bit: Number of LED
        :param value: True/False
        """
        self.modbus_id = self.config.SFAR_MODULES.SFAR_RED
        self.write_coils(self.do_register, bit, value)

    def read_do_sfar_red(self, bit: int) -> bool:
        """
        Read state of the specific red LED
        :param bit: Number of LED
        :return: True when LED is on, False when LED is off
        """
        self.modbus_id = self.config.SFAR_MODULES.SFAR_RED
        return self.read_coil(self.do_register, bit)

    def set_all_leds(self, value: int) -> None:
        """
        Possibility of all LEDs bitwise control
        :param value: Bit value in decimal units
        """
        self.modbus_id = self.config.SFAR_MODULES.SFAR_GREEN
        self.write_reg(self.do_register, value)
        self.modbus_id = self.config.SFAR_MODULES.SFAR_RED
        self.write_reg(self.do_register, value)
