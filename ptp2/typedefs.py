import struct

try:
    import numpy as np
    fromstring = lambda byte_str,type_: np.fromstring(byte_str, type_)

except ImportError:
    import array
    fromstring = lambda byte_str, type_: array.array(type_, byte_str)



PTP_USB_COMMAND         = 1
PTP_USB_DATA            = 2
PTP_USB_RESPONSE        = 3
PTP_USB_EVENT           = 4


__all__ = ['PTP_CONTAINER_TYPE', 'PTP_OPCODE', 'PTP_RESPONSE_CODE', 'PTP_EVENT_CODE',
    'ParamContainer', 'DataContainer', 'CHDK_LV_Data', 'CHDK_FrameBuffer', 'CHDK_DataHeader']

class PTP_CONTAINER_TYPE(object):
    COMMAND         = 1
    DATA            = 2
    RESPONSE        = 3
    EVENT           = 4


class PTP_OPCODE(object):
    '''From gPhoto ptp.h'''
    #PTP v1.0 operation codes
    UNDEFINED                   = 0x1000
    GET_DEVICE_INFO             = 0x1001
    OPEN_SESSION                = 0x1002
    CLOSE_SESSION               = 0x1003
    GET_STORAGE_IDS             = 0x1004
    GET_STORAGE_INFO            = 0x1005
    GET_NUM_OBJECTS             = 0x1006
    GET_OBJECT_HANDLES          = 0x1007
    GET_OBJECT_INFO             = 0x1008
    GET_OBJECT                  = 0x1009
    GET_THUMB                   = 0x100A
    DELETE_OBJECT               = 0x100B
    SEND_OBJECT_INFO            = 0x100C
    SEND_OBJECT                 = 0x100D
    INITIATE_CAPTURE            = 0x100E
    FORMAT_STORE                = 0x100F
    RESET_DEVICE                = 0x1010
    SELF_TEST                   = 0x1011
    SET_OBJECT_PROTECTION       = 0x1012
    POWER_DOWN                  = 0x1013
    GET_DEVICE_PROP_DESC        = 0x1014
    GET_DEVICE_PROP_VALUE       = 0x1015
    SET_DEVICE_PROP_VALUE       = 0x1016
    RESET_DEVICE_PROP_VALUE     = 0x1017
    TERMINATE_OPEN_CAPTURE      = 0x1018
    MOVE_OBJECT                 = 0x1019
    COPY_OBJECT                 = 0x101A
    GET_PARTIAL_OBJECT          = 0x101B
    INITIATE_OPEN_CAPTURE       = 0x101C

    #PTP v1.1 operation codes
    START_ENUM_HANDLES          = 0x101D
    ENUM_HANDLES                = 0x101E
    STOP_ENUM_HANDLES           = 0x101F
    GET_VENDOR_EXTENSION_MAPS   = 0x1020
    GET_VENDOR_DEVICE_INFO      = 0x1021
    GET_RESIZED_IMAGE_OBJECT    = 0x1022
    GET_FILESYSTEM_MANIFEST     = 0x1023
    GET_STREAM_INFO             = 0x1024
    GET_STREAM                  = 0x1025


class PTP_RESPONSE_CODE(object):
    '''From gPhoto ptp.h'''
    # PTP v1.0 response codes
    UNDEFINED                      = 0x2000
    OK                             = 0x2001
    GENERAL_ERROR                  = 0x2002
    SESSION_NOT_OPEN               = 0x2003
    INVALID_TRANSACTION_ID         = 0x2004
    OPERATION_NOT_SUPPORTED        = 0x2005
    PARAMETER_NOT_SUPPORTED        = 0x2006
    INCOMPLETE_TRANSFER            = 0x2007
    INVALID_STORAGE_ID             = 0x2008
    INVALID_OBJECT_HANDLE          = 0x2009
    DEVICE_PROP_NOT_SUPPORTED      = 0x200A
    INVALID_OBJECT_FORMAT_CODE     = 0x200B
    STORE_FULL                     = 0x200C
    OBJECT_WRITE_PROTECTED         = 0x200D
    STORE_READ_ONLY                = 0x200E
    ACCESS_DENIED                  = 0x200F
    NO_THUMBNAIL_PRESENT           = 0x2010
    SELF_TEST_FAILED               = 0x2011
    PARTIAL_DELETION               = 0x2012
    STORE_NOT_AVAILABLE            = 0x2013
    SPECIFICATION_BY_FORMAT_UNSUPPORTED = 0x2014
    NO_VALID_OBJECT_INFO           = 0x2015
    INVALID_CODE_FORMAT            = 0x2016
    UNKNOWN_VENDOR_CODE            = 0x2017
    CAPTURE_ALREADY_TERMINATED     = 0x2018
    DEVICE_BUSY                    = 0x2019
    INVALID_PARENT_OBJECT          = 0x201A
    INVALID_DEVICE_PROP_FORMAT     = 0x201B
    INVALID_DEVICE_PROP_VALUE      = 0x201C
    INVALID_PARAMETER              = 0x201D
    SESSION_ALREADY_OPENED         = 0x201E
    TRANSACTION_CANCELED           = 0x201F
    SPECIFICATION_OF_DESTINATION_UNSUPPORTED = 0x2020

    # PTP V1.1 RESPONSE CODES
    INVALID_ENUM_HANDLE            = 0x2021
    NO_STREAM_ENABLED              = 0x2022
    INVALID_DATA_SET               = 0x2023


