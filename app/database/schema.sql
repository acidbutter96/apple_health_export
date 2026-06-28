DO $$
BEGIN
    CREATE TYPE parse_status AS ENUM (
        'running',
        'completed',
        'failed',
        'skipped'
    );
EXCEPTION
    WHEN duplicate_object THEN NULL;
END $$;

CREATE TABLE IF NOT EXISTS parse_runs (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    file_hash varchar(64) NOT NULL,
    file_path text,

    status parse_status NOT NULL DEFAULT 'running',

    started_at timestamptz NOT NULL DEFAULT now(),
    finished_at timestamptz,

    total_records integer NOT NULL DEFAULT 0,
    inserted_records integer NOT NULL DEFAULT 0,
    skipped_records integer NOT NULL DEFAULT 0,
    failed_record_count integer NOT NULL DEFAULT 0,

    error_message text
);

CREATE TABLE IF NOT EXISTS health_records (
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

CREATE TABLE IF NOT EXISTS failed_records (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    parse_run_id bigint NOT NULL REFERENCES parse_runs (id),

    file_hash varchar(64) NOT NULL,
    record_index integer,

    raw_record jsonb,
    error_message text NOT NULL,
    error_type text,

    failed_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS benchmark_health_records (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    record_hash varchar(64) NOT NULL,

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

    metadata jsonb NOT NULL DEFAULT '{}'::jsonb
);

CREATE TABLE IF NOT EXISTS benchmark_results (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    strategy text NOT NULL,
    input_size integer NOT NULL,
    batch_size integer,

    elapsed_seconds double precision NOT NULL,
    rows_per_second double precision NOT NULL,

    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE UNIQUE INDEX IF NOT EXISTS unique_completed_file_hash
ON parse_runs (file_hash)
WHERE status = 'completed';

CREATE INDEX IF NOT EXISTS idx_parse_runs_file_hash
ON parse_runs (file_hash);

CREATE INDEX IF NOT EXISTS idx_health_records_type
ON health_records (type);

CREATE INDEX IF NOT EXISTS idx_health_records_start_date
ON health_records (start_date);

CREATE INDEX IF NOT EXISTS idx_health_records_type_start_date
ON health_records (type, start_date);

CREATE INDEX IF NOT EXISTS idx_health_records_parse_run_id
ON health_records (parse_run_id);

CREATE INDEX IF NOT EXISTS idx_failed_records_parse_run_id
ON failed_records (parse_run_id);
