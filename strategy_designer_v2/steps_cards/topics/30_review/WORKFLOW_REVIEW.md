# What the hourly story says about the research workflow: a review (2026-11-20)

Asked by the operator: "based on the story line, make a deep review and suggest the main improvements to the research
workflow; step back and think cleverly." Source: `STORYLINE.md` (the same folder) and the runs it links. Proposals only:
nothing here is built.

## The one-sentence diagnosis
The workflow asks two questions, "is the effect real?" (step 5) and "does the book pay?" (step 6), and it learns from
neither in a way that changes what it tries next. Between them sits a question nobody owns: **is this effect large enough
to trade, the way the book will trade it?** Most of what went wrong on hourly bars sits in that gap.

## Seven weaknesses, from the story
| # | Weakness | Evidence (story line) | Where it lives |
|---|---|---|---|
| W1 | **No one owns "is it tradeable".** An idea is written, tested and confirmed without anyone asking whether its move pays for a trade | 22 hourly ideas confirmed, 0 profitable; moves of 4 to 13 bps against a round trip of 21 (1.1, 1.3) | steps 1, 2, 3, 7 |
| W2 | **The test does not measure what the book trades.** Step 3 dropped the idea's holding period; step 5's measure and the book's bets differ | 2.4; 2.7: 2 confirmed ideas whose bets lose against the drift | steps 3, 5 |
| W3 | **What one step learns does not reach the others.** The analyst named the costs 38 times; the selection did not follow, and the next briefs and ideas did not know | 2.1, 2.2 | step 7, select_next, steps 1 and 2 |
| W4 | **Nothing is carried from one run to the next as knowledge.** "Hourly moves of 1 to 4 bars cannot pay", "a round trip costs about 21 bps", "daily ideas pay on hourly bars when held": all in topic cards for people, none in what the steps read | the whole story; findings repeated by hand | `common/`, the briefs |
| W5 | **Shared rules are built before their cases are written.** The holding rule's 3 defects were found only when the operator asked for a check case by case | 3.2 | the engine, shared code |
| W6 | **Every question costs a full backtest.** No cheaper way to answer "what if", and a cut backtest restarts from zero | thread 4; replays answered several questions in seconds where the record allowed | step 4, the record, the runs |
| W7 | **The same years judge more and more variants.** Holding rules, windows, more coins, reruns: all on folds A to D; the unseen dates disagree often (the 2016-17 bull market) | 1.5; topic 31 | step 5, step 7, the folds |

## Improvements, grouped by what they change
### I1. Make "tradeable" a notion every step reads (answers W1, W2)
- **One definition in `common/`: the edge of a bet.** The move the idea predicts from the bar after its signal, over
  its horizon, net of the coin's drift, against the cost of a round trip (measured, about 21 bps on the venue now). Steps
  1 and 2 aim at it, step 3 tests it, step 5 measures it, the diagnosis reads it.
- **Step 5 measures on the book's own bets.** The verdict's main measure is computed on the bets the book takes (the
  same rule as the holding period: a rise of the forecast of at least the band, held for the horizon), so "confirmed"
  and "the book's bets earn" cannot disagree (fixes 2.7 at the root).
- **Step 3 cannot drop what the idea claims:** horizon, side, condition. Already done for the horizon (2.4); the same
  rule for the rest, written in step 3's card.
