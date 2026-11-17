# Run brief: night_run (2026-11-17, written before the run)

**Purpose.** Two things, in this order.
1. **Validate `run_brief`** (scope 3 of the orchestration): from a brief to its ideas, then the loop, on one brief from
   step 1's list, with a small budget (its card's "done when").
2. **Research new theories end to end, unattended.** demo_run took one idea of brief 002 down four generations: 6 of
   12 ideas confirmed, none with a profitable book (the effects are real but too small to pay). This run asks whether
   that holds for other theories: are there real effects in other families, and does any pay?

**Scope.**
- Run `night_run`; the default data (six coins, folds A to D, daily bars) unless a brief or an idea asks for other data.
- Briefs, from step 1's list (`01_brief/briefs/`), one after the other in the same run, so their ideas and the lines'
  ideas compete in one queue by `select_next`'s score:
  1. 003, volume separates reversal from continuation (also the first run of volume ideas since the engine's
     warm-up fix A: they never ran before);
  2. 011, weekend moves reverse on weekdays;
  3. 010 or 005 (RSI), if time allows.
- Budgets, each the run's total, so the run is read between stages: stage 1 (validation) 6 USD; then 25, 40, 60.
  The real limit is the operator's 5-hour usage window.
- Nothing in a step changes during the run. A defect that stops the chain is fixed only if the fix is general and
  proven; it is written in the reading.

**Pre-registered outcomes.**
- **A.** An idea confirmed with a profitable book: the first goal. Next: the parked topic "proven and profitable,
  what next" (on data the analysis did not see).
- **B.** Real effects again, none paying: the demo_run pattern holds across theories, so the limit is the book, not
  the theory. Next: the same parked topic, framed as "what makes a small real effect pay".
- **C.** Nothing real (inconclusive, rejected or not observable throughout): these theories show nothing on this data.
- **D.** A chain defect (a step that fails, a refusal, a status that does not follow from the files): fixed or parked.
- **E (validation).** `run_brief` meets its "done when", or the reading says what failed.

## Reading
(written during and after the run)

**Stage 1 (00:09 to 00:11 UTC; brief 003; budget 6 USD; spent 0.43 USD).** Step 2 wrote 4 ideas (0.04 USD). The loop
took them in score order; step 3 refused all four as missing-components, and the loop stopped: "no candidate left".
- **Why:** each idea needs a graded measure of the day's volume against its own recent average, and no component in the
  catalogue computes one. The four answers converge on one component (the bar's volume over the mean of the last
  N bars), written in `03_test_plan/night_run/plans/COMPONENT_WISHLIST.md`. A new component is a change to
  `trading-bot/`, so it waits for the operator: parked in `POTENTIAL_ADJUSTMENTS.md`.
