
To run the tests:

```bash
mpremote u0 mount . run run_tests.py
```
The results will looks like below:

```
Running tests...
--- Running test_case_1 ---
PASS: original test case s b'1234\n\r\x00ABC,123\x00\t' == b'1234\n\r\x00ABC,123\x00\t'
PASS: original test case t {'op': 'ping', 'args': {}} == {'op': 'ping', 'args': {}}
PASS: original test case v ("This isn't,", -0.0012, 'RR', (1, 2, -3), b'a: problem!') == ("This isn't,", -0.0012, 'RR', (1, 2, -3), b'a: problem!')
PASS: original test case v type ("This isn't,", -0.0012, 'RR', (1, 2, -3), b'a: problem!') is an instance of <class 'tuple'>
PASS: original test case v[3] type (1, 2, -3) is an instance of <class 'tuple'>
--- Running test_simple_tuple ---
PASS: simple tuple equality (1, 2, 3) == (1, 2, 3)
PASS: simple tuple type (1, 2, 3) is an instance of <class 'tuple'>
--- Running test_nested_tuple ---
PASS: nested tuple equality (1, (2, 3), 4) == (1, (2, 3), 4)
PASS: nested tuple type (1, (2, 3), 4) is an instance of <class 'tuple'>
PASS: nested tuple inner type (2, 3) is an instance of <class 'tuple'>
--- Running test_tuple_mixed_types ---
PASS: mixed tuple equality ('hello', 123, True, None, b'\x01\x02') == ('hello', 123, True, None, b'\x01\x02')
PASS: mixed tuple type ('hello', 123, True, None, b'\x01\x02') is an instance of <class 'tuple'>
--- Running test_empty_tuple ---
PASS: empty tuple equality () == ()
PASS: empty tuple type () is an instance of <class 'tuple'>
--- Running test_tuple_in_dict ---
PASS: tuple in dict equality {'key': (10, 20, 'val')} == {'key': (10, 20, 'val')}
PASS: tuple in dict type (10, 20, 'val') is an instance of <class 'tuple'>
--- Running test_tuple_in_list ---
PASS: tuple in list equality [1, (2, 'three'), 4] == [1, (2, 'three'), 4]
PASS: tuple in list type (2, 'three') is an instance of <class 'tuple'>
--- Test Summary ---
All 7 tests PASSED!
```
