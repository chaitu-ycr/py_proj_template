from py_proj_template.main import MyPackage


def test_importing():
    pkg_instance = MyPackage()
    assert pkg_instance.say_hello()
