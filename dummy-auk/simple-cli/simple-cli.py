import serial
import time
import sys
import cmd
import os

sername = "/dev/tty.usbmodem204C397F32321"
ser = ''

def start():
    global ser 
    ser = serial.Serial(sername, 115200, timeout=1)    
    while True:
        print("starting...")
        ser.write(b'!START\n') 
        time.sleep(1)
        data = ser.readline().decode()
        if "Started ok" in data:
            print("Dummy started")
            break;

def checkSerial():
    if ser == '':
        print("Please run start command first!")
        return -1
    if not ser.is_open:
        print("Port is closed, run start command first")
        return -1
    try:
        ser.read() # Attempt to read from port 
    except serial.SerialException:
        print("Port device disconnected, run start command again")
        return -1
    except AttributeError:
        print("Port not open yet, run start command first")    
        return -1
    return 0

def stop():
    while True:
        print("stopping...")
        ser.write(b'!DISABLE\n') 
        time.sleep(1)
        data = ser.readline().decode()
        print(data)
        if "ok" in data:
            print("Dummy stopped")
            break;

def dce_kp(node, kp):
    if checkSerial() == -1:
        return
    s = '#SET_DCE_KP ' + node + ' ' + kp +'\n'
    data = s.encode('utf-8') 
    ser.write(data) 
    
def dce_ki(node, kp):
    if checkSerial() == -1:
        return
    s = '#SET_DCE_KI ' + node + ' ' + kp +'\n'
    data = s.encode('utf-8') 
    ser.write(data) 

def dce_kd(node, kp):
    if checkSerial() == -1:
        return
    s = '#SET_DCE_KD ' + node + ' ' + kp +'\n'
    data = s.encode('utf-8') 
    ser.write(data) 

def node_reboot(node):
    if checkSerial() == -1:
        return
    s = '#REBOOT ' + node +'\n'
    data = s.encode('utf-8') 
    ser.write(data) 

class DummyCLI(cmd.Cmd):
    completekey = 'tab'
    prompt = 'Dummy-> '

    def do_start(self, args):
        print("starting dummy ...")
        start()

    def do_stop(self, args):
        print("stopping dummy ...")
        stop()

    def do_kp(self, args):
        numbers = args.split()
        if len(numbers) < 2:
            print("Usage: kp node p_value")
            return
        
        dce_kp(numbers[0], numbers[1])

    def do_ki(self, args):
        numbers = args.split()
        if len(numbers) < 2:
            print("Usage: ki node i_value")
            return
        
        dce_ki(numbers[0], numbers[1])

    def do_kd(self, args):
        numbers = args.split()
        if len(numbers) < 2:
            print("Usage: kd node d_value")
            return
        
        dce_kd(numbers[0], numbers[1])

    def do_reboot(self, args):
        numbers = args.split()
        if len(numbers) < 1:
            print("Usage: reboot node")
            return
        
        node_reboot(numbers[0])

    def do_quit(self, args):
        return True

    def do_help(self, arg):
        print("""
        Welcome to Dummy simple command tool!
        Type help to see available commands.
        """)
        super().do_help(arg)

def main(args):
    cli = DummyCLI()
    cli.cmdloop()    
  
if __name__ == '__main__':
   main(sys.argv)
