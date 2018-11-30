from unittest import TestCase

from condominio import Condominio


class TestCondominio(TestCase):
    def setUp(self):
        self.Cd  = Condominio

    def tearDown(self):
        self.Cd.dispose()

