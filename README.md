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

*linux*: `which pip3` should return 
>`/flashcarpi/venv/bin/pip3`

*windows*: `where pip` should return 
>`\flashcarpi\venv\Scripts\pip.exe `

*linux*: `which python` should return 
>`/flashcarpi/venv/bin/python`

*windows*: `where python` should return 
>`\flashcarpi\venv\Scripts\python.exe`


# Install dependencies
make sure loaction is set in the `flashcarpi/` folder and the (venv) is active.

run `pip install -r requirements.txt`

**check if dependencies are installed correctly**

`pip list` should return a list of 3rd-party dependencies required for this project
