# Generation 6: selection (orchestrator, 2026-11-13)

Source: 7.f on N4-01 (`07f_real_and_profitable/overnight_run/test_relative_calmar/`), run with the relative-Calmar check (step 6 test option): the only line never run, because no book met its entry condition under the agreed rule.

- **Taken: f1** (a 20-day high made below the close of 60 bars earlier is followed by a larger ten-bar rise): rests on F5 (t 3.32, 87 non-overlapping events) and F4; one coin; distinct. It is the opposite of N5-02 (from 7.d on the same backtest: such highs fall back within a week; inconclusive): two lines read contrary ideas from one dataset, so only a test decides.
- **Not taken: f2** (next-day rise after a high, in a volatile uptrend): overlaps N3-01 and N4-03, already tested.
- **Not taken: f3** (the same idea on coins other than those carried by one rally window): not an idea; its situation is chosen by the backtest's result, not known at a bar's close.
