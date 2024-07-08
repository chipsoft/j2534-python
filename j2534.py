# -*- coding: utf-8 -*-

from ctypes import *
from sys import platform

from constants import err, cmd

MAX_MSG_DATA_SIZE = 4128
my_dll = None


# Определение структур
class SConfig(Structure):
    _fields_ = [('Parameter', c_ulong), ('Value', c_ulong)]


class GConfig(Structure):
    _fields_ = [('Parameter', c_ulong)]


class SConfigList(Structure):
    _fields_ = [('NumOfParams', c_ulong), ('ConfigPtr', POINTER(SConfig))]


# class GConfigList(Structure):
#     _fields_ = [('NumOfParams', c_ulong), ('ConfigPtr', POINTER(GConfig * 50))]


class SByteArray(Structure):
    _fields_ = [('BytePtr', c_ubyte * MAX_MSG_DATA_SIZE)]


class SByteArrayPointer(Structure):
    _fields_ = [('NumOfBytes', c_ulong), ('BytePtr', POINTER(c_ubyte * MAX_MSG_DATA_SIZE))]


class PassThruMsg(Structure):
    _fields_ = [('ProtocolID', c_ulong), ('RxStatus', c_ulong),
                ('TxFlags', c_ulong), ('Timestamp', c_ulong),
                ('DataSize', c_ulong), ('ExtraDataIndex', c_ulong),
                ('Data', SByteArray)]


# Обёртка для возвращаемых числовых параметров
class LongInt:
    def __init__(self, value=0):
        self.value = value


# Преобразуем PassThruMsg в список следующего формата:
# [ProtocolID, [Data], TXFlags, ExtraDataIndex, Timestamp, RxStatus]
def create_list_from_passthru_msg(passthru_msg):
    data = []
    result = []
    for i in range(0, passthru_msg.DataSize):  # Наполняем список полученными данными
        data.append(passthru_msg.Data.BytePtr[i])
    result.append(
        [passthru_msg.ProtocolID, data, passthru_msg.TxFlags, passthru_msg.ExtraDataIndex, passthru_msg.Timestamp,
         passthru_msg.RxStatus])
    return result


# Функция для разбора кортежа в тип PASSTHRU_MSG
def create_passthru_msg(tuple_param):
    extra_data, timestamp, rxstatus = 0, 0, 0
    len_of_tuple = len(tuple_param)
    assert len_of_tuple > 3 or len_of_tuple < 6, ('Wrong parametrs')
    p_data = SByteArray((c_ubyte * MAX_MSG_DATA_SIZE)(*tuple_param[1]))
    protocol_id_c = tuple_param[0]
    tx_status = tuple_param[2]
    data_count = len(tuple_param[1])
    # Пока не придумаю лучшее решение
    if len_of_tuple == 4:
        extra_data = tuple_param[-1]
    elif len_of_tuple == 5:
        timestamp = tuple_param[-1]
        extra_data = tuple_param[-2]
    elif len_of_tuple == 6:
        rxstatus = tuple_param[-1]
        timestamp = tuple_param[-2]
        extra_data = tuple_param[-3]

    return PassThruMsg(c_ulong(protocol_id_c), c_ulong(rxstatus), c_ulong(tx_status),
                       c_ulong(timestamp), c_ulong(data_count), c_ulong(extra_data), p_data)


# Функция для предотвращения от повторения кода в is_passthru_msgs_equal
def help_choice(msg1, msg2, n, checker):
    if len(msg1) >= n and len(msg2) >= n:
        if msg1[n - 1] != msg2[n - 1]:
            checker = False
    elif len(msg1) >= n:
        if msg1[n - 1] != 0:
            checker = False
    elif len(msg2) >= n:
        if msg2[n - 1] != 0:
            checker = False
    return checker


