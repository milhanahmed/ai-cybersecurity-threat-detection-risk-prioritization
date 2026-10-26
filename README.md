# AI-Assisted Cybersecurity Threat Detection and Risk Prioritization

Capstone project for the University of the People Master of Science in Information Technology.

## Project
**An AI-Assisted Cybersecurity Threat Detection and Risk Prioritization Framework for Small and Medium-Sized Organizations**

## Purpose
This repository contains the source code, documentation, architecture artifacts, evaluation materials, and supporting configuration for the capstone project.

## Planned workflow
The project follows a two-branch workflow:
- `main`: stable, submission-ready baseline.
- `development`: active implementation and integration work.

Changes should be developed on `development`, reviewed/tested, and then merged into `main` when stable.

## Repository structure
```text
src/            Application source modules
data/sample/    Non-sensitive sample data only
models/         Model artifacts and metadata
tests/          Automated tests
docs/           Requirements, architecture, and reports
notebooks/      Exploratory analysis and experiments
config/         Non-secret configuration templates
```

## Security and privacy
Do not commit credentials, API keys, personal data, production logs, or confidential organizational data. Use synthetic or appropriately anonymized datasets.

## Status
The Unit 8 revision implements the integrated dashboard, API, classifier, risk scoring, SQLite persistence, analyst authentication, and stricter input validation. The recorded final suite passes all 33 tests, including regressions for the six Week 7 validation and access-control failures. This remains an academic prototype: independent legacy-benchmark testing found poor recall in the existing classifier, and contemporary representative detection performance has not been established. The native-feature candidate in the supporting evaluation is an offline experiment, not the dashboard model.


## Unit 8 deliverables
- [Final capstone report (Word)](docs/reports/unit8/MSIT_U8_Final_Capstone_Report.docx)
- [Presentation script (Word)](docs/reports/unit8/MSIT_U8_Presentation_Script.docx)
- [Supporting source, test logs, screenshots, and evaluation data (ZIP)](docs/reports/unit8/MSIT_U8_Supporting_Artifacts.zip)
- [Evidence, limitations, and document checksums](docs/reports/unit8/README.md)

The report follows the official UoPeople template and contains Chapters 1–6, testing outcomes, architecture diagrams, code and output screenshots, charts, references, and appendices. The separate script provides a 14-slide presentation plan targeting approximately 13 minutes with live-demo instructions.

## Local demonstration setup
Use Python 3.12 and an isolated virtual environment. Install dependencies with `python -m pip install -r requirements-tested.txt` and run `python -m pytest tests -v`.

Before starting the service, configure `CYBER_USERNAME`, `CYBER_PASSWORD` (at least 16 characters), and `CYBER_DB_PATH` in your shell. Choose your own temporary local credentials and a fresh synthetic-data database. The application reads these environment variables directly and does not load `.env` automatically.

Run `uvicorn src.api.app:app --host 127.0.0.1 --port 8000`, then open http://127.0.0.1:8000/ and enter the configured credentials in the browser authentication prompt. Use a clean URL without credentials. The dashboard, analysis endpoint, and event history require authentication; `/health` is public. Tests use demonstration-only credentials and synthetic data.

HTTP Basic authentication is a local demonstration control. External use requires HTTPS, managed identity, operational review, and further validation. Container execution, production recovery, and representative analyst acceptance have not been verified. The supporting archive includes the independent NSL-KDD experiment and its dataset attribution; see its README for reproduction instructions.
