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
