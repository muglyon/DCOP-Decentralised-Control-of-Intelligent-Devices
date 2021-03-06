# Constants

NB_ROOMS = 4
NB_ZONES = 4

DIMENSION = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 120, 180, 210, 241]
DIMENSION_SIZE = len(DIMENSION)
INFINITY_IDX = DIMENSION.index(241)


MIN_TAU_VALUE = 5
MAX_NB_DEVICES = 6
URGT_TIME = 30
T_SYNCHRO = 30
THIRTY_SECONDS = 30
TWO_MINUTS = 120
THREE_HOURS = 180
TIMEOUT = 60  # 1 min
INFINITY = 241

MQTT_SERVER = "10.33.120.182"
MQTT_PORT = 1883
KEEP_ALIVE_PERIOD = 60

DATA = "data"
VARS = "vars"

SERVER = "SERVER/"

# Log types
STATE = "State"
INFO = "Info"
DFS = "Dfs"
UTIL = "Util"
VALUE = "Value"
RESULTS = "Results"
LOG = "Log"
EVENT = "Event"
