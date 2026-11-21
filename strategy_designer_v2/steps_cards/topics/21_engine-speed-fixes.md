# Topic 21: Speed fixes of the engine

Status: closed (2026-11-18)  
Where: engine  
Opened: 2026-11-18 (finer bars)

## Question
Where does a backtest on finer bars spend its time, and what can be removed without changing a result?

## Seen
- Measured first (`topics/33_review/duration/8_finer_bars_measure.md`), then three fixes, each proven by four backtests
  with identical files (192 + 24 + 4 + 1,036):
  1. the history table built from typed columns;
  2. the warm-up checked once, on a copy of the real strategy;
  3. the record's nested details expanded once per column.
- Gains, measured alone: 1h BTC fold A 329 s to 135 s; 1h ZEC window with 401 holes 446 s to 18 s; 19 coins daily
  701 s to 458 s; an 1h window with a one-year history 683 s to 57 s.

## Why it matters
Hourly research was too slow to run overnight.

## Options
| Option | Gain | Risk |
|---|---|---|
| Measure, then fix the largest costs, each with a proof of identical files | faster, results unchanged | shared code |

Recommended: as done.

## Decisions
| Date | Decision | By | Why | Rejected, and why |
|---|---|---|---|---|
| 2026-11-18 | Optimise only where the measurement shows the time goes, each fix proven | operator | the backtest must be monitored and the analysis clever enough to find the relevant points, if any | guessing |

## Status and next
Closed. Lives in the engine.

## Links
Commits f24796af, 3a8c95e1, ee2701d2; `topics/33_review/duration/9_data_and_table_proof.md`.
