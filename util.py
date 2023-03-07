import shutil
import json
import os
import platform
import psutil
import sys
import time
import zipfile

RED = "\033[31m"
YELLOW = "\033[33m"
RESET = "\033[0m"

USAGE = """Manual-Siyuan-Backup 0.1.0
usage: python main.py <command>

These are available commands:
    backup  Generate a backup
    config  Configure related paths
    restore Restore the latest backup to your workspace
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


def ask(hint: str) -> bool:
    while True:
        print("%s [y/n] " % hint, end="")
        res = input().strip().lower()

        if len(res) != 1 or (res != "y" and res != "n"):
            error("Invalid input")
            break
        else:
            return True if res == "y" else False
    return False


def save_config(config: dict) -> None:
    try:
        with open("config.json", "w") as f:
            f.write(json.dumps(config, indent=4))
    except Exception as what:
        error("Panicked. %s" % what)


def load_config() -> dict[str, str]:
    try:
        with open("config.json", "r") as f:
            config: dict = json.loads(f.read())
            keys = config.keys()

            if len(
                    keys
            ) != 2 or "workspace_path" not in keys or "backup_path" not in keys:
                error("Invalid configuration file.")
                os.remove("config.json")
                exit(0)

            return config

    except Exception as what:
        error("Panicked. %s" % what)

    return {"workspace_path": "", "backup_path": ""}


def set_config(config: dict, type: int) -> None:
    with open("config.json"):
        npath = ""
        print("Input the new path: ", end="")
        npath = input()

        if type == 1:  # workspace path
            if not os.path.exists(npath):
                error("Invalid workspace path")
                exit(0)
            config["workspace_path"] = npath
        else:
            if not os.path.exists(npath):
                warn("Backup path doesn't exist. Folder created")
                os.makedirs(npath)
            config["backup_path"] = npath

        save_config(config)

def check_env() -> bool:
    py_ver = platform.python_version_tuple()
    if sys.platform != "win32":  # I don't use Linux or MacOS...
        error("This script can only be run on Windows")
    if int(py_ver[0] == 2) or (int(py_ver[0]) == 3 and
                               int(py_ver[1]) < 10):  # I like newer things!
        error("This script requires Python interpreter 3.10 or higher")
        return False
    return True


def check_siyuan() -> bool:
    siyuan_path: str = os.getenv(
        "LOCALAPPDATA") + "\\Programs\\SiYuan\\SiYuan.exe"  # type: ignore
    if not os.path.exists(siyuan_path):
        error("Siyuan is not detected")
        return False

    pids = psutil.process_iter()
    for pid in pids:
        if (pid.name() == "SiYuan.exe" or pid.name() == "SiYuan-Kernel.exe"):
            error("Siyuan is running")
            return False
    return True


def check_path(config: dict) -> bool:
    if not os.path.exists("config.json"):
        print("Configure related paths (Please use slash '/'):")
        print("Workspace path: ", end="")
        config["workspace_path"] = input()
        print("Backup path: ", end="")
        config["backup_path"] = input()

        save_config(config)

    if not os.path.exists(config["workspace_path"]):
        error("Invalid workspace path")
        return False

    if not os.path.exists(config["backup_path"]):
        warn("Backup path doesn't exist. Folder created")
        os.makedirs(config["backup_path"])

    return True


def rremove(path: str) -> None:
    try:
        for root, dirs, files in os.walk(path):
            for file in files:
                os.remove(os.path.join(root, file))
            for dir in dirs:
                shutil.rmtree(root + "\\" + dir)
    except Exception as what:
        error("Panicked. %s" % what)


def zipdir(wpath: str, bpath: str) -> None:
    zipf_name = str.format("{}\\syb_{}.zip", bpath,
                           time.strftime("%Y%m%d%H%M%S", time.localtime()))
    zipf = zipfile.ZipFile(zipf_name, "w", zipfile.ZIP_DEFLATED)

    _wpath = wpath + "\\data"
    for root, dirs, files in os.walk(_wpath):
        if len(dirs) == 0 and len(files) == 0:  # for empty folder
            zipf.write(root, arcname=os.path.relpath(root, _wpath))
        for file in files:
            abs_path = os.path.join(root, file)
            zipf.write(abs_path, arcname=os.path.relpath(abs_path, _wpath))
    zipf.close()


def unzip(wpath: str, bpath: str) -> None:
    flist = [
        os.path.join(bpath, file) for file in os.listdir(bpath)
        if os.path.isfile(bpath + "\\" + file)
    ]
    flist = sorted(flist, key=lambda x: os.path.getctime(x), reverse=True)

    print("%d backups detected: " % len(flist))
    for i, f in enumerate(flist):
        print("  %d\t%s" % (i + 1, f.split(os.sep)[-1]))
    print("Input the index that will be used to restore: ", end="")

    index = 0
    target = ""
    try:
        index = int(input())
        target = flist[index - 1]
    except IndexError:
        error("Invalid index")
        exit(0)

    _wpath = wpath + "\\data"
    try:
        with zipfile.ZipFile(target, "r", zipfile.ZIP_DEFLATED) as zipf:
            zipf.extractall(_wpath)
    except Exception as what:
        error("Panicked. %s" % what)
