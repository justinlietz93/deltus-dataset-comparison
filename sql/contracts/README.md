# SQL Contracts

SQL Server work must preserve the domain result contract.

The MVP adapter reads metadata from `INFORMATION_SCHEMA.COLUMNS`, validates identifiers before building SQL, and only uses safe quoted identifiers for table reads.

Later server-side SQL should return the same sections:

- summary
- schema_overlap
- type_mismatches
- column_stats
- detailed_differences
- missing_before
- missing_after
- duplicate_keys
- warnings
