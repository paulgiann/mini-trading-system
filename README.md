Mini Trading System

Flow:
FIX -> Parser -> Order -> RiskEngine -> Logger

Quick start (Windows PowerShell):
- .\run.ps1          (setup + tests + coverage + generate events.json)
- .\run.ps1 test     (tests)
- .\run.ps1 cov      (coverage)
- .\run.ps1 run      (generate events.json)

Files:
- src/fix_parser.py
- src/order.py
- src/risk_engine.py
- src/logger.py
- src/main.py
- tests/test_system.py
- events.json (generated)

## Submission artifacts

- events_SUBMISSION.json (root) — sample event log output for grading
- submission/events.json — same content (kept for completeness)
