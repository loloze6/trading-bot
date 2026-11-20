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

## Reading, set 1 (`hold_ideas_1h_run`, 7 of 7, done 03:00 UTC)

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
| slow-3day d2 (72) | inconclusive | −1.44 / 0.14 / **0.24** | 0.00 / −0.02 | 19,201 / 3,461 / 3,310 | 0.9 / 18.3 / 31.9 | fails vs holding, mean return, Calmar |

**Counts.** slow-3day d2 is its parent's config (fresh-drop-rebound, in set 2) with an empty veto list added: the same book
again. With option 2: Sharpe after costs above 0 for 5 of 6 distinct books (all 6 without hold were below 0),
above holding the coin for 2 (grinding/jump, volatile evening-fall), step 6 passed by 0 (block: 1 book). Against the
block, on the 5 books both ran: Sharpe higher on 3, lower on 2, by 0.01 to 0.28; Calmar lower on the book that passed.

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

## Reading, set 2 (`hold_confirmed_1h_run`, 17 of 21 done; stopped 06:42 UTC)

The run's task was stopped at the 2-hour limit of a background task (after a container restart at 04:40 had already cut
one backtest), and was not restarted. Not run: `daily-move-reversal` g3 of 017-02 (24 bars; its backtest was cut, its
partial folder removed), and 3 ideas of 1 to 3 bars (017-03 g3, 017-01 g3, 017-03 g4). Set 3 was not run.

Every idea confirmed at step 5 both before and after (the hold does not change the verdict's measure). Sharpe after costs,
before (each idea's own run, no hold) and held; "per unit" = the held book at the closes without costs per unit traded.

| Horizon (bars held) | Ideas | Sharpe before → held | Per unit, held (bps) | Beats holding the coin | Step 6 |
|---|---|---|---|---|---|
| 24 to 72 | 4 | fresh-drop-rebound −1.44 → **0.24**; volatile-regime reversal −2.30 → **0.32**; daily-move reversal g2 −2.81 → **0.45**; up-jump reversal −2.77 → −0.90 | 31.9; 20.5; 25.1; −30.5 | 0 of 4 (−0.10 to −0.31 below it, the 3 positive) | 0 |
| 1 to 4 | 13 | all stay below 0: −1.08 → −0.81 at best, −16.35 → −12.09 at worst | 0.8 to 7.0 | 0 | 0 |

**Counts.** 0 of 17 profitable enough. Median Sharpe −2.30 → −1.05 (+1.25). **Outcome V2 (partly):** the median
rises by more than 0.5, but fewer than 3 pass step 6.

**What it shows.**
1. **The horizon decides.** 16 of the 21 confirmed hourly ideas have a horizon of 1 to 4 bars. Before costs they earn
   0.8 to 7 bps per unit traded; a unit costs about 10 bps. No holding rule can make them pay: the move they predict
   is smaller than one round trip.
2. **Long-horizon ideas are lifted from about −2.5 to about +0.3**, 3 of 4 (the fourth points the wrong way: held, it
   loses more, −30.5 bps per unit). They earn 20 to 32 bps per unit, enough to clear costs, not enough to beat holding
   the coin over the same years.
3. **Together with set 1** (its 5 books of 24 to 72 bars all positive, 2 failing only Calmar; slow-3day there is
   fresh-drop-rebound here): of 8 distinct long-horizon books held, 7 have a positive Sharpe after costs (0.24 to 1.14;
   0 of 8 without hold), 2 beat holding the coin, 0 pass step 6.

**So the vision is half proven.** Holding is necessary: without it no hourly book could pay. It is not sufficient: what
is still missing is ideas whose move over their horizon is well above the cost of a trip. The ideas the workflow found
on hourly bars are mostly 1-to-4-bar ideas, and the long ones have an edge of 20 to 60 bps per unit, close to the bar.
