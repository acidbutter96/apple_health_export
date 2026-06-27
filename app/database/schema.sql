CREATE TYPE parse_status AS ENUM (
    'running',
    'completed',
    'failed',
    'skipped'
);

CREATE TABLE parse_runs (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    file_hash varchar(64) NOT NULL UNIQUE,
    file_path text,

    status parse_status NOT NULL DEFAULT 'running',

    started_at timestamptz NOT NULL DEFAULT now(),
    finished_at timestamptz,

    total_records integer NOT NULL DEFAULT 0,
    inserted_records integer NOT NULL DEFAULT 0,
    skipped_records integer NOT NULL DEFAULT 0,
    failed_records integer NOT NULL DEFAULT 0,

    error_message text
);


CREATE TABLE health_records (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    record_hash varchar(64) NOT NULL UNIQUE,

    type text,
    source_name text,
    source_version text,
    device text,
    unit text,

    creation_date timestamptz,
    start_date timestamptz,
    end_date timestamptz,

    value text,
    value_numeric double precision,

    metadata jsonb NOT NULL DEFAULT '{}'::jsonb,

    parse_run_id bigint NOT NULL REFERENCES parse_runs (id)
);


CREATE TABLE failed_records (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    parse_run_id bigint NOT NULL REFERENCES parse_runs (id),

    file_hash varchar(64) NOT NULL,
    record_index integer,

    raw_record jsonb,
    error_message text NOT NULL,
    error_type text,

    failed_at timestamptz NOT NULL DEFAULT now()
);

