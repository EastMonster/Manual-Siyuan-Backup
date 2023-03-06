import json
import os
import platform
import sys
import time
import zipfile

RED = "\033[31m"
YELLOW = "\033[33m]"
RESET = "\033[0m"

USAGE = """Manual-Siyuan-Backup 0.1.0
usage: python main.py <command>

These are available commands:
    backup  b
    check   b
    config  View and configure related paths
    restore b
"""


def print_usage() -> None:
    print(USAGE, end="")


def warn(hint: str) -> None:
    print(
        str.format("{YELLOW}Warning: {RESET}{hint}.",
                   YELLOW=YELLOW,
                   RESET=RESET,
                   hint=hint))


def error(hint: str) -> None:
    print(
        str.format("{RED}Error: {RESET}{hint}.",
                   RED=RED,
                   RESET=RESET,
                   hint=hint))

def check_env() -> bool:
    py_ver = platform.python_version_tuple()
    if sys.platform != "win32":  # I don't use Linux or MacOS...
        error("This script can only be run on Windows")
    if int(py_ver[0] == 2) or (int(py_ver[0]) == 3 and int(py_ver[1]) < 10):  # I like newer things!
        error("This script requires Python interpreter 3.10 or higher")
        return False
    return True

def save_config(config: dict) -> None:
    try:
        with open("config.json", "w") as f:
            f.write(json.dumps(config, indent=4))
    except Exception as what:
        error("Panicked. %s" % what)


def load_config() -> dict[str, str] | None:
    try:
        with open("config.json", "r") as f:
            config = json.loads(f.read())

            if not os.path.exists(config["workspace_path"]):
                error("Invalid workspace path")
                exit(3)

            return config

    except Exception as what:
        error("Panicked. %s" % what)

    return None

def zipdir(wpath: str, bpath: str) -> None:
    zipf_name = str.format("{}\\syb_{}.zip", bpath, time.strftime("%Y%m%d%H%M%S", time.localtime()))
    zipf = zipfile.ZipFile(zipf_name, "w", zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(wpath + "\\data"):
        for file in files:
            abs_path = os.path.join(root, file)
            zipf.write(abs_path, arcname=os.path.relpath(abs_path, wpath))
    zipf.close()
