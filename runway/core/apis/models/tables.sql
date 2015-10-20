CREATE TABLE runway_api_keys (
    id SERIAL NOT NULL,
    "user" INTEGER NOT NULL,
    key VARCHAR NOT NULL,
    
    PRIMARY KEY (id),
    FOREIGN KEY("user") REFERENCES runway_users (id)
);