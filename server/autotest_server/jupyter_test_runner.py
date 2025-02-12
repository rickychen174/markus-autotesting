import os
from typing import Dict, List
import pytest
import nbformat
import tempfile
from notebook_helper import merger
from testers.jupyter.lib.jupyter_pytest_plugin import JupyterPlugin


def merge_ipynb_files(test_file: str, submission_file: str):
    tempf = tempfile.NamedTemporaryFile(dir=os.getcwd(), mode="w", delete=False, suffix=".ipynb")
    new_notebook = merger.merge(test_file, submission_file)
    nbformat.write(new_notebook, tempf)
    tempf.close()
    return tempf.name


def run_jupyter_tests(test_file: str) -> List[Dict]:
    plugin = JupyterPlugin()
    pytest.main([test_file], plugins=["notebook_helper.pytest.notebook_collector_plugin", plugin])
    # os.unlink(test_file)


run_jupyter_tests(merge_ipynb_files("Homework_5_test_patched.ipynb", "Homework_5_submission_patched.ipynb"))
