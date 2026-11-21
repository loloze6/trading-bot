# Run brief: d_line_1h_run (2026-11-19, written before the run)

**Purpose.** Topic 30 found that the new hourly ideas are real but too small for their costs (0.3 to 4.6 bps earned per
unit traded, against 5.7 to 10.6 bps of cost), and that line 7.d, which reads why a book does not pay and proposes
what would, saw it in 38 of 39 analyses: its ideas were never tested (select_next followed confirmations; changed
2026-11-19). This run answers one question: **do 7.d's ideas, aimed at a bigger move per trade, make a confirmed hourly
effect pay?** (topic 30, change 2; operator's go 2026-11-19.)

**The ideas, by one rule:** every idea line 7.d wrote for the slow_1h_run backtests step 5 confirmed (8 parents, 17
ideas). Not chosen by hand. They push the same way: hold longer (24 hours or 3 days instead of 2 hours) or trade only
when the move is larger (high-volatility weeks, after a sharp fall).

| Idea file | Parent's verdict | Idea |
|---|---|---|
| `07d_not_profitable/slow_1h_run/016-06_down-even-volume-continuation.g1_fresh-drop-rebound_1h/ideas/016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound.md` | confirmed (+2.75) | When a coin has fallen over the past 3 days, the larger its fall over the last 1 day, the more it rises over the next 3 days, and the deeper its 3-day fall, the larger that rebound. |
| `07d_not_profitable/slow_1h_run/016-06_down-even-volume-continuation.g1_fresh-drop-rebound_1h/ideas/016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold.md` | confirmed (+2.75) | When a coin has fallen over the past 3 days, the larger its fall over the last 1 day, the more it rises over the next 3 days, with the rise building across the whole 3 days rather than in the first hours after the drop. |
| `07d_not_profitable/slow_1h_run/016-03_up-jump-price-reversal_1h/ideas/016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising.md` | confirmed (+2.74) | When a coin has risen over the past 3 days, the smaller the share of that rise that came from its few biggest hourly gains (a grind of many small hourly steps), the more the coin keeps rising over the next 3 days. |
| `07d_not_profitable/slow_1h_run/016-03_up-jump-price-reversal_1h/ideas/016-03_up-jump-price-reversal.d2_jump-rises-continue-less.md` | confirmed (+2.74) | When a coin has risen over the past 3 days, the larger the share of that rise that came from its few biggest hourly gains, the smaller the coin's further rise over the next 3 days. |
| `07d_not_profitable/slow_1h_run/016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift_1h/ideas/016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d1_late-utc-rebound-after-falls.md` | confirmed (+7.68) | Each coin rises over the two hours from 21:00 to 23:00 UTC, and the higher its hourly volatility over the past 7 days, the larger that rise, the more so the further the coin fell over the past 24 hours. |
| `07d_not_profitable/slow_1h_run/016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift_1h/ideas/016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d2_evening-bounce-after-drops.md` | confirmed (+7.68) | Each coin rises over the two hours after 21:00 UTC, and the larger its fall over the past 24 hours measured in units of its 7-day hourly volatility, the larger that rise. |
| `07d_not_profitable/slow_1h_run/016-03_up-jump-price-reversal.g1_late-evening-utc-rebound_1h/ideas/016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-rebounds-next-day.md` | confirmed (+5.27) | The more a coin has fallen over the 24 hours up to the 20:00 UTC close, the more it rises over the next 24 hours. |
| `07d_not_profitable/slow_1h_run/016-03_up-jump-price-reversal.g1_late-evening-utc-rebound_1h/ideas/016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d2_volatile-evening-fall-rebound.md` | confirmed (+5.27) | The more a coin has fallen over the 24 hours up to the 20:00 UTC close, the more it rises over the next 24 hours, only while its 10-day hourly volatility is high, and the higher that volatility the larger the rise. |
| `07d_not_profitable/slow_1h_run/016-04_down-jump-price-reversal.g1_volatile-regime-daily-move-reversal_1h/ideas/016-04_down-jump-price-reversal.g1_volatile-regime-daily-move-reversal.d1_reversal-only-in-high-volatility.md` | confirmed (+4.89) | The larger a coin's 24-hour return measured in units of its past 7-day hourly volatility, the more it moves the opposite way over the next 24 hours, only while the coin's 7-day volatility stands above its own 30-day usual level, and the further above it stands, the stronger the reversal. |
| `07d_not_profitable/slow_1h_run/016-04_down-jump-price-reversal.g1_volatile-regime-daily-move-reversal_1h/ideas/016-04_down-jump-price-reversal.g1_volatile-regime-daily-move-reversal.d2_daily-paced-move-reversal.md` | confirmed (+4.89) | The larger a coin's 24-hour return measured in units of its past 7-day hourly volatility, the more it moves the opposite way over the next 24 hours, with the reversal unfolding across the whole following day, so that the move as it stands at a day's close carries it rather than its hour-to-hour changes. |
| `07d_not_profitable/slow_1h_run/016-04_down-jump-price-reversal.g1_volatile-regime-daily-move-reversal_1h/ideas/016-04_down-jump-price-reversal.g1_volatile-regime-daily-move-reversal.d3_volatile-fall-rebound.md` | confirmed (+4.89) | The larger a coin's 24-hour fall measured in units of its past 7-day hourly volatility, the more it rises over the next 24 hours, and the more so the higher its 7-day volatility stands above its own 30-day usual level. |
| `07d_not_profitable/slow_1h_run/016-05_up-even-volume-continuation.g1_evening-utc-hour-drift_1h/ideas/016-05_up-even-volume-continuation.g1_evening-utc-hour-drift.d1_evening-drift-in-turbulent-weeks.md` | confirmed (+4.42) | Each day, the coin rises over the two hours after 20:00 UTC by more than in its other hours, only while its realised hourly volatility over the past 7 days is high against its own level over the past 30 days. Inside that state, the rise is larger the higher that 7-day volatility stands above its 30-day level. |
| `07d_not_profitable/slow_1h_run/016-05_up-even-volume-continuation.g1_evening-utc-hour-drift_1h/ideas/016-05_up-even-volume-continuation.g1_evening-utc-hour-drift.d2_evening-drift-outpaces-volatility.md` | confirmed (+4.42) | Over the two hours after 20:00 UTC, the coin's rise measured in units of its 7-day hourly volatility is larger the higher that volatility is. So the rise grows faster than the coin's volatility, not just in proportion to it. |
| `07d_not_profitable/slow_1h_run/016-08_down-volume-burst-reversal.g1_late-evening-rebound-after-daily-falls_1h/ideas/016-08_down-volume-burst-reversal.g1_late-evening-rebound-after-daily-falls.d1_daily-fall-multi-day-rebound.md` | confirmed (+2.65) | In the late-UTC-evening hours, the more a coin has fallen over its past 24 hours as of the 20:00 UTC close, the more it rises over the next 3 days. |
| `07d_not_profitable/slow_1h_run/016-08_down-volume-burst-reversal.g1_late-evening-rebound-after-daily-falls_1h/ideas/016-08_down-volume-burst-reversal.g1_late-evening-rebound-after-daily-falls.d2_grinding-falls-rebound-more.md` | confirmed (+2.65) | The more evenly a coin's 24-hour fall is spread across many small hourly steps rather than a few large hours, the more the coin rises over the next 2 days. |
| `07d_not_profitable/slow_1h_run/016-02_down-grind-price-continuation.g2_evening-rebound-after-daily-drop_1h/ideas/016-02_down-grind-price-continuation.g2_evening-rebound-after-daily-drop.d1_daily-drop-rebound-over-day.md` | confirmed (+2.78) | The more a coin has fallen over the past 24 hours relative to its own volatility, the more it rises over the next 24 hours that follow 21:00 UTC, not only over the two hours from 21:00 to 23:00 UTC. |
| `07d_not_profitable/slow_1h_run/016-02_down-grind-price-continuation.g2_evening-rebound-after-daily-drop_1h/ideas/016-02_down-grind-price-continuation.g2_evening-rebound-after-daily-drop.d2_evening-rebound-in-turbulence.md` | confirmed (+2.78) | The more a coin has fallen over the past 24 hours relative to its own volatility, the more it rises over the two hours from 21:00 to 23:00 UTC that follow, and the more so the higher the coin's own volatility over the past 20 days. |

**Data and steps:** each idea's own header (1h bars; the default coins BTC, ETH, LTC, XMR, XRP, ZEC; folds A to D),
`run_idea` unchanged: steps 3 to 7, and the unseen test for a confirmed and profitable idea.

**How it runs.** Run name `d_line_1h_run` (a run of its own, so it touches no file of slow_1h_run or intraday_1h_run).
One `run_idea` call per idea, in the table's order, each a tracked task of its own (the 2-hour limit of a background
task; a 1h backtest takes about 10 minutes):
```
python3 strategy_designer_v2/steps_cards/orchestration/run_idea/helper/run_idea.py IDEA_FILE --run d_line_1h_run --python VENV_PYTHON
```
No loop: the question is about these 17 ideas, not about where step 7 goes next (their step 7 lines still run, as
`run_idea` always does, and write the next ideas for later).

