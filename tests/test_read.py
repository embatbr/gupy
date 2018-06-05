"""Tests for the Read part of CRUD.
"""


import unittest

from common import *


BASE_URL = 'http://{host}:{port}'.format(**app_conn_settings)


class TestRead(unittest.TestCase):

    URL = '%s/profile' % BASE_URL


if __name__ == '__main__':
    unittest.main()
