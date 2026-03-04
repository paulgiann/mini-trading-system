# Coverage Report

Generated on: 2026-03-04 11:57:33

Command used:

`ash
pytest --cov=. --cov-report=term-missing
`

Output:

`	ext
============================= test session starts =============================
platform win32 -- Python 3.13.3, pytest-9.0.2, pluggy-1.6.0
rootdir: C:\Users\Pavlos\Desktop\mini-trading-system
configfile: pytest.ini
plugins: cov-7.0.0
collected 10 items

tests\test_system.py ..........                                          [100%]

=============================== tests coverage ================================
_______________ coverage: platform win32, python 3.13.3-final-0 _______________

Name                   Stmts   Miss  Cover   Missing
----------------------------------------------------
src\fix_parser.py         70     18    74%   12, 20, 24, 35, 41, 55, 59-60, 62, 66, 72-73, 75, 82-83, 85, 89-90
src\logger.py             28      0   100%
src\main.py               35      4    89%   24-27, 49-54
src\order.py              24      0   100%
src\risk_engine.py        25      2    92%   16, 22
tests\test_system.py      79      0   100%
----------------------------------------------------
TOTAL                    261     24    91%
============================= 10 passed in 0.11s ==============================

`
