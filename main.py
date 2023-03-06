# Manual-Siyuan-Backup, 0.1.0

import sys
import os
import psutil
from util import *

config = {
    "workspace_path": "",
    "backup_path": ""
}

def check() -> bool:
    if not check_env():
        return False

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

    if not os.path.exists("config.json"):
        print("Configure related paths (Please use slash '/'):")
        print("Workspace path: ", end="")
        config["workspace_path"] = input()
        print("Backup path: ", end="")
        config["backup_path"] = input()

        if not os.path.exists(config["workspace_path"]):
            error("Invalid workspace path")
            exit(3)

        os.makedirs(config["backup_path"], exist_ok=True)

        save_config(config)

    return True

def main():
    params = sys.argv

    if (len(params) < 2):
        print_usage()
        exit(0)

    if not check():
        exit(1)

    config = load_config()
    if config is None:
        exit(0)

    match params[1]:
        case "backup":
            zipdir(config["workspace_path"], config["backup_path"])
        case "check":
            check()
        case "config":
            NotImplemented
        case "restore":
            NotImplemented
        case default:
            print_usage()

if __name__ == '__main__':
    main()
