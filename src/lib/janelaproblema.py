from gi.repository import Gtk
# from gi.overrides import Gtk


class JanelaProblema:

    def __init__(self):
        pass

    def msginformativo(self, janela=None, texto_primario='', texto_secundario=''):
        dialog = Gtk.MessageDialog(janela, Gtk.DialogFlags.MODAL,
                                   Gtk.MessageType.INFO,
                                   Gtk.ButtonsType.OK,
                                   texto_primario)
        dialog.format_secondary_text(texto_secundario)
        dialog.run()
        dialog.destroy()

    def msgerro(self, janela=None, texto_primario='', texto_secundario=''):
        dialog = Gtk.MessageDialog(janela, Gtk.DialogFlags.MODAL,
                                   Gtk.MessageType.ERROR,
                                   Gtk.ButtonsType.CANCEL,
                                   str(texto_primario))
        dialog.format_secondary_text(str(texto_secundario))
        dialog.run()
        dialog.destroy()

    def msgwarning(self, janela=None, texto_primario='', texto_secundario=''):
        dialog = Gtk.MessageDialog(janela, Gtk.DialogFlags.MODAL,
                                   Gtk.MessageType.WARNING,
                                   Gtk.ButtonsType.OK_CANCEL,
                                   str(texto_primario))
        dialog.format_secondary_text(texto_secundario)
        response = dialog.run()
        dialog.destroy()
        if response == Gtk.ResponseType.OK:
            return True
        elif response == Gtk.ResponseType.CANCEL:
            return False

    def msgquestion(self, janela=None, texto_primario='', texto_secundario=''):
        dialog = Gtk.MessageDialog(janela, Gtk.DialogFlags.MODAL,
                                   Gtk.MessageType.QUESTION,
                                   Gtk.ButtonsType.YES_NO,
                                   str(texto_primario))
        dialog.format_secondary_text(texto_secundario)
        response = dialog.run()
        dialog.destroy()
        if response == Gtk.ResponseType.YES:
            return True
        elif response == Gtk.ResponseType.NO:
            return False
