import sys
import os

# cur_dir = os.getcwd()
# if cur_dir.endswith('client') and not cur_dir.endswith('rabbitmq_client'):
#     cur_dir += '/rabbitmq_client'
# sys.path.append(cur_dir)
# print(sys.path)

import unittest
from random import randint, seed

from rabbitmq_client import proto
from rabbitmq_client.broker_interactions import Interacter

class TestServer(unittest.TestCase):
    def setUp(self) -> None:
        print('jopetski')
        return super().setUp()
    
    def valid_test(self) -> None:
        number = randint(0, 2**32)
        interacter = Interacter()
        result = interacter.call(number)

        self.assertEqual(result, 2 * number)

    def type_error_test(self) -> None:
        data = 'string'
        interacter = Interacter()
        result = interacter.call(data)
        print(result)

print(__name__)
if __name__ == '__main__':
    unittest.main()