from ..lib import cron_f

def cron():
    """
    () -> IO ()
    Run the cron jobs on the system. Usually this will be called automatically by the OS if setup on crontab.
    """
    cron_f.background_process()
    
    return "Cron process performed"
