import configparser
import os


class Parametros:

    def __init__(self):
        pass

    def carrega_parametros(self):

        dic_parametros = dict()

        caminho_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        caminho = '/'.join([caminho_base, 'parametros.ini'])

        config = configparser.ConfigParser()
        config.read(caminho)
        if config.get('BANCODEDADOS', 'IPSERVIDOR') == '':
            return False
        if config.get('BANCODEDADOS', 'NOMEBANCO') == '':
            return False
        if config.get('BANCODEDADOS', 'PORTA') == '':
            return False
        if config.get('BANCODEDADOS', 'CLIENTEENCODING') == '':
            return False

        dic_parametros['IPSERVIDOR'] = config.get('BANCODEDADOS', 'IPSERVIDOR')
        dic_parametros['NOMEBANCO'] = config.get('BANCODEDADOS', 'NOMEBANCO')
        dic_parametros['PORTA'] = config.get('BANCODEDADOS', 'PORTA')
        dic_parametros['CLIENTEENCODING'] = config.get('BANCODEDADOS', 'CLIENTEENCODING')
        dic_parametros['USUARIO'] = config.get('BANCODEDADOS', 'USUARIO')
        dic_parametros['SENHA'] = config.get('BANCODEDADOS', 'SENHA')

        dic_parametros['LOG_CAMINHO'] = config.get('LOG', 'LOG_CAMINHO')
        dic_parametros['TIPO_LOG'] = config.get('LOG', 'TIPO_LOG')

        dic_parametros['AMBIENTE_TELA'] = config.get('AMBIENTE', 'TELA')

        dic_parametros['DSN'] = "dbname='%s' user='%s' password='%s' host='%s' port='%s'" % (
                dic_parametros['NOMEBANCO'],
                dic_parametros['USUARIO'],
                dic_parametros['SENHA'],
                dic_parametros['IPSERVIDOR'],
                dic_parametros['PORTA'])

        return dic_parametros
