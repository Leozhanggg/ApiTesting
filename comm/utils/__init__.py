import os
from comm.utils.readYaml import read_yaml_data


def get_case(file_path):
    case_yaml = file_path.replace('\\', '/').replace('/testcase/', '/page/').replace('.py', '.yaml')
    case_path = os.path.dirname(case_yaml)
    case_data = read_yaml_data(case_yaml)
    return case_path, case_data
