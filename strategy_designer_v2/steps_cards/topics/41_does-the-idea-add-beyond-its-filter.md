# Topic 41: what a paying book earns beyond the known effects (reference books)

Status: open (designing: the definitions below, for the operator's review; nothing built)  
Where: research: shared definitions (`common/measures.md`), step 6 (`06_profitability/`)  
Opened: 2026-11-21, the designer session, from night 3 (`runs/NIGHT3_RUN.md`, the "Check" sections); redesigned the same
day with the operator: "keep it simple, standard, structured".

## Question
When a book pays, how much of its profit comes from an effect we already know (the market, momentum), and how much is
its own?

## Seen
- Night 3: 19 ideas confirmed and profitable. On 7 of them, the same book without the idea's own signal (its trend
  condition alone) paid on all six checks, with a Sharpe 0 to 0.15 lower, or higher (the 1h rebounds: 1.19 alone against
  0.87 to 1.02). The other paying ideas are momentum outright. Step 6 compares a book with holding the coins, never with
  momentum, so momentum is found again under new names.
- That check edited each config by hand (which part is "the condition"): not one rule for every config shape.

## Why it matters
Without it, briefs and runs are spent rediscovering momentum, and a book that adds nothing to it looks like a discovery.

## The business definitions (to go into `common/measures.md` on the operator's go)
1. **A reference book:** the simplest book of one known effect, on the same coins, the same dates, the same bar size and
   the same costs as the book judged, built from prices only, the same way for every idea. Two references:
   - **holding:** long every coin all the time, equal weight (what step 6 already computes as "holding");
   - **momentum:** long a coin while its return over the last 30 days is above 0, flat otherwise, equal weight. (One
     setting, written once; a decision for the operator: 30 days, the length the night's paying ideas used most.)
   A new reference is added only when a run shows a new known effect, with its own definition here.
2. **The split of a book's daily return:** each day's return of the book = what is left + the sensitivity to holding ×
   holding's return that day + the sensitivity to momentum × momentum's return that day + noise. The standard way to
   measure a strategy against known effects (a regression of the book's daily returns on the references' daily
   returns, over all the windows together). Three readings:
   - **sensitivity** (one per reference, signed): how strongly, and in which direction, the book follows that reference.
     +0.8 follows it, −0.8 does the opposite: both use the effect.
   - **share explained** (0 to 100 %, the sign does not count): how much of the book's ups and downs the references
     explain together.
   - **what is left** (per day) and its **t**: what the book earns beyond the references, and whether it is reliably
     above 0.
   No threshold: the numbers are reported, they decide nothing (visibility, as the rules ask).

What the readings mean (examples, not rules):
| Readings | Meaning |
|---|---|
| large share explained, what is left about 0 | a known effect in disguise, whatever its sign |
| large share explained, what is left reliably above 0 | a known effect, improved (timing, exit) |
| small share explained, what is left reliably above 0 | a source of profit of its own: what the research looks for |

## How it fits step 6 (one calculation, no duplicate)
Step 6 already builds the book's daily returns and holding's daily returns from the record (`06_profitability/card.md`,
"The backtest's book"). The split uses those same daily returns, plus momentum's, built the same way from the same
closing prices. Step 6's "Sharpe minus holding's Sharpe" stays as it is (a pass/fail measure); the split is reported next
to it, in `check.md` and `result.json`, as information, not as a seventh check.

## Plan (for the operator's go)
| # | Change | Gain | Effort | Risk |
|---|---|---|---|---|
| 1 | The definitions above in `common/measures.md`; step 6's card updated (a new field, its "for, used by, without it") | one meaning for every reader before any formula | small | none |
| 2 | Step 6's helper: momentum's daily returns from the record's closes; the split; written next to the six measures; tests on books whose answer is known by construction (a book equal to momentum: share explained 100 %, what is left 0; a book of noise: about 0 %) | the numbers for every new book | small (one function, no new backtest: prices are in the record) | none to the verdicts: the six checks unchanged |
| 3 | Proof: step 6 rerun on fixed records, its six measures and verdicts identical file by file, the split added; then read on night 3's 19 paying books, against the controls already run (they should read "momentum in disguise"), and on step 7 A/B's 1-day reversal (it should read differently) | shows the split says what the controls said, without editing any config | small (no model call) | if the readings disagree with the controls, the definition is wrong: rework it before use |
| 4 | Step 7 reads the split with the rest of the step 6 check (it already reads `check.md`) | its next ideas aim at what is left, not at momentum again | none (it reads the file) | none |

Not in this topic: grouping ideas into families (after this, with the operator), the two measures of topic 42.

## Decisions
| Date | Decision | By | Why | Rejected, and why |
|---|---|---|---|---|
| 2026-11-21 | Reference books and the split of the daily return, instead of removing each idea's "signal" by hand | the operator ("go; keep it simple, standard, structured") | one rule for every config; the standard measure; reuses step 6's daily returns | the hand-made control: not one rule for every config shape; correlation alone: it reads momentum used the other way round as a new effect (the operator's remark) |

## Status and next
Waiting for the operator's go on the definitions (and the 30-day setting), then the plan in order.

## Links
`runs/NIGHT3_RUN.md`, `06_profitability/card.md`, `common/measures.md`, topic 42, `common/findings.md`.
