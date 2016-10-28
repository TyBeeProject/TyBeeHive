from sensors import RandomSensor

PID_FILE = '/run/tybeeback.pid'

HIVE_ID = 1

PAUSE_DELAY = 5

SENSORS_PATH = '/media/nowhere/Etude/TyBee/Code/TyBeeHive/sensors-enabled'

UPSTREAM_URL = 'http://127.0.0.1'
UPSTREAM_PORT = 8000
UPSTREAM_PATH = 'datas/putDatas'

# Sensor list with their configuration
SENSORS = [
    RandomSensor(0, "random Sensor")
]