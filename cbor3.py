#--------------------------------------------
# The MIT License (MIT)
# 
# Copyright (c) 2023 Arduino SA
# Copyright (c) 2018 KPN (Jan Bogaerts)
# 
# Edited 2025 Sharil Tumin - add tuple type
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#--------------------------------------------

import io
import struct

_VERSION_ = (3, 'shariltumin', '20251218')

class CBORDecodeError(Exception):
    # Raised when an error occurs deserializing a CBOR datastream.
    pass

break_marker = object()

class CBORSimpleValue(object):  # noqa: PLW1641
    # Represents a CBOR "simple value".
    # :param int value: the value (0-255)
    def __init__(self, value):
        if value < 0 or value > 255:
            raise TypeError("simple value too big")
        self.value = value

    def __eq__(self, other):
        if isinstance(other, CBORSimpleValue):
            return self.value == other.value
        elif isinstance(other, int):
            return self.value == other
        return NotImplemented

    def __repr__(self):
        return "CBORSimpleValue({self.value})".format(self=self)

def decode_uint(decoder, subtype, allow_indefinite=False):
    # Major tag 0
    if subtype < 24:
        return subtype
    elif subtype == 24:
        return struct.unpack(">B", decoder.read(1))[0]
    elif subtype == 25:
        return struct.unpack(">H", decoder.read(2))[0]
    elif subtype == 26:
        return struct.unpack(">L", decoder.read(4))[0]
    elif subtype == 27:
        return struct.unpack(">Q", decoder.read(8))[0]
    elif subtype == 31 and allow_indefinite:
        return None
    else:
        raise CBORDecodeError("unknown unsigned integer subtype 0x%x" % subtype)

def decode_negint(decoder, subtype):
    # Major tag 1
    uint = decode_uint(decoder, subtype)
    return -uint - 1

def decode_bytestring(decoder, subtype):
    # Major tag 2
    length = decode_uint(decoder, subtype, allow_indefinite=True)
    if length is None:
        # Indefinite length
        buf = bytearray()
        while True:
            initial_byte = decoder.read(1)[0]
            if initial_byte == 255:
                return buf
            else:
                length = decode_uint(decoder, initial_byte & 31)
                value = decoder.read(length)
                buf.extend(value)
    else:
        return decoder.read(length)

def decode_string(decoder, subtype):
    # Major tag 3
    return decode_bytestring(decoder, subtype).decode("utf-8")

def decode_array(decoder, subtype):
    # Major tag 4
    items = []
    length = decode_uint(decoder, subtype, allow_indefinite=True)
    if length is None:
        # Indefinite length
        while True:
            value = decoder.decode()
            if value is break_marker:
                break
            else:
                items.append(value)
    else:
        for _ in range(length):
            item = decoder.decode()
            items.append(item)
    return items

def decode_tuple(decoder, subtype):
    return tuple(decode_array(decoder, subtype))

def decode_map(decoder, subtype):
    # Major tag 5
    dictionary = {}
    length = decode_uint(decoder, subtype, allow_indefinite=True)
    if length is None:
        # Indefinite length
        while True:
            key = decoder.decode()
            if key is break_marker:
                break
            else:
                value = decoder.decode()
                dictionary[key] = value
    else:
        for _ in range(length):
            key = decoder.decode()
            value = decoder.decode()
            dictionary[key] = value

    return dictionary

def decode_special(decoder, subtype):
    # Simple value
    if subtype < 20:
        return CBORSimpleValue(subtype)

    # Major tag 7
    return special_decoders[subtype](decoder)

def decode_simple_value(decoder):
    return CBORSimpleValue(struct.unpack(">B", decoder.read(1))[0])

def decode_float16(decoder):
    decoder.read(2)
    raise NotImplementedError  # no float16 unpack function

def decode_float32(decoder):
    return struct.unpack(">f", decoder.read(4))[0]

def decode_float64(decoder):
    return struct.unpack(">d", decoder.read(8))[0]

major_decoders = {
    0: decode_uint,
    1: decode_negint,
    2: decode_bytestring,
    3: decode_string,
    4: decode_array,
    5: decode_map,
    6: decode_tuple,
    7: decode_special,
}

special_decoders = {
    20: lambda self: False,
    21: lambda self: True,
    22: lambda self: None,
    # 23 is undefined
    24: decode_simple_value,
    25: decode_float16,
    26: decode_float32,
    27: decode_float64,
    31: lambda self: break_marker,
}

class CBORDecoder(object):
    # Deserializes a CBOR encoded byte stream.
    def __init__(self, fp):
        self.fp = fp

    def read(self, amount):
        # Read bytes from the data stream.
        # :param int amount: the number of bytes to read
        data = self.fp.read(amount)
        if len(data) < amount:
            raise CBORDecodeError(
                "premature end of stream (expected to read {} bytes, got {} instead)".format(
                    amount, len(data)
                )
            )

        return data

    def decode(self):
        # Decode the next value from the stream.
        # :raises CBORDecodeError: if there is any problem decoding the stream
        try:
            initial_byte = self.fp.read(1)[0]
            major_type = initial_byte >> 5
            subtype = initial_byte & 31
        except Exception as e:
            raise CBORDecodeError(
                "error reading major type at index {}: {}".format(self.fp.tell(), e)
            )

        decoder = major_decoders[major_type]
        try:
            return decoder(self, subtype)
        except CBORDecodeError:
            raise
        except Exception as e:
            raise CBORDecodeError(
                "error decoding value {}".format(e)
            )  # tell doesn't work on micropython at the moment

