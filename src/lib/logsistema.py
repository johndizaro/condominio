import socket

try:
    from src.lib.janelaproblema import JanelaProblema
except ImportError as problema:
    print(problema)
    logging = None
    exit(1)

try:
    import logging
except ImportError as problema:
    print(problema)
    logging = None
    exit(1)


class LogSistema:
    def __init__(self, *arg, **kwarg):

        self.ge_dic_param_sis = {}
        self.ge_dic_usuario = {}

        self.ge_ip_local = ""

        if kwarg['dic_param_sis']:
            self.ge_dic_param_sis = kwarg['dic_param_sis']
        else:
            self.JanelaProblema.msgerro(self,
                                        janela=None,
                                        texto_primario=self.__class__.__name_,
                                        texto_secundario='Não foi possivel trazer DIC_DB!')
            exit(1)

        x = 0
        if self.ge_dic_param_sis['TIPO_LOG'] == 'DEBUG':
            x = logging.DEBUG
        elif self.ge_dic_param_sis['TIPO_LOG'] == 'INFO':
            x = logging.INFO
        elif self.ge_dic_param_sis['TIPO_LOG'] == 'WARNING':
            x = logging.WARNING
        elif self.ge_dic_param_sis['TIPO_LOG'] == 'ERROR':
            x = logging.ERROR
        elif self.ge_dic_param_sis['TIPO_LOG'] == 'CRITICAL':
            x = logging.CRITICAL
        else:
            self.JanelaProblema.msgerro(self,
                                        janela=None,
                                        texto_primario=self.__class__.__name_,
                                        texto_secundario='Opção inválida em [LOG]...LOG_CAMINHO =???!')
            exit(1)

        xip = str(socket.gethostbyname(socket.gethostname()))

        logging.basicConfig(level=x,
                            format='%(asctime)s '
                                   '%(ip)s'
                                   'ARQUIVO:%(filename)s '
                                   'MODULO:%(module)s '
                                   'FUNÇÃO:%(funcName)s '
                                   'LINHA:%(lineno)d '
                                   'MENSAGEM:%(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S',
                            filename=self.ge_dic_param_sis['LOG_CAMINHO'],
                            filemode='a'
                            )

        # logging.info("LOG INICIADA PARA O IP:{ip}".format(ip=str(socket.gethostbyname(socket.gethostname()))))
