# Run brief: d_line_1h_v2_run (2026-11-19, written before the run)

**Purpose.** d_line_1h_run (stopped at 8 of 17, operator) showed that 7.d's ideas point the right way (trade less, hold
longer) but that their books did not hold: step 3 dropped every holding period, so a "24-hour" idea was held 1 hour and
continuous ideas re-sized every hour (topic 30). Since 2026-11-19 the engine has `strategies.min_holding_bars` and
step 3's code sets it to the plan's horizon (`common/forecast.md`, 7). This run answers: **with the book holding for
its idea's horizon, do the same ideas pay?**

**The ideas:** the same 8 idea files as d_line_1h_run's first 8 (the 7 it backtested and the one step 3 refused as
missing a component), through `run_idea` again, in a run of their own. Step 3 plans them again (its config may differ
in more than the holding period: compared idea by idea).

- `07d_not_profitable/slow_1h_run/016-06_down-even-volume-continuation.g1_fresh-drop-rebound_1h/ideas/016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d1_deep-decline-fresh-drop-rebound.md`
- `07d_not_profitable/slow_1h_run/016-06_down-even-volume-continuation.g1_fresh-drop-rebound_1h/ideas/016-06_down-even-volume-continuation.g1_fresh-drop-rebound.d2_slow-three-day-rebound-hold.md`
- `07d_not_profitable/slow_1h_run/016-03_up-jump-price-reversal_1h/ideas/016-03_up-jump-price-reversal.d1_grinding-rises-keep-rising.md`
- `07d_not_profitable/slow_1h_run/016-03_up-jump-price-reversal_1h/ideas/016-03_up-jump-price-reversal.d2_jump-rises-continue-less.md`
- `07d_not_profitable/slow_1h_run/016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift_1h/ideas/016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d1_late-utc-rebound-after-falls.md`
- `07d_not_profitable/slow_1h_run/016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift_1h/ideas/016-02_down-grind-price-continuation.g1_late-utc-volatile-coin-drift.d2_evening-bounce-after-drops.md`
- `07d_not_profitable/slow_1h_run/016-03_up-jump-price-reversal.g1_late-evening-utc-rebound_1h/ideas/016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-rebounds-next-day.md`
- `07d_not_profitable/slow_1h_run/016-03_up-jump-price-reversal.g1_late-evening-utc-rebound_1h/ideas/016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d2_volatile-evening-fall-rebound.md`

**Predicted, before the run** (the replay of d_line_1h_run's books with a hold of the horizon, topic 30): net after
costs positive for 6 of the 7 backtested (the 2-hour idea not), units traded down 5 to 7 times for the 72-hour ideas,
earned per unit 22 to 59 bps against about 10 of cost. A replay is not step 6: step 6 also asks a Sharpe above
holding's, one window left out, and a Calmar above 0.75.

**Expected outcomes:**
| Outcome | What the counts would show | What follows |
|---|---|---|
| A. The fix pays | at least one idea confirmed and profitable enough (steps 5 and 6) | the holding rule stays; hourly ideas go back to the loop (select_next, step 7 as built) |
| B. Costs solved, not the bar | earned per unit above the cost for most, books positive after costs, but step 6 fails on its other bars (holding's Sharpe, Calmar) | the hourly books now earn; the question becomes the size of the edge against holding the coin |
| C. No change | earned per unit and net close to d_line_1h_run's | the replay misled; read why before anything else |

**How:** run `d_line_1h_v2_run`, one `run_idea` per idea, in 2 batches of 4 (tracked tasks, 2-hour limit); no loop.
**Budget:** 12 USD (d_line_1h_run: 7.76 USD for 8 ideas). About 2 hours.
**Read after:** per idea, against d_line_1h_run: step 3's config (holding period, anything else), units traded, hours per
position, earned and cost per unit, net, steps 5 and 6; then which outcome happened.
