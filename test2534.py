from constants import cmd, protocols, misc

from j2534 import *

# Connect DLL
set_dll(r"C:\Program Files (x86)\Drew Technologies, Inc\J2534\j2534-logger\ptshim32.dll")

# PassThruOpen
deviceId = LongInt()
result = pt_open(None, deviceId)
print("pt_open: result = {0}, deviceId = {1}".format(result, deviceId.value))

# PassReadVersion
firmware_version = create_string_buffer(255)
dll_version = create_string_buffer(255)
api_version = create_string_buffer(255)
result = pt_read_version(deviceId, firmware_version, dll_version, api_version)
print(firmware_version.value, dll_version.value, api_version.value)

# ============================================================================
# PassThruConnect
channelID = LongInt()
result = pt_connect(
    deviceId, protocols.ISO9141, misc.ISO9141_NO_CHECKSUM or misc.ISO9141_K_LINE_ONLY, 10400, channelID
)
print("pt_connect: result = {0}, channelID = {1}".format(result, channelID.value))

# PassThruStartMsgFilter
filterID = LongInt()
result = pt_start_msg_filter(channelID, misc.PASS_FILTER,
                             (protocols.ISO9141, (0x00, 0x00), 0, 0),
                             (protocols.ISO9141, (0x00, 0x00), 0, 0),
                             None, filterID)
print("pt_start_msg_filter: result = {0}, filterID = {1}".format(result, filterID.value))

result = pt_ioctl(channelID, cmd.SET_CONFIG, ((cmd.FIVE_BAUD_MOD, 0),), None)
print("pt_ioctl: result = {0}".format(result))

# five_init_res = []
# result = pt_ioctl(channelID, FIVE_BAUD_INIT, (0x33,), five_init_res)
# print("pt_ioctl: result = {0}".format(result))

# PassThruDisconnect
result = pt_disconnect(channelID)
print("pt_disconnect: result = {0}".format(result))
# ============================================================================

# PassThruConnect
channelID = LongInt()
result = pt_connect(deviceId, protocols.ISO14230, 0, 10400, channelID)
print("pt_connect: result = {0}, channelID = {1}".format(result, channelID.value))

# PassThruStartMsgFilter
filterID = LongInt()
result = pt_start_msg_filter(
    channelID,
    misc.PASS_FILTER,
    (protocols.ISO14230, (0x00,), 0, 0),
    (protocols.ISO14230, (0x00,), 0, 0),
    None,
    filterID
)
print("pt_start_msg_filter: result = {0}, filterID = {1}".format(result, filterID.value))

fast_init_res = []
result = pt_ioctl(channelID, cmd.FAST_INIT, (protocols.ISO14230, (0x81, 0x10, 0xf1, 0x81), 0), fast_init_res)
print('fast_init_res:', fast_init_res)    # Тут мы должны получить сообщение в виде списка [...]

# PassThruDisconnect
result = pt_disconnect(channelID)
print("pt_disconnect: result = {0}".format(result))

# PassThruConnect
channelID = LongInt()
result = pt_connect(deviceId, protocols.ISO15765, misc.CAN_29BIT_ID, 500000, channelID)
print("pt_connect: result = {0}, channelID = {1}".format(result, channelID.value))

# PassThruStartMsgFilter
filterID = LongInt()
result = pt_start_msg_filter(
    channelID,
    misc.FLOW_CONTROL_FILTER,
    (protocols.ISO15765, (0xff, 0xff, 0xff, 0xff), misc.ISO15765_FRAME_PAD | misc.CAN_29BIT_ID, 0),
    (protocols.ISO15765, (0x18, 0xda, 0xf1, 0x11), misc.ISO15765_FRAME_PAD | misc.CAN_29BIT_ID, 0),
    (protocols.ISO15765, (0x18, 0xda, 0x11, 0xf1), misc.ISO15765_FRAME_PAD | misc.CAN_29BIT_ID, 0),
    filterID
)
print("pt_start_msg_filter: result = {0}, filterID = {1}".format(result, filterID.value))

# PassThruStartPeriodicMsg
# pMsgID = LongInt()
# result = pt_start_periodic_msg(channelID,
#                                (ISO15765, (0x18, 0xda, 0x11, 0xf1, 0x3e), ISO15765_FRAME_PAD | CAN_29BIT_ID), pMsgID,
#                                600)
# print("pt_start_periodic_msg: result = {0}, pMsgID = {1}".format(result, pMsgID.value))

