# Review of the v2 guided tour (direction, 2026-11-08, rewritten after the operator's reading)

Runs read, PRs merged, blocks in the registry: one run under the current rules (`runs/real_01_daily_breadth_fold_a/003`: 10 ideas, none passed either test), nothing merged to master, nothing on the shelf that counts. Sources: the eleven stop files. The inspector's findings are code reads, not checked by a second pass; where one would change a ruling I say so. This review proposes; the operator rules.

## Words used below, defined once
- **An idea** is one sentence about the market that can be tested with numbers, written by the ideas model from your brief.
- **The idea's number** is a quantity the idea's code computes at each bar's close from past bars only (for example: the last three days' move divided by the usual daily move). Positive means the idea expects the price to go up, negative down, and a bigger value means a stronger expectation. In the files this is called `strength`.
- **The engine's position size** is what the trading engine makes of that number: it divides it by its usual size over the past 500 bars, scales it so the usual size is 10, and cuts it at 20. That becomes the position: 10 is 100% invested, 20 is 200%. In the files this is called `forecast`.
- **Test 1** asks: did the idea's number rank the next returns? It is a rank correlation, computed on the engine's output files, between the position size at each bar and the return over the idea's horizon. Pass if the correlation is at least the idea's own threshold, with the same sign in 5 of 6 windows, on at least 30 bars.
- **Test 2** asks: did the book make money? Net return positive in 5 of 6 windows, median window Sharpe at least 1, worst window drawdown at most 20%, at full size or at a 20% volatility target.
- **The book** is the sequence of positions the engine took and their result.
- **The two rules** you set on 2026-11-06: the engine is the only thing that reads price data, so both tests are computed from its output files; and positions are graded, never on-off.

## The verdict
v2 does what its pages say in one place and not in four others. Its sequence is right: brief, ideas, the engine runs each idea, two tests on the engine's output, the analyst reads the result, one next idea. The two rules are respected in the files today, but nothing in the code would stop a violation: the checks on the idea's code are a short list of forbidden words. The one step you asked to read the book is given the book only when the idea already passed test 1, which is the opposite of when it is needed. The records mix the results from before the clean-up with the live ones without a mark. Every result so far is one fold, one brief, no pass. What follows is five decisions and then a short build of small changes.

## Your four questions

**Stop 01. Briefs carry workflow details. Why, and what to do.**
Why: v2 has no brief format and no check of a brief. The only rule is one README line saying four fields are read. The real brief is the v1 brief pasted under a v2 head, so it carries v1 words (criterion menu, profitability bars, step 1a, blocks) that nothing in v2 can act on. The ideas model is told to read the whole brief as its scope, so those words become scope.
Challenge: the pasting was my shortcut; the missing format is the cause. Also found: the code reads two head fields (product, bar size), not four; the venue field is read by nothing (Kraken is a constant in the engine step); the fold is a command-line option, not a brief line, although it decides which months the idea is judged on; the fee is written in three places with three values and the brief's is read by nothing.
Proposal: a one-page brief format with exactly the fields code reads (goal, product, bar size, fold), a prose limit, and a refusal with a reason when the head is malformed. The v1 tour asked for the same at its stop 01.

**Stop 03. Can the ideas call produce your three kinds of idea?**
Only the first kind, "a signal predicts the next return". Run 003 shows eight well-formed ones.
The second kind, "an indicator identifies a market state", cannot be tested: the only test is the correlation of the idea's number with the next return, and no comparison between state and non-state bars is computed. The format has an `event` flag meant for this, but test 1 uses it only to choose which bars to correlate on, not to compare against the others.
The third kind, "one exit closes too late, another compensates", has no field and no test. The engine holds a position for as long as the number says, rebalanced every bar; there is no exit an idea can name.
Why the format is like this: on 2026-11-06, to make every idea linear and testable the same way, we fixed one test for all ideas. That choice was never written as a choice.
Challenge: one test is simple, but it means your kinds two and three cannot enter the pipeline at all. Either you accept that v2 tests signals only, or a second test (correlation on state bars against the others) is added for kind two. Kind three needs the book to have a horizon first (see stop 05).

**Stop 05. The order idea, test, config, test 1. Should ideas be tested on the forecast only?**
What exists in code: the idea's code computes the number; a fixed template turns it into an engine config (the same template for every idea: standardise, 20% volatility target, 5 bps per side); the engine runs it; test 1 and test 2 read the output. No model writes a config.
Why the template is fixed and the prompt says "do not design the strategy config": because v1's config-writing step (1b) was a model call that mostly copied its input and cost money; and because under the linear rule the idea's number is the whole signal, so the only design left is sizing and costs, which should be the same for every idea so that ideas are comparable.
Challenge: that reasoning holds for sizing and costs. It does not hold for the holding period: the idea states a horizon (3 to 20 bars), test 1 measures returns at that horizon, but the book rebalances every bar and ignores it. So the book being judged is not the book the idea describes, and every book in run 003 was 97 to 99% invested and paid 5% to 134% of its gross in fees. The engine already has a smoothing operation that could use the idea's horizon.
On your question: test 1 today uses the engine's position size, not the idea's number. The two differ because of the 500-bar scaling and the cut at 20, which in run 003 flattened 6% to 70% of bars. The idea's number is in the same output file. Testing the idea on its own number, and the book on the engine's, is one more line in the same loop and gives the clean separation you describe. The design is clear; it is written on no page, and the README's step "Config (AI, then code checks)" is false.

