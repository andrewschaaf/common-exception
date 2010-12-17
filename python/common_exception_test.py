
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


class TestTest(TestCase):
    def runTest(self):
        for text in [TEXT, TEXT2]:
            print common_exception.fromExceptionText(text)


if __name__ == '__main__':
    import unittest
    unittest.main()
