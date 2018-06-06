

class ComboBoxDados:
    def __init__(self, *arg, **kwarg):
        pass

    def get_dado_combo(self, comboboxm,  col_traz):
        """
        Pegar o texto ativo no combobox corrente
        """
        model = comboboxm.get_model()
        active = comboboxm.get_active_iter()
        if active:
            # self.GeCorFundo =  model[active][self.COL_CB05_T07_DESC]
            return model[active][col_traz]
        return None

    def set_dado_combo(self, comboboxm, text, coluna):
        """
        setar um texto  para um combobox
        """
        model = comboboxm.get_model()
        active = 0
        while True:
            if str(model[active][coluna]) == str(text):
                comboboxm.set_active(active)
                break
            active += 1