def loads(payload, **kwargs):
    # Deserialize an object from a bytestring.
    # :param bytes payload: the bytestring to serialize
    # :param kwargs: keyword arguments passed to :class:`~.CBORDecoder`
    # :return: the deserialized object
    fp = io.BytesIO(payload)
    return CBORDecoder(fp, **kwargs).decode()

def load(fp, **kwargs):
    # Deserialize an object from an open file.
    # :param fp: the input file (any file-like object)
    # :param kwargs: keyword arguments passed to :class:`~.CBORDecoder`
    # :return: the deserialized object
    return CBORDecoder(fp, **kwargs).decode()

class CBOREncodeError(Exception):
    # Raised when an error occurs while serializing an object into a CBOR datastream.
    pass

def encode_length(major_tag, length):
    if length < 24:
        return struct.pack(">B", major_tag | length)
    elif length < 256:
        return struct.pack(">BB", major_tag | 24, length)
    elif length < 65536:
        return struct.pack(">BH", major_tag | 25, length)
    elif length < 4294967296:
        return struct.pack(">BL", major_tag | 26, length)
    else:
        return struct.pack(">BQ", major_tag | 27, length)

def encode_semantic(encoder, tag, value):
    encoder.write(encode_length(0xC0, tag))
    encoder.encode(value)

def encode_float(encoder, value):
    # Handle special values efficiently
    import math

    if math.isnan(value):
        encoder.write(b"\xf9\x7e\x00")
    elif math.isinf(value):
        encoder.write(b"\xf9\x7c\x00" if value > 0 else b"\xf9\xfc\x00")
    else:
        encoder.write(struct.pack(">Bd", 0xFB, value))

def encode_int(encoder, value):
    # Big integers (2 ** 64 and over)
    if value >= 18446744073709551616 or value < -18446744073709551616:
        if value >= 0:
            major_type = 0x02
        else:
            major_type = 0x03
            value = -value - 1

        values = []
        while value > 0:
            value, remainder = divmod(value, 256)
            values.insert(0, remainder)

        payload = bytes(values)
        encode_semantic(encoder, major_type, payload)
    elif value >= 0:
        encoder.write(encode_length(0, value))
    else:
        encoder.write(encode_length(0x20, abs(value) - 1))

def encode_bytestring(encoder, value):
    encoder.write(encode_length(0x40, len(value)) + value)

def encode_bytearray(encoder, value):
    encode_bytestring(encoder, bytes(value))

def encode_string(encoder, value):
    encoded = value.encode("utf-8")
    encoder.write(encode_length(0x60, len(encoded)) + encoded)

def encode_map(encoder, value):
    encoder.write(encode_length(0xA0, len(value)))
    for key, val in value.items():
        encoder.encode(key)
        encoder.encode(val)

def encode_array(encoder, value):
    encoder.write(encode_length(0x80, len(value)))
    for item in value:
        encoder.encode(item)

def encode_tuple(encoder, value):
    encoder.write(encode_length(0xC0, len(value))) # 0xC0 >> 5 == 6
    for item in value:
        encoder.encode(item)

def encode_boolean(encoder, value):
    encoder.write(b"\xf5" if value else b"\xf4")

def encode_none(encoder, value):
    encoder.write(b"\xf6")

cbor_encoders = {  # supported data types and the encoder to use.
    bytes: encode_bytestring,
    bytearray: encode_bytearray,
    str: encode_string,
    int: encode_int,
    float: encode_float,
    bool: encode_boolean,
    type(None): encode_none,
    list: encode_array,
    tuple: encode_tuple,
    dict: encode_map,
}

class CBOREncoder(object):
    # Serializes objects to a byte stream using Concise Binary Object Representation.

    def __init__(self, fp):
        self.fp = fp

    def _find_encoder(self, obj):
        return cbor_encoders[type(obj)]

    def write(self, data):
        # Write bytes to the data stream.
        # :param data: the bytes to write
        self.fp.write(data)

    def encode(self, obj):
        # Encode the given object using CBOR.
        # :param obj: the object to encode
        encoder = self._find_encoder(obj)
        if not encoder:
            raise CBOREncodeError("cannot serialize type %s" % type(obj))
        encoder(self, obj)

def dumps(obj, **kwargs):
    # Serialize an object to a bytestring.
    # :param obj: the object to serialize
    # :param kwargs: keyword arguments passed to :class:`~.CBOREncoder`
    # :return: the serialized output
    # :rtype: bytes
    fp = io.BytesIO()
    dump(obj, fp, **kwargs)
    return fp.getvalue()

def dump(obj, fp, **kwargs):
    # Serialize an object to a file.
    # :param obj: the object to serialize
    # :param fp: a file-like object
    # :param kwargs: keyword arguments passed to :class:`~.CBOREncoder`
    CBOREncoder(fp, **kwargs).encode(obj)
