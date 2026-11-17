# Step card: components (DRAFT 2026-11-17, for the operator's review; not validated, nothing built)

A step outside the chain of steps 1 to 7: it does not test an idea, it adds to the bot what step 3 lacked to test
one. It changes `trading-bot/` (shared code), so each component it builds needs the operator's go (CLAUDE.md).

## Business objective, one question
Which strategy components does the bot lack to test the ideas waiting for them, and is each one built right?

**Establish, from the wish lists of past runs, the components the bot lacks, ranked by the ideas waiting for them, and
add each one the operator chooses to the engine: computed exactly as specified, from data known at the bar's close,
proven to change nothing else, so that the waiting ideas can be tested.**

## Input
- **The wish lists of past runs:** every `03_test_plan/<run>/plans/COMPONENT_WISHLIST.md` block (one per idea step 3
  refused as missing-components: the plan id, then one line per component asked for).
- **The component catalogue** (`03_test_plan/helper/reference/component_catalogue.md`): what exists, so that a wish
  an existing component (or a combination) already covers is not built twice.
- **For a build:** one specification the operator chose (below), the component contract (the base class
  `SubStrategyComponent`: `update`, `is_ready`, `get_required_periods`, `raw_value`) and one existing component as the
  worked example, pasted into the call.

## Output
Two outputs, one per part of the step:
1. **The wanted list** (`components/WANTED.md`): one row per component the bot lacks, with its specification and the
   ideas waiting for it, ranked by that count.
2. **A component**, once the operator chooses one row: the class in `trading-bot/strategies/strategy_components.py`,
   its tests, its catalogue row, and its proof.

## What a component is
**A component is one measure of the market, computed at a bar's close from the coin's own bars (or a feed) up to that
bar, that a config can use as a forecast source or in a regime rule.**

- **One measure, named by what it measures**, not by the idea that asked for it: "a bar's volume against its recent
  average", not "volume burst". Several ideas asking for the same measure in other words want one component.
- **Its parameters are the measure's settings** (a window, a horizon). A parameter is added only when two waiting
  ideas need two different values of it (volume_run: one bar against 30 for some ideas, the mean of 5 or 10 bars
  against 30 or 90 for others: one component with a short window, default 1). No parameter "in case".
