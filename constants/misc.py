CAN_XON_XOFF_PS = 0x800A
ANALOG_IN_1 = 0x800B
ANALOG_IN_2 = 0x800C
ANALOG_IN_3 = 0x800D
ANALOG_IN_4 = 0x800E
ANALOG_IN_5 = 0x800F
ANALOG_IN_6 = 0x8010
ANALOG_IN_7 = 0x8011
ANALOG_IN_8 = 0x8012
ANALOG_IN_9 = 0x8013
ANALOG_IN_10 = 0x8014
ANALOG_IN_11 = 0x8015
ANALOG_IN_12 = 0x8016
ANALOG_IN_13 = 0x8017
ANALOG_IN_14 = 0x8018
ANALOG_IN_15 = 0x8019
ANALOG_IN_16 = 0x801A
ANALOG_IN_17 = 0x801B
ANALOG_IN_18 = 0x801C
ANALOG_IN_19 = 0x801D
ANALOG_IN_20 = 0x801E
ANALOG_IN_21 = 0x801F
ANALOG_IN_22 = 0x8020
ANALOG_IN_23 = 0x8021
ANALOG_IN_24 = 0x8022
ANALOG_IN_25 = 0x8023
ANALOG_IN_26 = 0x8024
ANALOG_IN_27 = 0x8025
ANALOG_IN_28 = 0x8026
ANALOG_IN_29 = 0x8027
ANALOG_IN_30 = 0x8028
ANALOG_IN_31 = 0x8029
ANALOG_IN_32 = 0x802A

# See T3_MAX = 0x24

# ===========================Miscellaneous definitions=============================

SHORT_TO_GROUND = 0xFFFFFFFE
VOLTAGE_OFF = 0xFFFFFFFF

NO_PARITY = 0
ODD_PARITY = 1
EVEN_PARITY = 2

# SWCAN
DISBLE_SPDCHANGE = 0  # 2
ENABLE_SPDCHANGE = 1  # 2
DISCONNECT_RESISTOR = 0  # 2
CONNECT_RESISTOR = 1  # 2
AUTO_RESISTOR = 2  # 2

# Mixed Mode
CAN_MIXED_FORMAT_OFF = 0  # 2
CAN_MIXED_FORMAT_ON = 1  # 2
CAN_MIXED_FORMAT_ALL_FRAMES = 2  # 2

# ========================PassThruConnect definitions========================

# 0 = Receive standard CAN ID (11 bit)
# 1 = Receive extended CAN ID (29 bit)
CAN_29BIT_ID = 0x00000100

# 0 = The interface will generate and append the checksum as defined in ISO 9141-2 and ISO 14230-2 for
# transmitted messages, and verify the checksum for received messages.
# 1 = The interface will not generate and verify the checksum-the entire message will be treated as
# data by the interface
ISO9141_NO_CHECKSUM = 0x00000200

# 0 = either standard or extended CAN ID types used – CAN ID type defined by bit 8
# 1 = both standard and extended CAN ID types used – if the CAN controller allows prioritizing either standard
# (11 bit) or extended (29 bit) CAN ID's then bit 8 will determine the higher priority ID type
CAN_ID_BOTH = 0x00000800

# 0 = use L-line and K-line for initialization address
# 1 = use K-line only line for initialization address
ISO9141_K_LINE_ONLY = 0x00001000

# =================RxStatus definitions=================

# 0 = received i.e. this message was transmitted on the bus by another node
# 1 = transmitted i.e. this is the echo of the message transmitted by the PassThru device
TX_MSG_TYPE = 0x00000001

# 0 = Not a start of message indication
# 1 = First byte or frame received
START_OF_MESSAGE = 0x00000002
ISO15765_FIRST_FRAME = 0x00000002  # v2 compat from v0202

ISO15765_EXT_ADDR = 0x00000080  # DT Accidentally refered to in spec

# 0 = No break received
# 1 = Break received
RX_BREAK = 0x00000004

# 0 = No TxDone
# 1 = TxDone
TX_INDICATION = 0x00000008  # Preferred name
TX_DONE = 0x00000008

# 0 = No Error
# 1 = Padding Error
ISO15765_PADDING_ERROR = 0x00000010

# 0 = no extended address,
# 1 = extended address is first byte after the CAN ID
ISO15765_ADDR_TYPE = 0x00000080

# CAN_29BIT_ID							0x00000100  defined above

SW_CAN_NS_RX = 0x00040000  # /*-2*/
SW_CAN_HS_RX = 0x00020000  # /*-2*/
SW_CAN_HV_RX = 0x00010000  # /*-2*/

connect_definitions = {'CAN_29BIT_ID': 0x00000100, 'ISO9141_NO_CHECKSUM': 0x00000200, 'CAN_ID_BOTH': 0x00000800,
                       'ISO9141_K_LINE_ONLY': 0x00001000}
# TxFlags definitions

# 0 = no padding
# 1 = pad all flow controlled messages to a full CAN frame using zeroes
ISO15765_FRAME_PAD = 0x00000040

# ISO15765_ADDR_TYPE=0x00000080  defined above
# CAN_29BIT_ID=0x00000100  defined above

# 0 = Interface message timing as specified in ISO 14230
# 1 = After a response is received for a physical request, the wait time shall be reduced to P3_MIN
# Does not affect timing on responses to functional requests
WAIT_P3_MIN_ONLY = 0x00000200

SW_CAN_HV_TX = 0x00000400  # /*-2*/

# 0 = Transmit using SCI Full duplex mode
# 1 = Transmit using SCI Half duplex mode
SCI_MODE = 0x00400000

# 0 = no voltage after message transmit
# 1 = apply 20V after message transmit
SCI_TX_VOLTAGE = 0x00800000

DT_PERIODIC_UPDATE = 0x10000000  # /*DT*/

# Filter definitions

# Allows matching messages into the receive queue. This filter type is only valid on non-ISO 15765 channels
PASS_FILTER = 0x00000001

# Keeps matching messages out of the receive queue. This filter type is only valid on non-ISO 15765 channels
BLOCK_FILTER = 0x00000002

# Allows matching messages into the receive queue and defines an outgoing flow control message to support
# the ISO 15765-2 flow control mechanism. This filter type is only valid on ISO 15765 channels.
FLOW_CONTROL_FILTER = 0x00000003
