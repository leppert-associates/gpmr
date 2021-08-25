CREATE TABLE lab_results (
            id INTEGER PRIMARY KEY
            cas TEXT,
            parameter TEXT,
            value REAL,
            unit TEXT,
            detection_limit REAL,
            dilution_factor REAL,
            mdl REAL,
            method TEXT,
            sample_number TEXT,
            qualifier TEXT,
            datetime TEXT,
            laboratory TEXT,
            location TEXT
            )
