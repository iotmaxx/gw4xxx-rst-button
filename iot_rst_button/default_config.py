from iot_rst_button.version import __version__

serviceDescription = "IoTmaxx reset button handler"
configFile = "/config/rst_button.cfg"
dbusService = "webconfig.service"
#serviceFile = "/config/iot_launcher.d/gwmqtt.json"

defaultConfig = {
    "com.iotmaxx.rst_button": {
#        'config':   '/data_inactive/webconfig.yaml',
        'config':   '/config/webconfig.yaml',
        'rst.ip':   True
    },
}
    
