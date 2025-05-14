DROP TABLE IF EXISTS hotspots;

CREATE TABLE hotspots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    call_number TEXT not NULL,
    is_disabled BOOLEAN not NULL
);