class Checks:
    MAX_PROTOCOL_ID = 0xFFFFFFFF
    MAX_BYTE_VALUE = 0xFF

    @classmethod
    def check_passthru_msg(cls, tuple_param):
        check = True
        if len(tuple_param) > 6 or len(tuple_param) < 2:
            check = False
        # Проверка ProtocolID на диапазон 0 - 0xFFFFFFFF
        if tuple_param[0] > cls.MAX_PROTOCOL_ID:
            check = False
        # Проверка на непустой кортеж и значение данных в пределах 0хFF
        if tuple_param[1]:
            for data in tuple_param[1]:
                if data > cls.MAX_BYTE_VALUE:
                    check = False
        else:
            check = False
        # TXFlags, ExtraDataIndex, Timestamp, RxStatus находятся в диапазоне 0 - 0xFFFFFFFF
        if len(tuple_param) >= 3:
            if tuple_param[2] > cls.MAX_PROTOCOL_ID:
                check = False
        if len(tuple_param) >= 4:
            if tuple_param[3] > cls.MAX_PROTOCOL_ID:
                check = False
        if len(tuple_param) >= 5:
            if tuple_param[4] > cls.MAX_PROTOCOL_ID:
                check = False
        if len(tuple_param) >= 6:
            if tuple_param[5] > cls.MAX_PROTOCOL_ID:
                check = False

        return check

    @classmethod
    def check_sconfig(cls, sconfig_param):
        print(sconfig_param)
        check = True
        if sconfig_param:
            for sconfig in sconfig_param:
                if type(sconfig) is tuple:
                    if len(sconfig) != 2:
                        check = False
                    if sconfig[0] > cls.MAX_PROTOCOL_ID or sconfig[1] > cls.MAX_PROTOCOL_ID:
                        check = False
                else:
                    if sconfig_param[0] > cls.MAX_PROTOCOL_ID or sconfig_param[1] > cls.MAX_PROTOCOL_ID:
                        check = False
        else:
            check = False
        return check

    @classmethod
    def is_passthru_msgs_equal(cls, msg1, msg2):
        checker = True
        if msg1[0] != msg2[0] or msg1[1] != msg2[1]:
            checker = False
        for k in [3, 4, 6]:
            checker = help_choice(msg1, msg2, k, checker)

        return checker


def pt_open(p_name, p_device_id):
    name = c_void_p(p_name)
    device_id = c_ulong(p_device_id.value)
    result = my_dll.PassThruOpen(name, byref(device_id))
    p_device_id.value = device_id.value
    return result


def pt_close(device_id):
    result = my_dll.PassThruClose(c_ulong(device_id.value))
    return result


def pt_connect(device_id, protocol_id, flags, baud_rate, p_channel_id):
    channel_id = c_ulong(p_channel_id.value)
    result = my_dll.PassThruConnect(c_ulong(device_id.value), c_ulong(protocol_id), c_ulong(flags), c_ulong(baud_rate),
                                    byref(channel_id))
    p_channel_id.value = channel_id.value
    return result


def pt_disconnect(channel_id):
    return my_dll.PassThruDisconnect(c_ulong(channel_id.value))


def pt_read_msg(ChannelID, pMsg, pNumMsgs, Timeout):
    p_msg_list = []
    num_msgs = c_ulong(pNumMsgs.value)
    for i in range(0, pNumMsgs.value):
        p_msg_list.append(PassThruMsg())
    ptr = (PassThruMsg * pNumMsgs.value)(*p_msg_list)  # Преобразуем в массив
    result = my_dll.PassThruReadMsgs(c_ulong(ChannelID.value), byref(ptr), byref(num_msgs), c_ulong(Timeout))
    pNumMsgs.value = num_msgs.value  # Заполняем числом вычитанных сообщений
    for i in range(0, pNumMsgs.value):  # Даже если возникла ошибка, возвращаем полученные сообщения
        pMsg.append(create_list_from_passthru_msg(ptr[i]))
    return result


def pt_write_msg(channel_id, pMsg, p_num_msgs, timeout):
    p_msg_list = []
    num_msgs = c_ulong(p_num_msgs.value)  # Число сообщений, которые необходимо отправить
    if pMsg:
        if type(pMsg[0]) == tuple:
            for p in pMsg:
                msg = create_passthru_msg(p)
                p_msg_list.append(msg)
        else:
            msg = create_passthru_msg(pMsg)
    else:
        msg = c_void_p(None)

    if p_msg_list:
        p_msg = byref((PassThruMsg * p_num_msgs.value)(*p_msg_list))
    else:
        p_msg = byref(msg)
    result = my_dll.PassThruWriteMsgs(c_ulong(channel_id.value), p_msg, byref(num_msgs),
                                      c_ulong(timeout))  # byref(num_msgs)
    p_num_msgs.value = num_msgs.value
    return result


def pt_start_msg_filter(ChannelID, FilterType, pMaskMsg, pPatternMsg, pFlowControlMsg, pFilterID):
    channel_id = c_ulong(ChannelID.value)
    filter_type = c_ulong(FilterType)
    pcontrolmsg = c_ulong(0)
    if pFlowControlMsg:
        controlmsg = create_passthru_msg(pFlowControlMsg)
        pcontrolmsg = byref(controlmsg)
    maskmsg = create_passthru_msg(pMaskMsg)
    patternmsg = create_passthru_msg(pPatternMsg)
    pmaskmsg, ppatternmsg = byref(maskmsg), byref(patternmsg)
    filter_id_code = c_ulong(pFilterID.value)
    result = my_dll.PassThruStartMsgFilter(channel_id, filter_type, pmaskmsg, ppatternmsg,
                                           pcontrolmsg, byref(filter_id_code))
    pFilterID.value = filter_id_code.value
    return result


