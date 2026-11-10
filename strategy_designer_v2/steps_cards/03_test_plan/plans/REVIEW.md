# Review of the plans in this folder

These plans come from the final helper, run once on all 29 ideas of step 2, exercise 3 (opus): 58 plans, daily (`_1d`) and hourly (`_1h`). The briefs are those of step 1, exercise 5. Cost: 3.03 USD for the 58 calls (about 0.05 each, with the references cached). Log: `../plans_run_log.txt`. No refusal.

## Counts

| | plans | untestable |
|---|---|---|
| 001 RSI extremes (4 ideas) | 8 | 0 |
| 002 moving-average cross (6 ideas) | 12 | 0 |
| 003 thin and heavy volume (6 ideas) | 12 | 0 |
| 004 bitcoin leads altcoins (7 ideas) | 0 | 14: all need a second coin |
| 005 RSI divergence (6 ideas) | 4 | 8 |
| Total | 36 | 22 |

## Checks

- **`../helper/check_plans.py`, on all 36 plans:** the hard rules hold in every config, and every criterion has its parts. It first flagged two criteria as missing parts ("t below -2", "counting each next-bar return once"). Both were false alarms; the checker's patterns are fixed.
- **Read by hand, all 32 non-divergence configs:**
  - Every config takes the same side as its idea: `clip` keeps the long side for the "up" ideas and the short side for the "down" ideas.
  - Settings are conventional: RSI 14, SMA 50/200, the 200 average for "price crosses the long average", one-bar moves for the volume ideas.
  - The volume ideas gate on volume in the regime detector (vetoes), as the card allows.

## Forced plans: not sent to step 4

Four divergence plans fail the card's criterion "never forced". Each deviation says the config cannot compare RSI at the two peaks, which is what the idea is about:

- `005-01_bearish-rsi-divergence-reversal_1d` and `_1h`
- `005-05_bearish-divergence-uptrend-continues_1d`
- `005-06_bullish-divergence-downtrend-continues_1h`

Over exercises 7 to 10 the same kind of idea (005-01) was untestable 4 times in 4. On this wider set, 4 of 12 divergence plans were forced. The "not close" line lowers the rate, but does not stop it. A fix to try: name the case in the prompt ("an idea that compares two peaks cannot be built: answer untestable"). It is not made or tested yet. These four plans stay here for the record, and step 4's index marks them "not run".

## For step 2

As in the exercises, 002-01 and 002-05 (and their mirrors, 002-02 and 002-06) give identical configs. Step 4 runs them anyway: they are separate plans, with separate criteria.
