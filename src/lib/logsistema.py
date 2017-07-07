import socket

try:
    import logging
except ImportError as problema:
    print(problema)
    logging = None
    exit(1)


class LogSistema:
    def __init__(self, **kwarg):

        self.ge_dic_param_sis = {}
        self.ge_dic_usuario = {}

        self.ge_ip_local = ""

        if kwarg['dic_param_sis']:
            self.ge_dic_param_sis = kwarg['dic_param_sis']
        else:
            exit(1)

        tipo_log = 0
        if self.ge_dic_param_sis['TIPO_LOG'] == 'DEBUG':
            tipo_log = logging.DEBUG
        elif self.ge_dic_param_sis['TIPO_LOG'] == 'INFO':
            tipo_log = logging.INFO
        elif self.ge_dic_param_sis['TIPO_LOG'] == 'WARNING':
            tipo_log = logging.WARNING
        elif self.ge_dic_param_sis['TIPO_LOG'] == 'ERROR':
            tipo_log = logging.ERROR
        elif self.ge_dic_param_sis['TIPO_LOG'] == 'CRITICAL':
            tipo_log = logging.CRITICAL
        else:
            logging.error("Problemas na confiuração do LOG ")
            exit(1)

        ip = str(socket.gethostbyname(socket.gethostname()))

        formato_msg = '%(levelname)8s: ' \
                      '\t%(asctime)s ' \
                      'IP:{:<15} ' \
                      'FILENAME:%(filename)-20s ' \
                      'FUNCNAME:%(funcName)-30s ' \
                      'MODULE:%(module)-s ' \
                      'LINENO:%(lineno)d ' \
                      'MSG: %(message)-s'.format(ip)

        logging.basicConfig(
            format=formato_msg,
            level=tipo_log,
            filename=self.ge_dic_param_sis['LOG_CAMINHO'])

        logging.info(" Entrou no sistema ")


