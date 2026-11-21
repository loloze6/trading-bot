# Topic 16: Data gathering separate from the backtest

Status: closed (2026-11-18)  
Where: research: data and engine  
Opened: 2026-11-18 (operator's question: is Kraken called during the backtest?)

## Question
Should the backtest ever call the exchange, or only read the data gathered before it?

## Seen
- Before: the backtest loader filled missing periods from Kraken while it ran, so a backtest's data could change with
  the day it ran, and a hole could not be told apart from a day never fetched.
- The operator's case: 2023 and 2025 fetched, 2024 a hole. Is the hole Kraken's, or a fetch never made?
- Built: `trading-bot/data/coverage.py` and `local_data/coverage.yaml`: every data tool records the days it fetched.
  The backtest reads local files only; requested days outside the coverage raise `DataNotFetched`. A hole inside a
  covered range is the exchange's own and is read as it is.
- Proof: four backtests rerun, 192 + 24 + 4 + 1,036 files identical.
- 2026-11-19: the fetcher's fallback for a failed fill (`tolerate_fill_failure`) removed; no caller was left (a fixed
  backtest, 576 engine files identical).

## Why it matters
A backtest must read the same data every time, and a missing day must say whether it was fetched.

## Options
| Option | Gain | Risk |
|---|---|---|
| The backtest reads local files only; a coverage record says what was fetched | reproducible; a hole is explained | data must be fetched before a run |
| Keep filling from Kraken during the backtest | no preparation | results change with the day; Kraken's API gives only 720 recent bars |

Recommended: local-only read with a coverage record.

## Decisions
| Date | Decision | By | Why | Rejected, and why |
|---|---|---|---|---|
| 2026-11-18 | The backtest never calls the exchange; data tools fetch and record their days | operator | gathering data is a phase before the backtest, not part of it; a hole must be checked against what was fetched, not guessed | filling during the backtest |
| 2026-11-19 | The fill-failure fallback removed | operator's go (clean-up 5), on the design session's proposal | no caller since the local-only read; obsolete code is removed | keeping it unused |

## Status and next
Closed. Lives in `trading-bot/data/coverage.py` and the data tools.

## Links
Commits 941caa29, 97d8c94a, 434a71c5; `topics/33_review/duration/9_data_and_table_proof.md`.
