# flowcontrolpy
Interfaces to arduino board for pneumatic flow control

Python version of this [Java package.](https://github.com/cabrittin/FlowControl)

Arduino firmware is available [here](https://github.com/cabrittin/arduino_state)

Within your python environment
```
pip install -r requirements.txt
```

Basic functionality can be demonstrated with
```
python run_flowcontrol.py
```

Modify config.ini for your Serial connection. 

This was primarily developed on linux. Super weird, but the one Windows machine that I tested required a delay after instatiating the Arduino class:
```
ard = Arduino()                                                                         
time.sleep(1) ##This delay was REQUIRED on the WINDOWS machine that I tested
```