**Budget:** 25 USD (slow_1h_run cost 1.14 USD an idea: about 20 USD). Stop at the budget, an idea already started
finished. Time: about 4 hours.

**Expected outcomes, written before the run:**
| Outcome | What the counts would show | What it means, what follows |
|---|---|---|
| A. 7.d's direction pays | at least one idea confirmed and profitable enough (step 5 and step 6) | the hourly research can pay with the current steps; the select_next change is the fix; let the loop run on hourly briefs again |
| B. Closer, not there | the edge per unit traded rises well above the parents' (above about 5 bps) but no book is profitable | the direction is right, not enough: change 3 (the edge per trade against its cost as a shared notion that steps 3 and 7 read) |
| C. No better | the edge per unit traded stays near the parents' (0.3 to 4.6 bps) | holding longer or filtering does not grow the edge enough; the hourly ideas need another source of edge (the theme of the briefs) |

**Read after the run:** per idea, step 5, step 6, and the book at the bars' closes against its costs (the edge and the
cost per unit traded, `topics/30_review/frictionless.py`), next to its parent's; then which outcome happened.

**Who runs it:** the run session, between its own stretches (the operator's split: this session designs, the run
session runs), after merging master.

## Reading (2026-11-19; stopped at 8 of 17 by the operator, 7.76 USD)
**Between B and C, and the cause found is upstream of the analyst.** 0 of 8 profitable; 7 backtested, 1 refused by step 3
(a component missing). Earned per unit traded 0.9 to 6.7 bps against 10.0 to 11.0 of cost (parents: −6.6 to 5.5).
- **The analyst (7.d) points the right way:** its ideas say trade less, hold longer, on bigger moves.
- **Step 3 dropped every holding period:** its instructions listed "a holding period dropped" as an allowed adaptation,
  since a config could not hold a position. So `evening-fall-rebounds-next-day` (a rise "over the next 24 hours") was
  held 1 hour per position, `slow-three-day-rebound-hold` gave its parent's book exactly, and the continuous ideas
  re-sized every hour (up to 72 % of their trading). The forecast moving, not the sizing, made 97 to 100 % of it.
- **A replay of the books with a hold of each idea's horizon** (no backtest): net after costs positive for 6 of 7, earned
  per unit 22 to 59 bps; a wider band (0.5) stays negative everywhere; shorter holds lose the gain, and longer holds
  than the idea's horizon pay the market's drift, not the idea.
- **Why stopped:** the 9 ideas left would meet the same gap; the fix comes first (operator).
**Next:** the holding period (`strategies.min_holding_bars` = the horizon, set by step 3's code; topic 30), then the same
8 ideas again: `runs/D_LINE_1H_V2_RUN.md`.
