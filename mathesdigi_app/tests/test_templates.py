import os
import re

from bs4 import BeautifulSoup


def get_heft_template_dict():
    heft_template_dict = {}
    templates_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates', 'mathesdigi_app')
    for dirpath, dirnames, filenames in os.walk(templates_dir):
        for heft in dirnames:
            template_list = []
            for dirpath, dirnames, templates in os.walk(os.path.join(dirpath, heft)):
                template_list = [template for template in templates]
            heft_template_dict.update({heft: template_list})
    return templates_dir, heft_template_dict


def get_existing_sub_task_id(templates_dir, heft, template):
    template_path = os.path.join(templates_dir, heft, template)
    with open(template_path) as fp:
        soup = BeautifulSoup(fp, 'html.parser')
    existing_sub_task_id_list = [field.get('name') for field in soup.find_all(['input', 'textarea'])
                                 if re.match(r"^\d\w\d\w$", str(field.get('name')))]
    if not existing_sub_task_id_list or len(existing_sub_task_id_list) > 1:
        return None
    else:
        return existing_sub_task_id_list[0]


def test_template_task_id():
    templates_dir, heft_template_dict = get_heft_template_dict()
    for heft, template_list in heft_template_dict.items():
        for template in template_list:
            sub_heft = "A"
            task = None
            sub_task = None
            sub_task_id = f"{heft}{sub_heft}{task}{sub_task}"
            existing_sub_task_id = get_existing_sub_task_id(templates_dir, heft, template)

            print(heft, template, existing_sub_task_id)
    assert False


def test_template_links():
    pass
