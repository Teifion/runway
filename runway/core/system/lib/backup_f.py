from datetime import date, datetime, timedelta
from . import site_settings_f
import transaction
import os

def perform_backup(config):
    """Backs up the database"""
    print("1")
    
    file_path = "{}/{}/{}.db_backup".format(
        config["backup_path"],
        config["name"],
        datetime.today().strftime("%Y-%m-%d"),
    )
    
    print("2")
    
    args = "--username={user} {db}".format(
        user = config["db_username"],
        db   = config["db_name"]
    )
    
    print("3")
    
    # Perform actual backup
    os.system("/usr/bin/pg_dump --file={} {}".format(file_path, args))
    
    print("/usr/bin/pg_dump --file={} {}".format(file_path, args))
    
    print("4")
    
    # Now try to delete the backup from exactly 15 days ago
    exact_delete_dt = datetime.today() - timedelta(days=15)
    
    print("5")
    
    del_path = "{}/{}".format(
        config["backup_path"],
        config["name"],
    )
    del_file = exact_delete_dt.strftime("%Y-%m-%d")
    
    print("6")
    
    os.system("find {} -type f -name '{}.db_backup' -exec rm {{}} \;".format(del_path, del_file))
    
    with transaction.manager:
        site_settings_f.set_setting("runway.latest_backup", file_path)
    
    print("7")
    
    os.system("rm {};".format("/tmp/temp_duplicate.sql"))
    os.system("cp {} {};".format(file_path, "/tmp/temp_duplicate.sql"))
    
    print("8")
    
    return file_path

def restore(file_path):
    pass
