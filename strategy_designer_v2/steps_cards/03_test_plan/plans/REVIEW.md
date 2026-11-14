# Review of the plans in this folder

**What these plans are.** The current helper (the fidelity rule, three outcomes, short lines, symmetric criteria), run once on all 29 ideas of step 2, exercise 3 (opus): one plan per idea, on daily bars (`_1d`). The briefs are those of step 1, exercise 5. Cost: 1.40 USD for 30 calls. Logs: `run_log.txt`, and `run_log_rerun.txt` for one rerun (below).

**History.** These plans replace those written before the symmetric criteria (commit `a904a95` and earlier). The hourly plans of the earlier night stay in `../exercise_hourly_anticipation/`, as a record.

## Outcomes

| | plan | untestable | missing-components |
|---|---|---|---|
| 001 RSI extremes (4 ideas) | 4 | 0 | 0 |
| 002 moving-average cross (6 ideas) | 6 | 0 | 0 |
| 003 thin and heavy volume (6 ideas) | 5 | 0 | 1: 003-06 |
| 004 bitcoin leads altcoins (7 ideas) | 0 | 7: two coins | 0 |
| 005 RSI divergence (6 ideas) | 0 | 0 | 6: RSI at an earlier high or low |
| Total | 15 | 7 | 7 |

- **Every plan's fit is "adapted".**
- **One outcome changed:** 003-06 (down move, retrace by volume) is now missing-components: a graded relative volume. Its mirror, 003-05 (up move), is still a plan, with volume as an above/below-average split. The same judgement went two ways on two mirror ideas. This is the inconsistency already parked (`POTENTIAL_ADJUSTMENTS.md`: "unusually low volume" adapted or replaced). The wish list has 7 blocks.

## Checks

- **No code refusal:** every answer passed on its first attempt.
- **The symmetric criteria hold in 15 of 15 plans:** every reject needs t of 2 or more against the idea.
- **One rerun, 002-03.** Its first plan added a second reject rule: "a slope near 0 also rejects, when |t| < 0.5". That is a reject with no evidence against the idea, which the prompt forbids. It was rerun once (closed book, no data seen), and the second plan rejects only on t ≤ -2. Logged in `run_log_rerun.txt`. Code does not catch this; it is the only case in this run.
- **`../helper/check_plans.py`:** every config passes the hard-rule checks. Two criterion flags are false alarms: 003-01 has a 1-bar horizon, so there is nothing to overlap; 003-02 writes its number as "2 or more".

## What changed in the configs

12 of 15 config files differ from the previous plans. After step 4's canonical form (component labels and default params ignored), 7 changed what the engine computes: 001-02, 002-02, 003-01, 003-02, 003-03, 003-04, 003-05. 002-02 and 003-05 are the two plans the situation check flagged in step 5, exercise 7. Of these, 003-01 and 003-02 have a config the engine refuses (step 4): 003-01 ran before, and no longer does.
