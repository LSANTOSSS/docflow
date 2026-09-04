# Structural validation

DocFlow separates baseline validation from optional structural policies. This keeps existing documents compatible while allowing stricter projects to opt in to additional guarantees.

## Baseline rule

`structure.required_headings` remains available for presets and custom configurations. Missing required headings make validation fail and are reported as actionable issues.

## Optional rules

The following rules are disabled by default and can be enabled independently:

```yaml
structure:
  required_headings:
    - Overview
  unique_headings: true
  single_h1: true
  no_heading_level_skips: true
```

### `unique_headings`

Requires heading text to be unique, using case-insensitive comparison. Repeated headings are reported with code `duplicate_heading`.

### `single_h1`

Requires exactly one level-1 heading in the document. A missing or repeated H1 is reported with code `invalid_h1_count`.

### `no_heading_level_skips`

Rejects jumps in heading hierarchy between consecutive headings, such as H2 directly to H4. The issue code is `heading_level_skip`.

The first heading is not required to be H1 by this rule alone; use `single_h1` when that contract is desired.

## Validation report

The JSON report keeps the existing compatibility fields and adds structural evidence such as:

- `duplicate_headings`;
- `h1_count`;
- `heading_level_skips`;
- one entry in `checks` for every enabled policy;
- actionable entries in `issues` for every failure.

Only rules explicitly enabled in configuration can block an export. This allows DocFlow to strengthen validation without silently changing the behavior of existing configurations.
