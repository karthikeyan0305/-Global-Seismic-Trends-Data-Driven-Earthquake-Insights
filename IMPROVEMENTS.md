# Code Improvement Plan

This document captures high-impact ways to improve the current earthquake analytics project.

## 1) Security and configuration (highest priority)

- **Move database credentials out of source code** and into environment variables (or `.env` + `python-dotenv`).
- Add a `.env.example` file and update `config.py` to read from `os.getenv` with safe defaults.
- Ensure secrets are never committed to Git history.

## 2) Fix pathing and project structure inconsistencies

- Current code references `../data/...` while CSV files are at repo root in this snapshot. Standardize this by:
  - creating a real `data/` directory, or
  - using `pathlib.Path(__file__).resolve().parent` for robust file paths.
- Align README tree with actual repository layout.

## 3) Improve API reliability and correctness

- Add `timeout`, `retries`, and backoff for USGS API requests.
- Validate response schema before reading nested keys.
- Prevent overshooting the configured `ENDTIME` when computing month end ranges.
- Add logging (`logging` module) instead of print-only observability.

## 4) Data quality and cleaning enhancements

- Avoid blanket median-imputation for every numeric column; use column-specific policies:
  - keep some fields nullable (e.g., `felt`, `cdi`, `mmi`),
  - use domain-aware defaults only where needed.
- Preserve missingness indicators (e.g., `is_mag_missing`) for downstream analysis.
- Add checks for impossible values (e.g., invalid latitude/longitude bounds).

## 5) Database loading and schema control

- Avoid `if_exists="replace"` as default in production-like workflows (can drop table each run).
- Introduce explicit schema migrations and primary keys (`id`) to prevent accidental destructive writes.
- Add batch upsert strategy for incremental ingestion.

## 6) Streamlit app maintainability and performance

- Refactor long `if/elif` query chain into modular query functions in a dictionary registry.
- Avoid mutating global `df` in-place inside query branches.
- Add input validation and graceful handling for missing columns in each query.
- Add charts for key results and cache expensive computations where appropriate.

## 7) SQL and analytics parity

- Ensure SQL scripts and Streamlit/Pandas query logic produce equivalent outputs for shared metrics.
- Add validation tests comparing SQL vs Pandas aggregates on sample data.

## 8) Testing and developer experience

- Add automated tests (`pytest`) for:
  - fetch transforms,
  - cleaning logic,
  - edge cases (empty API payload, malformed geometry, missing columns).
- Add formatting/linting (`black`, `ruff`) and pre-commit hooks.
- Add a Makefile or task runner for common workflows.

## 9) Documentation

- Update README setup instructions to include:
  - virtualenv creation,
  - dependency install command,
  - `.env` configuration,
  - run commands for pipeline + dashboard.
- Add architecture diagram and data dictionary.

## Suggested implementation order

1. Security/config + path fixes
2. API robustness + logging
3. Cleaning policy updates
4. DB write strategy
5. Streamlit refactor
6. Tests + linting + docs
