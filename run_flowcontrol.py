"""
@name: run_flowcontrol.py                      
@description:                  

    Script to demonstrate usage of module flowcontrol.py

@author: Christopher Brittin   
@email: "cabrittin"+ <at>+ "gmail"+ "."+ "com"
@date: 2022-09              
"""

import argparse
import time

from flowcontrol import Arduino

CONFIG = 'config.ini'

if __name__=="__main__":
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-c','--config',
                dest = 'config',
                action = 'store',
                default = CONFIG,
                required = False,
                help = 'Config file')
    
    params = parser.parse_args()
    ard = Arduino(config_file=params.config) 
    
    print('Checking firmware')
    assert ard.checkFirmware(), f'Firmware {ard.firmwareVersion} not found on Arduino board'
    print(f'Firmware {ard.firmwareVersion} found')
    
    print('Turn on inject')
    ard.inject()
    time.sleep(1)   
    
    print('Turn on flush')
    ard.flush()
    time.sleep(1)   
    
    print('Turn on stimulus')
    ard.stimulus()
    time.sleep(1)

    print('Turn OFF')
    ard.off()
    time.sleep(1)

    print('Pulse')
    pulse_on = 500
    pulse_off = 500
    num_pulses = 5
    ard.pulse(pulse_on,pulse_off,num_pulses)


