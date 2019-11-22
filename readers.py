from smartcard.System import readers
from smartcard.scard import SCARD_CTL_CODE, SCARD_SHARE_DIRECT, SCARD_SHARE_SHARED





class nfcReader():
    def __init__(self, reader):
        self._reader = reader.createConnection()
        self.direct_connection()
        self.remove_led_and_buzzer()
        
    def direct_connection(self):
        self._reader.connect(mode = SCARD_SHARE_DIRECT)
        
    def control(self, code, buffer):
        return self._reader.control(code, buffer)

    def remove_led_and_buzzer(self):
        pass
    def set_led(self, red, green):
        pass

class acr122uReader(nfcReader):

    pass

class acr1252uReader(nfcReader):
    def remove_led_and_buzzer(self):
        self._reader.control(SCARD_CTL_CODE(3500), [0xE0, 0x00, 0x00, 0x21, 0x01, 0x00])

    def beep(self, length = 5):
        #self._reader.control(SCARD_CTL_CODE(3500), [0xFF, 0x00, 0x40, 0xC3, 0x04, 0x04, 0x06, 0x01, 0x01]);
        self._reader.control(SCARD_CTL_CODE(3500), [0xE0, 0x00, 0x00, 0x28, 0x01, length]);

    def set_led(self, red, green):
        val = int('0b000000{}{}'.format(int(green), int(red)), 2)
        ans = self._reader.control(SCARD_CTL_CODE(3500), [0xE0, 0x00, 0x00, 0x29, 0x01, val])

    def led_and_buzzer_control(self, final_red_led_state, final_green_led_state, red_led_state_mask, green_led_state_mask, initial_red_led_blinking_state, initial_green_led_blinking_state, red_led_blinking_mask, green_led_blinking_mask, t1, t2, repetition, link_to_buzzer):
        #greenledblink, redledblink, green t1 or t2, red t1 or t2, green final state, red final state,
        led_state_control = int('0b{}{}{}{}{}{}{}{}'.format(int(final_red_led_state), int(final_green_led_state), int(red_led_state_mask), int(green_led_state_mask), int(initial_red_led_blinking_state), int(initial_green_led_blinking_state), int(red_led_blinking_mask), int(green_led_blinking_mask)),2)
        ans = self._reader.control(SCARD_CTL_CODE(3500), [0xFF, 0x00, 0x40, led_state_control, 0x04, int(t1),int(t2), int(repetition), int(link_to_buzzer)])

def getReader(readerNum = 0):
    reader = readers()[readerNum]
    if str(reader) == 'ACS ACR122U':
        return acr122uReader(reader)
    else:
        return acr1252uReader(reader)  
    
    """elif reader == 'ACS ACR1252 1S CL Reader [ACR1252 Dual Reader PICC] 00 00':
        print ('newone')
    else:
        print('not rego')
    pass
    """