class PTP_EVENT_CODE(object):
    '''From gPhoto ptp.h'''
    UNDEFINED                       = 0x4000
    CANCEL_TRANSACTION              = 0x4001
    OBJECT_ADDED                    = 0x4002
    OBJECT_REMOVED                  = 0x4003
    STORE_ADDED                     = 0x4004
    STORE_REMOVED                   = 0x4005
    DEVICE_PROP_CHANGED             = 0x4006
    OBJECT_INFO_CHANGED             = 0x4007
    DEVICE_INFO_CHANGED             = 0x4008
    REQUEST_OBJECT_TRANSFER         = 0x4009
    STORE_FULL                      = 0x400A
    DEVICE_RESET                    = 0x400B
    STORAGE_INFO_CHANGED            = 0x400C
    CAPTURE_COMPLETE                = 0x400D
    UNREPORTED_STATUS               = 0x400E



class _PyStructure(object):

    def __init__(self, fields, endian='<', bytestr=None):

        if endian in '@=<>!':
            self._fmt = endian
        else:
            raise ValueError('Illegal endian type %s, see `struct` pydocs' %(endian))

        self._fields = []

        for (name, type_) in fields:
            #numeric
            if type_[-1] in 'bBhHiIlLqQfd':
                setattr(self, name, 0)

            #character types
            elif type_[-1] in 'cs':
                setattr(self, name, '')

            #boolean type
            elif type_[-1] in '?':
                setattr(self, name, False)

            else:
                raise(TypeError('Unsupported type %s' %(type_)))

            self._fmt += type_
            self._fields.append(name)

        self._size = struct.calcsize(self._fmt)

        if bytestr is not None:
            self.unpack(bytestr)

    def unpack(self, bytestr):
        vals = struct.unpack(self.fmt, bytestr[:self.size])
        for n, name in enumerate(self.fields):
            setattr(self, name, vals[n])

    def pack(self):
        vals = []
        for name in self.fields:
            vals.append(getattr(self, name))

        return struct.pack(self.fmt, *vals)

    def __str__(self):
        d = {}
        for name in self.fields:
            d[name] = getattr(self, name)

        return str(d)

    @property
    def fmt(self):
        return self._fmt

    @property
    def fields(self):
        return self._fields

    @property
    def size(self):
        return self._size




class CHDK_FrameBuffer(_PyStructure):

    def __init__(self, bytestr=None):
        fields = [
                    ('fb_type', 'i'),
                    ('data_start', 'i'),
                    ('buffer_width', 'i'),
                    ('visible_width', 'i'),
                    ('visible_height', 'i'),
                    ('margin_left', 'i'),
                    ('margin_top', 'i'),
                    ('margin_right', 'i'),
                    ('margin_bot', 'i'),
                ]

        _PyStructure.__init__(self, fields, endian='<', bytestr=bytestr)


class CHDK_DataHeader(_PyStructure):

    def __init__(self, bytestr=None):
        fields = [
                    ('version_major', 'i'),
                    ('version_minor', 'i'),
                    ('lcd_aspect_ratio', 'i'),
                    ('palette_type', 'i'),
                    ('palette_data_start', 'i'),
                    ('vp_desc_start', 'i'),
                    ('bm_desc_start', 'i'),
                ]

        _PyStructure.__init__(self, fields, endian='<', bytestr=bytestr)

