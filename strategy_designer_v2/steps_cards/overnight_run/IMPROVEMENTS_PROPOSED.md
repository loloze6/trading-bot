# Improvements proposed after the overnight run (for review; nothing here is applied for good)

Each item: what is wrong, the evidence from the night, what was tested, and a recommendation. The raw log, in the order things were found, is `IMPROVEMENTS.md`. "Behind an option" means the default behaviour is unchanged.

## A. Trusting a confirmation (the most important)

**A1. Test every confirmation on unseen data.** (log 5, 10, 19)
- Evidence: N1-04 (rebound after a large drop) confirmed on the 6 coins (z 7.0, twice), nearly profitable; on 9 unseen coins, barely confirmed (z 2.04) and not profitable at all. N2-01 (the bar after Friday) confirmed (t 2.59), then t -0.19 on unseen coins. N3-04 (a dip in an uptrend) confirmed (t 3.06), then t 0.69. Only N3-02 held.
- Tested: `oos.py` (the same plan, unchanged, on 9 other coins).
- Recommendation: **apply**, as a standard step after any confirmation or profitable book, in the orchestration. To settle with it: which unseen data (the parked "data rule").

**A2. Report a confirmation's strength over time.** (log 11, 17)
- Evidence: every confirmation draws most of its strength from 2018 to 2021; N1-04 +12 points then +3.9 in 2024 to 2025; N3-04 t 3.18, then 0.21, then 0.82. Step 5 pools every period; 7.f (fragility) runs only on profitable books, so a confirmed but unprofitable idea's fading is checked by nobody.
- Recommendation: **apply** in one of two ways: step 5 prints its main measure per fold next to the verdict (information, the verdict unchanged), or the orchestration does. And the unseen-coin test should cover the same years as the discovery where the coins have data, so that coins and years are tested separately (tonight's first unseen test mixed them).

## B. Step 7's evidence

**B1. Count overlapping returns once.** (log 9; applied tonight in step 7, which is in testing)
- Evidence: the most recurrent theme (trend with momentum, about 12 times) rested on overlapping 20-day returns; tested by step 3's plan: t 0.65.
- Recommendation: **keep** the line now in step 7's rules (non-overlapping samples, the number of independent cases next to a t).

**B2. Step 7's statistics are inflated by its search.** (log 16)
- Evidence: findings at t 3.8 to 5.5 became t 0.06 to 0.91 once tested; even after B1, t 4.0 became 0.82. Not a bug: the best of many cuts.
- Recommendation: **apply** two small things: step 7 reports how many cuts it tried next to its strongest t; the orchestration never ranks ideas on step 7's t. Only unseen data decides (A1).

**B3. One call, not analyst then deducer.** (log 2)
- Evidence: blind judgement, 9 wins of 16; 59 % of ideas found again on a rerun against 42 %; 17 % of ideas with a value fitted to the data against 29 %; 0.27 against 0.35 USD.
- Recommendation: **apply**: one call as step 7's mode; keep the split as an option for later tests.

**B4. Run an analysis twice, or weigh ideas that recur.** (log 3)
- Evidence: only about half of the ideas come back on a rerun.
- Recommendation: **decide**: it doubles step 7's cost; given B2, recurrence is a weak signal too. I would not apply it now.

**B5. Values found in the data, and ideas comparing coins.** (log 4, 15)
- Evidence: 17 % of one-call ideas name a value absent from the plan ("past 30 days"); five ideas of generation 3 compare a coin with BTC (the one-coin rule).
- Recommendation: **apply** the second (a code check that refuses another coin's name in an idea, sent back once); **wait** on the first: tonight's tests do not show these values hurting more than the others.

## C. What the test vessel can express

**C1. Simple components were missing, and the most recurrent themes could not be tested.** (log 6, 7, 13, 14, 18)
- Evidence: 5 of 9 generation 1 ideas refused for a missing component; "after an event" ideas untestable (N4-01).
- Tested (additive classes in `trading-bot/strategies/strategy_components.py`, each checked against pandas, seen by step 3 only with `--reference-dir reference_overnight`): `MovingAverageSlopeComponent`, `MovingAverageAgeComponent`, `WeekdayComponent`, `WeekdayReturnComponent`, `BarsSinceHighComponent`. With them, step 3 wrote faithful plans for every blocked idea; its fidelity rule still refused a plan that tested another claim (the first weekday plan).
- Recommendation: **decide** which to keep. My view: keep the slope, the age and the recency of a high (general, small, needed by recurring ideas); keep the weekday measure only if calendar ideas stay in scope (the effect did not carry over to unseen coins); drop `WeekdayReturnComponent` (it tests a learned seasonality, not a stated idea).

**C2. The step 7 to step 3 hand-off breaks closed book.** (log 1)
- Evidence: step 3 pastes the whole idea file; a step 7 idea file holds its "Why", with numbers measured on the data.
- Tested: `handoff.py` (a clean copy: brief, data lines, idea, consequence).
- Recommendation: **apply**, in step 3 (read only the idea's own fields) or in step 7 (write a clean idea file next to the analysis).

## D. Step-level defects

**D1. Step 5: a false "mismatch".** (log 8)
- Evidence: N1-01's check read the regime detector's components, which the engine never records; it scored 0 % instead of failing. Rerun with a corrected record description: inconclusive, twice.
- Tested: `record_description_overnight.md`, selected with `--record-description`.
- Recommendation: **apply**: the corrected description as the default.

## E. Judging profitability

**E1. Step 6's verdict depends on the position's size.** (log 12)
- Evidence: N1-04's book at the engine's size: Calmar 0.748 (fails); at half size 0.827 (passes). With a common risk level (`--target-vol 0.2`, tested on 24 books), no verdict changes, but the daily-return bar becomes a hidden Sharpe bar of about 0.9.
- Recommendation: **decide**: the risk level books are judged at, and whether the magnitude bar is a return or a Sharpe. My view: judge at one common volatility and turn the magnitude bar into a Sharpe bar (size-free), so a book is not passed or failed by its leverage.
