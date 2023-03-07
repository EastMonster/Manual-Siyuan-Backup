import sys
import os
from util import *

config = {
    "workspace_path": "",
    "backup_path": ""
}

def check() -> bool:
    return check_env() and check_siyuan() and check_path(config)

def do_config() -> None:
    print("Current config: ")
    for k, v in config.items():
        print("    %s: %s" % (k, v))

    print("Available options: ")
    print("""    1. Change workspace path
    2. Change backup path
    3. Delete config.json
    0. Do nothing""")
    print("Would you like to...[1/2/3/0]: ", end="")

    option = 0
    try:
        option = int(input())
    except ValueError:
        error("Invalid option")
        exit(0)

    match option:
        case 1:
            set_config(config, 1)
        case 2:
            set_config(config, 2)
        case 3:
            os.remove("config.json")
        case 0:
            return
        case default:
            error("Invalid option")
            exit(0)

def restore() -> None:
    if ask("This will DELETE all files in your current workspace. Continue?") is True:
        root = config["workspace_path"] + "\\data"
        rremove(root)
        unzip(config["workspace_path"], config["backup_path"])

def main():
    params = sys.argv
    global config

    if (len(params) < 2):
        print_usage()
        exit(0)

    config = load_config()

    if not check():
        exit(0)

    match params[1]:
        case "backup":
            zipdir(config["workspace_path"], config["backup_path"])
        case "config":
            do_config()
        case "restore":
            restore()
        case default:
            print_usage()

if __name__ == '__main__':
    main()
