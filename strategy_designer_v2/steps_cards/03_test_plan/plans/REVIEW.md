# Review of the plans in this folder

**What these plans are.** The current helper (the fidelity rule, three outcomes, concise output), run once on all 29 ideas of step 2, exercise 3 (opus): 58 plans, daily (`_1d`) and hourly (`_1h`). The briefs are those of step 1, exercise 5. Cost: 2.89 USD for 58 calls. Log: `run_log_fidelity.txt`.

**History.** These plans replace those written before the fidelity rule. The earlier runs' logs are `run_log.txt` and `run_log_divergence_rerun.txt`.

## Outcomes

| | plan | untestable | missing-components |
|---|---|---|---|
| 001 RSI extremes (4 ideas) | 8 | 0 | 0 |
| 002 moving-average cross (6 ideas) | 12 | 0 | 0 |
| 003 thin and heavy volume (6 ideas) | 9 | 0 | 3 (hourly: 003-01, 003-04, 003-06) |
| 004 bitcoin leads altcoins (7 ideas) | 0 | 14: two coins | 0 |
| 005 RSI divergence (6 ideas) | 0 | 0 | 12: RSI at an earlier high or low |
| Total | 29 | 14 | 15 |

- **Every plan's fit is "adapted".** None is exact: every situation is a threshold the config makes graded.
- **The wish list,** `COMPONENT_WISHLIST.md`, has 15 blocks. Several divergence ideas propose the same kind of component (RSI at the previous swing high or low; RSI's position in its own range). One hourly volume block asks for a graded "relative volume" component.

## Checks

- **One code refusal:** a retry that the second answer passed (see the log).
- **`../helper/check_plans.py`:** every plan passes the hard-rule checks on its config. Two criteria were flagged for "overlapping returns". Both are false alarms: 002-06_1h uses Newey-West errors over next-bar returns, and 003-03_1h counts each one-bar return as one case.
- **Every refusal** has its fidelity and its reason.

## One inconsistency to know

**The same volume idea, two judgements.** For 003-01 on daily bars, the fidelity says "unusually low volume" becomes "volume below its 20-bar average": *adapted*, so it is a plan. On hourly bars, the same idea's fidelity says "below average" is not "unusually low": *replaced*, so it is missing-components. 003-04 and 003-06 split the same way.

Both readings can be defended. By the card's rule, a threshold is an adaptation, which favours the daily reading. The model is stricter on one bar size than on the other. It is the one judgement in this run that differs between the two bar sizes.
