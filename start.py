import LTC3351

# dc590b_serial_port = 'COM99' #Modify this line as appropriate (for Linux, '/dev/ttyXX', etc)
# dc590b = LTC3351.ltc_dc590b_interface(serial_port = dc590b_serial_port, PEC = False)
# LTC3351.LTC3351.ARA = lambda self: dc590b.alert_response()
# chip = LTC3351.LTC3351(read_function = dc590b.read_word, write_function = dc590b.write_word, verbose = False)

# chip.print_status()

class regreader:
    def __init__(self, dumpFileName):
        self.dumpFileName = dumpFileName

    def read_word(self, addr_7bit, command_code):
        '''SMBus Read Word Protocol.
        Packet Error Checking controlled by class init.
        Slave device address specified in 7-bit format.
        Returns 16-bit data from slave.'''

        retVal = "XXXX"
        # addr_hex = '0x' + format(addr_7bit, '02X')
        command_code_hex = '0x' + format(command_code, '02X')
        # print("read_word addr_7bit", addr_7bit, addr_hex)
        # print("read_word command_code", command_code, command_code_hex)
        dumpFile = open(self.dumpFileName, "r")
        while True:
            lines = dumpFile.readline()
            words = lines.split()
            if command_code_hex in words[0]:
                retVal = words[1]    
                break
        # print("read_word retVal", int(retVal, 16))
        return int(retVal, 16)

    def write_word(self, addr_7bit, data16, command_code):
        print("called regreader.write_word function")


cls = regreader(dumpFileName="map_dump2.txt")

chip = LTC3351.LTC3351(read_function = cls.read_word, write_function = cls.write_word, verbose = False)

chip.print_status()

# from sys import argv

# script, file_dump = argv

# dump = open(file_dump, "r")
# Lines = dump.readlines()
# for line in Lines:
#     words = line.split()
#     match words:
#         case 0x00:
#  

