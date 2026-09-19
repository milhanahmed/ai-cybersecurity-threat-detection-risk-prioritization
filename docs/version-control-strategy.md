# Version Control and Collaboration Strategy

## Repository
https://github.com/milhanahmed/ai-cybersecurity-threat-detection-risk-prioritization

## Branching model
`main` is the stable, submission-ready baseline. `development` is the active implementation, documentation, testing and integration branch. Work is performed on `development` and reviewed before being merged into `main`.

## Commit convention
Examples: `docs: add system architecture blueprint`; `docs: define software requirements`; `feat: implement risk scoring`; `test: add preprocessing validation tests`; `fix: handle malformed event input`.

## Traceability
Requirements use FR and NFR identifiers. Architecture modules map to those requirements, implementation modules map to architecture components, and tests map to functional behavior. This provides traceability from requirement to design, code, test and documented result.

## Documentation consistency
Documentation changes are committed alongside relevant design or implementation changes. The technical report and repository documentation will use the same architecture modules, requirement identifiers and evaluation terminology.

## Security
Secrets, credentials, production data, private logs and local environment files are excluded through repository practice and `.gitignore`. Only synthetic or authorized sample data should be committed.