- **Graded where it is a forecast source** (step 3's hard rule: no on/off forecast); a regime measure is bounded or
  scale-stable.
- **Defined on every bar the data gives once warm.** NaN only when the data itself is missing; the engine refuses a NaN
  loudly, so a value undefined on real data (a zero average volume, a zero range) would stop a run.
- **No lookahead:** the value at bar t uses only rows up to t (CLAUDE.md's hard rule; its "why this can't leak" note
  is in the class's docstring).

## The fields
**A row of the wanted list** (written by the specification part):
1. **name:** the class name, `<Measure>Component`.
   - For: one name per measure, reused by every later wish.
   - Used by: the operator, the build part, step 3 (once built).
   - Without it: the same measure is wished under many names (the night runs: 11 "VolumeRatioComponent", 5 other
     names for it) and nothing counts the ideas waiting.
2. **specification:** the exact output on bar t (formula, columns read, parameters and defaults), range and sign,
   kind (graded or regime measure), warm-up, what happens at a NaN or a zero denominator.
   - For: what the build must compute, fixed before the code.
   - Used by: the build part, its tests, the catalogue row.
   - Without it: the code decides the measure, and the tests check the code against itself.
3. **waiting ideas:** each idea's plan id and run, and which part of the idea the component measures (situation,
   comparison, outcome); their count.
   - For: the rank, and the ideas to rerun once built.
   - Used by: the operator (what to build first), the end check.
   - Without it: a component is built for nobody, or its ideas are never rerun.
4. **status:** wanted, built (with its commit), or not buildable (with why: the data is not in the bars).
   - For: what is left.
   - Used by: the operator.
   - Without it: a built component stays on the list.

**A component** (written by the build part): the class with its docstring (the specification, the leak note), the
standard tests, its catalogue row, its proof (below).

## The sequence
1. **Specification** (one model call, on demand or after a run): all wish blocks and the catalogue in; out: the wanted
   list. The model groups the wishes by measure, writes one specification per measure (the general form, parameters
   only where waiting ideas differ), and marks a wish the catalogue already covers. Code counts the waiting ideas and
   ranks.
2. **The operator chooses** a row (the go for the shared-code change).
3. **Build** (one model call): the specification, the contract and the worked example in; out: the class, one test
   that computes the value by hand on rows up to t, and the catalogue row.
4. **Checks in code, the same for every component** (a standard test harness, not written by the model):
   - the value at bar t is unchanged when every row after t is changed (no lookahead);
   - not ready before `get_required_periods()` rows, ready at it;
   - the hand computation matches on several bars and parameters;
   - on every cached coin's real data, no NaN once warm;
   - the engine runs it in a config and the config validator accepts it, as a forecast source and in a regime rule;
   - every class in the file has a catalogue row (the catalogue's class count is computed, not written by hand).
5. **Proof** (code): one fixed backtest rerun with the new code, compared file by file with its record; allowed
   differences named (run ids, times, temporary paths). The bot's whole suite passes.
6. **End check:** the waiting ideas rerun through `run_idea` in a new run. Step 3 now plans them, or its new refusals
   say what is still missing (a new wish, back to 1).

## Storage and naming
```
components/
  card.md                this card
  WANTED.md              the wanted list (one row per component, ranked)
  helper/
    system_prompt_spec.md, system_prompt_build.md
    make_wanted.py       the specification call; reads every run's COMPONENT_WISHLIST.md
    build_component.py   the build call; writes the class, its test and its catalogue row
    test_harness.py      the standard checks of step 4, for any component class
  builds/<Name>/         per component: the call's answer, the checks' output, the proof's comparison
  validation/reading.md  once validated
(the class: trading-bot/strategies/strategy_components.py; its tests: trading-bot/tests/; its row: step 3's catalogue)
```

## The AI
- **Closed book**, as every step: the wish blocks, the catalogue, the contract and the example are pasted into the call.
- **Specification:** model judgment is needed to see that two wishes are one measure. Code does the rest (counts, rank).
- **Build:** the model writes the class and one hand computation. Every other check is the standard harness, so the
  model never writes the test that judges it (it cannot check its code against itself).
- **Model:** Opus (code, exact formulas). **Cost:** to be measured.

## Quality criteria
- One row per measure; no two rows the same measure; no row an existing component already covers.
- A specification is exact enough to compute by hand, and covers every waiting idea's variant without a parameter
  nobody asked for.
- The built component passes every standard check, and the proof shows nothing else changed.
- The end check: the ideas waiting for it are planned by step 3, or their new refusal names a different measure.

## Fixed inputs for the iterations
The wish blocks of the night runs and of volume_run (the measures still wanted): a multi-bar volume average (2 ideas),
a past high or its break (13), RSI's time above or below its midline (several), a price-RSI divergence, a bar's wick or
place in its range (7), a move held over the next bars (2).

## Variants compared
To set: specification and build in one call or two; Opus or Sonnet for the build.

## Who judges the output
The operator: the wanted list ("is this the measure these ideas need?") and the choice of what to build. Code judges the
build (the harness, the proof). The waiting ideas' rerun judges the business result.

## Done when
On the fixed inputs: the wanted list groups the wishes as the operator would, twice in a row; two components built
through the card pass every check and the proof; and their waiting ideas get past step 3.

## Open (for the operator)
1. **One step or several?** Recommended: one step with two parts (specification, build), the operator's choice between
   them. Two separate steps would duplicate the inputs; one call for both would build before the operator chooses.
2. **When is it called, automatically?** Recommended: the specification after each run (cheap, changes nothing), the
   build only on the operator's go (it changes shared code: never automatic).
3. **One list of wanted components?** Recommended: yes, `WANTED.md`, rebuilt from every run's wish blocks. A further
   option: give step 3 the wanted list, so it reuses a name already wanted (a change to a validated step: later).
4. **Acceptance criteria:** "Done when" above.
5. **Test:** with the components still wanted (fixed inputs), two built through the card.

## What this step does not do
It does not test an idea, decide which component to build, or change an existing component.
