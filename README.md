# FlashCarPi
utilization of a raspberry pi as a dash unit within a car

clone this environment to the RPi home directory

# Create virtual environment using venv
```
*linux*
cd /home/flashcarpi/
python3 -m venv ./venv
```
```
*windows*
cd \path\to\project\flashcarpi
python3 -m venv venv
```

# Get into virtual environment (venv)
once in the project folder activate the environment
```
*linux*
source ./venv/bin/activate
```
```
*windows*
venv\Scripts\activate
```
*should return*
>`(venv) pi@raspberrypi:~/flashcarpi $ `

**check python interpreter and pip location**

*linux*: `which python` should return 
>`/flashcarpi/venv/bin/python`

*linux*: `which pip3` should return 
>`/flashcarpi/venv/bin/pip3`

*windows*: `where python` should return 
>`\flashcarpi\venv\Scripts\python.exe`

*windows*: `where pip` should return 
>`\flashcarpi\venv\Scripts\pip.exe `

# Install dependencies
make sure loaction is set in the `flashcarpi/` folder and the (venv) is active.

run `pip install -r requirements.txt`

**check if dependencies are installed correctly**

`pip list` should return a list of 3rd-party dependencies required for this project

# Shutdown Script
move shutdowndowncheck.py to /home/pi/bin/button

tell the RPi to run the script on startup

 run `sudo nano /etc/rc.local` in terminal to edit the file
 
 then add the following before `exit 0`
 
 `python /home/pi/bin/button/shutdowncheck.py &`

# Setting up I2C
Open up a terminal window and type:  `sudo raspi-config`

>Choose option: 5 Interfacing Options

>Choose option: P5 I2C and hit enter

>Choose:  <Yes> to turn on the I2C interface
  
>Choose: Ok

>Choose:  Finish

set `dtoverlay=i2c-rtc,pcf8523` to `dtoverlay=i2c-bcm2708`
this is an older i2c protocol that doesnt default enable repeated start

Reboot the RPi
  
test with
`ls /dev/*i2c*`
it should return
>`/dev/i2c-1`

install the i2c tools to get the command line tools needed to interact with i2c.  `sudo apt-get install -y i2c-tools`

next test for the wired I2c devices `sudo i2cdetect -y 1`

it should return a grid similar to this


```
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- -- 
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
20: -- -- -- -- 24 -- -- -- -- -- -- -- -- -- -- -- 
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
60: -- -- 62 -- -- -- -- -- UU -- -- -- -- -- -- -- 
70: -- -- -- -- -- -- -- --  
```
the garmin lidar lite has the 0x62 address


# Setting up bluetooth OBD II 
plug the Bluetooth OBD II into the port inside the car

then run the following commands

```
bluetoothctl
power on      # ensures bluetooth is on
pairable on   # ensures bluetooth is pairable
agent on      # makes pairing persistent
default-agent
scan on       # scans for bluetooth devices
              # the OBDII adapter should read something
              # like this - 00:00:00:00:00:00 Name: OBDII
              # If it asks for a pin, the default pin is 1234
scan off      #turn off scanning once your adapter has been found
pair <adapter mac address>       #pair to your adapters mac address
trust <adapter mac address>      #keeps pairing even after reboot
quit                             #exits out of bluetoothctl
```

OBD is a serial port we need to bind it to a port on the pi

`sudo rfcomm bind rfcomm0 <adapter mac address>`

 **to get the bluetooth adapter to connect automatically**
 
 `sudo nano /etc/rc.local`
 
 then add the following before `exit 0`
 
 `rfcomm bind rfcomm0 <adapter mac address>`
 
 then edit the bluetooth config file
 
 `sudo nano /etc/systemd/system/dbus-org.bluez.service`
 
 find the line that says "ExecStart=/usr/lib/bluetooth/bluetoothd", and change it to this:
```
ExecStart=/usr/lib/bluetooth/bluetoothd -C
ExecStartPost=/usr/bin/sdptool add SP
```
