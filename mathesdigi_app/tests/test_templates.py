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
            match = re.match(r"(?P<task>^\d)_task_(?P<sub_task>\w).html$", template)
            if "task" in template and match:
                heft_nr = heft[heft.rfind(r"\d")]
                sub_heft = "A"
                task = match.group("task")
                sub_task = match.group("sub_task")
                actual_sub_task_id = f"{heft_nr}{sub_heft}{task}{sub_task}"
                existing_sub_task_id = get_existing_sub_task_id(templates_dir, heft, template)

                assert actual_sub_task_id == existing_sub_task_id


def test_template_links():
    templates_dir, heft_template_dict = get_heft_template_dict()
    for heft, template_list in heft_template_dict.items():
        template_list.sort()
        for index in range(1, len(template_list) - 1):
            current_template = template_list[index]
            next_template = template_list[index+1].strip(".html")
            previous_template = template_list[index-1].strip(".html")

            template_path = os.path.join(templates_dir, heft, current_template)
            with open(template_path) as fp:
                soup_string = str(BeautifulSoup(fp, 'html.parser'))

            is_next_url = f"'{next_template}' as forward_url" in soup_string
            is_previous_url = f"'{previous_template}' as backward_url" in soup_string

            assert is_next_url
            assert is_previous_url


def test_this_task_proccess():
    pass
