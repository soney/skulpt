__author__ = 'bmiller'

def testEqual(actual, expected, places=5):
    if isinstance(expected,int):
        if actual == expected:
            print('Pass')
            return True
    elif isinstance(expected,float):
        if abs(actual-expected) < 10**(-places):
            print('Pass')
            return True
    else:
        if actual == expected:
            print('Pass')
            return True
    print('Test Failed: expected ' + str(expected) + ' but got ' + str(actual))
    return False

def testNotEqual(actual, expected):
    pass