- Gain: the workflow stops spending runs on ideas that cannot pay, and stops confirming ideas the book does not trade.
  Effort: medium (a definition, step 5's measure, prompts). Risk: step 5 changes its verdicts, so its proof is a rerun of
  past verdicts with the counts that change.

### I2. Close the learning loop (answers W3, W4)
- **A findings register that the steps read**, next to the shared definitions (`common/findings.md`): short, dated,
  measured statements with their evidence. For example: "on 1h, ideas of 1 to 4 bars capture 4 to 13 bps, a round trip
  costs about 21"; "a daily idea held for its horizon pays about as well on 1h". Steps 1, 2 and 7 read it, the way they
  read the definitions. Each entry is added by a run's reading, on the operator's go. Findings stay open to new evidence
  (a finding is not a rule).
- **Step 7 gets the diagnosis** (decided): the analyst sees size, timing and trend in numbers, and its proposals aim at
  the weakest reading.
- **select_next follows what the analysis says**, not only scores: a line whose analyses name the same blocker several
  times gets its ideas tested (the 7.d case). Topic 32 holds the question; this gives it a reason.
- Gain: the next brief does not repeat what is known. Effort: small for the register, medium for step 7. Risk: a wrong
  finding steers many runs, so each entry carries its evidence and date and can be withdrawn.

### I3. Use finer bars for what they are good at (answers W1, a new direction)
**Tested on the records (2026-11-20, `runs/RETRO_DIAGNOSIS_RUN.md`): not supported as it stands.** On 12 daily ideas also
run on hourly bars, the daily version captured more per bet 10 times out of 12. A real test needs a plan that enters
once, when the daily condition first holds during the day; none of the records did that.

The story shows two things hourly bars do well:
- **They time the entry of a daily idea.** Paying continuation books move 100 to 120 bps on the signal's own bar
  (opening time), and their move runs past the horizon.
- **They let a book act during the day**, where a daily book waits for the close.

So, besides "hourly-native ideas" (mostly too small), a second kind of brief: **a daily idea, its condition watched
hourly, entered when it becomes true.** That is the same edge, caught earlier, a move per bet a daily book cannot catch.
It needs no new engine rule: the plan states the daily condition on hourly closes. Gain: possibly the first edge that
hourly bars add, not just keep. Effort: a brief (step 1) and the step 3 guide. Risk: none for the workflow; it is a
research direction to test with one brief.

### I4. Specify shared rules by cases first (answers W5)
- Every new rule in the engine starts as its cases (the definition's expected position bar by bar), written before the
  code and kept as its tests (as `core/holding_period.py` now does).
- Every run checks the engine against the rule on its records (check C): a replay from the recorded inputs, 0 bars
  differing. That is a standard check, not a review tool.
- Gain: defects found before a night of runs, not after. Effort: small per rule. Risk: none.

### I5. Answer questions cheaply before backtesting (answers W6)
- **Record what a replay needs:** each component's raw value on every bar (today only where its regime is active, so a
  regime-gated book cannot be replayed). A replay then answers questions on windows, sizing, holding, the band and
  costs in seconds, as information before a backtest (no gate).
- **Rerun only what can change** after an engine change (used once, saved hours): written as a rule in the run
  function's card.
- **A cut backtest resumes per coin and fold** instead of restarting from zero (since change C, one call per coin and
  fold exists to build on). With parallel sessions and the operator's CLI (topic 37), long runs stop being cut.
- Gain: hours per question become seconds or minutes. Effort: medium (recording is shared code: proof, go). Risk:
  records grow; only the columns replays need.

### I6. Protect the judgment as variants multiply (answers W7)
- **Count the variants judged on the same folds**, in each run's reading (visibility, no ledger, no gate): how many
  versions of this idea and its rules have seen folds A to D.
- **Topic 31's question becomes urgent:** choose on some folds, judge on others. Step 7.g picked the best hour in the
  record and was judged on the same years, which flattered its t.
- **The unseen dates are read by market regime:** "beats holding" fails in strong bull years (2016-17, holding Sharpe
  about 3.7) for any long book. The test should say whether a book holds against the market of its period, not only
  against one number.
- Gain: results that hold outside the years that chose them. Effort: medium. Risk: fewer ideas pass; that is the point.

### I7. Look past single books (a direction, for later)
The paying books are mostly one family: long, trend-following, half of their gain the market's. The workflow judges each
book alone. Briefs aimed at what the current paying books lack (two-sided, mean reversion, falling markets) and a view
of books together (topic 08's observe-and-advise) would show whether a new book adds anything. For later: first make
single books trustworthy (I1, I6).

## Recommended order
| Order | Improvement | Why first |
|---|---|---|
| 1 | **I1: "tradeable" in `common/`, step 5 on the book's own bets** | The root of most of the story: ideas confirmed that cannot pay, a test that does not measure the book |
| 2 | **I2: findings register, step 7 reads the diagnosis** | Without it the next brief repeats the hourly lesson; cheap to start |
| 3 | **I3: one brief "daily idea, entered when its condition becomes true on hourly closes"** | The cleverest open question: what hourly bars can add, not only keep |
| 4 | I4 and I5 | They make every later run safer and cheaper; partly in place (cases for the holding rule, speed A to D, parallel sessions) |
| 5 | I6, then I7 | Needed before trusting a winner; I7 once single books are trustworthy |

Not recommended now: a lower Calmar threshold for 1h, a minimum horizon on 1h, tuning horizons from the data (patches or
look-ahead in disguise; story line 1.4, 1.5, 2.5).
