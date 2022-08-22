from gw4xxx_hal.gw4x00.internalIOs import GW4100UserButton, setLEDon
from iot_rst_button.default_config import defaultConfig, dbusService
import yaml
from pydbus import SystemBus
import json
import time

rstStates = ['init', 'idle', 'armed', 'reset', 'done' ]

def ipReset():
    bus = SystemBus()
    systemd = bus.get(".systemd1")
    iot_unit = bus.get(".systemd1", systemd.GetUnit(dbusService))
    # stop webconfig
    job1 = systemd.StopUnit(dbusService, "fail")
    if iot_unit.ActiveState != 'inactive':
        print("Waiting for service shutdown")
        time.sleep(1)
    if iot_unit.ActiveState != 'inactive':
        print("service shutdown failed")
#    print(f"will open: '{defaultConfig['com.iotmaxx.rst_button']['config']}'")
    with open(defaultConfig['com.iotmaxx.rst_button']['config'], "r+") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
#        print(json.dumps(data, indent=4))
        ethInterfaces = data['network']['ethernet']['interfaces']
        for interface in ethInterfaces:
            if interface['interface'] == 'eth0':
                interface["dhcp_client"]            = False
                interface["dhcp_server"]            = True
                interface["forwarding_via_modem"]   = False
                interface["ipv4"]                   = "192.168.1.1/24"
                interface["ipv6"]                   = ""
                interface["dhcp_server_offset"]     = 99
                interface["dhcp_server_size"]       = 10
                interface["dhcp_server_lease_time"] = 6
                f.seek(0)
                yaml.dump(data, f)
                f.truncate()    
    # start webconfig
    job2 = systemd.StartUnit(dbusService, "fail")
    if iot_unit.ActiveState != 'active':
        print("Waiting for service start")
        time.sleep(1)
    if iot_unit.ActiveState != 'active':
        print("service start failed")

def startHandler(config):
    rstState = 'idle'
    ledOn = False
    rstCnt = 30
    but = GW4100UserButton()
    while True:
        if rstState == 'init':
            rstCnt = 30
            ledOn = False
            setLEDon(1, False)
            rstState = 'idle'
        elif rstState == 'idle':
            if but.waitForButtonEvent() == 'pressed':
                rstState = 'armed'
        elif rstState == 'armed':
            if but.waitForButtonEvent(sec=0,nsec=100000000) == 'released':
                rstState = 'init'
            if rstCnt == 0:
                rstState = 'reset'
            else:
                rstCnt -= 1
                setLEDon(1, ledOn)
                ledOn = not ledOn
        elif rstState == 'reset':
#            print('Perform reset')
            ipReset()
            setLEDon(1, True)
            rstState = 'done'
        elif rstState == 'done':
            if but.waitForButtonEvent() == 'released':
                rstState = 'init'