def pt_stop_msg_filter(channel_id, filter_id):
    channel_id = c_ulong(channel_id.value)
    filter_id_code = c_ulong(filter_id.value)
    return my_dll.PassThruStopMsgFilter(channel_id, filter_id_code)


def pt_set_programming_voltage(DeviceID, PinNumber, Voltage):
    voltage = c_ulong(Voltage.value)
    result = my_dll.PassThruSetProgrammingVoltage(c_ulong(DeviceID.value), c_ulong(PinNumber), voltage)
    Voltage.value = voltage.value
    return result


def pt_read_version(device_id, firmware_version, dll_version, api_version):
    result = my_dll.PassThruReadVersion(c_ulong(device_id.value), firmware_version,
                                        dll_version, api_version)
    return result


def pt_start_periodic_msg(ChannelID, pMsg, pMsgID, TimeInterval):
    if pMsg:
        PTMsg = create_passthru_msg(pMsg)
    else:
        PTMsg = 0
    pPTMsg = byref(PTMsg)
    msgid = c_ulong(pMsgID.value)
    result = my_dll.PassThruStartPeriodicMsg(c_ulong(ChannelID.value), pPTMsg, byref(msgid), c_ulong(TimeInterval))
    pMsgID.value = msgid.value
    return result


def pt_ioctl(ChannelID, IoctlID, pInput, pOutput):
    channel_id = c_ulong(ChannelID.value)
    ioctl_id = IoctlID
    if ioctl_id == cmd.SET_CONFIG:
        set_config = []
        for param in pInput:
            set_config.append(SConfig(c_ulong(param[0]),
                                      c_ulong(param[1])))
        array = (SConfig * len(set_config))(*set_config)
        input_pt = SConfigList(c_ulong(len(set_config)), array)
        result = my_dll.PassThruIoctl(channel_id, c_ulong(ioctl_id), pointer(input_pt), c_void_p(None))

    elif ioctl_id == cmd.GET_CONFIG:
        get_config = []
        for param in pInput:
            get_config.append(SConfig(param, 0))
        array = (SConfig * len(get_config))(*get_config)
        input_pt = SConfigList(c_ulong(len(get_config)), array)
        result = my_dll.PassThruIoctl(channel_id, c_ulong(ioctl_id), pointer(input_pt), c_void_p(None))
        if result == err.STATUS_NOERROR:
            for i in range(0, input_pt.NumOfParams):  # Наполняем список полученными данными
                pOutput.append(input_pt.ConfigPtr[i].Value)

    elif ioctl_id == cmd.FAST_INIT:
        pin = create_passthru_msg(pInput)
        p_input = pointer(pin)
        p_output = PassThruMsg()
        result = my_dll.PassThruIoctl(channel_id, c_ulong(ioctl_id), p_input, byref(p_output))
        if result == err.STATUS_NOERROR:
            #  Если данные получены, заполняем список
            pOutput.append(create_list_from_passthru_msg(p_output))

    elif ioctl_id == cmd.FIVE_BAUD_INIT:
        five_baud_data = SByteArray((c_ubyte * MAX_MSG_DATA_SIZE)(*pInput))
        p_output = PassThruMsg()
        result = my_dll.PassThruIoctl(channel_id, c_ulong(ioctl_id), pointer(five_baud_data), byref(p_output))
        if result == err.STATUS_NOERROR:
            #  Если данные получены, заполняем список
            pOutput.append(create_list_from_passthru_msg(p_output))

    elif ioctl_id == cmd.READ_VBATT:
        obd2_voltage = c_ulong(pOutput.value)
        result = my_dll.PassThruIoctl(channel_id, c_ulong(ioctl_id), c_void_p(None), byref(obd2_voltage))
        pOutput.value = int(obd2_voltage.value)

    else:
        p_input = c_void_p(None)
        p_output = c_void_p(None)
        result = my_dll.PassThruIoctl(channel_id, c_ulong(ioctl_id), p_input, p_output)

    return result


def check_passthru_msg(msg):
    return False


def check_sconfig(sconfig):
    return False


# Задаем dll, через которую работаем
def set_dll(dll_name):
    if platform == "win32":
        global my_dll;
        my_dll = windll.LoadLibrary(dll_name)
    return 0

# my_dll = windll.LoadLibrary(r"C:\Users\Vlad\Desktop\Task_car\ptshim32.dll")  # подключаем нашу dll
# my_dll = windll.LoadLibrary(
#    r"C:\Program Files (x86)\Drew Technologies, Inc\J2534\j2534-logger\ptshim32.dll")  # подключаем нашу dll
