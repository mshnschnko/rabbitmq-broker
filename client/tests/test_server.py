import sys
import os

import unittest
from random import randint, seed, shuffle

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
        with self.assertRaises(ValueError):
            interacter.call(data)

    def too_big_number_test(self) -> None:
        data = 99999999999999999999999999999999999999999999999
        interacter = Interacter()
        with self.assertRaises(ValueError):
            interacter.call(data)

if __name__ == '__main__':
    unittest.main()