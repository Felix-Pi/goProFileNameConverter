from unittest import TestCase
from main import *

class Test(TestCase):
    def test_validate_path(self):
        assert 'LRV/' == validate_path('LRV')
        assert 'LRV/' == validate_path('LRV/')

        os.scandir('~"/Pictures/GoPro/2020-12-25/"')
