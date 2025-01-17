GET_CONFIG = 0x01
SET_CONFIG = 0x02
READ_VBATT = 0x03
FIVE_BAUD_INIT = 0x04
FAST_INIT = 0x05
CLEAR_TX_BUFFER = 0x07
CLEAR_RX_BUFFER = 0x08
CLEAR_PERIODIC_MSGS = 0x09
CLEAR_MSG_FILTERS = 0x0A
CLEAR_FUNCT_MSG_LOOKUP_TABLE = 0x0B
ADD_TO_FUNCT_MSG_LOOKUP_TABLE = 0x0C
DELETE_FROM_FUNCT_MSG_LOOKUP_TABLE = 0x0D
READ_PROG_VOLTAGE = 0x0E
SW_CAN_HS = 0x8000
SW_CAN_NS = 0x8001
SET_POLL_RESPONSE = 0x8002
BECOME_MASTER = 0x8003

DATA_RATE = 0x01
LOOPBACK = 0x03
NODE_ADDRESS = 0x04
NETWORK_LINE = 0x05
P1_MAX = 0x07
P3_MIN = 0x0A
P4_MIN = 0x0C
W1 = 0x0E
W2 = 0x0F
W3 = 0x10
W4 = 0x11
W5 = 0x12
TIDLE = 0x13
TINIL = 0x14
TWUP = 0x15
PARITY = 0x16
BIT_SAMPLE_POINT = 0x17
SYNC_JUMP_WIDTH = 0x18
W0 = 0x19
T1_MAX = 0x1A
T2_MAX = 0x1B
T4_MAX = 0x1C
T5_MAX = 0x1D
ISO15765_BS = 0x1E
ISO15765_STMIN = 0x1F
DATA_BITS = 0x20
FIVE_BAUD_MOD = 0x21
BS_TX = 0x22
STMIN_TX = 0x23
T3_MAX = 0x24
ISO15765_WFT_MAX = 0x25

# J2534-2
CAN_MIXED_FORMAT = 0x8000  # /*-2*/
J1962_PINS = 0x8001  # /*-2*/
SW_CAN_HS_DATA_RATE = 0x8010  # /*-2*/
SW_CAN_SPEEDCHANGE_ENABLE = 0x8011  # /*-2*/
SW_CAN_RES_SWITCH = 0x8012  # /*-2*/
ACTIVE_CHANNELS = 0x8020  # Bitmask of channels being sampled
SAMPLE_RATE = 0x8021  # Samples/second or Seconds/sample
SAMPLES_PER_READING = 0x8022  # Samples to average into a single reading
READINGS_PER_MSG = 0x8023  # Number of readings for each active channel per PASSTHRU_MSG structure
AVERAGING_METHOD = 0x8024  # The way in which the samples will be averaged.
SAMPLE_RESOLUTION = 0x8025  # The number of bits of resolution for each channel in the subsystem. Read Only.
INPUT_RANGE_LOW = 0x8026  # Lower limit in millivolts of A/D input. Read Only.
INPUT_RANGE_HIGH = 0x8027  # Upper limit in millivolts of A/D input. Read Only.


# Dict for converting string parameters to hex values.
convert = {
    'DATA_RATE': DATA_RATE,
    'LOOPBACK': LOOPBACK,
    'NODE_ADDRESS': NODE_ADDRESS,
    'NETWORK_LINE': NETWORK_LINE,
    'P1_MAX': P1_MAX,
    'P3_MIN': P3_MIN,
    'P4_MIN': P4_MIN,
    'W1': W1,
    'W2': W2,
    'W3': W3,
    'W4': W4,
    'W5': W5,
    'TIDLE': TIDLE,
    'TINIL': TINIL,
    'TWUP': TWUP,
    'PARITY': PARITY,
    'BIT_SAMPLE_POINT': BIT_SAMPLE_POINT,
    'SYNC_JUMP_WIDTH': SYNC_JUMP_WIDTH,
    'W0': W0,
    'T1_MAX': T1_MAX,
    'T2_MAX': T2_MAX,
    'T4_MAX': T4_MAX,
    'T5_MAX': T5_MAX,
    'ISO15765_BS': ISO15765_BS,
    'ISO15765_STMIN': ISO15765_STMIN,
    'DATA_BITS': DATA_BITS,
    'FIVE_BAUD_MOD': FIVE_BAUD_MOD,
    'BS_TX': BS_TX,
    'STMIN_TX': STMIN_TX,
    'T3_MAX': T3_MAX,
    'ISO15765_WFT_MAX': ISO15765_WFT_MAX,
    'CAN_MIXED_FORMAT': CAN_MIXED_FORMAT,
    'J1962_PINS': J1962_PINS,
    'SW_CAN_HS_DATA_RATE': SW_CAN_HS_DATA_RATE,
    'SW_CAN_SPEEDCHANGE_ENABLE': SW_CAN_SPEEDCHANGE_ENABLE,
    'SW_CAN_RES_SWITCH': SW_CAN_RES_SWITCH,
    'ACTIVE_CHANNELS': ACTIVE_CHANNELS,
    'SAMPLE_RATE': SAMPLE_RATE,
    'SAMPLES_PER_READING': SAMPLES_PER_READING,
    'READINGS_PER_MSG': READINGS_PER_MSG,
    'AVERAGING_METHOD': AVERAGING_METHOD,
    'SAMPLE_RESOLUTION': SAMPLE_RESOLUTION,
    'INPUT_RANGE_LOW': INPUT_RANGE_LOW,
    'INPUT_RANGE_HIGH': INPUT_RANGE_HIGH
}
convert_reverse = {value: key for key, value in convert.items()}

ioctl_convert = {
    'GET_CONFIG': GET_CONFIG,
    'SET_CONFIG': SET_CONFIG,
    'READ_VBATT': READ_VBATT,
    'FIVE_BAUD_INIT': FIVE_BAUD_INIT,
    'FAST_INIT': FAST_INIT,
    'CLEAR_TX_BUFFER': CLEAR_TX_BUFFER,
    'CLEAR_RX_BUFFER': CLEAR_RX_BUFFER,
    'CLEAR_PERIODIC_MSGS': CLEAR_PERIODIC_MSGS,
    'CLEAR_MSG_FILTERS': CLEAR_MSG_FILTERS,
    'READ_PROG_VOLTAGE': READ_PROG_VOLTAGE,
}
ioctl_reverse = {value: key for key, value in ioctl_convert.items()}

