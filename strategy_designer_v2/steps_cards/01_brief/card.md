# Step card 1: Brief (2026-11-09)

## Business objective, one question
Which trading theory should the pipeline research?

## Input
The operator's request: nothing (a theory of the helper's choice), a theme in the operator's words, or a source the operator pastes. Or no request at all: the operator writes the brief by hand.

## Output
One brief: one theory, with its optional context. Or "not researchable", with the reason, when the request can only be met by a theory about several coins moving together: no brief is written, and no other theory is put in its place.

## What a brief is
**A brief is one theory about how a market behaves, as a claim or a question, with its reason where known and what would prove it wrong, and optional limits on where it applies.**

- The theory is the only mandatory part. The context (venue, coins, bar, period, side) is optional.
- A brief says what to research, never how: no workflow words (thresholds, step names, config settings, fees, budgets).
- A question stays a question.

## The fields of a brief
1. **Theory** (body, mandatory): one claim or one question, its reason if it has one, what would prove it wrong; the helper is told at most 250 words.
   - For: states what to research.
   - Used by: step 2.
   - Without it: there is nothing to research.
2. **venue, instruments** (header, optional)
   - For: the market the theory is about.
   - Used by: step 2.
   - Without it: no limit set on market.
3. **bar** (header, optional)
   - For: the time scale the theory is about.
   - Used by: step 2.
   - Without it: no limit set on time scale.
4. **period** (header, optional): years or fold ids.
   - For: the years the theory is meant to hold in.
   - Used by: step 2.
   - Without it: no limit set on period.
5. **side** (header, optional): long only, or long and short.
   - For: a theory about falling prices means something else if the book cannot go short.
   - Used by: step 2.
   - Without it: no limit set on side.
6. **source** (header, only when the helper wrote from one)
   - For: lets anyone check the theory against what it rests on.
   - Used by: the operator, and step 2 if it needs the original.
   - Without it: a theory said to come from a source cannot be checked against it.
7. **Index line** (in `INDEX.md`)
   - For: the list of theories already written, read before each new one.
   - Used by: the helper, for its next brief.
   - Without it: the helper writes its most typical theory again (exercise 2: four no-theme calls, one theory).

The header keys are a closed list, which keeps workflow words out.

## Storage and naming
Modelled on a pre-registered hypothesis (short, written before the data, never rewritten) and a decision record (one numbered plain-text file per decision).

```
01_brief/
  card.md                this card
  helper/
    system_prompt.md     the helper's instructions
    make_brief.py        one closed-book call; refuses only a major deviation; saves the brief; adds its index line
  briefs/
    INDEX.md             one line per brief
    NNN_short-name.md    one file per brief
  exercise_1 ... 8/      the comparison exercises
  hourly_run/, full_data_run/   the briefs of a named run: copies with header lines the operator set for that run
```

- **One file per brief**: a header of `key: value` lines, then the theory in plain prose.
- **Naming**: `NNN` is a running number; `short-name` is three to five words of the theory. The file name is the brief's id.
- **Never edited** once the pipeline has read it. A reworded theory gets a new number, so one number never names two theories.
- **Index line format**: `NNN_short-name: one or two short sentences [header lines]`. The helper writes the line; `make_brief.py` adds it. A brief written by hand needs its line written by hand.

**Example** (`briefs/004_bitcoin-leads-altcoins-lagged-response.md`, from exercise 5):
```
---
---
Large coins lead small coins over short horizons. When bitcoin makes a sharp move,
smaller and less traded coins take on part of that move only later... (prose, at most 250 words)
```

## The AI
**What it does.** It writes one brief from its own knowledge, from a theme, or from a source. It knows trading and nothing of the pipeline. One request, one call. Running it is the operator's act.

**Closed book.** One model call: no tools, no files, no web, no repository, an empty working folder, no settings. The index and the source are pasted into the call. One note cannot be removed in this cloud environment: an account note with the operator's email. It says nothing of trading or the pipeline.

**Checks in code** (`make_brief.py`). Code refuses only a major deviation: no `---` header, a header key outside the list, no theory, a theory over 900 words or an index line over 100 (guards against a runaway answer, not length rules). A refused answer is sent back with the reason, up to three attempts. Minor deviations are fixed, not refused: bold and headings are stripped, the short-name is made file-safe (at most eight words), a missing index line falls back to the theory's first words, a missing `other-theories` line is recorded as not given.

**Model.** Opus. Haiku broke rules of meaning; sonnet kept two faults the prompt forbids; opus met them all and was stable.

**Cost.** 0.02 to 0.05 USD per brief from a theme or no theme; about 0.12 per call with a long source. A retry doubles it.

**Prompt**: `helper/system_prompt.md`.

## Quality criteria on the brief
- One theory, not a list.
- About one coin at a time: what one coin's own prices and volumes do. It may name several coins if it holds for each separately. A relation between coins cannot be tested: each coin is tested on its own bars only. Such a request gets "not researchable", not a substitute theory. A pair that trades as one instrument (ETH/BTC) is one instrument.
- A theory, not a formula or a trading rule: no entry, hold or exit, no parameter value.
- Says why, or says it does not know.
- Can be wrong: some market behaviour would refute it; it does not say how to test it (no condition on the check, such as what to control for, or which coins it must hold for).
- No workflow words; no header key outside the list; no header value taken from a code setting.
- Cites no result, price or event, from a source or from memory.
- Faithful to its request: a question stays a question.
- Faithful to its source, when it has one; the reason says whether it is the source's or the helper's.
- Not the same as a brief in the index (same claim, same reason, same market). A close one is allowed.
- Plain prose, about 250 words at most.

## Fixed inputs for the iterations
1. No theme.
2. A theme in the operator's words: whether RSI indicators predict the price behaviour of BTC, ETH and BNB.
3. A source: a TradingView strategy listing page, pasted by the operator.

## Variants compared
- Exercise 1: haiku, sonnet and opus on the three inputs.
- Exercise 2: sonnet and opus, twice each.
- Exercises 3 to 6: opus, as the prompt and the index were built.
- Exercise 7: the one-coin rule (a relation between coins cannot be tested). Exercise 8: `not-researchable` when a request can only be met by such a relation.

## Who judges the output
The operator: "would I research this theory?" and, with a source, "is this what the source says?". Code checks the shape. Each exercise has a one-page reading against the criteria.

## Done when
On two exercises in a row, on the three inputs, the helper's brief meets every criterion and would be kept with wording changes only.

Status: met by exercises 7 and 8, both clean (`exercise_8/reading.md`); they cover the no-theme and theme inputs and the cases of the one-coin rule. The source input was last run in exercise 6.

## What this step does not do
It does not write ideas, judge whether a theory is promising, check that the engine can test it, or set anything about how it is tested.
