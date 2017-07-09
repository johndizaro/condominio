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

# try:
#     import re
# except ImportError as problema:
#     print(problema)
#     re = None
#     exit(1)
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
    from src.libsistema.pesqbloco import PesqBloco
except Exception as problema:
    print(problema)
    exit(1)

try:
    from src.lib.comboboxdados import ComboBoxDados
except Exception as problema:
    print(problema)
    exit(1)


class CadBloco:
    def __init__(self, **kwarg):
        logging.info('entrei no cadbloco')

        #
        # rotina  para salvar em string  quem chamou e quem foi chamada
        #
        # import traceback
        # stack = traceback.extract_stack()
        # chamador_filename, chamador_codeline, chamador_funcName, chamador_text = stack[-2]
        # print(inspect.getframeinfo(inspect.currentframe())[2])
        # print(chamador_filename, chamador_codeline, chamador_funcName, chamador_text)
        # chamado_filename, chamado_codeline, chamado_funcName, chamado_text = stack[-1]
        # print(inspect.getframeinfo(inspect.currentframe())[2])
        # print(chamado_filename, chamado_codeline, chamado_funcName, chamado_text)

        self.col_a01_id_condominio = 0
        self.col_a01_nome = 1

        self.col_a03_id_condominio = 0
        self.col_a03_id_bloco = 1
        self.col_a03_nome_bloco = 2

        self.ge_dic_dados = dict()
        self.ge_dic_param_sis = dict()
        self.ge_selecionado = False
        self.ge_titulo = None

        self.ge_a03_id_bloco = 0

        self.JP = JanelaProblema()

        if kwarg['dic_param_sis']:
            self.ge_dic_param_sis = kwarg['dic_param_sis']
        else:
            msg = 'Esta faltando os parametros do sistema'
            logging.error(msg)

            self.JP.msgerro(janela=None,
                            # texto_primario="class:{} - def:{} - linha:{}".format(str(self.__class__.__name__),
                            #                                                      str(sys._getframe(0).f_code.co_name),
                            #                                                      str(sys._getframe(0).f_lineno)),
                            texto_secundario=msg)
            exit(1)

        if kwarg['titulo']:
            self.ge_titulo = kwarg['titulo']
        else:
            msg = 'Esta faltando o parametro Título do sistema'
            logging.error(msg)

            self.JP.msgerro(janela=None,
                            # texto_primario="class:{} - def:{} - linha:{}".format(str(self.__class__.__name__),
                            #                                                      str(sys._getframe(0).f_code.co_name),
                            #                                                      str(sys._getframe(0).f_lineno)),
                            texto_secundario=msg)
            exit(1)

        self.CBD = ComboBoxDados()
        self.PC = PesqCondominio(dic_param_sis=self.ge_dic_param_sis)
        self.PB = PesqBloco(dic_param_sis=self.ge_dic_param_sis)

        self.ge_a01_id_condominio = None
        self.ge_selecionado = False

        self.builder = Gtk.Builder()
        try:
            self.caminho = '/'.join([abspath(dirname(__file__)), 'glade', 'menu-principal.glade'])
            self.builder.add_objects_from_file(self.caminho, ["w03_bloco"])
        except Exception as msg:
            logging.error(msg)
            self.JP.msgerro(janela=None,
                            # texto_primario="class:{} - def:{} - linha:{}".format(str(self.__class__.__name__),
                            #                                                      str(sys._getframe(0).f_code.co_name),
                            #                                                      str(sys._getframe(0).f_lineno)),
                            texto_secundario=msg)
            exit(1)

        self.builder.connect_signals(self)
        self.w03 = self.builder.get_object("w03_bloco")
        self.w03.set_title(self.ge_titulo)

        self.l03_a03_id_condominio = self.builder.get_object("l03_a03_id_condominio")
        self.l03_a03_id_condominio.set_markup("<b>{a}</b>".format(a=self.l03_a03_id_condominio.get_text()))
        self.cb03_a03_id_condominio = self.builder.get_object("cb03_a03_id_condominio")

        # PREPARAÇÃO DO cb03_a03_id_condominio
        self.lst_cb03_a03_id_condominio = Gtk.ListStore(str, str)
        self.desenha_cb03_a03_id_condominio(cb=self.cb03_a03_id_condominio, lista=self.lst_cb03_a03_id_condominio)
        registros = self.PC.pesquisar_condominios()
        self.preencher_combo_condominio(lista=self.lst_cb03_a03_id_condominio, lst_dic_condominio=registros)
        # ----------------------

        self.l03_e03_a03_nome_bloco = self.builder.get_object("l03_e03_a03_nome_bloco")
        self.l03_e03_a03_nome_bloco.set_markup("<b>{a}</b>".format(a=self.l03_e03_a03_nome_bloco.get_text()))
        self.e03_a03_nome_bloco = self.builder.get_object("e03_a03_nome_bloco")

        # PREPARAÇÃO DO TREEVIEW
        self.tv03_a03 = self.builder.get_object("tv03_a03")

        self.lst_tv03 = Gtk.ListStore(str, str, str)
        self.tv03_a03.set_model(self.lst_tv03)
        self.desenha_tv03(tv=self.tv03_a03)
        # res = self.pesquisar_bloco()
        # self.preencher_bloco(lista=self.lst_tv03, res=res)
        # -------------------------------------------------------------------

        self.w03.set_visible(True)
        self.w03.show_all()

        #
        # curframe = inspect.currentframe()
        # print('--->', curframe.f_lineno)
        #
        # (frame, filename, line_number,function_name, lines, index) = inspect.getouterframes(inspect.currentframe())[1]
        # print('1->',frame, '\n1->',filename, '\n1->',line_number, '\n1->',function_name, '\n1->',lines, '\n1->',index)
        #
        # calframe = inspect.getouterframes(curframe, 2)
        # print(calframe)
        #
        # print('caller name:', calframe[1][3])

    def desenha_tv03(self, tv):
        """
        desenha as colunas do treeview
        :param tv:recebe o objeto do treeview
        :return:
        """

        tv.set_rules_hint(True)
        tv.set_grid_lines(3)

        # TV_PEN.set_has_tooltip(True)
        tv.set_property("headers-visible", True)

        cell_tv03_a03_id_condominio = Gtk.CellRendererText()
        col_tv03_a03_id_condominio = Gtk.TreeViewColumn("ID.Condominio",
                                                        cell_tv03_a03_id_condominio,
                                                        text=self.col_a03_id_condominio)
        col_tv03_a03_id_condominio.set_visible(False)
        tv.append_column(col_tv03_a03_id_condominio)

        cell_tv03_a03_id_bloco = Gtk.CellRendererText()
        col_tv03_col_a03_id_bloco = Gtk.TreeViewColumn("ID.Bloco",
                                                       cell_tv03_a03_id_bloco,
                                                       text=self.col_a03_id_bloco)
        col_tv03_col_a03_id_bloco.set_visible(False)
        tv.append_column(col_tv03_col_a03_id_bloco)

        cell_tv03_a03_nome_bloco = Gtk.CellRendererText()
        col_tv03_col_a03_nome_bloco = Gtk.TreeViewColumn("ID.Bloco",
                                                         cell_tv03_a03_nome_bloco,
                                                         text=self.col_a03_nome_bloco)
        col_tv03_col_a03_nome_bloco.set_visible(True)
        tv.append_column(col_tv03_col_a03_nome_bloco)

        tv.set_enable_search(True)
        tv.set_headers_clickable(True)

    def desenha_cb03_a03_id_condominio(self, cb, lista):
        """
        Desenha as colunas do cb03_a03_id_condomini
        :param cb: combobox
        :param lista: liststore definição das colunas
        :return:
        """
        cb.set_model(lista)
        cb.set_active(self.col_a01_id_condominio)

        cell_a01_id_condominio = Gtk.CellRendererText()
        cb.pack_start(cell_a01_id_condominio, True)
        cb.add_attribute(cell_a01_id_condominio, "text", self.col_a01_id_condominio)
        cell_a01_id_condominio.set_visible(False)

        cell_a01_nome = Gtk.CellRendererText()
        cb.pack_start(cell_a01_nome, True)
        cb.add_attribute(cell_a01_nome, "text", self.col_a01_nome)
        cell_a01_nome.set_visible(True)

    def preencher_combo_condominio(self, lista, lst_dic_condominio):
        """
        Colocra as informações nas colunas determinadas
        :param lista: definição das coluna para preencher
        :param lst_dic_condominio:
        :return:
        """
        lista.clear()

        for i in lst_dic_condominio:
            lista.append([
                str(i['a01_id_condominio']),
                str(i['a01_nome']) if i['a01_nome'] else None,
            ])

    def on_b03_fechar_clicked(self):
        """
        libera o CadBloco - apagar da tela
        :param:
        :return:
        """

        self.w03.destroy()

    def on_b03_salvar_clicked(self):
        """
        Manda executar a validação dos campos da tela bem como verifica se
        os dados devem ser alterados ou incluidos
        :param:
        :return:
        """

        dic_dados = self.validar_campos()
        if not dic_dados:
            return False

        if dic_dados:
            if self.ge_selecionado:
                dados_salvo = self.alterar(dic_dados=dic_dados)
            else:
                dados_salvo = self.incluir(dic_dados=dic_dados)
            if dados_salvo:
                self.limpar_tela()
                res = self.PB.pesquisar_blocos(id_condominio=self.ge_a01_id_condominio)
                self.mostrar_dados_tv03(lista=self.lst_tv03, res=res)
        else:
            msg = "Problemas ao Dicionário não encontrado"
            logging.error(msg)
            self.JP.msgerro(janela=self.w03,
                            # texto_primario="class:{} - def:{} - linha:{}".format(str(self.__class__.__name__),
                            #                                                      str(sys._getframe(0).f_code.co_name),
                            #                                                      str(sys._getframe(0).f_lineno)),
                            texto_secundario=msg)
            exit(1)

    def on_cb03_a03_id_condominio_changed(self, widget):
        """
        verifica qual opção do combobox foi selecionado
        :param widget:
        :return:
        """

        try:
            self.ge_a01_id_condominio = self.CBD.get_dado_combo(comboboxm=widget,
                                                                col_pesq=self.col_a01_nome,
                                                                col_traz=self.col_a01_id_condominio)

            res = self.PB.pesquisar_blocos(id_condominio=self.ge_a01_id_condominio)
            self.mostrar_dados_tv03(lista=self.lst_tv03, res=res)
            # res = self.pesquisar_portarias(id_condominio=id_condominio)
            # self.mostrar_dados_tv02(lista=self.lst_tv02, res=res)
            # self.ge_id_condominio = id_condominio
        except ValueError:
            pass

    def on_tv03_a03_key_press_event(self, widget, event):

        keyval = Gdk.keyval_name(event.keyval)
        if keyval == 'Return' or keyval == 'KP_Enter':

            selection = widget.get_selection()
            modelx, iterx = selection.get_selected()

            self.limpar_tela()

            try:
                id_bloco = str(modelx.get_value(iterx, self.col_a03_id_bloco))
                self.ge_a03_id_bloco = id_bloco

            except ValueError:
                self.ge_selecionado = True
                return False
            finally:
                self.ge_selecionado = True

            dic_bloco = self.consulta_bloco(id_bloco=id_bloco)

            if len(dic_bloco) != 0:
                self.mostrar_dados_tela(dic_dados_bloco=dic_bloco)
                self.ge_selecionado = True

            else:
                self.limpar_tela()

    def mostrar_dados_tv03(self, lista, res):
        """
        Coloca os dados recebidos em 'res'
        :param lista:
        :param res:lista de dicionarios com os dados do bloco para ser encaixado no treeview
        :return:
        """

        lista.clear()
        for i in res:
            lista.append([
                str(i['a03_id_condominio']),
                str(i['a03_id_bloco']),
                str(i['a03_nome_bloco']),
            ])

    def limpar_tela(self):
        """
        Limpar todos os campo para que da classe bem como as entradas da tela
        :return:
        """

        self.ge_selecionado = False
        self.ge_a03_id_bloco = 0

        self.e03_a03_nome_bloco.set_text('')

        self.e03_a03_nome_bloco.set_property("primary-icon-stock", None)

    def validar_campos(self):
        """
        Valida todos os campos
        :return:retrna um dicionario de dados com os dados validados ou retorna Falso no caso de dados inválidos
        """
        dic_dados = dict()

        valido = True
        # numerovalido = re.compile(r'[0-9]')

        dic_dados['a03_id_bloco'] = self.ge_a03_id_bloco
        dic_dados['a03_id_condominio'] = self.ge_a01_id_condominio

        if len(str(self.e03_a03_nome_bloco.get_text().strip())) == 0:
            self.e03_a03_nome_bloco.set_property("primary-icon-stock", Gtk.STOCK_DIALOG_ERROR)
            self.e03_a03_nome_bloco.grab_focus()
            valido = False
        else:
            dic_dados['a03_nome_bloco'] = str(self.e03_a03_nome_bloco.get_text().strip())
            self.e03_a03_nome_bloco.set_property("primary-icon-stock", None)

        if not valido:
            dic_dados = False

        return dic_dados

    def incluir(self, dic_dados):
        """
        Incluir novos blocos no banco de dados
        :param dic_dados: dicionario de dados validados para salvar no banco de dados
        :return: retorn Falso quando não foi possivel salvar e True quando foi ṕossivel salvar os dados
        """

        try:
            conn = psycopg2.connect(self.ge_dic_param_sis['DSN'])
            conn.set_client_encoding(self.ge_dic_param_sis['CLIENTEENCODING'])
        except psycopg2.ProgrammingError as msg:
            logging.error(msg)
            self.JP.msgerro(janela=self.w03,
                            texto_primario="Problema na rotina de Incluir",
                            # texto_primario="class:{} - def:{} - linha:{}".format(str(self.__class__.__name__),
                            #                                                      str(sys._getframe(0).f_code.co_name),
                            #                                                      str(sys._getframe(0).f_lineno)),
                            texto_secundario=msg)
            return False

        cur = conn.cursor()
        try:
            cur.execute(
                """
             INSERT INTO a03_blocos
             (
             a03_id_condominio,
             a03_nome_bloco
             ) VALUES(
             %s,
             %s
             );
             """, (
                    dic_dados['a03_id_condominio'] if "a03_id_condominio" in dic_dados else 0,
                    dic_dados['a03_nome_bloco'] if "a03_nome_bloco" in dic_dados else None,
                )
            )
        except (psycopg2.DatabaseError, psycopg2.ProgrammingError) as msg:
            logging.error(msg)
            self.JP.msgerro(janela=self.w03,
                            texto_primario='Problma ao Incluir dados novos',
                            # texto_primario="class:{} - def:{} - linha:{}".format(str(self.__class__.__name__),
                            #                                                      str(sys._getframe(0).f_code.co_name),
                            #                                                      str(sys._getframe(0).f_lineno)),
                            texto_secundario=msg)
            return False

        conn.commit()
        cur.close()

        del conn, cur
        return True

    def alterar(self, dic_dados):
        """

        :param dic_dados:
        :return:
        """
        try:
            conn = psycopg2.connect(self.ge_dic_param_sis['DSN'])
            conn.set_client_encoding(self.ge_dic_param_sis['CLIENTEENCODING'])
        except psycopg2.ProgrammingError as msg:
            logging.error(msg)
            self.JP.msgerro(janela=self.w03,
                            texto_primario='Problema ao Alterar Dados',
                            # texto_primario="class:{} - def:{} - linha:{}".format(str(self.__class__.__name__),
                            #                                                      str(sys._getframe(0).f_code.co_name),
                            #                                                      str(sys._getframe(0).f_lineno)),
                            texto_secundario=msg)
            return False

        cur = conn.cursor()
        try:
            cur.execute("""
            UPDATE  a03_blocos SET
            a03_id_condominio = %s,
            a03_nome_bloco = %s
            WHERE a03_id_bloco = %s;
            """, (
                dic_dados['a03_id_condominio'] if "a03_id_condominio" in dic_dados else '0',
                dic_dados['a03_nome_bloco'] if "a03_nome_bloco" in dic_dados else None,
                dic_dados['a03_id_bloco'] if "a03_id_bloco" in dic_dados else '0',
            )
                        )

        except psycopg2.DatabaseError as msg:
            logging.error(msg)
            self.JP.msgerro(janela=self.w03,
                            texto_primario='Problema ao Atualisar dados',
                            # texto_primario="class:{} - def:{} - linha:{}".format(str(self.__class__.__name__),
                            #                                                      str(sys._getframe(0).f_code.co_name),
                            #                                                      str(sys._getframe(0).f_lineno)),
                            texto_secundario=msg)
            return False

        conn.commit()
        cur.close()

        del conn, cur
        return True

    def consulta_bloco(self, id_bloco):

        dic_dados = {}

        try:
            conn = psycopg2.connect(self.ge_dic_param_sis['DSN'])
            conn.set_client_encoding(self.ge_dic_param_sis['CLIENTEENCODING'])

            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute(""" SELECT *
                            FROM  a03_blocos
                            WHERE a03_id_bloco = %s;
                            """, (id_bloco,)
                        )
            registros = cur.fetchall()

        except psycopg2.ProgrammingError as msg:
            logging.error(msg)
            self.JP.msgerro(janela=self.w03,
                            texto_primario='Problemas ao Carregar Blocos',
                            # texto_primario="class:{} - def:{} - linha:{}".format(str(self.__class__.__name__),
                            #                                                      str(sys._getframe(0).f_code.co_name),
                            #                                                      str(sys._getframe(0).f_lineno)),
                            texto_secundario=msg)
            return False

        for registro in registros:
            dic_dados = dict(registro)

        if not registros:
            return False

        cur.close()

        del conn, cur, registros

        return dic_dados

    def mostrar_dados_tela(self, dic_dados_bloco):

        for key, value in dic_dados_bloco.items():
            if key == 'a03_nome_bloco':
                if value is not None:
                    self.e03_a03_nome_bloco.set_text(str(value))
                else:
                    self.e03_a03_nome_bloco.set_text('')
