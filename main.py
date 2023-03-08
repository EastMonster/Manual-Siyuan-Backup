import os
import sys
from util import *

config = {"workspace_path": "", "backup_path": ""}


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

    if option == 1:
        set_config(config, 1)
    elif option == 2:
        set_config(config, 2)
    elif option == 3:
        os.remove("config.json")
    elif option == 0:
        return
    else:
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

    if params[1] == "backup":
        zipdir(config["workspace_path"], config["backup_path"])
    elif params[1] == "config":
        do_config()
    elif params[1] == "restore":
        restore()
    else:
        print_usage()


if __name__ == '__main__':
    main()
