import xcffib
import struct
import six
_events = {}
_errors = {}
class AxisInfo(xcffib.Struct):
    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Struct.__init__(self, unpacker)
        base = unpacker.offset
        self.resolution, self.minimum, self.maximum = unpacker.unpack("Iii")
        self.bufsize = unpacker.offset - base
    def pack(self):
        buf = six.BytesIO()
        buf.write(struct.pack("=Iii", self.resolution, self.minimum, self.maximum))
        return buf.getvalue()
    def synthetic(self, resolution, minimum, maximum):
        self.resolution = resolution
        self.minimum = minimum
        self.maximum = maximum
    fixed_size = 12
class ValuatorInfo(xcffib.Struct):
    def __init__(self, unpacker):
        if isinstance(unpacker, xcffib.Protobj):
            unpacker = xcffib.MemoryUnpacker(unpacker.pack())
        xcffib.Struct.__init__(self, unpacker)
        base = unpacker.offset
        self.class_id, self.len, self.axes_len, self.mode, self.motion_size = unpacker.unpack("BBBBI")
        self.axes = xcffib.List(unpacker, AxisInfo, self.axes_len)
        self.bufsize = unpacker.offset - base
    def pack(self):
        buf = six.BytesIO()
        buf.write(struct.pack("=BBBBI", self.class_id, self.len, self.axes_len, self.mode, self.motion_size))
        buf.write(xcffib.pack_list(self.axes, AxisInfo))
        return buf.getvalue()
    def synthetic(self, class_id, len, axes_len, mode, motion_size, axes):
        self.class_id = class_id
        self.len = len
        self.axes_len = axes_len
        self.mode = mode
        self.motion_size = motion_size
        self.axes = axes
xcffib._add_ext(key, structExtension, _events, _errors)
