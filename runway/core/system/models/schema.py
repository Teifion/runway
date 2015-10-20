from ...base import DBSession
from .user import User

version = 0.4

schema = {
    (0.1, 0.1, 0.2): (
        'ALTER TABLE runway_users ADD COLUMN group_owner INTEGER;',
        'ALTER TABLE runway_users ADD COLUMN group_edit INTEGER;',
        'ALTER TABLE runway_users ADD COLUMN group_view INTEGER;',
        'ALTER TABLE runway_users ADD CONSTRAINT users_group_owner_fkey FOREIGN KEY (group_owner) REFERENCES runway_users (id) MATCH FULL;',
        
        "DROP TABLE runway_user_group_memberships CASCADE",
        "DROP TABLE runway_user_groups CASCADE",
        
        """
        CREATE TABLE runway_user_group_memberships (
            "user" INTEGER NOT NULL,
            "group" INTEGER NOT NULL,
            
            PRIMARY KEY ("user", "group"),
            FOREIGN KEY("user") REFERENCES runway_users (id),
            FOREIGN KEY("group") REFERENCES runway_users (id)
        );
        """,
        # _add_users_to_groups,
    ),
    (0.2, 0.2, 0.3): (
        "ALTER TABLE runway_users ADD COLUMN active BOOLEAN NOT NULL default TRUE",
    ),
    (0.3, 0.3, 0.4): (
        "ALTER TABLE runway_users ADD COLUMN initials VARCHAR NOT NULL default ''",
    ),
    # (1.2, 1.2, 1.3): (
    #     "ALTER TABLE call_audit_audits ADD COLUMN q3 INTEGER",
    # ),
    # (1.0, 1.1, 1.3): (
    #     "ALTER TABLE call_audit_audits ADD COLUMN q4 INTEGER",
    # ),
    
    # (1.3, 1.3, 1.4): (
    #     "ALTER TABLE call_audit_audits ADD COLUMN q5 INTEGER",
    # ),
}

# Useful sql commands
# List tables
"SELECT table_schema, table_name FROM information_schema.tables ORDER BY table_schema, table_name;"

# List fields in table
"SELECT column_name, data_type, character_maximum_length FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = 'runway_users';"

# Manual SQL required to get the installation to work (assuming it doesn't work right away
'''
demo sql "ALTER TABLE runway_users ADD COLUMN group_owner INTEGER;";
demo sql "ALTER TABLE runway_users ADD COLUMN group_edit INTEGER;";
demo sql "ALTER TABLE runway_users ADD COLUMN group_view INTEGER;";
demo sql "ALTER TABLE runway_users ADD CONSTRAINT users_group_owner_fkey FOREIGN KEY (group_owner) REFERENCES runway_users (id) MATCH FULL;";

demo sql "DROP TABLE runway_user_group_memberships;";
demo sql "DROP TABLE runway_user_groups;";

demo sql "CREATE TABLE runway_user_group_memberships (
    \"user\" INTEGER NOT NULL,
    \"group\" INTEGER NOT NULL,
    
    PRIMARY KEY (\"user\", \"group\"),
    FOREIGN KEY(\"user\") REFERENCES runway_users (id),
    FOREIGN KEY(\"group\") REFERENCES runway_users (id)
);";

'''
