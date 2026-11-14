# Improvements proposed after the overnight run (for review; nothing here is applied for good)

## Status after the operator's review (2026-11-13)

| Item | What | Status |
|---|---|---|
| F1 | 7.d starts from what failed; a repair is the tested idea amended, in full | **Applied** |
| New | Step 7: an idea is graded or a regime, never an on/off threshold | **Applied** (`07_common/helper/common_rules.md`) |
| E1, F3 | Sizing by each coin's volatility, 2 % a day, signal unchanged (±20) | **Applied** in step 3 (code adds it to every config); N7-01 now passes on 3 of 4 data sets |
| F4 | Label a step 7 what-if | **Not taken** |
| F5, A1 | Limits per data set; unseen-data test after a confirmation | **Parked**: moved to `POTENTIAL_ADJUSTMENTS.md` |
| F2 | For an amended idea, step 5 tests the new part | Rethought (2026-11-14): no new notion; see the supporting check |
| E2 | Calmar bar absolute or relative to holding | **Kept** at 0.75 (operator) |
| A2 | Step 5 shows its result per period (information only) | **Not taken**: no informational field |
| B1, B6 | Step 7 rules: non-overlapping returns; the coin's mean over all windows; book claims on the book's daily returns | Challenged (2026-11-14): one shared definition of the measures proposed |
| B5 | Step 7 code check: an idea about another coin or the market is sent back | Challenged: a word list, with false refusals; removal proposed |
| B3 | One call as step 7's mode | Already the default in the card |
| B2, B4 | Count of cuts; run twice | B2 **not taken**; B4 open (decide from the validation runs) |
| B7 | An idea's situation is known at a bar's close | Covered by step 2's definition; to confirm a line in step 7 |
| C1 | Which test components to keep | Reviewed (2026-11-14) against the conventions; see the review |
| C2 | Step 3 reads only the idea, not step 7's numbers | **Applied**: step 3 reads brief, data lines, Idea, Consequence |
| D1 | Step 5's corrected record description as default | **Applied**; recording the detector's values **parked** |
| Open | No step looks for regimes directly | **Approved** as a line; to design |

Each item: what is wrong, the evidence from the night, what was tested, and a recommendation. The raw log, in the order things were found, is `IMPROVEMENTS.md`. "Behind an option" means the default behaviour is unchanged.

## F. The business reading (added after the morning report: the most useful)

**F1. 7.d must start from the measure that failed.** (log 33, 35, 36)
- What was wrong: across the night, every 7.d idea sharpened the gain; the books closest to passing failed only on their falls; no idea asked when the book should not be long. The loop therefore refined signals and never repaired a book.
- Tested: 7.d's prompt with one change ("start from what failed; an idea that adds gain but leaves the failing measure where it is does not answer; a stop or an exit can be turned into an idea about the market"), on the four books failing only on Calmar. The findings start from the falls; the ideas address them. One of them, N4-01 amended with an exit (N7-01), gave the night's best book: under the agreed rule, profitable on both large unseen samples, Calmar short by 0.05 to 0.07 on the two others, market exposure halved (beta 0.45 against 0.79).
- Also: a fix must be stated as the tested idea amended, in full (not as a separate negative idea, which is tested alone as a short book; not by reference to the parent, whose definitions are then lost: N7-02).
- **Applied** (operator, 2026-11-13): 7.d's line prompt and card. The same logic likely holds for the other lines: each should start from what its entry condition says failed.

**F2. Step 5 should test the part of an amended idea that carries its value.** (log 37)
- What was wrong: N7-01's plan measured the gain half ("the rise appears near the high"); its book earns from the exit half ("below the 20-day average, nothing"). On unseen coins the book pays and the measure is inconclusive.
- Recommendation: **decide**: for an amended idea, step 3's main measure should test the amendment (the difference between the kept and the removed cases), not the original claim again. My view: yes; it is what "is the idea real?" means for a fix.

**F3. The falls are partly the book's, not the idea's.** (log 34)
- What was found: in N1-04 and N3-04 the deepest falls are crash days hitting every coin at once, with many coins held together. No one-coin idea removes that.
- Recommendation: **decide** where book sizing belongs: step 6's common risk level (E1), or a step of its own between the backtest and the profitability check. Not built.

