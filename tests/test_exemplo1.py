import  unittest
from os.path import abspath, dirname

import gi
from src.lib.parametros import Parametros
from gi.repository import Gtk
# from src.menuprinc import MenuPrinc

try:
    from src.lib.parametros import Parametros
except Exception as prob:
    print(prob)
    exit(1)

# def refresh_gui():
#     while Gtk.events_pending():
#         Gtk.main_iteration_do(block=False)


class TestMenuPrinc(unittest.TestCase):

    def setUp(self):

        self.caminho_src = abspath(dirname(__file__))

        self.Pr = Parametros()


    def test_carrega_parametros(self):

        self.assertTrue(self.Pr.carrega_parametros())



    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    # def tearDown(self):
    #     self.widget.dispose()





    def test_numbers_3_4(self):
        self.assertEqual(3 * 4, 12)


if __name__ == '__main__':
    unittest.main()

# import unittest
#
# class TestStringMethods(unittest.TestCase):
#
#     def test_upper(self):
#         self.assertEqual('foo'.upper(), 'FOO')
#
#     def test_isupper(self):
#         self.assertTrue('FOO'.isupper())
#         self.assertFalse('Foo'.isupper())
#
#     def test_split(self):
#         s = 'hello world'
#         self.assertEqual(s.split(), ['hello', 'world'])
#         # check that s.split fails when the separator is not a string
#         with self.assertRaises(TypeError):
#             s.split(2)
#
# if __name__ == '__main__':
#     unittest.main()