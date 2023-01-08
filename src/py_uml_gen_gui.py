"""Python 🐍 UML diagrams generator GUI"""

__version__ = "0.0.1"

# Import Python Libraries here
import os
import sys
import subprocess
import threading
import logging
from logging import handlers
import PySimpleGUI as Sg


class PyUmlGenGui:
    r"""The PyUmlGenGui class represents python UML diagrams generator.
    """

    def __init__(self) -> None:
        self.gui_main_window = None
        self.pylance_thread_run_status = False
        self.log = logging.getLogger('PY_UML_GEN_GUI_LOG')
        self.__py_uml_gen_gui_log_initialisation()
        self.__pylance_cmd_template = 'pylance __PACKAGE_NAME__ __OPTIONS__ --colorized -o __OUTPUT_FORMAT__ -d __OUTPUT_DIRECTORY__'
        self.__final_command = None

    def gui(self):
        gui_title = 'Python UML diagrams generator GUI'
        Sg.theme('LightGreen')
        layout = [
            [Sg.HorizontalSeparator(color='green')],
            [Sg.Text("input list of python files / modules. separate inputs with semicolon(;)", text_color='dark blue')],
            [Sg.Text("donot give spaces after semicolon(;)", text_color='dark blue')],
            [Sg.Multiline(key='__ML_INPUT__', expand_x=True, size=(64, 2))],
            [Sg.HorizontalSeparator(color='green')],
            [[Sg.Text("select / adjust options according to your need ", text_color='dark blue')],
             [Sg.Checkbox('-a', key='__CB_ANCESTOR__', default=True,
                          tooltip='show <ancestor> generations of ancestor classes not in <projects>'),
              Sg.Combo(values=[0, 1, 2, 3, 4, 5], default_value=0, key='__C_ANCESTOR__', size=(2, 1)),
              Sg.Checkbox('-s', key='__CB_ASSOCIATION_LEVEL__', default=True,
                          tooltip='show <association_level> levels of associated classes not in <projects>'),
              Sg.Combo(values=[0, 1, 2, 3, 4, 5], default_value=0, key='__C_ASSOCIATION_LEVEL__', size=(2, 1)),
              Sg.Checkbox('-my', key='__CB_MY__', default=True,
                          tooltip='include module name in representation of classes. This will include the full module path in the class name'),
              Sg.Checkbox('-b', key='__CB_BUILTIN_OBJECTS__', default=True,
                          tooltip='include builtin objects in representation of classes'),
              Sg.Checkbox('--colorized', key='__CB_COLORISED__', default=True,
                          tooltip='Use colored output. Classes/modules of the same package get the same color.')]],
            [Sg.HorizontalSeparator(color='green')],
            [[Sg.Text("select output format --> ", text_color='dark blue'),
              Sg.Combo(values=['dot', 'html', 'pdf', 'bmp', 'gif', 'jpg', 'json', 'png'], default_value='html', key='__C_OUTPUT_FORMAT__',
                       enable_events=True, size=(6, 1))],
             [Sg.Text("select output directory --> ", text_color='dark blue'),
              Sg.FolderBrowse('BROWSE', target=(Sg.ThisRow, 2)), Sg.Input(r'D:\.py_logs', key='__OUTPUT_DIR__', expand_x=True)],
             [Sg.Text("set project name --> ", text_color='dark blue'),
              Sg.Input('project_name', key='__CB_PROJECT__', size=(20, 1))]],
            [Sg.HorizontalSeparator(color='green')],
            [Sg.Button('GENERATE', size=(10, 1), tooltip='click to generate diagram'),
             Sg.Text("status -->", text_color='green'),
             Sg.Text("Not Yet Generated", key='__STATUS__', text_color='green')]
        ]
        self.gui_main_window = Sg.Window(gui_title, layout, size=(720, 350), font=('Consolas', 12, 'bold'))

        # --------------------- EVENT LOOP ---------------------
        while True:
            event, values = self.gui_main_window.read(timeout=100)
            if event in (Sg.WIN_CLOSED, 'Exit'):
                break
            if event == 'GENERATE':
                inputs = values['__ML_INPUT__'].replace('; ', ';').replace('\n', ';').replace(';;', ';').replace(';', ' ')
                ancestor = f"-a{values['__C_ANCESTOR__']}" if values['__CB_ANCESTOR__'] else ''
                association_level = f"-s{values['__C_ASSOCIATION_LEVEL__']}" if values['__CB_ASSOCIATION_LEVEL__'] else ''
                include_module = f"-my" if values['__CB_MY__'] else ''
                builtin_objects = f"-b" if values['__CB_BUILTIN_OBJECTS__'] else ''
                colorised = f"--colorized" if values['__CB_COLORISED__'] else ''
                output_format = f"-o {values['__C_OUTPUT_FORMAT__']}"
                project_name = f"-p {values['__CB_PROJECT__']}"
                output_dir = f"-d {values['__OUTPUT_DIR__']}"
                if inputs == '':
                    self.log.warning("generation not possible without input modules...")
                    self.gui_main_window['__STATUS__'].update(f"generation not possible without input modules...")
                else:
                    self.__final_command = f"pyreverse {inputs} {ancestor} {association_level} {include_module} {builtin_objects} {colorised} {output_format} {project_name} {output_dir}"
                    thread_obj = threading.Thread(target=self.pylance_thread, daemon=True)
                    thread_obj.start()

    def pylance_thread(self):
        exec_cmd = self.__final_command
        self.pylance_thread_run_status = True
        try:
            self.log.info("Started generation")
            self.gui_main_window['__STATUS__'].update("Started generation")
            self.gui_main_window['GENERATE'].update(disabled=True)
            self.gui_main_window['__STATUS__'].update("generation inprogress ...")
            process = subprocess.run(exec_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            if process.returncode == 0:
                self.log.info(process.stdout)
                self.log.info("Completed generation")
                self.gui_main_window['__STATUS__'].update("Completed generation")
            else:
                self.log.info(process.stdout)
                self.log.warning("Failed generation")
                self.gui_main_window['__STATUS__'].update("Failed generation")
        except Exception as msg:
            self.log.warning(f"Failed to generate due to {msg}")
            self.gui_main_window['__STATUS__'].update(f"Failed to generate due to {msg}")
        self.pylance_thread_run_status = False
        self.gui_main_window['GENERATE'].update(disabled=False)

    def __py_uml_gen_gui_log_initialisation(self):
        py_uml_gen_gui_log_dir = r'D:\.py_logs'
        if not os.path.exists(py_uml_gen_gui_log_dir):
            os.mkdir(py_uml_gen_gui_log_dir)
        self.log.setLevel(logging.DEBUG)
        log_format = logging.Formatter("%(asctime)s [PY_UML_GEN_GUI_LOG] [%(levelname)s]  %(message)s")
        ch = logging.StreamHandler(sys.stdout)
        ch.setFormatter(log_format)
        self.log.addHandler(ch)
        fh = handlers.RotatingFileHandler(fr'{py_uml_gen_gui_log_dir}\py_uml_gen_gui.log', maxBytes=(1048576 * 5), backupCount=7)
        fh.setFormatter(log_format)
        self.log.addHandler(fh)


if __name__ == '__main__':
    app_obj = PyUmlGenGui()
    app_obj.gui()
