# Unit 8 final capstone deliverables

[Final report](MSIT_U8_Final_Capstone_Report.docx) · [Presentation script](MSIT_U8_Presentation_Script.docx) · [Supporting artifacts](MSIT_U8_Supporting_Artifacts.zip) · [Readable script](presentation-script.md)

## Verification and scope
The report contains 14,734 words excluding the title and reference list under the recorded whitespace-based counting method. Chapters 1–6 contain 12,591 words including tables and captions. The report was rendered to 78 pages and the separate presentation script to 16 pages; every page was visually reviewed. Both Word packages passed ZIP/XML and relationship-target integrity checks. The report includes 20 figures and 17 clickable references. The presentation plan uses 14 slides and targets approximately 13 minutes including the demonstration; rehearse against the 10–15 minute requirement.

The delivered code closes the six Week 7 validation/access regressions and adds configured analyst authentication plus safer dashboard input and display handling. The final suite reports 33 passing tests and one framework deprecation warning. A fresh extraction of the supporting archive reproduced all 33 passes. The archive contains 62 files covered by its internal SHA-256 manifest. Document and archive checksums are recorded in [SHA256SUMS.txt](SHA256SUMS.txt).

The independent NSL-KDD experiment is a legacy-benchmark evaluation with documented limitations. The frozen event model with its lossy adapter detected 1 of 12,833 attacks. A separate offline native-feature candidate achieved 75.56% accuracy and 62.57% recall after exclusion of 118 test feature vectors also present in training. That candidate is not integrated into the application. These results do not establish contemporary SME detection performance or production readiness.

## Publication provenance
The report and supporting ZIP preserve the verified submission artifacts as prepared on 26 October 2026, before this GitHub publication. Their statements that the final revision was local and not yet pushed describe that preparation milestone. The repository root now contains the published application revision and an updated setup guide. The archive preserves its own original source snapshot and README for reproducibility; its historical Week 7 records remain separately labeled. The unchanged baseline is commit `9d4cf2722093ab657e681976314e073647cc5b56`.

Operational credentials, databases, caches, and installed dependencies are excluded. The only literal credentials in tests are demonstration-only fixtures. Use synthetic data for the local demonstration. Consult the archive README for benchmark attribution and reproduction commands.
