import logging
import re

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
    from gi.repository import Gtk, Gdk
except ImportError as problema:
    Gdk = None
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

# try:
#     import sys
# except ImportError as problema:
#     print(problema)
#     sys = None
#     exit(1)

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


class CadCondominio:
    def __init__(self, **kwarg):

        self.col_a01_id_condominio = 0
        self.col_a01_nome = 1
        self.col_a01_endereco = 2
        self.col_a01_numero = 3
        self.col_a01_bairro = 4
        self.col_a01_cidade = 5

        # self.ge_dic_dados = dict()
        # self.ge_dic_param_sis = dict()
        self.ge_selecionado = False

        self.ge_a01_id_condominio = None

        self.JP = JanelaProblema()

        if kwarg['dic_param_sis']:
            self.ge_dic_param_sis = kwarg['dic_param_sis']
        else:
            msg = 'Esta faltando os parametros do sistema'
            logging.error(msg)
            self.JP.msgerro(janela=None, texto_primario="PARAMETROS", texto_secundario=msg)
            exit(1)

        if kwarg['titulo']:
            self.ge_titulo = kwarg['titulo']
        else:
            msg = 'Esta faltando titulo da tela'
            logging.error(msg)
            self.JP.msgerro(janela=None, texto_primario="PARAMETROS", texto_secundario=msg)
            exit(1)

        self.builder = Gtk.Builder()
        try:
            self.caminho = '/'.join([abspath(dirname(__file__)), 'glade', 'menu-principal.glade'])
            self.builder.add_objects_from_file(self.caminho, ["w01_condominio"])
        except Exception as msg:
            logging.error(msg)
            self.JP.msgerro(janela=None, texto_primario=self.ge_titulo, texto_secundario=msg)
            exit(1)

        self.builder.connect_signals(self)
        self.w01 = self.builder.get_object("w01_condominio")
        self.w01.set_title("Cadastro de Condiminio")

        self.l01_a01_nome = self.builder.get_object("l01_a01_nome")
        self.l01_a01_nome.set_markup("<b>{a}</b>".format(a=self.l01_a01_nome.get_text()))
        self.e01_a01_nome = self.builder.get_object("e01_a01_nome")

        self.l01_a01_endereco = self.builder.get_object("l01_a01_endereco")
        self.l01_a01_endereco.set_markup("<b>{a}</b>".format(a=self.l01_a01_endereco.get_text()))
        self.e01_a01_endereco = self.builder.get_object("e01_a01_endereco")

        self.l01_a01_numero = self.builder.get_object("l01_a01_numero")
        self.l01_a01_numero.set_markup("<b>{a}</b>".format(a=self.l01_a01_numero.get_text()))
        self.e01_a01_numero = self.builder.get_object("e01_a01_numero")

        self.l01_a01_bairro = self.builder.get_object('l01_a01_bairro')
        self.l01_a01_bairro.set_markup("<b>{a}</b>".format(a=self.l01_a01_bairro.get_text()))
        self.e01_a01_bairro = self.builder.get_object('e01_a01_bairro')

        self.l01_a01_cidade = self.builder.get_object('l01_a01_cidade')
        self.l01_a01_cidade.set_markup("<b>{a}</b>".format(a=self.l01_a01_cidade.get_text()))
        self.e01_a01_cidade = self.builder.get_object('e01_a01_cidade')

        self.b01_excluir = self.builder.get_object('b01_excluir')

        # PREPARAÇÃO DO TREEVIEW
        self.tv01_a01 = self.builder.get_object("tv01_a01")

        self.lst_tv01 = Gtk.ListStore(str, str, str)
        self.tv01_a01.set_model(self.lst_tv01)
        self.desenha_tv01(tv=self.tv01_a01)
        res = self.pesquisar_condominio()
        self.preencher_condominio(lista=self.lst_tv01, res=res)
        # -------------------------------------------------------------------

        self.w01.set_visible(True)
        self.w01.show_all()

    def on_tv01_a01_key_press_event(self, widget, event):

        keyval = Gdk.keyval_name(event.keyval)
        if keyval == 'Return' or keyval == 'KP_Enter':

            selection = widget.get_selection()
            modelx, iterx = selection.get_selected()

            self.limpar_tela()

            try:
                id_condominio = str(modelx.get_value(iterx, self.col_a01_id_condominio))
                self.ge_a01_id_condominio = id_condominio
            except ValueError:
                return False
            finally:
                self.ge_selecionado = True
                self.b01_excluir.set_sensitive(True)

            dic_condominio = self.consulta_condominio(id_condominio=id_condominio)

            if len(dic_condominio) != 0:
                self.mostrar_dados(dic_dados=dic_condominio)
                self.ge_dic_dados = dic_condominio
                self.ge_selecionado = True
            else:
                self.limpar_tela()

    def on_b01_fechar_clicked(self, widget):

        tela = widget.get_parent_window()
        tela.destroy()

    def on_b01_exluir_clicked(self, widget):

        if not self.ge_selecionado:
            msg = "Você deverá selecionar o condomínio antes de exclui-lo"
            self.JP.msgwarning(janela=self.w01, texto_primario="ATENÇÃO", texto_secundario=msg)
            return False

        msg = "Deseja realmente apagar todas as informações deste Condominio?" \
              "Cuidado isto não tem volta a menos que suas copias de segurança estejam em dia."
        resposta = self.JP.msgquestion(janela=self.w01, texto_primario="Excluir condomínio", texto_secundario=msg)

        if resposta:
            self.apagar(id_condominio=self.ge_dic_dados['a01_id_condominio'])
            res = self.pesquisar_condominio()
            self.preencher_condominio(lista=self.lst_tv01, res=res)
            self.limpar_tela()

        self.e01_a01_nome.grab_focus()

    def on_b01_salvar_clicked(self, widget):

        if not self.validar_campos():
            return False

        if self.ge_selecionado:
            dados_salvo = self.alterar(dic_dados=self.ge_dic_dados)
        else:
            dados_salvo = self.incluir(dic_dados=self.ge_dic_dados)

        if dados_salvo:
            self.limpar_tela()
            res = self.pesquisar_condominio()
            self.preencher_condominio(lista=self.lst_tv01, res=res)
        else:
            msg = "Problemas ao salvar informações"
            logging.error(msg)
            self.JP.msgerro(janela=self.w01, texto_primario=self.ge_titulo)
            exit(1)
        self.e01_a01_nome.grab_focus()

    def apagar(self, id_condominio):
        try:
            conn = psycopg2.connect(self.ge_dic_param_sis['DSN'])
            conn.set_client_encoding(self.ge_dic_param_sis['CLIENTEENCODING'])
        except psycopg2.ProgrammingError as msg:
            logging.error(msg)
            self.JP.msgerro(janela=self.w01, texto_primario=self.ge_titulo, texto_secundario=msg)
            return False

        cur = conn.cursor()
        try:
            cur.execute(
                """
             DELETE  FROM  a01_condominio WHERE a01_id_condominio = %s;

             """, (
                    id_condominio,
                )
            )
        except psycopg2.DatabaseError as msg:
            logging.error(msg)
            self.JP.msgerro(janela=self.w01, texto_primario=self.ge_titulo, texto_secundario=msg)
            return False

        conn.commit()
        cur.close()

        del conn, cur
        return True

    def limpar_tela(self):
        """
        Limpeza de campos de tela e variaveis de trabalho
        """

        self.ge_selecionado = False
        self.ge_dic_dados = {}
        self.ge_a01_id_condominio = None

        self.e01_a01_nome.set_text('')
        self.e01_a01_bairro.set_text('')
        self.e01_a01_cidade.set_text('')
        self.e01_a01_endereco.set_text('')
        self.e01_a01_numero.set_text('')

        self.e01_a01_nome.set_property("primary-icon-stock", None)
        self.e01_a01_bairro.set_property("primary-icon-stock", None)
        self.e01_a01_cidade.set_property("primary-icon-stock", None)
        self.e01_a01_endereco.set_property("primary-icon-stock", None)
        self.e01_a01_numero.set_property("primary-icon-stock", None)

    def validar_campos(self):

        """
        Validar campos para salvar no banco de dados
        retorna True para valido
        retorna False para invalido
        :return: boolean
        """
        valido = True
        numerovalido = re.compile(r'[0-9]')

        self.ge_dic_dados['a01_id_condominio'] = self.ge_a01_id_condominio

        if len(str(self.e01_a01_nome.get_text().strip())) == 0:
            self.ge_dic_dados = {}
            self.e01_a01_nome.set_property("primary-icon-stock", Gtk.STOCK_DIALOG_ERROR)
            self.e01_a01_nome.grab_focus()
            valido = False
        else:
            self.ge_dic_dados['e01_a01_nome'] = str(self.e01_a01_nome.get_text().strip())
            self.e01_a01_nome.set_property("primary-icon-stock", None)

        if len(str(self.e01_a01_endereco.get_text().strip())) == 0:
            self.ge_dic_dados = {}
            self.e01_a01_endereco.set_property("primary-icon-stock", Gtk.STOCK_DIALOG_ERROR)
            self.e01_a01_endereco.grab_focus()
            valido = False
        else:
            self.ge_dic_dados['e01_a01_endereco'] = str(self.e01_a01_endereco.get_text().strip())
            self.e01_a01_endereco.set_property("primary-icon-stock", None)

        if len(str(self.e01_a01_bairro.get_text().strip())) == 0:
            self.ge_dic_dados = {}
            self.e01_a01_bairro.set_property("primary-icon-stock", Gtk.STOCK_DIALOG_ERROR)
            self.e01_a01_bairro.grab_focus()
            valido = False
        else:
            self.ge_dic_dados['e01_a01_bairro'] = str(self.e01_a01_bairro.get_text().strip())
            self.e01_a01_bairro.set_property("primary-icon-stock", None)

        if len(str(self.e01_a01_cidade.get_text().strip())) == 0:
            self.ge_dic_dados = {}
            self.e01_a01_cidade.set_property("primary-icon-stock", Gtk.STOCK_DIALOG_ERROR)
            self.e01_a01_cidade.grab_focus()
            valido = False
        else:
            self.ge_dic_dados['e01_a01_cidade'] = str(self.e01_a01_cidade.get_text().strip())
            self.e01_a01_cidade.set_property("primary-icon-stock", None)

        wcampo = numerovalido.sub('', self.e01_a01_numero.get_text().strip())
        if len(wcampo) > 0 or self.e01_a01_numero.get_text() == "":
            self.ge_dic_dados = {}
            self.e01_a01_numero.set_property("primary-icon-stock", Gtk.STOCK_DIALOG_ERROR)
            self.e01_a01_numero.grab_focus()
            valido = False
        else:
            self.ge_dic_dados['e01_a01_numero'] = self.e01_a01_numero.get_text()
            self.e01_a01_numero.set_property("primary-icon-stock", None)

        return valido

    def consulta_condominio(self, id_condominio):

        dic_dados = {}

        try:
            conn = psycopg2.connect(self.ge_dic_param_sis['DSN'])
            conn.set_client_encoding(self.ge_dic_param_sis['CLIENTEENCODING'])

            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute(""" SELECT *
                            FROM  a01_condominio
                            WHERE a01_id_condominio = %s;
                            """, (id_condominio,)
                        )
            registros = cur.fetchall()

        except psycopg2.ProgrammingError as msg:
            logging.error(msg)
            self.JP.msgerro(janela=self.w01, texto_primario=self.ge_titulo, texto_secundario=msg)
            return False

        for registro in registros:
            dic_dados = dict(registro)

        if not registros:
            return False

        cur.close()

        del conn, cur, registros

        return dic_dados

    def alterar(self, dic_dados):
        """
        Alteração dos dados no banco de dados
        retorna True caso a alteração no bano de dados seja bem sucedida
        returna False caso a alteração no bano dee dados seja mal sucidida

        :param dic_dados: dicionario de dados validos
        :return boolean:
        """
        try:
            conn = psycopg2.connect(self.ge_dic_param_sis['DSN'])
            conn.set_client_encoding(self.ge_dic_param_sis['CLIENTEENCODING'])
        except psycopg2.ProgrammingError as msg:
            logging.error(msg)
            self.JP.msgerro(janela=self.w01, texto_primario=self.ge_titulo, texto_secundario=msg)
            return False

        cur = conn.cursor()
        try:
            cur.execute("""
             UPDATE a01_condominio SET
             a01_nome = %s,
             a01_endereco = %s,
             a01_numero = %s,
             a01_cidade = %s,
             a01_bairro = %s
             WHERE a01_id_condominio = %s;
             """, (
                str(dic_dados['e01_a01_nome']),
                str(dic_dados['e01_a01_endereco']),
                str(dic_dados['e01_a01_numero']),
                str(dic_dados['e01_a01_cidade']),
                str(dic_dados['e01_a01_bairro']),
                str(dic_dados['a01_id_condominio']),
            )
                        )

        except psycopg2.DatabaseError as msg:
            logging.error(msg)
            self.JP.msgerro(janela=self.w01, texto_primario=self.ge_titulo, texto_secundario=msg)
            return False

        conn.commit()
        cur.close()

        del conn, cur
        return True

    def incluir(self, dic_dados):
        """
         inclução dos dados no banco de dados
         retorna True caso a inclução no banco de dados seja bem sucedida
         returna False caso a inclução no banco dee dados seja mal sucidida

         :param dic_dados: dicionario de dados validos
         :return boolean:
         """

        try:
            conn = psycopg2.connect(self.ge_dic_param_sis['DSN'])
            conn.set_client_encoding(self.ge_dic_param_sis['CLIENTEENCODING'])
        except psycopg2.ProgrammingError as msg:
            logging.error(msg)
            self.JP.msgerro(janela=self.w01, texto_primario=self.ge_titulo, texto_secundario=msg)
            return False

        cur = conn.cursor()
        try:
            cur.execute(
                """
             INSERT INTO a01_condominio
             (
             a01_nome,
             a01_endereco,
             a01_numero,
             a01_cidade,
             a01_bairro
             ) VALUES(
             %s,
             %s,
             %s,
             %s,
             %s
             );
             """, (
                    dic_dados['e01_a01_nome'],
                    dic_dados['e01_a01_endereco'],
                    dic_dados['e01_a01_numero'],
                    dic_dados['e01_a01_cidade'],
                    dic_dados['e01_a01_bairro']
                    # dic_motorista['t03_rt'] if "t03_rt" in dic_motorista else '0'
                )
            )
        except psycopg2.DatabaseError as msg:
            logging.error(msg)
            self.JP.msgerro(janela=self.w01, texto_primario=self.ge_titulo, texto_secundario=msg)
            return False

        conn.commit()
        cur.close()

        del conn, cur
        return True

    def mostrar_dados(self, dic_dados):
        """
        Mostra as informações na tela  com informaçãos ou limpando os campos
        :param dic_dados:
        :return:
        """
        # for key, value in dic_dados.items():
        #     if key == 'a01_nome':
        #         if value is not None:
        #             self.e01_a01_nome.set_text(str(value))
        #         else:
        #             self.e01_a01_nome.set_text('')
        #
        #     if key == 'a01_endereco':
        #         if value is not None:
        #             self.e01_a01_endereco.set_text(str(value))
        #         else:
        #             self.e01_a01_endereco.set_text('')
        #
        #     if key == 'a01_numero':
        #         if value > 0:
        #             self.e01_a01_numero.set_text(str(value))
        #         else:
        #             self.e01_a01_numero.set_text('')
        #
        #     if key == 'a01_bairro':
        #         if value is not None:
        #             self.e01_a01_bairro.set_text(str(value))
        #         else:
        #             self.e01_a01_bairro.set_text('')
        #
        #     if key == 'a01_cidade':
        #         if value is not None:
        #             self.e01_a01_cidade.set_text(str(value))
        #         else:
        #             self.e01_a01_cidade.set_text('')

        if 'a01_nome' in dic_dados.keys():
            self.e01_a01_nome.set_text(str(dic_dados['a01_nome']))
        else:
            self.e01_a01_nome.set_text('')
        if 'a01_endereco' in dic_dados.keys():
            self.e01_a01_endereco.set_text(str(dic_dados['a01_endereco']))
        else:
            self.e01_a01_endereco.set_text('')
        if 'a01_numero' in dic_dados.keys():
            if int(dic_dados['a01_numero']) > 0:
                self.e01_a01_numero.set_text(str(dic_dados['a01_numero']))
            else:
                self.e01_a01_numero.set_text('')
        else:
            self.e01_a01_numero.set_text('')
        if 'a01_bairro' in dic_dados.keys():
            if str(dic_dados['a01_bairro']) is not None:
                self.e01_a01_bairro.set_text(str(dic_dados['a01_bairro']))
            else:
                self.e01_a01_bairro.set_text('')
        else:
            self.e01_a01_bairro.set_text('')
        if 'a01_cidade' in dic_dados.keys():
            if str(dic_dados['a01_cidade']) is not None:
                self.e01_a01_cidade.set_text(str(dic_dados['a01_cidade']))
            else:
                self.e01_a01_cidade.set_text('')
        else:
            self.e01_a01_cidade.set_text('')

    def desenha_tv01(self, tv):
        """
        Desenha treeview inclui as colunas de informações
        :param tv:
        :return:
        """

        tv.set_rules_hint(True)
        tv.set_grid_lines(3)

        # TV_PEN.set_has_tooltip(True)
        tv.set_property("headers-visible", True)

        cell_tv01_a01_id_condominio = Gtk.CellRendererText()
        col_a01_id_condominio = Gtk.TreeViewColumn("ID.Condominio", cell_tv01_a01_id_condominio,
                                                   text=self.col_a01_id_condominio)
        col_a01_id_condominio.set_visible(False)
        tv.append_column(col_a01_id_condominio)

        cel_tv01_a01_nome = Gtk.CellRendererText()
        col_01_a01_nome = Gtk.TreeViewColumn("Nome", cel_tv01_a01_nome, text=self.col_a01_nome)
        col_01_a01_nome.set_visible(True)
        tv.append_column(col_01_a01_nome)
        col_01_a01_nome.connect("clicked", self.clicado_col_tv01, tv, self.col_a01_nome)
        col_01_a01_nome.set_reorderable(True)

        cel_tv01_a01_endereco = Gtk.CellRendererText()
        col_a01_endereco = Gtk.TreeViewColumn("Endereço", cel_tv01_a01_endereco, text=self.col_a01_endereco)
        col_a01_endereco.set_visible(True)
        tv.append_column(col_a01_endereco)
        col_a01_endereco.connect("clicked", self.clicado_col_tv01, tv, self.col_a01_endereco)
        col_a01_endereco.set_reorderable(True)

        tv.set_enable_search(True)
        tv.set_headers_clickable(True)

    def clicado_col_tv01(self, widget, tv, coluna):

        tv.set_enable_search(True)
        widget.set_sort_column_id(coluna)

        tv.set_search_column(coluna)

    def pesquisar_condominio(self):

        lst_dic_dados = []

        try:
            conn = psycopg2.connect(self.ge_dic_param_sis['DSN'])
            conn.set_client_encoding(self.ge_dic_param_sis['CLIENTEENCODING'])

            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute(""" SELECT a01_id_condominio,
                                   a01_nome,
                                   concat(a01_endereco, ',',
                                   a01_numero, ', ',
                                   a01_bairro, ', ',
                                   a01_cidade ) as end_completo
                            FROM  a01_condominio ORDER BY UPPER(a01_nome);
                            """
                        )
            registros = cur.fetchall()

        except psycopg2.ProgrammingError as msg:
            logging.error(msg)
            self.JP.msgerro(janela=self.w01, texto_primario=self.ge_titulo, texto_secundario=msg)
            return False

        for registro in registros:
            lst_dic_dados.append(dict(registro))

        if not registros:
            return False

        cur.close()

        del conn, cur, registros

        return lst_dic_dados

    def preencher_condominio(self, lista, res):

        lista.clear()
        for i in res:
            lista.append([
                str(i['a01_id_condominio']),
                str(i['a01_nome']),
                str(i['end_completo']),
            ])
