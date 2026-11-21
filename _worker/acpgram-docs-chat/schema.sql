-- Request counters of the documentation chat.
-- bucket: a day (2026-11-21) or a minute (2026-11-21T10:15), UTC;
-- key: a short hash of the reader's address, or '*' for the total of the day.
-- Rows of the past days are deleted by the worker itself.
CREATE TABLE IF NOT EXISTS usage (
  bucket TEXT NOT NULL,
  key    TEXT NOT NULL,
  n      INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (bucket, key)
) WITHOUT ROWID;
