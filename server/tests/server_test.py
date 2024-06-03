import unittest
from random import Random, randint, seed

from rabbitmq_server.server import Server

class TestServer(unittest.TestCase):
    def setUp(self) -> None:
        seed(42)
        return super().setUp()

    def test_valid_number(self) -> None:
        n = randint(0, 100000)
        server = Server()