CREATE TABLE IF NOT EXISTS mappings (
    session_id TEXT    NOT NULL,
    token      TEXT    NOT NULL,
    value      TEXT    NOT NULL,
    pii_type   TEXT    NOT NULL,
    created_at INTEGER NOT NULL,
    expires_at INTEGER NOT NULL,
    PRIMARY KEY (session_id, token)
);

CREATE INDEX IF NOT EXISTS idx_session ON mappings(session_id);
CREATE INDEX IF NOT EXISTS idx_expiry  ON mappings(expires_at);
-- Reverse lookup: value+type → token (deduplication within session)
CREATE INDEX IF NOT EXISTS idx_value   ON mappings(session_id, value, pii_type);
