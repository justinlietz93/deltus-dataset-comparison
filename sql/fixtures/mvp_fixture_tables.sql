-- Optional manual SQL Server smoke fixtures for the 0.1.0 adapter.
-- These tables mirror the Python fixture cases at tests/fixtures/mvp_cases.json.

CREATE SCHEMA deltus_fixture;
GO

CREATE TABLE deltus_fixture.identical_before (
  id int NOT NULL,
  name nvarchar(100) NULL,
  amount decimal(18, 4) NULL,
  load_date datetime NULL
);

CREATE TABLE deltus_fixture.identical_after (
  id int NOT NULL,
  name nvarchar(100) NULL,
  amount decimal(18, 4) NULL,
  load_date datetime NULL
);

INSERT INTO deltus_fixture.identical_before (id, name, amount, load_date) VALUES
(1, N'alpha', 10.0, '2026-01-01'),
(2, N'beta', 20.0, '2026-01-01');

INSERT INTO deltus_fixture.identical_after (id, name, amount, load_date) VALUES
(1, N'alpha', 10.0, '2026-01-01'),
(2, N'beta', 20.0, '2026-01-01');
GO
