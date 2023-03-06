## Manual-Siyuan-Backup
A simple script to backup notes in [Siyuan](https://github.com/siyuan-note/siyuan) manually.

*I backup them all to my OneDrive😋*
### Usage
At first use, configuration is required. Input the path of your Siyuan workspace and the path where you want to store all the backups.

Since then, just type `python main.py backup` to generate a backup zip file.

To import your backup to Siyuan, type `python main.py restore`. You should keep in mind that it will DELETE all the files in `yourWorkspace\data` and copy backup data into it.

### License
MIT