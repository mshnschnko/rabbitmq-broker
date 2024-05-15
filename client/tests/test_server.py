import sys
import os

import unittest
from random import randint, seed

from rabbitmq_client.broker_interactions import Interacter

class TestServer(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()
    
    def valid_test(self) -> None:
        number = randint(0, 2**32)
        interacter = Interacter()
        result = interacter.call(number)

        self.assertEqual(result, 2 * number)

    def value_error_test(self) -> None:
        data = 'string'
        interacter = Interacter()
        try:
            result = interacter.call(data)
        except Exception as e:
            self.assertEqual(type(e), ValueError)

if __name__ == '__main__':
    unittest.main()