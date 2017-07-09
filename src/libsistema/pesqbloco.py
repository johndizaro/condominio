import logging

__author__ = 'John Evan Dizaro'

try:
    import gi

    gi.require_version('Gtk', '3.0')
except ImportError as problema:
    gi = None
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
    from os.path import dirname, abspath
except Exception as problema:
    print(problema)
    exit(1)

try:
    from src.lib.janelaproblema import JanelaProblema
except Exception as problema:
    print(problema)
    exit(1)


class PesqBloco:
    def __init__(self, **kwarg):

        self.ge_dic_param_sis = dict()
        self.JP = JanelaProblema()

        if kwarg['dic_param_sis']:
            self.ge_dic_param_sis = kwarg['dic_param_sis']
        else:
            msg = 'Esta faltando os parametros do sistema'
            logging.error(msg)
            self.JP.msgerro(janela=None,
                            texto_primario="Pesquisa de Condomínio",
                            texto_secundario=msg)
            exit(1)

    def pesquisar_blocos(self, id_condominio=0):
        """
        Faz a leitura de todos os blocos do condomínio especificado
        :return: lista de dicionarios com todos os campos  por ordem de a01_nome
        :param id_condominio:número do condominio para trazer a relação de blocos do mesmo
        :return:
        """

        lst_dic = []
        try:
            conn = psycopg2.connect(self.ge_dic_param_sis['DSN'])
            conn.set_client_encoding(self.ge_dic_param_sis['CLIENTEENCODING'])
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

            cur.execute("""SELECT * FROM a03_blocos
                           WHERE a03_id_condominio = %s
                           ORDER BY a03_nome_bloco ASC ;
                        """, (id_condominio,)
                        )
        except psycopg2.Error as msg:
            logging.error(msg)
            self.JP.msgerro(janela=None,
                            texto_primario="Pesquisa de Condomínio",
                            texto_secundario=msg)
            return False

        try:
            registros = cur.fetchall()
        except Exception as msg:
            logging.error(msg)
            self.JP.msgerro(janela=None,
                            texto_primario="Pesquisa de Condomínio",
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