- **Defect found and fixed (general):** an idea step 3 could not plan was counted in its line's record as a failure
  (step 2's record fell from 0.20 to 0.17 after each refusal). A record now counts only ideas with a verdict from
  step 5 (`select_next`, test added). An idea that was never tested says nothing about the line that wrote it.
- **run_brief:** steps 2 and the loop chained as the card says; the "done when" is not met yet (no line's idea was
  reached, as no idea could be tested). Next: a brief whose ideas the catalogue can express.

**Stage 2 (00:16 to 02:27 UTC; brief 011 added; budget 25 USD; two machine restarts, resumed).** 23 ideas from brief 011
and its lines, generations 0 to 3: **11 confirmed** (t +2.9 to +5.6), 7 inconclusive, 5 not testable
(missing-components); **none profitable**. Run total: 27 ideas, 25.48 USD, about 4 to 5 minutes an idea.
- **The books first.** The confirmed ideas are short reversals: after a weekend move, after a large or volatile fall,
  the coin moves back over 1 to 3 days. Their books: Sharpe 0.1 to 0.9, mean daily return 0.01 % to 0.06 % (about 4 %
  to 20 % a year), Calmar under 0.75; 4 of 11 beat holding the coin on Sharpe. The best: "high-volatility fall
  reversal" (Sharpe 0.89, +0.34 over holding, Calmar 0.70). The ideas that trade most (0.8 trades a bar) lose: costs.
- **Outcome B, again:** real effects, none pays. With demo_run: 17 confirmed ideas from two theories, none paying. The
  limit is the book, not the theory. What a practitioner would change: not find more such effects one at a time, but
  ask what makes small real effects pay (combine several into one book, hold them on fewer and stronger cases, cut
  costs). That is the parked topic "proven and profitable, what next": the operator's to open.
- **Missing components recur:** a bar's volume against its own average (7 ideas in all, briefs 003 and 011), the
  close's place in the day's high-low range (1), a weekend move held as the forecast over the next days (2). Parked.
- **Outcome E met:** `orchestration/run_brief/validation/reading.md`.
- **Seen, not acted on:** two ideas from different parents gave the same t (+2.75) and the same failures, probably the
  same test written twice in different words; `select_next`'s duplicate rule only catches identical text.

**Stage 3 (02:28 to 02:38 UTC; brief 010 added to night_run; stopped after 2 ideas).** Step 2 wrote 4 RSI ideas, but
they ranked below the 7.g line's generation-3 ideas (score 0.17 against 0.18): step 2's record is 0 of 4, 7.g's 10 of
13. The two turns went to further variants of the same short reversal. Stage 3's purpose was a new theory, so it was
stopped between two ideas (the last turn's idea had not reached a plan: nothing half-written) and brief 010 runs in its
own run, `night_rsi_run` (budget 15 USD), under the same outcomes.
- **Finding for the operator (the score is theirs, not changed):** 7.g's record is high because its ideas keep
  confirming one effect in new words (a fall in a volatile day rebounds), so the score keeps choosing that effect's
  variants over a new theory's ideas. A line's record rewards re-finding a known effect as much as finding a new one.

**night_rsi_run (02:38 to 02:41 UTC, plus restarts; brief 010; spent 0.31 USD).** Step 2 wrote 8 ideas; step 3 refused
all 8 as missing-components: each needs how long, or how often, RSI has stayed above (or below) its midpoint, and no
component measures that. The run stopped: "no candidate left". Parked with the other components.

**Stage 4, written before it starts (02:51 UTC).** Of three briefs, two cannot be tested at all (12 of 12 ideas refused
for missing components). Purpose: find out whether other theories in step 1's list can be tested with today's
catalogue, each in its own small run so a line's variants do not crowd them out: brief 006 (quiet narrow ranges
precede large moves) in `night_006_run`, then brief 005 (RSI divergence) in `night_005_run`, 10 USD each.
Outcomes: as above (A to D); and **F**: their ideas are refused too, so the catalogue, not the theories, is the limit
on new research until components are added.

**Stage 4 (02:51 to 02:53 UTC; 0.29 USD).** Outcome **F**. Brief 006 (`night_006_run`): 3 ideas "untestable" (they
predict a larger move without its direction, which a long/short book cannot trade) and 2 missing-components. Brief 005
(`night_005_run`): 2 ideas, both missing-components (price-RSI divergence). With 003 and 010: **4 of the 5 briefs tried
cannot be tested with today's catalogue**; only 011 could.

**A diagnostic, no model call, no new backtest (02:55 UTC):** one book made of the 18 confirmed ideas' books (demo_run
and night_run), equal weight, measured exactly as step 6 does (`06_profitability/night_run/diagnosis/`). The books
move together little (mean correlation 0.20). The one book: Sharpe 0.90 (a single book: median 0.48), 0.34 above
holding, Calmar 0.98, mean 0.027 % a day; sized to a single book's volatility (x2): 0.054 % a day, lowest Sharpe with one
window left out 0.73: **it passes every bar of step 6's rule, where none of the 18 does alone.**
- **Caveat, decisive:** these 18 ideas were chosen because they were confirmed on this same data, and several are
  variants of one effect. This is in-sample: a direction, not a result. It must be judged on data the analysis never
  saw (the parked unseen-data question) before anything is concluded.
- **What it points to:** "what makes small real effects pay" has a first answer to test: combine them. That is the
  parked topic "proven and profitable, what next": the operator's to open.

