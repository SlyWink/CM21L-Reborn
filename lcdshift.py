import RPi.GPIO as GPIO
import time

GPIO_SER   = 11
GPIO_RCLK  = 13
GPIO_SRCLK = 15

BIT_RS  = 1
BIT_E   = 2
BITS_DB = [5,6,7,4]


class ShiftReg:

  def __init__(self, pin_ser, pin_rclk, pin_srclk):
    self.pin_ser = pin_ser
    self.pin_rclk = pin_rclk
    self.pin_srclk = pin_srclk
    self.work_byte = 0
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(self.pin_ser, GPIO.OUT)
    GPIO.setup(self.pin_rclk, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(self.pin_srclk, GPIO.OUT, initial=GPIO.LOW)
    self.clear()

  def __del__(self):
    GPIO.cleanup()

  def send(self):
    for i in range(7,-1,-1):
      if self.work_byte & (1 << i) > 0:
        GPIO.output(self.pin_ser,GPIO.HIGH)
      else:
        GPIO.output(self.pin_ser,GPIO.LOW)
      GPIO.output(self.pin_srclk,GPIO.HIGH)
      GPIO.output(self.pin_srclk,GPIO.LOW)
    GPIO.output(self.pin_rclk,GPIO.HIGH)
    GPIO.output(self.pin_rclk,GPIO.LOW)

  def sendByte(self,byte):
    self.work_byte = byte
    self.send()

  def clear(self):
    self.sendByte(0)

  def setBit(self,bit,send=False):
    self.work_byte |= (1<<bit)
    if send: self.send()

  def setBits(self,bits,send=False):
    for b in bits:
      self.setBit(b,send)

  def clearBit(self,bit,send=False):
    self.work_byte &= ~(1<<bit)
    if send: self.send()

  def clearBits(self,bits,send=False):
    for b in bits:
      self.clearBit(b,send)

  def toggleBit(self,bit,send=False):
    if self.work_byte & (1<<bit) > 0:
      self.clearBit(bit)
    else:
      self.setBit(bit)
    if send: self.send()

  def toggleBits(self,bits,send=False):
    for b in bits:
      self.toggleBit(b,send)


CMD_CLEAR    = 0x01
CMD_HOME     = 0x02
CMD_ENTRY    = 0x04
CMD_CONTROL  = 0x08
CMD_SHIFT    = 0x10
CMD_FUNCTION = 0x20
CMD_CGRAM    = 0x40
CMD_DDRAM    = 0x80

FUNCTION_8BITS  = 0x10
FUNCTION_4BITS  = 0x00
FUNCTION_2LINES = 0x08
FUNCTION_1LINE  = 0x00
FUNCTION_5X11   = 0x04
FUNCTION_5X8    = 0x00

ENTRY_MOVE_RIGHT       = 0x02
ENTRY_MOVE_LEFT        = 0x00
ENTRY_DISPLAY_SHIFT    = 0x01
ENTRY_DISPLAY_NO_SHIFT = 0x00

CONTROL_DISPLAY_ON  = 0x04
CONTROL_DISPLAY_OFF = 0x00
CONTROL_CURSOR_ON   = 0x02
CONTROL_CURSOR_OFF  = 0x00
CONTROL_BLINK_ON    = 0x01
CONTROL_BLINK_OFF   = 0x00

DDRAM_SECOND_LINE_OFFSET = 0x40

DELAY_E      = 500e-9
DELAY_RS     = 50e-6
DELAY_NIBBLE = 0.0005

 
class HD44780():
  def __init__(self, sr_rs, sr_e, sr_db47,io_ser=GPIO_SER,io_rclk=GPIO_RCLK,io_srclk=GPIO_SRCLK):
    self.sr_rs, self.sr_e, self.sr_db47 = sr_rs, sr_e, sr_db47
    self.sr = ShiftReg(io_ser, io_rclk, io_srclk)
    # Init display in 4 bit mode
    self._sendHigh4(CMD_FUNCTION|FUNCTION_8BITS)
    self._sendHigh4(CMD_FUNCTION|FUNCTION_8BITS)
    self._sendHigh4(CMD_FUNCTION|FUNCTION_8BITS)
    self._sendHigh4(CMD_FUNCTION|FUNCTION_4BITS)
    # 2 lines, 5x8 font
    self._sendByte(CMD_FUNCTION|FUNCTION_4BITS|FUNCTION_2LINES|FUNCTION_5X8)
    # Cursor moves right, non display shift
    self._sendByte(CMD_ENTRY|ENTRY_MOVE_RIGHT|ENTRY_DISPLAY_NO_SHIFT)
    self.clear()
    self.setControl()

  def _sendLow4(self,byte):
    byte &= 0x0F
    for i in range(3,-1,-1):
      if byte & (1<<i) > 0:
        self.sr.setBit(self.sr_db47[i])
      else:
        self.sr.clearBit(self.sr_db47[i])
    self.sr.setBit(self.sr_e, True)
    time.sleep(DELAY_E)
    self.sr.clearBit(self.sr_e, True)
    time.sleep(0.005)

  def _sendHigh4(self,byte):
    self._sendLow4(byte >> 4)

  def _sendByte(self,byte):
    self._sendHigh4(byte)
    self._sendLow4(byte)

  def clear(self):
    self._sendByte(CMD_CLEAR)

  def setControl(self,display=True,cursor=False,blink=False):
    bits = 0
    if display: bits |= CONTROL_DISPLAY_ON
    if cursor:  bits |= CONTROL_CURSOR_ON
    if blink:   bits |= CONTROL_BLINK_ON
    self._sendByte(CMD_CONTROL|bits)

  def _writeRam(self,data):
    self.sr.setBit(self.sr_rs,True)
    for b in data:
      if type(b) is str:
        self._sendByte(ord(b))
      else:
        self._sendByte(b)
    self.sr.clearBit(self.sr_rs,True)

  def display(self,line,text):
    self._sendByte(CMD_DDRAM | (DDRAM_SECOND_LINE_OFFSET * line))
    self._writeRam("{:16s}".format(text))

  def customChar(self,index,bytes):
    self._sendByte(CMD_CGRAM | ((index & 0x3F) <<3))
    self._writeRam(bytes)
