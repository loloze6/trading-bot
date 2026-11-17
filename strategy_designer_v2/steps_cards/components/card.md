# Step card: components (2026-11-17: built, not validated)

A step outside the chain of steps 1 to 7: it does not test an idea, it gives the bot the measures step 3 lacked to
test one. `loop` calls it on its own (see "When it is called"). It changes `trading-bot/` (shared code) under the
operator's standing go (2026-11-17): a component built through this card, its checks and its proof passed, may be added
on the working branch; merging into master stays the operator's go, with the build record (CLAUDE.md).

Its card has sections a step card usually has not ("When it is called", "Unblocking"): like `loop`, it is called by
another function and changes what that function does next.

## Business objective, one question
Which components must the bot gain so that the ideas waiting for them can be tested?

**Establish, for each wish step 3 wrote in a run, whether the bot already has the measure, can gain it, or cannot; add
the component when it can; so that the blocked ideas are unblocked and the run goes on.**

## Input
One wish at a time, closed book:
- **the wish:** one line of a run's `03_test_plan/<run>/plans/COMPONENT_WISHLIST.md` (its name, what it computes, from
  which bar columns, how its value grows, which part of the idea it measures), with its plan id;
- **the catalogue as it stands** (`03_test_plan/helper/reference/component_catalogue.md`), with the components built
  earlier in the same call of the step;
- **the component contract** (the base class `SubStrategyComponent`: `update`, `is_ready`, `get_required_periods`,
  `raw_value`) and one existing component as the worked example.

## Output
One answer per wish: **built**, **exists** or **cannot build**. For built: the class (or the setting added to an
existing class) in `trading-bot/strategies/strategy_components.py`, its hand computation test, its catalogue row. For
every answer: one line in `components/INDEX.md`.

## What a wish is
**A wish is what step 3 wrote when it refused an idea as missing-components: one measure a part of the idea needs and
the catalogue does not give.** An idea's refusal holds one wish or more (brief 012's ideas: a volume measure and a wick
measure).

## What a component is
**A component is one measure of the market, computed at a bar's close from the coin's own bars (or a feed) up to that
bar, that a config can use as a forecast source or in a regime rule.** Five rules:
1. **One measure, named by what it measures**, never by the idea that asked for it. Two wishes for the same measure get
   one component. The same quantity against another base, window or statistic is the same measure: one component, the
   base a setting (operator, 2026-11-17: the more standard and reusable, the better; exercise 1 built the lower wick
   over the range and over the price as two classes, merged into `LowerWickComponent`). A measure's mirror (its
   negative, or 1 minus it) is the same measure: exists when a config step gives it exactly (`negate` gives the
   negative; `standardise` divides by the past mean size without centring, so nothing gives 1 minus it), otherwise a
   setting on the same component (exercise 2: the share of bars with RSI below its midline, `side: below`).
2. **A setting is added only when a wish needs a value the component does not have, and that value changes its
   output on real data**; its default keeps the component's output as it was. A setting that changes nothing on real
   data is not added: the answer is exists (exercise 2: where an RSI of exactly 50 counts). One setting per purpose:
   two ways of doing one job (two ways to centre a value) are one setting with one value per way (operator,
   2026-11-17; exercise 3: `centred` and `log` on `VolumeRatioComponent` became `form`).
3. **Graded**: its value grows with what it measures (step 3 refuses an on/off forecast).
4. **A value on every bar of real data once warm**; no value (NaN) only where the data itself is missing.
5. **No lookahead**: the value at bar t uses only rows up to t; its docstring carries the "why this can't leak" note.

## The three answers
- **built:** no component gives the measure; the model writes it (a new class, or a setting on the class that gives the
  nearest measure), and it passes every check in code.
- **exists:** a component, with given settings, already gives exactly the measure. Nothing is built. It is also a
  finding on step 3, which should have found it: recorded in the line; fixed in step 3 if it repeats.
- **cannot build:** the measure needs data not in the coin's own bars or feeds, or the model does not know how, or its
  code still fails the checks after three attempts. Nothing is added; the idea stays blocked. Its index line holds the
  reason, so the wish is not asked again on every call (the operator decides what to do with it).

A measure that combines components in a way the config cannot (the config averages components, it does not multiply
them) is a measure like any other: built as one component.

## The index line
`components/INDEX.md`, one line per wish answered, for every run:
`<run> | <plan id> | <wish name> | built: <class> (<settings>) | exists: <class> (<settings>) | cannot build: <reason>`
- For: what each wish became, and which wishes are still open.
- Used by: `select_next` (which blocked ideas are unblocked), the operator.
- Without it: a wish is answered twice, or a blocked idea is never unblocked.

**Still open** = the wishes in the runs' wish lists with no line in the index: computed by code when needed, never
written by hand. The runs' wish lists are never changed: they are the runs' record.

## When it is called
**By `loop`, on its own**, between two ideas (after an idea's step 7, before `select_next` chooses the next one;
nothing is running then):
- **every 10 turns** of the run since the step was last called (counted from the run's own files, so restarts and
  resumes count right);
- **before the loop stops for "no candidate left"**, when the run has open wishes: what it builds can give the loop
  candidates again.

It answers **the open wishes of the run in progress**: the wishes step 3 wrote for that run's ideas (the brief's ideas
and the lines' ideas, every idea the run tested), not yet in the index. Its cost counts in the run's budget.

**By the operator**, naming one or more runs: their open wishes (for example the wishes of runs made before this step
existed).