# PassThruWriteMsg
# pNumMsgs = LongInt()
# result = pt_write_msg(channelID, (ISO15765, (0x18, 0xda, 0x11, 0xf1), ISO15765_FRAME_PAD | CAN_29BIT_ID),
#                       pNumMsgs, 600)

# Тест записи одного сообщения
# Даже одно сообщение передается в виде кортежа кортежов (сейчас программа рассчитана на передачу только одного кортежа)
# Тест передачи нескольких сообщений см. ниже - в "Тест множественной передачи сообщений"
pNumMsgs = LongInt(1)
result = pt_write_msg(
    channelID,
    ((protocols.ISO15765, (0x18, 0xda, 0x11, 0xf1, 0x3e, 0x00), misc.ISO15765_FRAME_PAD | misc.CAN_29BIT_ID),),
    pNumMsgs,
    600
)
print("pt_write_msg: result = {0}, pNumMsgs = {1}".format(result, pNumMsgs.value))

# PassThruReadMsg - получаем ответ от ЭБУ на pt_write_msg

# В readed_msg функция pt_read_msg должна записать прочитанное сообщение(сообзения) из ЭБУ.
# Фактически это список из списка прочитанных сообщений.
# В pMsgs мы передаем сколько сообщений мы хотим прочитать (в данном случае - 1)
# После вызова функции в pMsgs мы получим значение, сколько сообщений реально вычиталось

pMsgs = LongInt(20)
readed_msg = []
read = pt_read_msg(channelID, readed_msg, pMsgs, 900)
print("ptReadMsg = {0}, pMsgs= {1}, message = ".format(read, pMsgs.value), readed_msg)

# Тест множественной передачи сообщений
pNumMsgs = LongInt(2)
result = pt_write_msg(
    channelID,
    (
        (protocols.ISO15765, (0x18, 0xda, 0x16, 0xf1), misc.ISO15765_FRAME_PAD | misc.CAN_29BIT_ID),
        (protocols.ISO15765, (0x17, 0xda, 0x11, 0xf1), misc.ISO15765_FRAME_PAD | misc.CAN_29BIT_ID)
    ),
    pNumMsgs,
    600
)
print("pt_write_msg: result = {0}, pNumMsgs = {1}".format(result, pNumMsgs.value))

# PassThruStopMsgFilter
result = pt_stop_msg_filter(channelID, filterID)
print("pt_stop_msg_filter: result = {0}".format(result))

# PassThruIoctl
result = pt_ioctl(channelID, cmd.CLEAR_RX_BUFFER, None, None)
print("pt_ioctl (CLEAR_RX_BUFFER): result = {0}".format(result))

result = pt_ioctl(channelID, cmd.CLEAR_TX_BUFFER, None, None)
print("pt_ioctl (CLEAR_TX_BUFFER): result = {0}".format(result))

result = pt_ioctl(channelID, cmd.CLEAR_PERIODIC_MSGS, None, None)
print("pt_ioctl (CLEAR_PERIODIC_MSGS): result = {0}".format(result))

result = pt_ioctl(channelID, cmd.CLEAR_MSG_FILTERS, None, None)
print("pt_ioctl (CLEAR_MSG_FILTER): result = {0}".format(result))

result = pt_ioctl(channelID, cmd.CLEAR_FUNCT_MSG_LOOKUP_TABLE, None, None)
print("pt_ioctl (CLEAR_FUNCT_MSG_LOOKUP_TABLE): result = {0}".format(result))

voltage = LongInt()
result = pt_ioctl(deviceId, cmd.READ_VBATT, None, voltage)
print("pt_ioctl (READ_VBATT): result = {0}, voltage = {1} mV".format(result, voltage.value))

result = pt_ioctl(
    channelID,
    cmd.SET_CONFIG,
    ((cmd.DATA_RATE, 50000), (cmd.LOOPBACK, 1), (cmd.CAN_MIXED_FORMAT, 0)),
    None
)
print("pt_ioctl: result = {0}".format(result))

pout = []
result = pt_ioctl(channelID, cmd.GET_CONFIG, (cmd.DATA_RATE, cmd.LOOPBACK, cmd.CAN_MIXED_FORMAT), pout)
print('pout: ', pout)  # Тут мы должны получить список значений [500000, 1, 10].
# Скорее всего та тестовая DLL Хонды неправильно
# эти данные отдаст, но на выходе должен быть список значений типа int

# PassThruDisconnect
result = pt_disconnect(channelID)
print("pt_disconnect: result = {0}".format(result))

# PassThruClose
result = pt_close(deviceId)
print("pt_close: result = {0}".format(result))

print('\x1b[6;30;42m' + 'Finish!' + '\x1b[0m')
