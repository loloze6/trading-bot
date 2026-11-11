# Step card 3: Test plan (2026-11-10)

## Business objective, one question
How will we know whether this idea is real?

## Input
One idea from step 2, with its brief.

## Output
One test plan per idea, with one of three outcomes: **plan**, **untestable** or **missing-components**.

## What a test plan is
**A test plan is the one way we will check an idea against the market data, fixed before we look: what we measure, against what, on which data, and which result would confirm the idea and which would reject it.**

- **One test per idea.**
- **The vessel is the strategy config:** the test is a config the engine runs. Its hard rules apply:
  - every forecast is graded (no on/off);
  - `standardise` is the first transform of every component;
  - a regime (an on/off condition around a graded component) only when the idea itself is a condition;
  - no constant inside a regime.
- **Fidelity comes first.** The idea is split into three parts:
  - **the situation:** what the market shows at a bar;
  - **the comparison:** what the situation or the outcome is judged against, if the idea has one;
  - **the outcome:** what the price does next, and which way.

  Each part is **kept** (measured as the idea states it), **adapted** (the same thing, in the only form the config's logic allows) or **replaced** (a different quantity). The allowed adaptations are those the guide's design principle and its list of what the config cannot express force: a threshold or on/off condition made graded, "after X" made "while X", a holding period dropped. Settings from the brief or from convention are not adaptations.
- **The verdict transfer:** "if this test confirms, is the idea confirmed; if it rejects, is the idea rejected?". It is yes only if both answers are yes.
- **The three outcomes:**
  - **plan:** no part replaced, and the verdict transfer is yes. Its **fit** is *exact* when every part is kept, and *adapted* otherwise. Code works the fit out from the fidelity lines.
  - **untestable:** a part needs something outside the config's logic: another coin, data not in the coin's own bars or feeds, or anything the guide says the config cannot express.
  - **missing-components:** everything is in one coin's own bars or feeds and the config's logic could hold it, but no catalogue component computes a part, alone or combined. The idea goes in the component wish list.

  Neither refusal is a failure. A plan is never forced by replacing a part.

## What a forecast is
**The forecast is a number computed at each bar's close, for one coin, from the idea's indicators. It sets the position the idea calls for: the share of the portfolio held in that coin. Positive means long, negative means short, and the size grows with how strongly the indicators show the idea's situation. Zero means no position.**

- The chain: indicators → forecast → position. A change in the forecast changes the position: it opens, adds to, reduces or closes it.
- The price move times the position gives the portfolio's gain or loss on that bar. The portfolio's value rises when the position's side matches the price's direction.

## The fields of a test plan
**Header, written by the script:**
1. **idea, brief**
   - For: what is tested, and from which theory.
   - Used by: step 4, step 5, the operator.
   - Without it: a result cannot be traced to its idea.
2. **data-instruments, data-bar, data-period:** from the idea's header, else the default: BTC, ETH, LTC, XMR, XRP, ZEC (the cached coins with data in all four folds), 1d, folds A, B, C, D (24 windows). One idea has one bar size, decided before the test (`--bar` exists for exercises only). The model is told them; it does not choose them. The config has no key for them.
   - For: where and on what bars the test runs.
   - Used by: step 4.
   - Without it: step 4 picks the data, and the plan's settings (which depend on the bar size) may not fit.
3. **outcome:** plan, untestable or missing-components.
   - For: whether the plan goes to step 4.
   - Used by: step 4, the index.
   - Without it: a refusal has to be read to be recognised.
4. **fit** (plan only): exact or adapted, worked out by code from the fidelity.
   - For: at a glance, whether the test is the idea exactly or an allowed adaptation.
   - Used by: the operator, step 5.
   - Without it: an adapted test can be read as the idea itself.

**Body, from the model:**

5. **Fidelity** (always): one line each for the situation, the comparison and the outcome (the idea's part, then kept, adapted with how, or replaced with by what), and the verdict transfer (yes or no, with one sentence).
   - For: the proof that the test is the idea, or the part that stops it.
   - Used by: the operator, step 5; code checks that it agrees with the outcome.
   - Without it: a test of a different idea can pass as this one.
6. **Reason** (refusals only): why it cannot be built, in one or two sentences.
   - For: the refusal, explained.
   - Used by: the operator.
   - Without it: a refusal cannot be challenged.
7. **Forecast** (plan only): the forecast the config computes, in plain words.
   - For: the config, readable without JSON.
   - Used by: the operator, step 5 (which bars carry a position).
   - Without it: only the JSON says what is traded.
8. **Config** (plan only): the file name of the strategy config.
   - For: the test, in the engine's language.
   - Used by: step 4.
   - Without it: nothing to run.
9. **Criterion** (plan only): horizon (bars), main measure, supporting check (or none), confirm (with its number), reject, inconclusive (with the minimum count).
   - For: the result that confirms or rejects, fixed before the data.
   - Used by: step 5.
   - Without it: any result can be read as a success.

**Two more outputs:**

10. **The index line** (`INDEX.md`): `<plan id>: plan (fit: exact|adapted) [data]`, or `<plan id>: untestable|missing-components: <reason, first words> [data]`.
11. **The wish-list block** (`COMPONENT_WISHLIST.md`, missing-components only): `## <plan id>`, then one line per component: its short name, what it computes, from which bar columns, how its value grows, and which part of the idea it measures.
    - For: the components to add to the engine, with the ideas waiting for them.
    - Used by: the operator, to decide what to build.
    - Without it: missing components are lost in the plans.

## Storage and naming
```
03_test_plan/
  card.md                      this card
  helper/
    system_prompt.md           the helper's instructions
    make_test_plan.py          one closed-book call; checks the answer; saves the plan, its config, its index line, its wish block
    check_plans.py             code checks on saved plans, for the readings
    reference/                 trimmed copies of the strategy config guide and the component catalogue
  plans/
    INDEX.md                   one line per plan
    COMPONENT_WISHLIST.md      one block per missing-components plan
    REVIEW.md                  the review of a real run
    run_log*.txt               the logs of real runs
    NNN-KK_short-name_<bar>.md one test plan per idea and bar size
    NNN-KK_short-name_<bar>_config.json   its config (plans only)
  exercise_k/                  the comparison exercises
```

## The AI
**Closed book**, as in steps 1 and 2: one call per idea. The two trimmed references are in the system prompt; the idea, its brief and the data are in the request.

**The references** are trimmed copies of the originals in `strategy-research/docs/`. Everything that does not help write a config was removed:
- pipeline stages and decision numbers;
- the block manifest and the block combiner;
- the campaign sizing block.

Three passages were aligned with this card: regimes only when the idea is a condition, and `standardise` sets the scale, never `vol_target`. The copies must be refreshed by hand when the originals change.

**Checks in code** (`make_test_plan.py`). It refuses only a major deviation:
- a fidelity line missing, or one without kept, adapted or replaced;
- a verdict transfer without yes or no;
- an outcome that is not one of the three;
- a fidelity that contradicts the outcome: a plan with a replaced part or a "no" transfer, or a refusal with neither;
- for a plan:
  - an unreadable config;
  - a config without `regime_detector` or `strategies`;
  - a class or param the catalogue does not list;
  - a missing forecast, horizon, main measure, confirm or reject;
- for a refusal: no reason; for missing-components: no component line;
- a field over 300 words.

Up to three attempts. The script tells the model the data's windows (from the fold, no dates), and that warm-up bars are loaded before each window.

**Model.** Opus. In exercises 1 and 2, sonnet twice changed the idea's side and wrote "clearly" where a number was needed.

**Cost.** The references are most of the input. They sit in the system prompt, so they come from the model's cache once a call has been made in the last hour: 0.01 to 0.08 USD per idea. A call with a cold cache costs about 0.26.

**Prompt**: `helper/system_prompt.md`.

## Quality criteria on the test plan
- **Fidelity is filled, and it is honest:** each part's status matches what the config does, and the verdict transfer answers both questions.
- **The outcome follows from the fidelity.** A plan has no replaced part and a "yes" transfer.
  - Untestable only for what the config's logic cannot hold.
  - Missing-components only when the data is in one coin's own bars or feeds, and the catalogue's combinations were tried.
- **A refusal's reason** names what is missing. A wish block describes a component that could be built from the bars.
- **For a plan:**
  - the forecast says in plain words what the config computes;
  - the config follows the hard rules, takes the idea's side, and uses settings from the brief, else the single most common convention;
  - the criterion has one horizon in bars, one main measure and at most one supporting check, the evidence as a number, and overlapping returns counted once;
  - a reject needs evidence as strong as a confirm, in the other direction (if t ≥ 2 confirms, t ≤ -2 rejects). An estimate merely on the wrong side of zero is inconclusive. Found by step 5: six "rejected" verdicts rested on t between -0.52 and +0.24;
  - a result near zero is never a reject, even when the brief says "no difference" means wrong: it is inconclusive. Found by the runs after symmetric criteria (002-03 daily, 001-02 hourly);
  - holding is the coin's mean return over all the test's windows, never over a single window, which shares the bars that set the forecast. Found by the full-data run: a per-window mean gives t = -2.60 on random walks;
  - a rare extreme carries a position close to zero away from the extreme (the strongest graded dead zone). Found by the hourly run: the RSI-extreme books held a position on half the bars;
  - its minimum counts are counts the data's windows can give;
  - confirm, reject and inconclusive cover every result.

## Fixed inputs for the iterations
From step 2 (exercise 3, opus, and exercise 4 for 003-07), with their briefs:

| Idea | Case |
|---|---|
| `001-01` RSI high, then reversal | plan; a rare extreme; a short side |
| `001-03` RSI high, then continuation | plan; the same situation, the other answer |
| `002-01` up-cross, then drift | plan; a steady relation; the default data |
| `002-05` cross-to-cross span | plan; a state |
| `003-01` low-volume up move reverts | plan; a condition, so a regime is allowed |
| `004-01` altcoins follow bitcoin | untestable: another coin |
| `005-01` to `005-06` RSI divergence | missing-components: RSI at an earlier high or low |
| `003-07` quiet-hours moves revert | missing-components: the bar's hour |

## Variants compared
- **Exercises 1 and 2:** opus and sonnet. Opus was kept.
- **Exercise 3:** the plan in two calls (plan in words, then config). The config differed from the plan in 5 of 5 cases, so one call was kept.
- **Exercises 4 to 6:** the exact forecast first, the data's windows, one main measure, the evidence as a number, the settings rule.
- **Exercises 7 to 12:** "not close" lines, then the final helper.
- **Exercises 13 and 14:** the fidelity rule and the three outcomes, replacing the two lines of exercises 7 to 12, which named single cases. Right outcomes, but long lines.
- **Exercises 15 and 16:** one line asking for short lines. Fidelity lines about 40 % shorter.
- **Exercises 17 and 18:** symmetric criteria: a reject needs t ≤ -2 against the idea (or its mirror). 5 of 5 rejects, twice.
- **Exercises 19 and 20:** extremes held near zero away from the extreme (works); "no difference" rejects as an equivalence test (its band varied between runs: dropped).
- **Exercises 21 and 22:** a result near zero is never a reject. Both fixes hold twice; 003-07's fidelity drops part of the idea, twice.
- **Exercises 23 and 24:** each part stated in the idea's own words. The dropped part is now visible, but one plan per run still calls a replacement "adapted".
- **Exercises 25 and 26:** the prompt's list of adaptations closed, as in this card. Same outcomes twice, every adaptation one of the three.
- **Exercises 27 and 28:** holding is the coin's mean over all the test's windows; the new default data. Same outcomes twice.

Each exercise has its reading.

## Who judges the output
The operator: "if this test confirms, would I believe the idea; if it rejects, would I drop it?". Code checks the shape, the names and the agreement between fidelity and outcome. Each exercise has a one-page reading against the criteria.

## Done when
On two exercises in a row, on the fixed inputs, every plan meets every criterion. Status: met by exercises 27 and 28 (`exercise_27/reading.md`).

## Open
- **A pattern the engine refuses.** In step 4, volume plans could not run (five in the first run, 003-01 and 003-02 in the current one): their regime detector is a veto on a constant (`BuyAndHoldStrategy` with `volume_filter`), with the default regime flat. The engine stops at its warm-up check. The cause is under investigation by another agent.
- **For step 2:** 002-01 (after the cross) and 002-05 (from cross to cross) become the same forecast in this vessel; only their horizon and measure differ.
- **The default data** was BTC/USDT, 1d, fold A until exercise 26: 2 years, where t = 2 needs an annual Sharpe of about 1.4. It is now 6 coins and folds A to D (about 8 years).

## What this step does not do
It does not run the test, judge a result, or build a missing component.
