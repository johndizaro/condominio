from os.path import dirname, abspath
from unittest import TestCase




class TestParametros(TestCase):
    def test_carrega_parametros(self):

        from src.lib.parametros import Parametros

        self.caminho_src = abspath(dirname(__file__))
        self.Pr = Parametros()
        self.assertTrue(self.Pr.carrega_parametros())
