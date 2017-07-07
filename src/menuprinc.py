import logging
import traceback

__author__ = 'John Evan Dizaro'

try:
    import gi
    gi.require_version('Gtk', '3.0')
except Exception as msg:
    print(msg)
    exit(1)

try:
    from gi.repository import Gtk
    # from gi.repository import GLib, GObject, Gio, Pango, GdkPixbuf, Gtk, Gdk, GtkSource
    # import gi.repository
    # from gi.overrides.Gtk import Gtk
except Exception as problema:
    print(problema)
    exit(1)

try:
    import sys
except Exception as problema:
    print(problema)
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

try:
    from src.cadcondominio import CadCondominio
except Exception as problema:
    print(problema)
    exit(1)

try:
    from src.cadportaria import CadPortaria
except Exception as problema:
    print(problema)
    exit(1)

try:
    from src.cadbloco import CadBloco
except Exception as problema:
    print(problema)
    exit(1)

try:
    from src.lib.parametros import Parametros
except Exception as problema:
    print(problema)
    exit(1)

try:
    from src.lib.logsistema import LogSistema
except Exception as problema:
    print(problema)
    exit(1)


class MenuPrinc:
    def __init__(self, **kwarg):
        """
        inicialisacao dos campos do menu
        """

        self.JP = JanelaProblema()

        self.ge_dic_param_sis = dict()
        self.Pr = Parametros()
        self.ge_dic_param_sis = self.Pr.carrega_parametros()

        if not self.ge_dic_param_sis:
            problema = 'Dicionario de parametros vazio ou não localizado'
            logging.error(problema)
            self.JP.msgerro(janela=None,
                            texto_primario="Parametros",
                            texto_secundario=problema)
            exit(1)

        try:
            self.lg = LogSistema(dic_param_sis=self.ge_dic_param_sis)
        except IOError as problema:
            logging.error(problema)
            self.JP.msgerro(janela=None,
                            texto_primario="Log",
                            texto_secundario=problema)
            exit(1)




        self.caminho_src = abspath(dirname(__file__))

        self.builder = Gtk.Builder()

        try:
            self.caminho_tela = '/'.join([self.caminho_src, 'glade', 'menu-principal.glade'])
            self.builder.add_objects_from_file(self.caminho_tela, ["w00_principal"])
        except Exception as problema:
            logging.error(problema)
            self.JP.msgerro(janela=None,
                            texto_primario="Telas do sistema",
                            texto_secundario=problema)
            exit(1)



        self.builder.connect_signals(self)
        self.w00 = self.builder.get_object("w00_principal")
        # self.w00.set_title("Controle de Solicitação de Taxi")
        # self.w00.maximize()
        self.w00.set_visible(True)
        self.w00.show_all()

        Gtk.main()

    def on_mnu_cad_condominio_activate(self, widget):

        titulo = widget.get_label().strip('_')

        CadCondominio(dic_param_sis=self.ge_dic_param_sis, titulo=titulo)

    def on_mnu_cad_portaria_activate(self, widget):

        CadPortaria(dic_param_sis=self.ge_dic_param_sis)

    def on_mnu_cad_bloco_activate(self, widget):

        titulo = widget.get_label().strip('_')
        CadBloco(dic_param_sis=self.ge_dic_param_sis, titulo= titulo)

    def on_w00_principal_delete_event(self, widget):
        Gtk.main_quit()

    def on_w00_principal_destroy(self, widget):
        Gtk.main_quit()

    def on_w00_principal_destroy_event(self, widget):
        Gtk.main_quit()


if __name__ == "__main__":
    MenuPrinc()
