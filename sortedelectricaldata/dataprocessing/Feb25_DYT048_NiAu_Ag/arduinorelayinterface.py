import serial


class Arduino:
    def __init__(self, port):
        self.instr = serial.Serial(port)

    def off(self):
        self.instr.write(b'0') # any character aside frrom '+' and '-' turns off

    def enable_P1(self):
        self.instr.write(b'+')

    def enable_P2(self):
        self.instr.write(b'-')



