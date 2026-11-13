# Run brief: the overnight run (2026-11-12 to 13)

**Purpose (operator, 2026-11-12).** Act as a manual orchestrator of the workflow: step 7's analyses on existing backtests; their ideas through step 3 (test plan), step 4 (backtest), step 5 (is the idea real?) and step 6 (is the book profitable?); step 7 again on the new backtests, the line chosen by steps 5 and 6; and again. Aim: an idea proven real with a profitable book. On the way, find improvements, test them (behind an option or clearly marked, the agreed default unchanged), and list them for the operator's review in the morning. Also settle step 7's mode: one call, or analyst then deducer.

## How the loop runs
- **Step 7:** every line whose entry condition holds. Generation 1 starts from the full-data run's backtests (brief 002, 6 coins, folds A to D, daily). 002-05 and 002-06 are skipped: their books are identical to 002-01 and 002-02.
- **Selection (the orchestrator's choice, logged):** at most about eight ideas per generation, chosen by:
  1. a one-coin config could test it;
  2. its findings carry strong numbers (a t of 3 or more, or the same sign on most coins);
  3. it recurs across lines or modes;
  4. it is distinct from the others and from ideas already tested.
- **Hand-off to step 3:** a clean copy of each chosen idea (its brief, its data lines, the idea and its consequence), without step 7's "Why", whose numbers come from the data. Step 3 stays closed book.
- **Data:** the default (6 coins, folds A to D, daily). An idea step 7 found in that data and then confirmed on it is circular evidence. So every idea that passes step 5 or step 6 is tested again on **unseen coins**: coins the analyst never saw, in folds A and D (the years where they have data). The holdout is not touched.

## Pre-registered outcomes
- **A.** An idea is confirmed with a profitable book on the default data, and holds on unseen coins: a candidate for the operator (the holdout is the operator's decision).
- **B.** Ideas pass on the default data but not on unseen coins: what step 7 finds in data does not carry over. The data rule for step 7's ideas becomes the first improvement.
- **C.** Nothing passes after the generations the night allows: the improvements list says where the workflow is limited.
- **D.** Defects found on the way: each goes to the improvements list.

## Where the outputs go
Each step's outputs in its own folder, under `overnight_run/` (`03_test_plan/overnight_run/plans/`, `04_backtest/overnight_run/backtests/`, and so on; step 7's in each line's folder). The orchestrator's own files (selections, hand-off ideas, the improvements log) in `overnight_run/` next to this brief.

## Result (2026-11-13, about 3 a.m. UTC)

**What ran.** Seven generations: 30 ideas handed off from step 7, 25 test plans (2 refused for a missing component), 25 backtests on the default data plus 19 on unseen coins (4,936 coin-windows), about 140 step 7 analyses (exercise 2 included), the mode judgement. About 35 USD of model calls. Every idea and its numbers: `overnight_run/RESULTS.md`. Every selection: `overnight_run/gen*/selection.md`.

**Which pre-registered outcome happened.**
- **B, mostly:** 8 ideas were confirmed on the default data, and half did not carry over to unseen coins (N2-01, N3-04, N4-03, N5-03), or only weakly (N1-04).
- **A, for one idea, if the profitability rule is changed:** N4-01 (after a new 20-day closing high, the rise lasts 10 days or more; made tradable by the test component `BarsSinceHighComponent`) is confirmed on the 6 coins (twice, t 2.05) and on 9 unseen coins in 2022 to 2025 (t 2.23), and its book beats holding on Sharpe (+0.24, +0.24, +0.26) and on Calmar in all three data sets. It fails the agreed absolute Calmar bar (0.75) in two of them, which holding these coins never reaches outside the 2018 to 2021 boom. Its falls are as deep as holding's (about 80 %): not a book to trade alone without risk control. **And its effect depends on the market's state:** on the 6 coins, after a new high the 10 bars beat the coin's average by +3.24 % in 2018 to 2021 (t 2.53, 221 events) and +4.27 % in 2024 to 2025 (t 2.03, 111), but fall short by -2.06 % in the 2022 to 2023 bear market (t -2.49, 122). The pooled tests hide this. A third unseen sample (NEAR, SUI, TAO, ONDO, 2024 to 2025 only) is small: N4-01 not observable (59 events; +3.3 %, t 1.30), its book passing the relative bar; N4-04 inconclusive (+1.5 %, t 1.63, 49 cases). Both keep their direction. **7.f on N4-01** (run with the relative-Calmar check, the only way to reach it): with step 7's rules corrected (B6), its reading is that N4-01's book is mostly market exposure: beta 0.79 to holding, daily alpha t 1.61; its gain comes from rising, agitated markets and a few days. A practitioner would hedge or scale it, not trade it alone.
- **D:** 22 improvements found on the way (`overnight_run/IMPROVEMENTS_PROPOSED.md`, grouped, with recommendations).

**After the morning report: the business reading of 7.d** (generations 6 and 7). 7.d had been proposing gain refinements to books that failed on their falls. With its prompt changed to start from the failing measure (a test), it proposed N7-01: N4-01 with an exit once the close falls below its 20-day average. Its book is the night's best and the first to pass the agreed rule on data step 7 never saw: profitable on 9 unseen coins in 2022 to 2025 (Sharpe 0.91, +0.59 over holding, Calmar 0.80) and in 2018 to 2021 (Sharpe 1.80, Calmar 3.67); short of the Calmar bar by 0.07 on the 6 coins and 0.05 on the small sample. Its market exposure is about half N4-01's. Its idea is confirmed on the 6 coins only: the book earns from the exit, which step 5's measure did not test (F2). Still weak in the 2022 to 2023 bear market. Closest to outcome A under the agreed rule; not yet met.

**What the night says about the market.** Two families of effects are real here and hold on unseen coins: breakouts whose rise lasts (N3-02, N4-01) and dips bought within an uptrend over two to three days (N4-04, confirmed on unseen coins at t 3.56; its one-day version, N3-04, did not carry over). Short-term reversal (N1-04) and the weekday effect (N2-01) are real on the 6 coins but fade or do not carry over. Most effects are strongest in 2018 to 2021.

**What the night says about the workflow.** It works end to end and can find a real effect; its two weak points are trust and the profitability rule. Trust: step 7's statistics are inflated by its search (findings at t 4 to 5 become t 0 to 1), so only unseen data decides. The rule: an absolute Calmar bar that the market itself fails.
