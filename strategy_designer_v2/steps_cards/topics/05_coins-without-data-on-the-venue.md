# Topic 05: Coins without data on the reachable venue

Status: open  
Where: research: data  
Opened: 2026-11-17

## Question
Which coins can the research use, given the venue the data comes from?

## Seen
- BNB: no data on Kraken.
- TAO: solved 2026-11-19 (its daily bars load; topic 27).

## Why it matters
A coin listed as available but without data stops a backtest's windows.

## Options
| Option | Gain | Risk |
|---|---|---|
| Keep `common/data_available.md` in line with the coverage record (`local_data/coverage.yaml`) | one truth | a small upkeep |

Recommended: derive the list from the coverage record when opened.

## Decisions
None yet.

## Status and next
Opens with the quality of the backtest output.

## Links
`common/data_available.md`, `trading-bot/local_data/coverage.yaml`.