**F4. A what-if is a hint, not a result.** Not taken (operator, 2026-11-13): a step 7 output is taken as it is, with no label.

**F5. A budget of looks per data set.** (log 43)
- What was found: about 32 ideas tested on the 6 coins in one night, most of them refinements of the same few; each further repair found and confirmed there is weaker evidence.
- Recommendation: **decide**: the orchestration counts the ideas tested on a data set, and past a number (to be set), a confirmation there counts only with an unseen-data test. It is the data rule parked earlier, seen from the business side.

**Where N7-01 stands** (log 36, 41, 42): the best book of the night, and the first to pass the agreed rule on data step 7 never saw (2 of 4 data sets; Calmar 0.685 and 0.696 on the other two). What it earns from: the 20-day moving-average trend filter near fresh highs. Its remaining weakness is the bear-market regime (2018, 2022 to 2023), which neither signal repairs (N8-01) nor sizing fixed. The holdout is the operator's decision.

## A. Trusting a confirmation (the most important)

**A1. Test every confirmation on unseen data.** (log 5, 10, 19)
- Evidence: of 8 ideas confirmed on the 6 coins, 2 were confirmed again on 9 unseen coins (N4-01, t 2.23; N4-04, t 3.56), 2 kept their effect with fewer cases (N3-02, t 1.68 then 2.13 on a second sample; N1-04, z 2.04 with a third of the effect), and 4 did not carry over (N2-01 t -0.19, N3-04 t 0.69, N4-03 t 0.57, N5-03 t 0.75). Without this check, half the confirmations would have been taken for real.
- Tested: `oos.py` (the same plan, unchanged, on 9 other coins).
- Recommendation: **apply**, as a standard step after any confirmation or profitable book, in the orchestration. To settle with it: which unseen data (the parked "data rule").

**A2. Report a confirmation's strength over time.** (log 11, 17)
- Evidence: every confirmation draws most of its strength from 2018 to 2021; N1-04 +12 points then +3.9 in 2024 to 2025; N3-04 t 3.18, then 0.21, then 0.82. Step 5 pools every period; 7.f (fragility) runs only on profitable books, so a confirmed but unprofitable idea's fading is checked by nobody.
- Also N4-01, the night's best idea: on the 6 coins its effect is +3.24 % (t 2.53) in 2018 to 2021, -2.06 % (t -2.49) in the 2022 to 2023 bear market, +4.27 % (t 2.03) in 2024 to 2025. Its pooled confirmation hides a regime that reverses it.
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
- Tested (the second): a code check in step 7 that sends back an idea comparing with or depending on another coin or the market. Rerun of 7.b on N2-02 (which had produced such ideas): the first answer was refused (an idea about "altcoins"); the retry gave two one-coin ideas. It does not refuse an idea about the tested coin itself ("On BTC, when...").
- Recommendation: **apply** the second (kept in step 7, in testing); **wait** on the first: tonight's tests do not show these values hurting more than the others.

**B6. Step 7 needs two of the rules steps 3 and 6 already follow.** (log 26, 29, 30)
- Evidence, the baseline: 7.f compared each event with its own window's mean (the per-window bias step 3 has a rule against). Its strongest finding on N4-01 ("the drift appears only below the 60-day level", t 3.32) reverses with the coin's mean over all windows (t 1.35 below, 2.12 above). Its idea, tested as N6-01: inconclusive (t -0.36). The same pattern shows in 4 to 7 of the night's 187 exploration files.
- Evidence, the book: 7.f's first finding ("the gain rests on one coin-window") came from summed trade log returns, which one compounding trade dominates; on step 6's book the same removal changes the Sharpe from 0.79 to 0.72.
- Tested: both as lines in step 7's rules (`common_rules.md`, in testing), 7.f rerun on N4-01: both artefacts gone; its main number agrees with step 5's; its book findings now give beta to holding (0.79) and alpha (t 1.61). Rerun of 7.d on N4-01: the same; gen 5's contrary idea does not come back.
- Recommendation: **apply** both lines.

**B7. An idea's situation must be known at a bar's close.** (log 28)
- Evidence: 7.f proposed the same idea "on coins other than those whose gain came from one rally window": a selection by the backtest's result.
- Recommendation: **apply** as a line in step 7's rules (step 2's definition already says it); no code check (it cannot be read reliably by code).

