from sqlalchemy import (
    Column,
    Boolean,
    Integer,
    Float,
    String,
    Text,
    DateTime,
    ForeignKey,
)

from sqlalchemy.dialects.postgresql import ARRAY
from ...core.base import Base

class CronJob(Base):
    __tablename__ = 'runway_cron_jobs'
    id            = Column(Integer, primary_key=True)
    
    owner         = Column(Integer, ForeignKey("runway_users.id"), nullable=False, index=True)
    
    label         = Column(String, nullable=False)
    job           = Column(String, nullable=False)
    
    # Set to null when job is disabled/paused
    next_run      = Column(DateTime, nullable=True)
    last_run      = Column(DateTime, nullable=True)
    
    # Schedule is passed to human time, schedule_start means we can combine multiple times without it causing an issue
    schedule       = Column(String, nullable=False)
    schedule_start = Column(DateTime, nullable=True)
    
    data          = Column(Text, nullable=False)
    comments      = Column(Text, nullable=False, default="")
    
    # Stops it being run more than once at the same time
    locked        = Column(DateTime, nullable=True)

class CronLog(Base):
    """Used to log when the job was run, who it was run for etc etc"""
    
    __tablename__ = 'runway_cron_job_logs'
    id            = Column(Integer, primary_key=True)
    
    # Typically this will be the system account, it can be set to a user if the user
    # manually runs the job themselves
    runner        = Column(Integer, ForeignKey("runway_users.id"), nullable=False, index=True)
    
    job           = Column(Integer, ForeignKey("runway_cron_jobs.id"), nullable=True)
    start_time    = Column(DateTime, nullable=False)
    end_time      = Column(DateTime, nullable=False)
    
    # Success, Error, Terminated etc
    status        = Column(String, nullable=False)
    report        = Column(Text, nullable=False)

class CronInstance(object):
    """
    
    """
    permissions = []
    
    # Default data for new jobs of this type
    default_data = "{}"
    
    def __init__(self):
        super(CronInstance, self).__init__()
    
    def load(self, the_ujob):
        """Take a JSON string from the database and create data"""
        raise Exception("Not implemented by {} job".format(self.job_name))
    
    def save(self):
        """Return a JSON string of the data for the database"""
        raise Exception("Not implemented by {} job".format(self.job_name))
    
    def form_save(self, params):
        """Save the results of the form"""
        raise Exception("Not implemented by {} job".format(self.job_name))
    
    def form_render(self, request, the_job):
        """Used to render a form for editing details"""
        raise Exception("Not implemented by {} job".format(self.job_name))
    
    def perform_job(self, the_job):
        """Used to render a view"""
        raise Exception("Not implemented by {} job".format(self.job_name))
