---
title: "SQL Server Adapter"
status: planned
authority: canonical
---

# SQL Server Adapter

The SQL Server adapter is the first source adapter.

## Responsibilities

- inspect table metadata
- validate selected columns
- execute or wrap comparison SQL
- translate SQL result sets into the domain result contract
- support isolated comparison databases

## Non-responsibilities

- rendering reports
- choosing UI layout
- defining domain terms
- owning the result contract
