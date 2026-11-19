# Topic 09: Futures candles for a pre-live check, and the short side

Status: open  
Where: research and live  
Opened: 2026-11-18 (the live session's comparison)

## Question
How far do backtests on spot candles differ from what the bot does live on futures, and does it matter?

## Seen
- Live trades Kraken futures; the research backtests spot. Prices differ by 0.002 % to 0.05 %: 5 decisions in 321
  days differ (the 0.2 rule on a knife edge), at most 8.67 per 1,000.
- Futures candles start 2022-03-23 (ZEC 2022-08-24): they cannot replace spot for the folds (B and C are 2018 to 2021).
- Funding is the larger difference, and it is not modelled. In rising markets longs usually pay shorts, so the backtest
  understates what a short earns live (2026-11-19).

## Why it matters
An idea going live should be checked on the prices and costs it will trade at.

## Options
| Option | Gain | Risk |
|---|---|---|
| The data source as a backtest setting (spot by default) and a pre-live check on futures candles from 2022-03, funding modelled | the live conditions tested | shared code; funding data to gather |
| A brief testing the short side on purpose (side "short" or "long and short"), once funding is modelled | the short side judged with its real income | waits for funding |

Recommended: both, when a topic opens.

## Decisions
None yet.

## Status and next
Opens with the pre-live work.

## Links
Topic 19 (the 0.2 rule), topic 26.
