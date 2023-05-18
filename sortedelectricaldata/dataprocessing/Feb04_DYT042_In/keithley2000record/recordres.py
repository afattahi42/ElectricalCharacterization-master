import time
import serial

filename = 'resistivitytest.txt'

# configure the serial connections
ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=19200
)
ser.close()
ser.open()
ser.isOpen()

while True :
  #\r\n is for device terminators set to CR LF
  ser.write(':FETCh?\r\n'.encode('utf-8'))
  #wait one second before reading output.
  time.sleep(1)
  out=''
  while ser.inWaiting() > 0:
    out += ser.read(1).decode('utf-8')
  if out != '':
      out=out.rstrip()
      f = open(filename, 'a')
      f.write("%s,%s"%(time.time(),out)+"\n")
      print("%s,%s"%(time.time(),out))
      f.close()
