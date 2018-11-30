from src.menuprinc import MenuPrinc


class Condominio:
    def __init__(self):
        self.MP = MenuPrinc()
        self.podeentrar = True
        # self.lg = Login()
        # self.podeentrar = self.lg.podeentrar

        if self.podeentrar:
            # self.lg.a02.destroy()
            MenuPrinc()
        else:
            print(' -----', str(self.podeentrar), '-------')
            exit(1)


if __name__ == '__main__':
    Condominio()
