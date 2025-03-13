import os
import shutil
import json
import subprocess

PYTA_VERSION_PREFIX = "python-ta=="
PYTA_VERSION = "2.7.0"


def create_environment(settings_, env_dir, _default_env_dir):
    env_data = settings_.get("env_data", {})
    python_version = env_data.get("python_version", "3")
    env_properties = ["wheel"] + env_data.get("pip_requirements", "").split()
    pyta_version = env_data.get("pyta_version", PYTA_VERSION)
    pyta_version = PYTA_VERSION_PREFIX + pyta_version
    env_properties.append(pyta_version)
    requirements = os.path.join(os.path.dirname(os.path.realpath(__file__)), "requirements.txt")
    pip = os.path.join(env_dir, "bin", "pip")
    subprocess.run(
        [f"python{python_version}", "-m", "venv", "--clear", env_dir], check=True, text=True, capture_output=True
    )
    pip_install_command = [pip, "install", "-r", requirements, *env_properties]
    if env_data.get("pip_requirements_file"):
        pip_install_command.append("-r")
        pip_install_command.append(os.path.join(env_dir, "../", "files", env_data.get("pip_requirements_file")))
    subprocess.run(pip_install_command, check=True, text=True, capture_output=True)
    return {"PYTHON": os.path.join(env_dir, "bin", "python3")}


def settings():
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "settings_schema.json")) as f:
        settings_ = json.load(f)
    py_versions = [f"3.{x}" for x in range(11, 14) if shutil.which(f"python3.{x}")]
    python_versions = settings_["properties"]["env_data"]["properties"]["python_version"]
    python_versions["enum"] = py_versions
    python_versions["default"] = py_versions[-1]
    pyta_version = settings_["properties"]["env_data"]["properties"]["pyta_version"]
    pyta_version["default"] = PYTA_VERSION
    return settings_


def install():
    """no op"""
