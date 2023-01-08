import os
import sys

file_path = os.path.dirname(os.path.abspath(__file__)).replace('/', '\\')
root_path = '\\'.join(file_path.split('\\')[:-1])
sys.path.extend([file_path, fr'{root_path}\src'])


def test_tc1():
    from py_module import YourClass
    app_obj = YourClass()
    assert app_obj.demo_method()
