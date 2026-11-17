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

