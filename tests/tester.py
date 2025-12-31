
def assertEqual(a, b, msg=None):
    if a != b:
        print(f"FAIL: {msg or ''} {a} != {b}")
        return False
    print(f"PASS: {msg or ''} {a} == {b}")
    return True

def assertIsInstance(obj, cls, msg=None):
    if not isinstance(obj, cls):
        print(f"FAIL: {msg or ''} {obj} is not an instance of {cls}")
        return False
    print(f"PASS: {msg or ''} {obj} is an instance of {cls}")
    return True

def run_tests(test_functions):
    print("Running tests...")
    tests = 0
    failures = 0
    passed = 0
    for test_func in test_functions:
        tests += 1
        print(f"--- Running {test_func.__name__} ---")
        if not test_func():
            failures += 1
        else:
            passed +=1
    print("--- Test Summary ---")
    if failures == 0:
        print(f"All {tests} tests PASSED!")
    else:
        print(f"{passed} test(s) PASSED and {failures} test(s) FAILED.")
    return failures == 0