class CHDK_LV_Data(object):

    def __init__(self, bytestr=None):

        self.header  = None
        self.vp_desc = None
        self.bm_desc = None
        self.vp_data = None
        self.bm_data = None

        if bytestr is not None:
            self.unpack(bytestr)

    def unpack(self, bytestr):

        lb = 0
        self.header = CHDK_DataHeader()
        ub = self.header.size

        self.header.unpack(bytestr[lb:ub])

        lb = self.header.vp_desc_start
        self.vp_desc = CHDK_FrameBuffer()
        ub = lb + self.vp_desc.size
        self.vp_desc.unpack(bytestr[lb:ub])

        lb = self.header.bm_desc_start
        self.bm_desc = CHDK_FrameBuffer()
        ub = lb + self.bm_desc.size
        self.bm_desc.unpack(bytestr[lb:ub])


        if self.vp_desc.data_start > 0 :
            vp_size = self.vp_desc.buffer_width * self.vp_desc.visible_height * 6 / 4
            lb = self.vp_desc.data_start
            ub = lb + vp_size
            self.vp_data = fromstring(bytestr[lb:ub], 'B')

        if self.bm_desc.data_start > 0:
            bm_size = self.bm_desc.buffer_width * self.bm_desc.visible_height
            lb = self.bm_desc.data_start
            ub = lb + bm_size
            self.bm_data = fromstring(bytestr[lb:ub], 'B')

    def pack(self):
        total_size = self.header.size + self.vp_desc.size + self.bm_desc_size
        if vp_data is not None:
            total_size += len(vp_data) * 4

        if bm_data is not None:
            total_size += len(bm_data) * 4

        bytestr = ' ' * total_size

        lb = 0
        ub = self.header.size
        bytestr[lb:ub] = self.header.pack()

        lb=self.header.vp_desc_start
        ub=lb + self.vp_desc.size
        bytestr[lb:ub] = self.vp_desc.pack()

        lb = self.header.bm_desc_start
        ub = lb + self.bm_desc.size
        bytestr[lb:ub] = self.bm_desc.pack()

        if vp_data is not None:
            vp_size = self.vp_desc.buffer_width * self.vp_desc.visible_height * 6 / 4
            lb = self.vp_desc.data_start
            ub = lb + vp_size
            fmt = '<%dB' % (len(self.vp_data))
            bytestr[lb:ub] = struct.pack(fmt, *self.vp_data)

        if bm_data is not None:
            bm_size = self.bm_desc.buffer_width * self.bm_desc.visible_height
            lb = self.bm_desc.data_start
            ub = lb + bm_size
            fmt = '<%dB' % (len(self.bm_data))
            bytestr[lb:ub] = struct.pack(fmt, *self.bm_data)

        return bytestr



class ParamContainer(_PyStructure):


    def __init__(self, bytestr=None):

        header = [
                    ('length',            'I'),
                    ('type',              'H'),
                    ('code',              'H'),
                    ('transaction_id',    'I'),
                 ]

        _PyStructure.__init__(self, header, endian='<')

        self._params = []

        if bytestr is not None:
            self.unpack(bytestr)

        # else:
        #     for name, value in kwargs.iteritems():
        #         if name == 'params' and isinstance(value, list):
        #             self._params = params.copy()
        #         if hasattr(self, name):
        #             setattr(self, name, value)
        #         else:
        #             raise(AttributeError('%s has no attribute %s'%(self.__class__, name)))


    def unpack(self, bytestr):
        _PyStructure.unpack(self, bytestr[:12])

        num_params = (self.length - 12) / 4
        str_len = len(bytestr)
        exp_len = 12 + num_params * 4

        if str_len != exp_len:
            raise(IndexError('Expected string of size %d, got %d' %(exp_len, str_len)))

        if num_params > 0:
            p_fmt = '<%di' %(num_params)
            self._params = list(struct.unpack(p_fmt, bytestr[12:]))
            self._fmt += p_fmt[1:]

    def pack(self):
        header = _PyStructure.pack(self)
        p_fmt = '<%di' % (len(self.params))
        return header + struct.pack(p_fmt, *self.params)

    @property
    def params(self):
        return self._params[:]

    @params.setter
    def params(self, param_list):
        self.length = 12 + 4*len(param_list)
        self._params = param_list


    def __repr__(self):
        return '<{m}.{n} at {i:x} length={l} type={t} code={c:x} txid={tx} params={p}>'.format(
            m=self.__class__.__module__, n=self.__class__.__name__, i=id(self), l=self.length,
            t=self.type, c=self.code, tx=self.transaction_id,
            p=['0x'+struct.pack('>i', x).encode('hex') for x in self.params])



class DataContainer(_PyStructure):


    def __init__(self, bytestr=None):

        header = [
                    ('length',            'I'),
                    ('type',              'H'),
                    ('code',              'H'),
                    ('transaction_id',    'I'),
                 ]

        _PyStructure.__init__(self, header, endian='<')

        self.type = PTP_CONTAINER_TYPE.DATA
        self._data = ''

        if bytestr is not None:
            self.unpack(bytestr)

    def unpack(self, bytestr):

        _PyStructure.unpack(self, bytestr[:12])

        self._data = bytestr[12:]

    def pack(self):
        header = _PyStructure.pack(self)

        return header + self.data

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, bytestr):
        self.length = 12 + len(bytestr)
        self._data = bytestr
