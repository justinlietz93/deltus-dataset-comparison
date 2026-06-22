---
title: "ADR-0002: Replace SSRS with a Lightweight Report Reader"
status: current
authority: canonical
---

# ADR-0002: Replace SSRS with a Lightweight Report Reader

## Status

Accepted.

## Context

The historical system used SSRS because it was the available workplace reporting surface and produced PDF/Excel evidence. The modern project does not need to generate RDL.

## Decision

Build a small report reader and export layer over the comparison result contract.

## Required outputs

- HTML
- XLSX
- JSON manifest
- CSV result sections
- PDF after HTML stabilizes

## Consequences

- RDL generator work is not continued.
- SSRS report assets are preserved under legacy material.
- Report rendering is testable against fixture result contracts.
