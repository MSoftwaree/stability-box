class ModbusLibrary:
    client_modbus = None
    modbus_id = None

    def __init__(self):
        pass

    def modbus_init(self, client, modbus_id):
        self.client_modbus = client
        self.modbus_id = modbus_id

    def read_regs(self, address, count):
        result = self.client_modbus.read_holding_registers(address, count, unit=self.modbus_id)
        if hasattr(result, 'registers'):
            return result.registers
        else:
            return None

    def read_reg(self, address):
        registers = self.read_regs(address, 1)
        if registers is not None:
            registers = registers[0]
        return registers

    def read_coils(self, register, bit, count):
        result = self.client_modbus.read_coils(register * 16 + bit, count, unit=self.modbus_id)
        if hasattr(result, 'bits'):
            return result.bits
        else:
            return None

    def read_coil(self, register, bit):
        bits = self.read_coils(register, bit, 1)
        if bits is not None:
            bits = bits[0]
        return bits

    def write_reg(self, address, value):
        return self.client_modbus.write_register(address, value, unit=self.modbus_id)

    def write_coils(self, register, bit, value):
        return self.client_modbus.write_coil(register * 16 + bit, value, unit=self.modbus_id)
