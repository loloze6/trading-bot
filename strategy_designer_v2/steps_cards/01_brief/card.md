# Step card 1: Brief (2026-11-09)

## Objective, one question
Which trading theory should the pipeline research?

## Words used on this card
- **A theory**: a claim or a question about how a market behaves and, where known, why.
- **The context**: optional limits on where the theory applies.
- **Workflow words**: anything about how the pipeline works rather than what to research: thresholds, step names, config settings, fees, budgets.

## How a brief is made
By hand, or by the helper: an AI that knows trading and nothing of the pipeline, writing from its own knowledge, from a theme, or from a source the operator gives. Writing the file, or running the helper, is the operator's decision. Nothing else is needed.

## The folder
```
01_brief/
  card.md              this card
  helper/
    system_prompt.md   the helper's instructions
    make_brief.py      one closed-book call; checks the answer; saves the brief; adds its index line
  briefs/
    INDEX.md           one line per brief
    NNN_short-name.md  one file per brief
  exercise_1 ... 5/    the comparison exercises that shaped the helper
```

## The artifact
Modelled on a pre-registered hypothesis (short, written before the data, never rewritten) and a decision record (one numbered plain-text file per decision).

**Format**: one Markdown file. A header holds the context as `key: value` lines; the body is the theory in plain prose. The header keys are a closed list, which keeps workflow words out.

**Naming**: `NNN_short-name.md`. `NNN` is a running number; `short-name` is three to five words of the theory. The file name is the brief's id. A brief is never edited once the pipeline has read it; a reworded theory is a new number, so one number never names two theories.

**Index**: `briefs/INDEX.md`, one line per brief: `NNN_short-name: one or two short sentences [header lines]`. The helper writes the line; `make_brief.py` adds it. A brief written by hand needs its line written by hand.

**Example** (`briefs/004_bitcoin-leads-altcoins-lagged-response.md`, from exercise 5):
```
---
---
Large coins lead small coins over short horizons. When bitcoin makes a sharp move,
smaller and less traded coins take on part of that move only later... (prose, at most 200 words)
```

## Hand-over: the fields
1. **Theory** (body, mandatory): one claim or one question, its reason if it has one, what would prove it wrong; at most 200 words.
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
7. **The index line** (in `INDEX.md`)
   - For: the list of theories already written, read before each new one.
   - Used by: the helper, for its next brief.
   - Without it: the helper writes its most typical theory again (exercise 2: four no-theme calls, one theory).

## Quality criteria on the brief
- One theory, not a list.
- A theory, not a formula or a trading rule: no entry, hold or exit, no parameter value.
- Says why, or says it does not know.
- Can be wrong: some market behaviour would refute it; it does not say how to test it.
- No workflow words; no header key outside the list; no header value taken from a code setting.
- Cites no result, price or event, from a source or from memory.
- Faithful to its request: a question stays a question.
- Faithful to its source, when it has one; the reason says whether it is the source's or the helper's.
- Not the same as a brief in the index (same claim, same reason, same market). A close one is allowed.
- At most 200 words of plain prose.

## The helper
**Closed book.** One model call: no tools, no files, no web, no repository, an empty working folder, no settings. The index and the source are pasted into the call. One note cannot be removed in this cloud environment: an account note with the operator's email. It says nothing of trading or the pipeline.

**Model.** Opus. Exercise 1 compared haiku, sonnet and opus; exercise 2 compared sonnet and opus twice each. Haiku broke rules of meaning; sonnet kept two faults the prompt forbids; opus met them all and was stable.

**Checks in code** (`make_brief.py`): the header shape and keys, at most 200 words, no headings or bold, the short-name, an index line of at most 25 words, `other-theories` with a source. A refused answer is sent back with the reason, up to three attempts.

**Cost.** 0.02 to 0.05 USD per brief from a theme or no theme; about 0.12 per call with a long source. A retry doubles it.

## Fixed inputs for the iterations
1. No theme.
2. A theme in the operator's words: whether RSI indicators predict the price behaviour of BTC, ETH and BNB.
3. A source: a TradingView strategy listing page, pasted by the operator.

## Who judges the output
The operator: "would I research this theory?" and, with a source, "is this what the source says?". Code checks the shape. Each exercise has a one-page reading against the criteria.

## Done when
On two exercises in a row, on the three inputs, the helper's brief meets every criterion and would be kept with wording changes only. Status: exercise 5 meets it, with small faults listed in `exercise_5/reading.md`. The prompt changed after exercise 4 (the 200-word limit, plain prose), so strictly one exercise counts, not two.

## Open, from exercise 5
- Opus writes about 210 words when told 200, so most first answers are refused. Proposed: tell it "150 to 180 words", keep the code limit at 200. Untested.
- A refused answer's text is not kept. Proposed: keep it in the log. Untested.

## What this step does not do
It does not write ideas, judge whether a theory is promising, check that the engine can test it, or set anything about how it is tested.
