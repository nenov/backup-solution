# Backup solution

This is a small solution which synchronizes two folders: source and replica. The
program maintains a full, identical copy of source folder at replica folder. Support repetative execution and logging.

## Arguments

Source - Root location to be backed up

Replica - Destination folder for the backup

Log File - File for logging

Interval [optional] - How often the script should be executed. Allowed interval: [number]s/m/h/d


## Usage

```python
...\backup-solution>python main.py "C:\Users\***\Desktop\Backup" "C:\Users\***\Desktop\Replica" "C:\Users\***\Desktop\Log.txt" 10s
Starting synchronization ...
No changes found.
Synchronization finished. Next run in 10s.
...
```