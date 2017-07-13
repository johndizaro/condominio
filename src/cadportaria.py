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

try:
    import re
except ImportError as problema:
    print(problema)
    re = None
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

try:
    from src.libsistema.pesqcondominio import PesqCondominio
except Exception as problema:
    print(problema)
    exit(1)

try:
    from src.lib.comboboxdados import ComboBoxDados
except Exception as problema:
    print(problema)
    exit(1)


class CadPortaria:
    def __init__(self, **kwarg):

        # self.ge_dic_dados = dict()
        self.ge_dic_param_sis = dict()
        self.ge_selecionado = False

        self.ge_id_condominio = 0
        self.ge_id_portaria = 0

        self.col_cb02_a01_id_condominio = 0
        self.col_cb02_a01_nome = 1

        self.col_tv02_a02_id_condominio = 0
        self.col_tv02_a02_id_portaria = 1
        self.col_tv02_a02_nome_portaria = 2
        self.col_tv02_dados_portaria = 3

        self.JP = JanelaProblema()
        self.CBD = ComboBoxDados()

        if kwarg['dic_param_sis']:
            self.ge_dic_param_sis = kwarg['dic_param_sis']
        else:
            msg = 'Esta faltando os parametros do sistema'
            logging.error(msg)
            self.JP.msgerro(janela=None,
                            texto_primario="Cadastro de Portaria",
                            texto_secundario=msg)
            exit(1)

            self.ge_selecionado = False

        self.PC = PesqCondominio(dic_param_sis=self.ge_dic_param_sis)
        self.builder = Gtk.Builder()
        try:
            self.Caminho = '/'.join([abspath(dirname(__file__)), 'glade', 'menu-principal.glade'])
            self.builder.add_objects_from_file(self.Caminho, ["w02_portaria"])
        except Exception as msg:
            logging.error(msg)
            self.JP.msgerro(janela=None,
                            texto_primario="Cadastro de Portaria",
                            texto_secundario=msg)
            exit(1)

        self.builder.connect_signals(self)
        self.w02 = self.builder.get_object("w02_portaria")
        self.w02.set_title("Cadastro de Portaria")

        # ----------------------
        self.cb02_a02_id_condominio = self.builder.get_object("cb02_a02_id_condominio")

        self.lst_cb02 = Gtk.ListStore(str, str)
        self.cb02_a02_id_condominio.set_model(self.lst_cb02)
        self.desenha_cb02(cb=self.cb02_a02_id_condominio, lista=self.lst_cb02)
        registros = self.PC.pesquisar_condominios()
        # registros = self.carregar_condominio()
        self.preencher_combo_condominio(lista=self.lst_cb02, res=registros)

        # --------------------------
        # self.set_dado_combo(combobox=self.cb02_a02_id_condominio,
        #                     text=1,
        #                     coluna=self.col_cb02_a01_id_condominio)
        # --------------------------

        self.l02_a02_nome_portaria = self.builder.get_object("l02_a02_nome_portaria")
        self.l02_a02_nome_portaria.set_markup("<b>{a}</b>".format(a=self.l02_a02_nome_portaria.get_text()))
        self.e02_a02_nome_portaria = self.builder.get_object("e02_a02_nome_portaria")

        self.l02_a02_endereco = self.builder.get_object("l02_a02_endereco")
        self.l02_a02_endereco.set_markup("{a}".format(a=self.l02_a02_endereco.get_text()))
        self.e02_a02_endereco = self.builder.get_object("e02_a02_endereco")

        self.l02_a02_numero = self.builder.get_object("l02_a02_numero")
        self.l02_a02_numero.set_markup("{a}".format(a=self.l02_a02_numero.get_text()))
        self.e02_a02_numero = self.builder.get_object("e02_a02_numero")

        self.tv02_a02 = self.builder.get_object("tv02_a02")
        self.lst_tv02 = Gtk.ListStore(str, str, str, str)
        self.desenha_tv02(tv=self.tv02_a02)
        self.tv02_a02.set_model(self.lst_tv02)

        self.w02.set_visible(True)
        self.w02.show_all()

    def on_b02_fechar_clicked(self, widget):
        """
        :param:
        :return:
        """
        # tela = widget.get_parent_window()
        # tela.destroy()
        # self.w02.destroy()
        self.w02.destroy()

    def on_b02_salvar_clicked(self, widget):
        """
        executa as rotina para salvar e validas os campos de tela
        :param:
        :return:
        """
        # dados_salvos = False
        dic_dados = self.validar_campos()
        if not dic_dados:
            return False

        if self.ge_selecionado:
            dados_salvos = self.alterar(dic_dados=dic_dados)
        else:
            dados_salvos = self.incluir(dic_dados=dic_dados)

        if dados_salvos:
            id_condominio = self.ge_id_condominio
            self.limpar_tela()
            self.ge_id_condominio = id_condominio
            res = self.pesquisar_portarias(id_condominio=self.ge_id_condominio)
            self.mostrar_dados_tv02(lista=self.lst_tv02, res=res)
        else:
            msg = "Problemas ao salvar informações"
            logging.error(msg)
            self.JP.msgerro(janela=None,
                            texto_primario="Cadastro de Portaria",
                            texto_secundario=msg)

    def on_b02_excluir_clicked(self, widget):
        """
        Apaga portaria selecionada
        :param widget:
        :return:
        """

        apagado = False

        dic_dados = self.validar_campos()
        if not dic_dados:
            return False

        if self.ge_selecionado:
            apagado = self.apagar_portaria(id_portaria=dic_dados['a02_id_portaria'])
        else:
            msg = "Selecione uma portaria para apagar"
            logging.error(msg)
            self.JP.msgerro(janela=None,
                            texto_primario="Cadastro de Portaria",
                            texto_secundario=msg)

        if apagado:
            id_condominio = self.ge_id_condominio
            self.limpar_tela()
            res = self.pesquisar_portarias(id_condominio=id_condominio)
            self.mostrar_dados_tv02(lista=self.lst_tv02, res=res)
        else:
            msg = "Problemas ao Apagar Portaria"
            logging.error(msg)
            self.JP.msgerro(janela=None,
                            texto_primario="Cadastro de Portaria",
                            texto_secundario=msg)
            exit(1)

    def on_cb02_a02_id_condominio_changed(self, widget):
        """

        :param widget:
        :return:
        """
        try:
            id_condominio = self.CBD.get_dado_combo(comboboxm=widget,
                                                    col_traz=self.col_cb02_a01_id_condominio)
            res = self.pesquisar_portarias(id_condominio=id_condominio)
            self.lst_tv02.clear()
            if res:
                self.mostrar_dados_tv02(lista=self.lst_tv02, res=res)
                self.ge_id_condominio = id_condominio

        except AttributeError:
            pass

    def validar_campos(self):
        """
        Validação dos campos para salvar no banco de e dados
        :return: Se retorna dic_dados = False então tem problemas nos dados
                 Se retorna dic_dados com valors em um dicionario em pode salvar no banco de dados
        """

        dic_dados = dict()

        valido = True
        numerovalido = re.compile(r'[0-9]')

        if self.ge_id_condominio == 0:
            valido = False
        else:
            dic_dados['a02_id_condominio'] = self.ge_id_condominio
            dic_dados['a02_id_portaria'] = self.ge_id_portaria

        if len(str(self.e02_a02_nome_portaria.get_text().strip())) == 0:
            dic_dados = {}
            self.e02_a02_nome_portaria.set_property("primary-icon-stock", Gtk.STOCK_DIALOG_ERROR)
            self.e02_a02_nome_portaria.grab_focus()
            valido = False
        else:
            dic_dados['a02_nome_portaria'] = str(self.e02_a02_nome_portaria.get_text().strip())
            self.e02_a02_nome_portaria.set_property("primary-icon-stock", None)

        if len(str(self.e02_a02_endereco.get_text().strip())) > 0:
            dic_dados['a02_endereco'] = str(self.e02_a02_endereco.get_text().strip())
        else:
            dic_dados['a02_endereco'] = None

        if len(str(self.e02_a02_numero.get_text().strip())) > 0:
            wcampo = numerovalido.sub('', self.e02_a02_numero.get_text().strip())
            if len(wcampo) > 0:
                dic_dados = {}
                self.e02_a02_numero.set_property("primary-icon-stock", Gtk.STOCK_DIALOG_ERROR)
                self.e02_a02_numero.grab_focus()
                valido = False
            else:
                dic_dados['a02_numero'] = self.e02_a02_numero.get_text()
                self.e02_a02_numero.set_property("primary-icon-stock", None)

        if valido is False:
            dic_dados = False

        return dic_dados

    def limpar_tela(self):
        """
        Limpeza de campos de tela e variaveis de trabalho
        """

        # self.ge_dic_dados = dict()
        self.ge_selecionado = False

        self.ge_id_condominio = 0
        self.ge_id_portaria = 0

        self.e02_a02_nome_portaria.set_text('')
        self.e02_a02_endereco.set_text('')
        self.e02_a02_numero.set_text('')

        self.e02_a02_nome_portaria.set_property("primary-icon-stock", None)
        self.e02_a02_endereco.set_property("primary-icon-stock", None)
        self.e02_a02_numero.set_property("primary-icon-stock", None)

    def alterar(self, dic_dados):
        try:
            conn = psycopg2.connect(self.ge_dic_param_sis['DSN'])
            conn.set_client_encoding(self.ge_dic_param_sis['CLIENTEENCODING'])
        except psycopg2.ProgrammingError as msg:
            logging.error(msg)
            self.JP.msgerro(janela=None,
                            texto_primario="Cadastro de Portaria",
                            texto_secundario=msg)
            return False

        cur = conn.cursor()
        try:
            sql = """
                  UPDATE a02_portarias SET
                  a02_nome_portaria = %s,
                  a02_endereco = %s,
                  a02_numero = %s
                  WHERE a02_id_condominio = %s
                  AND a02_id_portaria = %s;
             """, (
                dic_dados['a02_nome_portaria'] if "a02_nome_portaria" in dic_dados else None,
                dic_dados['a02_endereco'] if "a02_endereco" in dic_dados else None,
                dic_dados['a02_numero'] if "a02_numero" in dic_dados else 0,
                dic_dados['a02_id_condominio'] if "a02_id_condominio" in dic_dados else 0,
                dic_dados['a02_id_portaria'] if "a02_id_portaria" in dic_dados else 0,
            )
            cur.execute(sql)
        except psycopg2.DatabaseError as msg:
            logging.error(msg)
            self.JP.msgerro(janela=None,
                            texto_primario="Cadastro de Portaria",
                            texto_secundario=msg)
            return False

        conn.commit()
        cur.close()

        del conn, cur
        return True

    def incluir(self, dic_dados):
        """
         inclução dos dados no banco de dados
         retorna True caso a inclução no banco de dados seja bem sucedida
         returna False caso a inclução no banco dee dados seja mal sucedida

         :param dic_dados: dicionario de dados validos
         :return boolean:
         """

        try:
            conn = psycopg2.connect(self.ge_dic_param_sis['DSN'])
            conn.set_client_encoding(self.ge_dic_param_sis['CLIENTEENCODING'])
        except psycopg2.ProgrammingError as msg:
            logging.error(msg)
            self.JP.msgerro(janela=None,
                            texto_primario="Cadastro de Portaria",
                            texto_secundario=msg)
            return False

        cur = conn.cursor()
        sql = """
             INSERT INTO a02_portarias
             (
             a02_id_condominio,
             a02_nome_portaria,
             a02_endereco,
             a02_numero
             ) VALUES(
             %s,
             %s,
             %s,
             %s
             );
             """, (
            dic_dados['a02_id_condominio'] if "a02_id_condominio" in dic_dados else 0,
            dic_dados['a02_nome_portaria'] if "a02_nome_portaria" in dic_dados else None,
            dic_dados['a02_endereco'] if "a02_endereco" in dic_dados else None,
            dic_dados['a02_numero'] if "a02_numero" in dic_dados else 0,
        )
        try:
            cur.execute(sql)
        except psycopg2.DatabaseError as msg:
            logging.error(msg)
            self.JP.msgerro(janela=None,
                            texto_primario="Cadastro de Portaria",
                            texto_secundario=msg)
            return False

        conn.commit()
        cur.close()

        del conn, cur
        return True

    def apagar_portaria(self, id_portaria):
        try:
            conn = psycopg2.connect(self.ge_dic_param_sis['DSN'])
            conn.set_client_encoding(self.ge_dic_param_sis['CLIENTEENCODING'])
        except psycopg2.ProgrammingError as msg:
            logging.error(msg)
            self.JP.msgerro(janela=None,
                            texto_primario="Cadastro de Portaria",
                            texto_secundario=msg)
            return False

        cur = conn.cursor()
        try:
            sql = """
             DELETE  from a02_portarias WHERE a02_id_portaria = %s;
             """, (id_portaria,
                   )
            cur.execute(sql)
        except psycopg2.DatabaseError as msg:
            logging.error(msg)
            self.JP.msgerro(janela=None,
                            texto_primario="Cadastro de Portaria",
                            texto_secundario=msg)
            return False

        conn.commit()
        cur.close()

        del conn, cur
        return True

    def mostrar_dados_tv02(self, lista, res):

        lista.clear()
        for i in res:
            lista.append([
                str(i['a02_id_condominio']),
                str(i['a02_id_portaria']),
                str(i['a02_nome_portaria']),
                str(i['dados_portaria']),
            ])

    def desenha_cb02(self, cb, lista):
        """
         DESENHA AS COLUNAS DO COMBO QUE IRÁ CONTER OS TIPOS DISPONIVEL
        :param cb:
        :param lista:
        :return:
        """
        cb.set_model(lista)
        cb.set_active(self.col_cb02_a01_id_condominio)

        cell_a01_id_condominio = Gtk.CellRendererText()
        cb.pack_start(cell_a01_id_condominio, True)
        cb.add_attribute(cell_a01_id_condominio, "text", self.col_cb02_a01_id_condominio)
        cell_a01_id_condominio.set_visible(False)

        cell_a01_nome = Gtk.CellRendererText()
        cb.pack_start(cell_a01_nome, True)
        cb.add_attribute(cell_a01_nome, "text", self.col_cb02_a01_nome)
        cell_a01_nome.set_visible(True)

    def desenha_tv02(self, tv):

        tv.set_rules_hint(True)
        tv.set_grid_lines(3)

        # TV_PEN.set_has_tooltip(True)
        tv.set_property("headers-visible", True)

        cell_tv02_a02_id_condominio = Gtk.CellRendererText()
        col_tv02_a02_id_condominio = Gtk.TreeViewColumn("ID.Condominio",
                                                        cell_tv02_a02_id_condominio,
                                                        text=self.col_tv02_a02_id_condominio)
        col_tv02_a02_id_condominio.set_visible(False)
        tv.append_column(col_tv02_a02_id_condominio)

        cell_tv02_a02_id_portaria = Gtk.CellRendererText()
        col_tv02_a02_id_portaria = Gtk.TreeViewColumn("ID.Portaria",
                                                      cell_tv02_a02_id_portaria,
                                                      text=self.col_tv02_a02_id_portaria)
        col_tv02_a02_id_portaria.set_visible(False)
        tv.append_column(col_tv02_a02_id_portaria)

        cel_tv02_a02_nome_portaria = Gtk.CellRendererText()
        col_tv02_a02_nome_portaria = Gtk.TreeViewColumn("Nome",
                                                        cel_tv02_a02_nome_portaria,
                                                        text=self.col_tv02_a02_nome_portaria)
        col_tv02_a02_nome_portaria.set_visible(True)
        tv.append_column(col_tv02_a02_nome_portaria)
        col_tv02_a02_nome_portaria.connect("clicked", self.clicado_col_tv02, tv, self.col_tv02_a02_nome_portaria)
        col_tv02_a02_nome_portaria.set_reorderable(True)

        cel_tv02_dados_portaria = Gtk.CellRendererText()
        col_tv02_dados_portaria = Gtk.TreeViewColumn("Endereço",
                                                     cel_tv02_dados_portaria,
                                                     text=self.col_tv02_dados_portaria)
        col_tv02_dados_portaria.set_visible(True)
        tv.append_column(col_tv02_dados_portaria)
        col_tv02_dados_portaria.connect("clicked", self.clicado_col_tv02, tv, self.col_tv02_dados_portaria)
        col_tv02_dados_portaria.set_reorderable(True)

        tv.set_enable_search(True)
        tv.set_headers_clickable(True)

    def clicado_col_tv02(self, widget, tv, coluna):
        """
        habilita pesquisa de tv
        """

        tv.set_enable_search(True)
        widget.set_sort_column_id(coluna)

        tv.set_search_column(coluna)

    def pesquisar_portarias(self, id_condominio=0):

        lst_dic_dados = []

        try:
            conn = psycopg2.connect(self.ge_dic_param_sis['DSN'])
            conn.set_client_encoding(self.ge_dic_param_sis['CLIENTEENCODING'])

            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute(""" select a02_id_condominio,
                                   a02_id_portaria,
                                   a02_nome_portaria,
                                   concat(a02_endereco, ', ', a02_numero) as dados_portaria
                            from a01_condominio, a02_portarias
                            WHERE a01_id_condominio = a02_portarias.a02_id_condominio
                            and a01_id_condominio = %s 
                            order by upper(a02_nome_portaria);
                            """, (id_condominio,))
            registros = cur.fetchall()

        except psycopg2.ProgrammingError as msg:
            logging.error(msg)
            self.JP.msgerro(janela=None,
                            texto_primario="Cadastro de Portaria",
                            texto_secundario=msg)
            return False

        for registro in registros:
            lst_dic_dados.append(dict(registro))

        if not registros:
            return False

        cur.close()

        del conn, cur, registros

        return lst_dic_dados

    def on_tv02_a02_key_press_event(self, widget, event):

        keyval = Gdk.keyval_name(event.keyval)
        if keyval == 'Return' or keyval == 'KP_Enter':

            selection = widget.get_selection()
            modelx, iterx = selection.get_selected()

            self.limpar_tela()

            try:
                id_condominio = str(modelx.get_value(iterx, self.col_tv02_a02_id_condominio))
                id_portaria = str(modelx.get_value(iterx, self.col_tv02_a02_id_portaria))
                self.ge_id_condominio = id_condominio
                self.ge_id_portaria = id_portaria
            except ValueError:
                return False
            finally:
                self.ge_selecionado = True

            dic_portaria = self.consulta_portaria(id_condominio=id_condominio, id_portaria=id_portaria)

            if len(dic_portaria) != 0:
                self.mostrar_dados_tela(dic_portaria=dic_portaria)
                # self.ge_dic_dados = dic_portaria
                self.ge_selecionado = True
            else:
                self.limpar_tela()

    def preencher_combo_condominio(self, lista, res):

        lista.clear()

        for i in res:
            lista.append([
                str(i['a01_id_condominio']),
                str(i['a01_nome']) if i['a01_nome'] else None,
            ])

    def consulta_portaria(self, id_condominio, id_portaria):

        dic_dados = {}

        try:
            conn = psycopg2.connect(self.ge_dic_param_sis['DSN'])
            conn.set_client_encoding(self.ge_dic_param_sis['CLIENTEENCODING'])

            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute(""" SELECT *
                            FROM a02_portarias
                            WHERE  a02_id_condominio = %s
                            AND  a02_id_portaria = %s;
                            ;
                            """, (id_condominio, id_portaria)
                        )
            registros = cur.fetchall()

        except psycopg2.ProgrammingError as msg:
            logging.error(msg)
            self.JP.msgerro(janela=None,
                            texto_primario="Cadastro de Portaria",
                            texto_secundario=msg)
            return False

        for registro in registros:
            dic_dados = dict(registro)

        if not registros:
            return False

        cur.close()

        del conn, cur, registros

        return dic_dados

    def mostrar_dados_tela(self, dic_portaria):

        for key, value in dic_portaria.items():
            if key == 'a02_nome_portaria':
                if value is not None:
                    self.e02_a02_nome_portaria.set_text(str(value))
                else:
                    self.e02_a02_nome_portaria.set_text('')

            if key == 'a02_endereco':
                if value is not None:
                    self.e02_a02_endereco.set_text(str(value))
                else:
                    self.e02_a02_endereco.set_text('')

            if key == 'a02_numero':
                if value > 0:
                    self.e02_a02_numero.set_text(str(value))
                else:
                    self.e02_a02_numero.set_text('')
