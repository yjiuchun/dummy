# Simple_cli

- a tiny tunning tools for motor pid parameters
1. change sername = "/dev/tty.usbmodem204C397F32321" to your serial name, it can be found with dmesg command
1. 'python3 simple_cli.py' to start code
1. 'start' commnd to get serial port started and enable motors
1. 'kp 1 200', will change motor 1 P parameter to 200
1. 'reboot 1', will reboot motor 1 to enable new parameter
1. 'press motor key 1 to calibrate it again with new parameter'
1. 'stop' will disable motors
