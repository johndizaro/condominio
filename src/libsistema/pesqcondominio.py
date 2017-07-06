import logging
import socket

__author__ = 'John Evan Dizaro'

try:
    import gi

    gi.require_version('Gtk', '3.0')
except ImportError as problema:
    gi = None
    print(problema)
    exit(1)

try:
    # from gi.repository import GLib, GObject, Gio, Pango, GdkPixbuf, Gtk, Gdk, GtkSource
    from gi.repository import Gtk
except ImportError as problema:
    Gtk = None
    print(problema)
    exit(1)

try:
    import psycopg2
    import psycopg2.extras
    import psycopg2.extensions
except ImportError as problema:
    print(problema)
    psycopg2 = None
    exit(1)

try:
    import re
except ImportError as problema:
    print(problema)
    re = None
    exit(1)
try:
    import sys
except ImportError as problema:
    print(problema)
    sys = None
    exit(1)

try:
    from os.path import dirname, abspath
except Exception as problema:
    print(problema)
    exit(1)

try:
    from src.lib.janelaproblema import JanelaProblema
except Exception as problema:
    print(problema)
    exit(1)


class PesqCondominio:
    def __init__(self, *arg, **kwarg):

        self.ge_dic_param_sis = dict()
        self.JP = JanelaProblema()

        if kwarg['dic_param_sis']:
            self.ge_dic_param_sis = kwarg['dic_param_sis']
        else:
            msg = 'Esta faltando os parametros do sistema'
            logging.error("IP:{ip} -class:{a} \t{b} ->def:{c} \t - {d}".format(
                ip=str(socket.gethostbyname(socket.gethostname())),
                a=str(self.__class__.__name__),
                b=str(sys._getframe(1).f_code.co_name),
                c=str(sys._getframe(0).f_code.co_name),
                d=str(msg)
            )
            )
            self.JP.msgerro(janela=None,
                            texto_primario="{aa} - {bb}".format(aa=str(self.__class__.__name__),
                                                                bb=str(sys._getframe(0).f_code.co_name)),
                            texto_secundario=msg)
            exit(1)

    def pesquisar_condominios(self):
        """
        Faz a leitura de todos os condomínios cadastrados no banco
        :return: lista de dicionarios com todos os campos  por ordem de a01_nome
        """

        lst_dic = []
        try:
            conn = psycopg2.connect(self.ge_dic_param_sis['DSN'])
            conn.set_client_encoding(self.ge_dic_param_sis['CLIENTEENCODING'])
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute("""SELECT * FROM a01_condominio ORDER BY a01_nome ASC ;""")
        except psycopg2.Error as msg:
            logging.error("IP:{ip} -class:{a} \t{b} ->def:{c} \t - {d}".format(
                ip=str(socket.gethostbyname(socket.gethostname())),
                a=str(self.__class__.__name__),
                b=str(sys._getframe(1).f_code.co_name),
                c=str(sys._getframe(0).f_code.co_name),
                d=str(msg)
            )
            )
            self.JP.msgerro(janela=None,
                            texto_primario="{aa} - {bb}".format(aa=str(self.__class__.__name__),
                                                                bb=str(sys._getframe(0).f_code.co_name)),
                            texto_secundario=msg)
            return False

        try:
            registros = cur.fetchall()
        except Exception as msg:
            logging.error("IP:{ip} -class:{a} \t{b} ->def:{c} \t - {d}".format(
                ip=str(socket.gethostbyname(socket.gethostname())),
                a=str(self.__class__.__name__),
                b=str(sys._getframe(1).f_code.co_name),
                c=str(sys._getframe(0).f_code.co_name),
                d=str(msg)
            )
            )
            self.JP.msgerro(janela=None,
                            texto_primario="{aa} - {bb}".format(aa=str(self.__class__.__name__),
                                                                bb=str(sys._getframe(0).f_code.co_name)),
                            texto_secundario=msg)
            return False

        if not registros:
            lst_dic = []
            return lst_dic

        cur.close()
        conn.close()

        del conn, cur

        for registro in registros:
            lst_dic.append(dict(registro))

        return lst_dic
