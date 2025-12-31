# cbor3 – Concise Binary Object Representation for MicroPython

This repository provides a MicroPython‑compatible implementation of CBOR (Concise Binary Object Representation), derived from the original work by Arduino SA and KPN (Jan Bogaerts), with added support for Python tuple types by Sharil Tumin.

CBOR is a compact binary data format ideal for environments with limited resources, such as MicroPython devices.

## Origin

The original source is located at:
`micropython/lib/micropython-lib/python-ecosys/cbor2/cbor2`
This version merges the original files into one and adds `tuple` support.

## Features

* Encode and decode Python objects to/from CBOR bytes

* Optimized for MicroPython on constrained devices

* Supports Python `tuple` types (encoded as CBOR arrays)

## Installation

Copy `cbor3.py` to your MicroPython device.

## Usage
### Encoding

```python

from cbor3 import dumps

data = {
    'string_data': 'Hello, CBOR!',
    'int_data': 12345,
    'float_data': 3.14159,
    'bool_true': True,
    'bool_false': False,
    'null_data': None,
    'byte_string': b'\x01\x02\x03',
    'list_data': [1, 'two', 3.0],
    'tuple_data': (1, 'two', 3.0),  # Tuple support added
    'map_data': {'key1': 'value1', 'key2': 2}
}

cbor_bytes = dumps(data)
print(cbor_bytes)
```

### Decoding

```python

from cbor3 import loads

decoded_data = loads(cbor_bytes)
print(decoded_data)

# Access tuple data
print(decoded_data['tuple_data'])
```

## Modifications

* Tuple Support: Added encoding/decoding for Python `tuple` types, treating them as CBOR arrays.
    Implemented by Sharil Tumin in 2025.

### Compatibility Note

Data encoded with `tuple` types is not compatible with the original `cbor2` library for decoding.
Data without tuples can still be decoded with `cbor2` without issues.
The library is renamed to cbor3 to avoid confusion.

## License

MIT License
Copyright (c) 2023 Arduino SA
Copyright (c) 2018 KPN (Jan Bogaerts)
Edited 2025 Sharil Tumin – added tuple support.

See full license text in `cbor3.py`.
