import importlib
import importlib.util
import inspect
import os
import xml.etree.ElementTree as ElementTree

from builtinsteps import Echo
from step import Step

DOT_PY = ".py"


def get_python_files(src):
    cwd = os.getcwd()
    py_files = []
    for root_dir, dirs, files in os.walk(src):
        for file in files:
            if file.endswith(".py"):
                py_files.append(os.path.join(cwd, root_dir, file))
    return py_files


def dynamic_import(module_name_to_import, py_path):
    module_spec = importlib.util.spec_from_file_location(module_name_to_import, py_path)
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module


def dynamic_import_from_src(src, star_import=False):
    my_py_files = get_python_files(src)
    for py_file in my_py_files:
        module_name = os.path.split(py_file)[-1].strip(".py")
        imported_module = dynamic_import(module_name, py_file)
        if star_import:
            for obj in dir(imported_module):
                globals()[obj] = imported_module.__dict__[obj]
        else:
            globals()[module_name] = imported_module
    return


step_definition_mapping = {
    'undefined': Step,
    'echo': Echo,
}


def init_step_definitions(step_def_directories):
    for step_def_directory in step_def_directories:
        # Search for python modules in step definitions folder
        step_definition_module_python_files = get_python_files(step_def_directory)

        # Scan for each python module if it has step definitions, add them to step definition mapping
        for py_file in step_definition_module_python_files:
            module_name = os.path.split(py_file)[-1].strip(DOT_PY)
            imported_step_def_module = dynamic_import(module_name, py_file)
            for importedObjectName in dir(imported_step_def_module):
                imported_object = imported_step_def_module.__dict__[importedObjectName]
                if inspect.isclass(imported_object):
                    if issubclass(imported_object, Step):
                        if imported_object.tag and (imported_object.tag not in step_definition_mapping):
                            print("Found step class: ", str(imported_object))
                            step_definition_mapping[imported_object.tag] = imported_object


print(step_definition_mapping)


def get_step(element):
    if element.tag in step_definition_mapping:
        step_type = step_definition_mapping[element.tag]
        step_object = step_type(element.attrib, element.text)
    else:
        step_object = Step(element.attrib, element.text)
    for child in element:
        step_object.add_steps(get_step(child))
    return step_object


def execute_file(file):
    tree = ElementTree.parse(file)
    steps = get_step(tree.getroot())

    for step in steps.steps:
        step.execute()


execute_file('app.xml')
