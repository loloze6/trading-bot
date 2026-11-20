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

## Reading, set 1 (`hold_ideas_1h_run`, 6 of 7 done at 02:50 UTC; slow-3day running)

Sharpe after costs; "units" = sum of the allocation changes over coins and windows (one unit costs about 10 bps);
"per unit" = the book at the bars' closes without costs, divided by the units traded.

| Idea (hold, bars) | Step 5 | Sharpe: none / block / option 2 | Calmar: block / opt 2 | Units: none / block / opt 2 | Per unit (bps): none / block / opt 2 | Step 6, option 2 |
|---|---|---|---|---|---|---|
| evening-bounce (2) | confirmed | −0.88 / −0.67 / **−0.39** | −0.13 / −0.08 | 8,131 / 7,297 / 7,131 | 6.7 / 7.3 / 8.5 | fails 5 checks |
| grinding-rises (72) | inconclusive | −1.02 / 0.88 / 0.87 | **0.87** / 0.65 | 13,210 / 3,698 / 3,296 | 4.0 / 44.6 / **60.6** | fails Calmar only |
| jump-rises (72) | inconclusive | same book as grinding-rises | | | | fails Calmar only |
| evening-fall d1 (24) | confirmed | −2.24 / **0.50** / 0.42 | 0.19 / 0.14 | 7,810 / 6,004 / 5,866 | 1.7 / 21.7 / 20.5 | fails vs holding, mean return, Calmar |
| volatile evening-fall d2 (24) | confirmed (new measure) | −1.19 / – / **1.14** | – / 0.64 | 3,571 / – / 2,604 | 1.8 / – / 53.2 | fails Calmar only |
| deep-decline (72) | confirmed | −1.04 / 0.09 / **0.24** | −0.02 / −0.01 | 14,109 / 2,558 / 2,942 | 1.6 / 18.3 / 33.4 | fails vs holding, mean return, Calmar |

**Counts.** With option 2: Sharpe after costs above 0 for 4 of 5 distinct books (all 5 without hold were below 0),
above holding the coin for 2 (grinding/jump, volatile evening-fall), step 6 passed by 0 (block: 1 book). Against the
block, on the 4 books both ran: Sharpe higher on 2, lower on 2, by 0.01 to 0.28; Calmar lower on the book that passed.

**What it shows.**
1. **Holding is what turns these books positive**, whichever form: Sharpe moves by +1.3 to +2.7 on every idea
   held 24 to 72 bars; the 2-bar idea moves little (+0.5), as expected for a hold that short.
2. **It is not only costs.** Without costs (at the closes), the held books earn 2 to 20 times more than the same
   ideas without hold (grinding 5,289 → 19,984). The payoff of these ideas comes at their horizon; a book that
   leaves before it misses the payoff and pays the trip anyway.
3. **Option 2 earns more per unit than the block** (60.6 vs 44.6 bps on grinding, 33.4 vs 18.3 on deep-decline) and
   trades about as much, but it holds through more drawdown: it keeps the size each rise asked for, where the block
   ignores later rises. That is what the definition says (the operator's ruling); its cost is a deeper fall, read by
   Calmar.
4. **What stops them now is Calmar** (return per year over the deepest fall, threshold 0.75): 2 of the 5 books
   fail only that, at 0.64 and 0.65. Not touched: the threshold is the same for every timeframe, and changing it for
   these would be a patch.

**Decision for set 2:** continue as written, with option 2 (the definition). Set 1 shows the lever works on
7.d's ideas; set 2 checks it on the 21 ideas already found real.
