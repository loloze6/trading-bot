# Review of the plans in this folder

These plans come from the final helper, run once on all 29 ideas of step 2, exercise 3 (opus): 58 plans, daily (`_1d`) and hourly (`_1h`). The briefs are those of step 1, exercise 5. Cost: 3.03 USD for the 58 calls (about 0.05 each, with the references cached), plus 0.23 USD for the divergence rerun. Log: `../plans_run_log.txt`. No refusal.

## Counts

| | plans | untestable |
|---|---|---|
| 001 RSI extremes (4 ideas) | 8 | 0 |
| 002 moving-average cross (6 ideas) | 12 | 0 |
| 003 thin and heavy volume (6 ideas) | 12 | 0 |
| 004 bitcoin leads altcoins (7 ideas) | 0 | 14: all need a second coin |
| 005 RSI divergence (6 ideas) | 0 | 12 (after the rerun below) |
| Total | 32 | 26 |

## Checks

- **`../helper/check_plans.py`, on all 36 plans:** the hard rules hold in every config, and every criterion has its parts. It first flagged two criteria as missing parts ("t below -2", "counting each next-bar return once"). Both were false alarms; the checker's patterns are fixed.
- **Read by hand, all 32 non-divergence configs:**
  - Every config takes the same side as its idea: `clip` keeps the long side for the "up" ideas and the short side for the "down" ideas.
  - Settings are conventional: RSI 14, SMA 50/200, the 200 average for "price crosses the long average", one-bar moves for the volume ideas.
  - The volume ideas gate on volume in the regime detector (vetoes), as the card allows.

## Forced plans, then a rerun

In the first run, four divergence plans failed the card's criterion "never forced":
- `005-01` (daily and hourly);
- `005-05` (daily);
- `005-06` (hourly).

Each deviation said the config cannot compare RSI at the two peaks, which is what the idea is about.

**The fix.** One prompt line: "the config has no memory of past turning points: an idea that compares a value now with its value at an earlier high or low cannot be built, and is untestable". It was tested in exercises 11 and 12: 6 of 6 divergence ideas untestable, twice, and the five testable plans unchanged.

**The rerun.** The 12 divergence plans in this folder were then rerun with the current prompt (log: `../plans_rerun_divergence_log.txt`, 0.23 USD). All 12 are now untestable. The configs the four forced plans left behind were removed. Step 4 did not run any of the four forced plans.

## For step 2

As in the exercises, 002-01 and 002-05 (and their mirrors, 002-02 and 002-06) give identical configs. Step 4 runs them anyway: they are separate plans, with separate criteria.
