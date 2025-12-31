from cbor3 import dumps, loads
from tester import assertEqual, assertIsInstance, run_tests

all_passed = True

def test_simple_tuple():
    global all_passed
    # Test a simple tuple
    original_tuple = (1, 2, 3)
    encoded = dumps(original_tuple)
    decoded = loads(encoded)
    all_passed &= assertEqual(original_tuple, decoded, "simple tuple equality")
    all_passed &= assertIsInstance(decoded, tuple, "simple tuple type")
    return all_passed

def test_nested_tuple():
    global all_passed
    # Test a nested tuple
    nested_tuple = (1, (2, 3), 4)
    encoded = dumps(nested_tuple)
    decoded = loads(encoded)
    all_passed &= assertEqual(nested_tuple, decoded, "nested tuple equality")
    all_passed &= assertIsInstance(decoded, tuple, "nested tuple type")
    all_passed &= assertIsInstance(decoded[1], tuple, "nested tuple inner type")
    return all_passed

def test_tuple_mixed_types():
    global all_passed
    # Test a tuple with mixed types
    mixed_tuple = ("hello", 123, True, None, b'\x01\x02')
    encoded = dumps(mixed_tuple)
    decoded = loads(encoded)
    all_passed &= assertEqual(mixed_tuple, decoded, "mixed tuple equality")
    all_passed &= assertIsInstance(decoded, tuple, "mixed tuple type")
    return all_passed

def test_empty_tuple():
    global all_passed
    # Test an empty tuple
    empty_tuple = ()
    encoded = dumps(empty_tuple)
    decoded = loads(encoded)
    all_passed &= assertEqual(empty_tuple, decoded, "empty tuple equality")
    all_passed &= assertIsInstance(decoded, tuple, "empty tuple type")
    return all_passed

def test_tuple_in_dict():
    global all_passed
    # Test a tuple within a dictionary
    data_with_tuple = {"key": (10, 20, "val")}
    encoded = dumps(data_with_tuple)
    decoded = loads(encoded)
    all_passed &= assertEqual(data_with_tuple, decoded, "tuple in dict equality")
    all_passed &= assertIsInstance(decoded["key"], tuple, "tuple in dict type")
    return all_passed

def test_tuple_in_list():
    global all_passed
    # Test a tuple within a list
    list_with_tuple = [1, (2, "three"), 4]
    encoded = dumps(list_with_tuple)
    decoded = loads(encoded)
    all_passed &= assertEqual(list_with_tuple, decoded, "tuple in list equality")
    all_passed &= assertIsInstance(decoded[1], tuple, "tuple in list type")
    return all_passed

def test_case_1():
    global all_passed
    all_passed = True
    s = b'1234\n\r\0ABC,123\0\t'
    t = {'op':'ping','args':{}}
    v = ("This isn't,", -0.0012, 'RR', (1,+2,-3), b"a: problem!")

    data = {'s':s, 't':t, 'v':v}
    pk = dumps(data)
    upk = loads(pk)

    all_passed &= assertEqual(s, upk['s'], "original test case s")
    all_passed &= assertEqual(t, upk['t'], "original test case t")
    all_passed &= assertEqual(v, upk['v'], "original test case v")
    all_passed &= assertIsInstance(upk['v'], tuple, "original test case v type")
    all_passed &= assertIsInstance(upk['v'][3], tuple, "original test case v[3] type")
    return all_passed

test_functions = [
    test_case_1,
    test_simple_tuple,
    test_nested_tuple,
    test_tuple_mixed_types,
    test_empty_tuple,
    test_tuple_in_dict,
    test_tuple_in_list,
]

run_tests(test_functions)
