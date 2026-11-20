# Run brief: the holding period, night of 2026-11-20 (written before the runs)

**Purpose (operator, 2026-11-20):** "in the morning, progress on the discovery and proof of the vision for making a finer
timeframe profitable." The vision: hourly ideas are real but their books lost to costs because they did not hold their
bets; with each bet held for its idea's horizon (`strategies.min_holding_bars`, the operator's option 2,
`common/forecast.md` 7), they pay. Topic 30.

**Method:** every set reruns existing plans unchanged except the holding period (`min_holding_bars` = the plan's own
horizon, set by code), through step 4, step 5 with each idea's saved measure (`--measure`: no model call; one exception
noted), step 6, and the unseen-dates test for a confirmed and profitable idea. So the only change is the holding rule,
compared idea by idea with the same plans' records without it. Script: `topics/30_review/hold_rerun.py`. 0 USD (about
0.3 USD for the one verdict without a saved measure). No merge into master.

| Set | Run | Ideas | Compared with | Question |
|---|---|---|---|---|
| 1 | `hold_ideas_1h_run` | the 7 plans of d_line_1h_v2_run (7.d's ideas) | the same plans held by the block (d_line_1h_v2_run, 6 of them) and the parents without hold (d_line_1h_run) | does option 2 beat the block on the same plans? |
| 2 | `hold_confirmed_1h_run` | the 21 confirmed hourly ideas of slow_1h_run (8) and intraday_1h_run (13; one needs a component built on the run session's branch) | their own records without hold (0 profitable of 22) | **the proof:** do ideas already found real now pay? |
| 3 | `hold_paying_run` | the 13 profitable books (10 daily, 3 hourly retests) | their own records without hold | does holding keep what already pays (daily and hourly on the same footing)? |

**Expected outcomes, set 2 (the vision):**
| Outcome | What the counts would show | Meaning |
|---|---|---|
| V1. Proven in-sample | 3 or more of the 21 confirmed and profitable enough (steps 5 and 6), and the median Sharpe after costs above 0 | hourly ideas pay when held; the hourly loop can resume on this rule; next, the unseen periods |
| V2. Partly | the median Sharpe rises clearly (by more than 0.5) but fewer than 3 pass step 6 | holding is necessary, not sufficient: the next lever is the size of the edge against holding the coin |
| V3. Not | Sharpe about unchanged | the replay misled; read why |

Set 1 decides option 2 against the block by the median Sharpe of the 7 and the number passing step 6. Set 3: no
paying book should turn unprofitable; if some do, the hold is not neutral on daily bars, and that is read before any
merge. **Read after each set**, written below, before the next one starts; each set continues only if the one before
gives a reason.

**Already known:** d_line_1h_v2_run (the block, 7 of 8 run, 6 backtested): 2 profitable enough, but they are one book
(`grinding-rises` and `jump-rises` got the same config from step 3: Sharpe 0.88, Calmar 0.87; inconclusive at step 5);
Sharpe after costs above 0 for 5 of 6 (0.09 to 0.88; the 2-hour idea −0.67), above holding's for 1. Without hold
(d_line_1h_run): 0 of 7, Sharpe −0.88 to −2.24.
