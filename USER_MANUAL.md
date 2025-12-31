# CBOR for MicroPython - User Manual

This manual provides detailed instructions on how to use the `cbor3.py` library for Concise Binary Object Representation (CBOR) encoding and decoding in MicroPython environments. This version includes enhanced support for Python `tuple` types.

## Table of Contents

1.  [Introduction](#1-introduction)
2.  [Installation](#2-installation)
3.  [Basic Usage](#3-basic-usage)
    *   [Encoding Python Objects](#encoding-python-objects)
    *   [Decoding CBOR Bytes](#decoding-cbor-bytes)
4.  [Supported Data Types](#4-supported-data-types)
5.  [Handling Tuples](#5-handling-tuples)
6.  [Error Handling](#6-error-handling)
7.  [API Reference](#7-api-reference)
    *   [`dumps(obj, **kwargs)`](#dumpsobj-kwargs)
    *   [`loads(payload, **kwargs)`](#loadspayload-kwargs)
    *   [`dump(obj, fp, **kwargs)`](#dumpobj-fp-kwargs)
    *   [`load(fp, **kwargs)`](#loadfp-kwargs)
8.  [Examples](#8-examples)

## 1. Introduction

CBOR (Concise Binary Object Representation) is a data format optimized for small message size and extensibility without the need for version negotiation. It's an ideal choice for data exchange in constrained systems, such as those powered by MicroPython, due to its efficiency and compact nature.

This `cbor3.py` library allows you to serialize Python objects into CBOR-encoded bytes and deserialize CBOR bytes back into Python objects. A key feature of this specific version is its explicit support for Python `tuple` types, which are encoded and decoded as CBOR arrays.

## 2. Installation

To use the `cbor3.py` library on your MicroPython device, simply copy the `cbor3.py` file to the device's filesystem. You can typically do this using `mpremote`, `ampy`, `rshell`, or your preferred MicroPython development tool.

Example using `mpremote`:

```bash
mpremote u0 cp cbor3.c :
```
(Replace **u0** (`/dev/ttyUSB0`) with the actual serial port of your MicroPython device.)

## 3. Basic Usage

### Encoding Python Objects

Use the `dumps()` function to serialize a Python object into a CBOR-encoded `bytes` object.

```py
from cbor3 import dumps

# Example data with various types, including a tuple
data_to_encode = {
    "name": "MicroPython Device",
    "id": 101,
    "active": True,
    "settings": ("mode_a", 1, False), # This will be encoded as a CBOR array
    "sensor_readings": [25.5, 26.1, 25.9],
    "raw_bytes": b'\xDE\xAD\xBE\xEF'
}

cbor_output = dumps(data_to_encode)
print("CBOR Bytes:", cbor_output)
print("Type:", type(cbor_output))
```

### Decoding CBOR Bytes

Use the `loads()` function to deserialize CBOR-encoded `bytes` back into a Python object.

```py
from cbor3 import loads

# Assuming cbor_output is the bytes object from the encoding example
decoded_data = loads(cbor_output)

print("Decoded Data:", decoded_data)
print("Type:", type(decoded_data))
print("Tuple data:", decoded_data["settings"])
print("Type of tuple data:", type(decoded_data["settings"]))
```

## 4. Supported Data Types

The `cbor3.py` library supports the following Python data types for encoding and decoding:

*   **Integers:** `int` (both positive and negative)
*   **Floating-point numbers:** `float` (encoded as double-precision CBOR floats)
*   **Byte strings:** `bytes`, `bytearray`
*   **Text strings:** `str` (encoded as UTF-8)
*   **Booleans:** `True`, `False`
*   **Null:** `None`
*   **Arrays/Lists:** `list`
*   **Tuples:** `tuple` 
*   **Maps/Dictionaries:** `dict`
*   **Simple Values:** `CBORSimpleValue` objects (for CBOR simple values 0-19 and 24-31)

## 5. Handling Tuples

This updated `cbor3.py` specifically adds support for Python `tuple` types. When a `tuple` is encountered during encoding, it is serialized as a CBOR array. During decoding, a CBOR array that was originally a Python `tuple` will be deserialized back into a Python `tuple`.

This ensures that data structures containing tuples can be faithfully round-tripped through CBOR serialization and deserialization.

## 6. Error Handling

The library defines two custom exceptions for error handling:

*   `CBORDecodeError`: Raised when an error occurs during the deserialization of a CBOR datastream (e.g., malformed CBOR, unexpected end of stream).
*   `CBOREncodeError`: Raised when an error occurs during the serialization of an object into a CBOR datastream (e.g., attempting to encode an unsupported Python type).

It is recommended to wrap `loads()` and `dumps()` calls in `try...except` blocks to handle potential errors gracefully.

```py
from cbor3 import loads, dumps, CBORDecodeError, CBOREncodeError

try:
    invalid_cbor = b'\xFF' # Malformed CBOR
    data = loads(invalid_cbor)
except CBORDecodeError as e:
    print(f"Decoding Error: {e}")

try:
    unencodable_obj = complex(1, 2)
    cbor_output = dumps(unencodable_obj)
except CBOREncodeError as e:
    print(f"Encoding Error: {e}")
```

## 7. API Reference

### `dumps(obj, **kwargs)`

Serializes a Python object `obj` into a CBOR-encoded `bytes` object.

*   `obj`: The Python object to serialize.
*   `**kwargs`: Additional keyword arguments (currently not used by `CBOREncoder`).

**Returns:** `bytes` - The CBOR-encoded data.

### `loads(payload, **kwargs)`

Deserializes a CBOR-encoded `bytes` object `payload` back into a Python object.

*   `payload`: The `bytes` object containing CBOR data.
*   `**kwargs`: Additional keyword arguments (currently not used by `CBORDecoder`).

**Returns:** `object` - The deserialized Python object.

### `dump(obj, fp, **kwargs)`

Serializes a Python object `obj` to a file-like object `fp`.

*   `obj`: The Python object to serialize.
*   `fp`: A file-like object open for writing in binary mode (e.g., `io.BytesIO`, a file opened with `open('file.cbor', 'wb')`).
*   `**kwargs`: Additional keyword arguments (currently not used by `CBOREncoder`).

### `load(fp, **kwargs)`

Deserializes a CBOR-encoded stream from a file-like object `fp`.

*   `fp`: A file-like object open for reading in binary mode (e.g., `io.BytesIO`, a file opened with `open('file.cbor', 'rb')`).
*   `**kwargs`: Additional keyword arguments (currently not used by `CBORDecoder`).

**Returns:** `object` - The deserialized Python object.

## 8. Examples

Refer to the [README.md](README.md) for basic usage examples and the `test.py` (and any new test files) for more comprehensive test cases.
