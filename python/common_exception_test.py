
from unittest import TestCase

import common_exception

TEXT = '''Traceback (most recent call last):
  File "test.py", line 15, in <module>
    main()
  File "test.py", line 11, in main
    f()
  File "test.py", line 8, in f
    g()
  File "test.py", line 5, in g
    raise Exception('OMG NOES')
Exception: OMG NOES
'''

TEXT2 = '''Traceback (most recent call last):
  File "test.py", line 15, in <module>
    main()
  File "test.py", line 11, in main
    f()
  File "test.py", line 8, in f
    g()
  File "test.py", line 5, in g
    raise Exception('OMG NOES')
Exception'''


class TestText(TestCase):
    def runTest(self):
        for text in [TEXT, TEXT2]:
            common_exception.fromExceptionText(text)


class TestCurrent(TestCase):
    def runTest(self):
        try:
            
            def g():
                x = 1
                raise Exception('OMG NOES')
            
            def f():
                x = 2
                g()
            
            f()
            
        except Exception:
            print common_exception.fromCurrentException()


if __name__ == '__main__':
    import unittest
    unittest.main()
