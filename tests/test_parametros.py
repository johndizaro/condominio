from os.path import dirname, abspath
from unittest import TestCase

from src.lib.parametros import Parametros


class TestParametros(TestCase):

    def setUp(self):

        self.caminho_src = abspath(dirname(__file__))

        self.Pr = Parametros()
        self.dicionario = self.Pr.carrega_parametros()

    def test_carrega_parametros(self):

        self.assertTrue(self.Pr.carrega_parametros())

    def test_conteudo_parametos(self):

        self.assertIsNotNone(self.Pr.carrega_parametros())

    def test_parametos_ipservidor(self):

        self.assertTrue('IPSERVIDOR' in self.dicionario)

    def test_parametos_nomebanco(self):

        self.assertTrue('NOMEBANCO' in self.dicionario)

    def test_parametos_porta(self):

        self.assertTrue('PORTA' in self.dicionario)

    def test_parametos_clienteencoding(self):

        self.assertTrue('CLIENTEENCODING' in self.dicionario)

    def test_parametos_usuario(self):

        self.assertTrue('USUARIO' in self.dicionario)

    def test_parametos_senha(self):

        self.assertTrue('SENHA' in self.dicionario)

    def test_parametos_log_caminho(self):

        self.assertTrue('LOG_CAMINHO' in self.dicionario)

    def test_parametos_tipo_log(self):

        self.assertTrue(self.dicionario['TIPO_LOG'] in ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'), msg='tipo de log inesistente')

    def test_parametos_ambiente_tela(self):

        self.assertTrue('AMBIENTE_TELA' in self.dicionario)

    def test_parametos_dns(self):

        self.assertTrue('DSN' in self.dicionario)
    #
    # def tearDown(self):
    #     self.Pr.dispose()