**Stop 06. What the event flag is; how one correlation tests any idea.**
The event flag marks the bars test 1 uses. In run 003 every idea set it to all bars, so it changed nothing. One correlation tests one thing: does the idea's number rank the next return. Ideas of the first kind are tested; the others are not, by construction. This is the choice of 2026-11-06, named on no page.

## Findings that bear on the two rules
**The checks are a list of words.** The idea's code runs inside the engine. The only check before it runs is a list of forbidden strings (`import`, `open`, `exec`, `eval`, `shift(-`). Reading a file with pandas, importing by another spelling, or using a backward fill all pass. Why it was built so: speed, on the night, with an honest model in mind. Challenge: the rules were written as properties of the system; here they are properties of the model's behaviour. The engine's structure allows a real test at low cost: run the idea's code on the history minus its last bar and check that earlier values do not change. That test catches any lookahead whatever its spelling.
**Graded positions are not bounded.** The cut at 20 means any number above twice its usual size becomes the maximum. In run 003 between 6% and 70% of bars sat at the maximum depending on the idea. At 70% the book is mostly a switch. Nothing reads that share except the analyst. Challenge: if the linear rule matters, a bound on that share belongs in code (refuse above a threshold, or widen the cut).
**The idea sets its own passing threshold.** The model writes `min_effect`; no floor exists. Why: "the idea judges itself" was the review's Level 0. Challenge: the model that writes the idea also sets how high its own bar is. One fixed threshold in code, the same for all, keeps the "written before the data" property and removes the conflict. You deferred the related "5% noise" question; this is the cheap half of it.
**The model call is one setting short of v1's closed book.** v1 found that `tools=[]` does not remove tools added by the user's own configuration and set one more option. v2 did not carry it. On your PC the ideas model could be offered file or web tools. One keyword.

## Findings on design
- **The analyst is denied the book when it matters.** You ruled it reads the backtest output. The runner gives it the book summary only for ideas that passed test 1; in run 003 nothing passed, so neither analyst call saw a book. It also strips exposure and cost drag from what the analyst sees, the two numbers a practitioner reads first. Why: a shortcut to keep the prompt short. Challenge: the condition contradicts the ruling; remove it.
- **The analyst found a measurement problem twice and nothing kept it.** Per-window correlations were consistently one sign while the pooled correlation was near zero. Pooling ranks across windows whose scale drifts can hide an effect that holds in every window. Decision needed: test 1 on the pooled correlation, or on the median of window correlations.
- **A consistently wrong-way idea is thrown away silently.** Six windows the wrong sign is a finding; the record says only "fail".
- **Test 2 details.** Two accounting bases in one test; a drawdown measured per window where your brief said whole-test; a 20% volatility target chosen in the night when your brief said 40%; a failing idea's headline is always the worse of its two books.

## Findings on records and pages
- 574 results from before the clean-up and 14 live ones share one "already tried" list, and all go to the ideas model as "do not repeat". Run 003 avoided two calendar ideas because they "already failed" under the deleted judge. A void mark per row, or a purge.
- Live ledger rows carry no run name; refused runs write none. A refused run folder is resumed and refused again at every launch until a hand intervenes.
- Two rules on the README's first page have no code: atomic writes, a budget per day. "Continuously" has no mechanism: the runner runs one brief and stops.
- The README's status paragraph holds two states of the same day; two steps of "The path" are false.

## Five decisions, each with my proposal
1. **Test 1 on which number.** Proposal: on the idea's own number, with the engine's position size as information beside it. Reason: the idea should not depend on an engine constant to be judged right or wrong.
2. **The horizon in the book.** Proposal: smooth the position over the idea's horizon with the engine's own operation. Reason: the book should be the book the idea describes, and fees are the first enemy in every run so far.
3. **What the analyst sees.** Proposal: the book summary for every idea that reached the engine, with exposure and cost drag. Reason: your ruling; the condition contradicts it.
4. **The passing threshold.** Proposal: one fixed value in code for all ideas; the model stops writing it. Reason: the writer of the idea should not set its own bar.
5. **The brief.** Proposal: a format of the fields code reads, a prose limit, a refusal with a reason. Reason: the brief is the one thing you write, and today nothing checks it.
Set aside for now, by your earlier words: a second test for state ideas; the queue and the budget; the holdout path.

## The build after the decisions: small changes, no new piece
The lookahead test by re-running the idea's code on the history minus its last bar. A stricter forbidden list. A bound on the share of bars at the maximum. The missing closed-book setting. A void mark on the pre-clean-up rows; run names and refusal rows in the ledger; a resume rule that skips a refused folder. One accounting basis for test 2; the better book as the fail headline. The README's stale lines. Deletions: the unused checker file, the component's unused horizon parameter, the format fields nothing reads, the sparse example, the test-only options, and the forty void briefs and forty void run folders moved out of the live folders.

## On the tour
Your note holds: the speeches matched the files and buried the decision under the parts. The next tour's prompt now asks, before any file name, what the element decides and what goes wrong without it. The direct answers were the useful part; the speeches should have read like them.