**Stage 5, written before it starts (03:00 UTC).** Purpose: two new theories chosen by step 1 itself (no theme: "a
trading theory of your choice"; step 1's list of the 11 briefs already written keeps it from repeating one), each in
its own run (`night_012_run`, `night_013_run`), 10 USD each. Outcomes: A to D, F as above.

**Stage 5 (03:00 to 03:57 UTC; briefs 013 and 012, each in its own run).** **Outcome A, for the first time.**
- **Brief 013** (anchoring to the recent high; `night_013_run`, 10.49 + 0.04 USD for step 2; stopped on the budget):
  20 ideas, 10 tested: 4 confirmed, 3 inconclusive, 3 mismatch; 10 not testable (missing components: volume against
  its average, breaking a past high). The lines walked away from the brief's theory (nearness to the high) to
  momentum: in 5 generations, 7.d then 7.g turned "near the high, the coin gains" into "in a rising two months, the
  larger the two-week rise, the larger the next week".
- **The first confirmed idea with a profitable book:** `013-01…g1_two-week-momentum-continuation.g1_momentum-continuation-in-uptrends`.
  Idea: "Among coins whose 60-day return is positive, the larger a coin's 14-day rise, the higher its return over the
  next 7 days" (long only). Step 5: confirmed, t +2.79 on 1,234 independent weekly cases, timing gain +0.06 % a day.
  Step 6, every bar passed: Sharpe 1.15 (holding: 0.55 lower), mean 0.076 % a day (about 32 % a year), lowest Sharpe
  with one window left out 0.99, Calmar 1.53, 0.15 trades a bar.
- **Caveat, as for the combined book:** found on the same data it was tested on, as the 8th tested idea of one lineage,
  each child written from what its parent's book showed. It is a well-known effect (trend following), which makes it
  more plausible, not proven. What decides is data the analysis never saw: the parked topic "proven and profitable,
  what next", the operator's to open. Not opened tonight.
- **Brief 012** (liquidation flush and partial rebound; `night_012_run`, 0.21 + 0.05 USD): 4 ideas, all missing
  components (volume against its average, the lower wick). Outcome F again: 5 of the 7 briefs tried tonight are
  blocked by the catalogue.

**Stage 6, written before it starts (04:00 UTC).** Purpose: let the loop go on in `night_013_run` (the only open
lineage that pays), 10 USD more (run total 20 USD), by `select_next`'s score as is. Its queue holds 27 candidates,
among them this idea's own child on 4-hour bars (score 0.125, low in the queue: the score is the operator's, not
changed). Outcomes: A to D, F as above; plus **G**: another confirmed and profitable idea, or the 4-hour child
confirming the momentum effect on other bars.

**Stage 6 (04:00 to 04:50 UTC; `night_013_run`, 9.65 USD; stopped on the budget, 20.14 USD in all).** 13 more ideas:
4 confirmed, 4 inconclusive, 1 mismatch, 4 missing components. Outcome **G**: two more confirmed ideas with a
profitable book. The run in all: 33 ideas, 8 confirmed, **3 confirmed and profitable**:

| Idea (last part of its id) | Step 5 | Sharpe | Over holding | Mean a day | Calmar |
|---|---|---|---|---|---|
| `g1_momentum-continuation-in-uptrends` (6 coins) | confirmed, t +2.79 | 1.15 | +0.59 | 0.076 % | 1.53 |
| `b1_nearness-to-high-more-coins` (19 coins) | confirmed, t +3.77 | 1.25 | +0.67 | 0.073 % | 1.68 |
| `g1_rising-month-weekly-momentum` (6 coins) | confirmed, t +3.47 | 0.97 | +0.42 | 0.063 % | 0.88 |

- **One effect, three wordings.** All three hold coins long while their recent trend is up, more so the stronger the
  rise: trend following. They are not three findings.
- **The first check on coins no analysis read** (`06_profitability/night_013_run/diagnosis/coin_groups.py`, no model
  call): the more-coins idea's 19-coin backtest split by step 6's own code. On the 6 coins the lineage's analyses read:
  Sharpe 1.01, +0.43 over holding, Calmar 0.97. On the 12 coins none read (TAO had no data): Sharpe 1.45, +0.40 over
  holding, 0.106 % a day, lowest Sharpe with one window left out 1.19, Calmar 2.53. **Every bar passed on coins the
  analysis never saw.**
- **What it is not:** the same years. Coins move together, so new coins over the same years are not new market
  conditions. The decisive test is on dates the analysis never saw: the parked topic "proven and profitable, what
  next", the operator's. Not opened.
- **Step back.** The lineage now mostly rewrites the same effect (8 of the 13 tested ideas in this stage were
  variants of momentum or of the one-day rebound). More turns here would buy little. The runs stop for the night.

## End of the night (04:50 UTC)
Seven briefs tried in six runs; 81 ideas through `run_idea`, 38 of them with a plan and a backtest (43 refused by step 3), 48.0 USD (47.61 in `run_idea`, 0.35 for step 2, 0.07 for step 1). Outcomes: **A** (3 confirmed and profitable,
one effect: trend following, and it holds on 12 unseen coins); **B** for brief 011 (real reversals, none paying);
**F** for 5 of 7 briefs (the catalogue lacks components: a bar's volume against its average, above all); **D** (two
chain defects found and fixed: an untested idea counted in a line's record; an interrupted idea counted as tested).
