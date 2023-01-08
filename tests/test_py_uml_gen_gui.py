import os
import sys

file_path = os.path.dirname(os.path.abspath(__file__)).replace('/', '\\')
root_path = '\\'.join(file_path.split('\\')[:-1])
sys.path.extend([file_path, fr'{root_path}\src'])

from py_uml_gen_gui import PyUmlGenGui
app_obj = PyUmlGenGui()


def test_check_convertion():
    print("hello !")