## C. What the test vessel can express

**C1. Simple components were missing, and the most recurrent themes could not be tested; and the vessel cannot hold a position after an event.** (log 6, 7, 13, 14, 18)
- Evidence: 5 of 9 generation 1 ideas refused for a missing component; "after an event" ideas untestable (N4-01).
- Tested (additive classes in `trading-bot/strategies/strategy_components.py`, each checked against pandas, seen by step 3 only with `--reference-dir reference_overnight`): `MovingAverageSlopeComponent`, `MovingAverageAgeComponent`, `WeekdayComponent`, `WeekdayReturnComponent`, `BarsSinceHighComponent`. With them, step 3 wrote faithful plans for every blocked idea; its fidelity rule still refused a plan that tested another claim (the first weekday plan).
- The recency component matters most: with it, the breakout effect (which lasts 10 bars or more) became a tradable idea, N4-01, the night's best result (confirmed on unseen coins; better than holding on every data set). Without it, step 3 rightly called the idea untestable.
- Recommendation: **decide** which to keep. My view: keep the recency of a high, the slope and the age (general, small, needed by recurring ideas; the recency of a high is the pattern for any "after an event" idea); keep the weekday measure only if calendar ideas stay in scope (the effect did not carry over to unseen coins); drop `WeekdayReturnComponent` (it tests a learned seasonality, not a stated idea).

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

**E2. The Calmar bar is absolute, and holding these coins never reaches it outside the 2018 to 2021 boom.** (log 21, 22)
- Evidence: holding's Calmar is 0.16 (6 coins, 2018 to 2025) and -0.05 (unseen coins, 2022 to 2025). Every book of the night failed 0.75 there, including those well ahead of holding. Volatility-scaled positions did not help (log 20).
- Tested: `--calmar-vs-hold` (the Calmar bar becomes holding's Calmar; the other five unchanged), on 57 books: 17 pass. With it, N4-01 is profitable on all three data sets, and is the night's one idea that meets outcome A (confirmed, and holding up on unseen coins).
- Recommendation: **decide**, and not this test option as such: it is too lenient alone (books only +0.06 of Sharpe ahead of holding pass). My view: keep an absolute bar on the Sharpe ahead of holding (for example +0.2), make the Calmar bar relative to holding, and require both on unseen coins. Tested afterwards on the same 59 books (code only, from the saved checks): 13 pass the five other measures with a Calmar above holding's and a Sharpe more than 0.2 ahead of holding (6 with 0.3). Required on every data set an idea ran on, only N4-01 passes (the 6 coins, and all three unseen samples). N2-04 passes on the 6 coins and the first unseen sample, then fails the second (Sharpe 0.02 behind holding); it is also not confirmed by step 5. Every other idea fails at least one data set.

## What I changed tonight for testing (to keep or revert)

| Change | Where | Default changed? |
|---|---|---|
| Five components: `MovingAverageSlopeComponent`, `MovingAverageAgeComponent`, `WeekdayComponent`, `WeekdayReturnComponent`, `BarsSinceHighComponent` | `trading-bot/strategies/strategy_components.py` (appended, marked "not yet approved") | No: additive classes; no existing config uses them |
| A copy of step 3's catalogue with their rows | `03_test_plan/helper/reference_overnight/` | No: used only with `--reference-dir` (new option of `make_test_plan.py`) |
| A corrected record description for step 5 | `05_verification/helper/record_description_overnight.md` | No: used only with `--record-description` (new option of `make_verdict.py`) |
| Step 6 options `--target-vol` and `--calmar-vs-hold` | `06_profitability/helper/check_profitability.py` | No: off unless passed; tests still pass |
| Step 7: non-overlapping samples, the coin's mean over all windows, book claims on the book's daily returns (its rules); which component columns exist (its data description); a code check against ideas about another coin | `07_common/helper/common_rules.md`, `data_description.md`, `analyse.py` | Yes, in step 7 (still in testing) |
| Orchestrator tools: hand-off, unseen-coin copy, mode judge, predictive check, results table | `overnight_run/*.py` | Not steps |