## How to call it
One command, the same for `loop` and for the operator:
```
python3 components/helper/build_component.py --runs NAME_run [NAME_run ...] --python VENV_PYTHON [--model MODEL]
python3 components/helper/build_component.py --runs NAME_run [NAME_run ...] --list
```
- `--runs`: the runs whose open wishes are answered (`loop` passes the run in progress).
- `--python`: the venv that runs the checks and the proof.
- `--list`: prints the open wishes of those runs (run, plan id, wish name), with no model call and nothing built.
Called again, it answers only the wishes still open: a wish with a line in the index is not asked twice.

## Unblocking
**An idea refused as missing-components is unblocked when every wish of its refusal is answered built or exists, and
the catalogue has changed since the refusal.** `select_next` then counts it as a candidate again, and `run_idea` calls
step 3 again for it: its new answer replaces the refusal (the refusal stays in the journal). An idea with one wish still
open, or answered cannot build, stays blocked.
- **Why the catalogue must have changed:** step 3 writes the catalogue's version in each plan's header. A refusal
  written with the catalogue as it is today would come back the same: step 3 missed a component it had (a finding on
  step 3, in its index line). Without this, such an idea would be unblocked and refused again without end.

## Checks in code (each build)
The same for every component, by a standard harness the model does not write (`trading-bot/tests/component_harness.py`):
- not ready before `get_required_periods()` rows, ready at it;
- the model's hand computation, which uses only the rows up to bar t, matches the class on several bars and settings
  (no lookahead is by construction: the engine hands a component the rows up to bar t only; this check makes sure it
  reads the right ones);
- on every cached coin's real data, a value on every bar once warm;
- the engine runs it in a config, and the config validator accepts it, as a forecast source and in a regime rule;
- every class in the file has one catalogue row, and the catalogue's class count is the file's;
- a class given a new setting: its output at the old defaults is unchanged on real data, and its output at the wish's
  settings differs, on real data, from the output without the new setting (rule 2);
- **proof:** one fixed backtest rerun with the new code gives the same files as its record (allowed differences: run
  ids, times, temporary paths); the bot's suite passes.

A failed check goes back to the model with its output (up to three attempts); then the answer is "cannot build".

## Storage and naming
```
components/
  card.md                this card
  INDEX.md               one line per wish answered, every run
  journal.jsonl          one line per wish: run, plan, wish, answer, USD, seconds, attempts
  helper/
    system_prompt.md     the instructions
    build_component.py   one call per open wish; writes, checks, proves or undoes; the index and journal lines
    wishes.py            the wishes, their answers, the open ones, the unblocking rule (used by select_next, run_idea)
    test_components.py   the tests of this code (a fake model call)
  builds/<class>/        per component built: the calls' answers, the checks' output, the proof
  validation/reading.md  once validated
(in trading-bot/: the class in strategies/strategy_components.py; its spec, the settings and the hand computation, in
 tests/built_components/<class>.py; the standard checks in tests/component_harness.py, run on every spec by
 tests/test_built_components.py; its row in step 3's catalogue)
```

## The AI
- **Closed book**, one call per wish: the wish, the catalogue, the contract and the example are pasted into the call.
- **The model** reads the wish against the catalogue, gives one of the three answers, and for built writes the class
  and one hand computation. Every other check is code, so the model never writes the test that judges it.
- **Model:** Opus (exact formulas, code). **Cost:** to be measured (the catalogue is most of the input, cached).

## Quality criteria
- One component per measure: no two components for the same measure.
- An answer the catalogue proves: exists names a class and settings that give exactly the measure; built adds what the
  catalogue lacks.
- A built component passes every check, and the proof shows nothing else changed.
- A cannot build names what is missing.

## Fixed inputs for the iterations
The open wishes after volume_run: a past high or its break, RSI's time above or below its midline, a price-RSI
divergence, a bar's wick or place in its range, a move held over the next bars, a mean of several bars' volume against a
longer mean, a scaled move times its volume ratio, volume against the median of the bars before t. And the wishes
`VolumeRatioComponent` answered, which must come back as exists.

## Variants compared
To set: Opus or Sonnet.

## Who judges the output
Code judges each build (the checks). The operator judges the card's validation.

## Validation (once, while the card is designed)
On the fixed inputs, twice in a row:
- **quality of the components:** every built component passes every check;
- **standardization:** one component per measure, named by it; the same docstring and checks for every component; the
  answered wishes come back as exists;
- **unblocking:** the blocked ideas are rerun; count those step 3 now plans.
Status: exercises 1 to 3 (`exercise_1/`, `exercise_2/`, `exercise_3/`): quality met (every build passes every check and
the proof, twice); unblocking met (46 of 49 refused ideas unblocked; the automatic path proven on night_rsi_run);
standardization: two findings for the operator (exercise 3).

## What it changes elsewhere (each in its own card)
- `loop`: the two calls (every 10 turns; before stopping for no candidate; never twice without a turn between); its
  spend counts the calls.
- `select_next`: an unblocked refusal is a candidate again.
- `run_idea`: step 3 called again for an unblocked idea.
- step 3: the catalogue's version in each plan's header (code only).

## Proof of the build (2026-11-17)
- Tests: this step's 6, loop's and select_next's new ones; the cards' suite passes (57); the bot's suite passes (1,518,
  with the harness run on `VolumeRatioComponent`, the first spec, which passes every check, real data included: 19
  coins, 13 s).
- Nothing that runs today changes: `select_next`'s ranking of all 11 runs, old code against new, is identical (426
  lines); the proof machinery run once: 588 files identical, the bot's suite passes (2 minutes).
- Not run yet: a real call of the step (its validation, on the 57 open wishes of the 11 runs).

## What this step does not do
It does not test an idea, choose which ideas to run, change a component's output at its defaults, or change how the
config combines components.
