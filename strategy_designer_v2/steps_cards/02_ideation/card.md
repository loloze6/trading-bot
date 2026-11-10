# Step card 2: Ideation (2026-11-09)

## Business objective, one question
Which testable ideas does this theory give?

Turn a theory into things the market data can confirm or reject, so a trader learns what to trade and what not to trade.

## Input
One brief from step 1: a theory, as a claim or a question, with its optional context.

## Output
The ideas the theory gives. Their number follows from the theory, not from a quota.

## What an idea is
**An idea is one thing we would see in the market if the theory were true, which a trader could act on, and which the data can confirm or reject.**

- The theory says what happens and why. The idea says what we would see. How to trade it is not this step.
- "Act on" means take a trade or refuse one. A confirmed idea says what to trade; a rejected idea says what not to trade.
- An idea is a statement with one direction, never "either this or that". "Either" is two things, and a claim that two groups merely differ can hardly be rejected.
- An idea says that something happens, never that something does not happen. Data can reject "X does not happen" but never confirm it.
- An idea says what we would see, not how to check it.
- A theory gives several ideas because it has several consequences, and a consequence can be seen in more than one way.
- A question brief gives one idea per answer it gives a reason for. Brief 001 gives "reversal" ideas and "continuation" ideas. Its third answer, "nothing", needs no idea: it is what we learn when the others are rejected. The brief stays a question.
- Two different situations are two ideas (brief 003: thin-volume moves, heavy-volume moves). Mirror situations are two situations (a high and a low RSI extreme; an upward and a downward cross).
- Not a new idea:
  - the same idea with another setting, such as a 21-bar RSI instead of a 14-bar one;
  - the same idea for another reason: that is another theory, so a new brief.

## The fields of an idea
1. **brief** (header, written by the script): the brief's file name, such as `001_rsi-extremes-predict-next-move`.
   - For: says which theory the idea comes from.
   - Used by: the operator, and anyone who reads the idea later.
   - Without it: the idea's number gives only the brief's number, and the theory must be looked up.
2. **The brief's header lines** (header, copied by the script, word for word): venue, instruments, bar, period, side, source, whichever the brief has.
   - For: the context the idea holds in, readable without opening the brief.
   - Used by: the next steps, which check the idea where the brief says it applies.
   - Without it: the idea file looks unlimited when its brief is limited.
3. **Idea** (body, mandatory): what we would see in the market, in one or two sentences of plain prose.
   - For: the idea itself.
   - Used by: the next steps, which confirm or reject it.
   - Without it: there is nothing to confirm or reject.
4. **Consequence** (body, mandatory): one line, the consequence of the theory, or the answer to the brief's question, that the idea shows.
   - For: shows the idea follows from the theory, and whether the ideas together cover it.
   - Used by: the operator.
   - Without it: ideas drift from the brief and nobody sees it.
5. **Index line** (in `INDEX.md`): the idea in one short sentence, with the brief's market lines in brackets (venue, instruments, bar, period, side), added by the script.
   - For: the list of ideas already written, read before each new call.
   - Used by: the helper.
   - Without it: close briefs give the same idea twice (005 and 001 both ask about RSI), and it is checked twice.

The header is mechanical: the model never writes it, so it cannot change it.

## Storage and naming
Modelled on step 1: a pre-registered hypothesis, one numbered file per record, never rewritten.

```
02_ideation/
  card.md                  this card
  helper/
    system_prompt.md       the helper's instructions
    make_ideas.py          one closed-book call; refuses only a major deviation; saves one file per idea; adds the index lines
  ideas/
    INDEX.md               one line per idea
    NNN-KK_short-name.md   one file per idea
  exercise_k/              the comparison exercises
```

- **One file per idea**: each idea is confirmed or rejected on its own, so each has its own id.
- **Naming**: `NNN` is the brief's number; `KK` numbers the ideas from that brief; `short-name` is three to five words. The file name is the idea's id.
- **Never edited** once the pipeline has read it. A reworded idea gets a new number.
- **Index line format**: `NNN-KK_short-name: the idea in one short sentence [the brief's market lines]`.

**Example** (`ideas/001-01_rsi-high-extreme-gives-back.md`):
```
---
brief: 001_rsi-extremes-predict-next-move
instruments: BTC, ETH, BNB
---
Idea: after a coin's RSI reaches an extreme high, price gives back part of the run over the
following bars.
Consequence: the reversal answer: a run that pushes RSI to an extreme reflects crowding that
unwinds once the pressure is spent.
```
Index line: `001-01_rsi-high-extreme-gives-back: after an extreme high RSI, price gives back part of the run [instruments: BTC, ETH, BNB]`

## The AI
**What it does.** It reads one brief and the ideas index, and writes the ideas the brief gives. One brief, one call. Running it is the operator's act.

**Closed book**, as in step 1. One model call: no tools, no files, no web, no repository, an empty working folder, no settings. The brief and the index are pasted into the call. The script writes the header, saves one file per idea and adds the index lines. It refuses only a major deviation: a block without its idea or its consequence, or a field over 300 words (a guard against a runaway answer, not a length rule). A refused answer is sent back with the reason, up to three attempts. Minor deviations are fixed, not refused: bold and headings are stripped, the short-name is made file-safe (at most eight words), a missing index line falls back to the idea, a missing `already-indexed` line is recorded as not given.

**Model.** Opus. Over exercises 2 and 3, opus wrote 58 ideas with no fault and respected the index on the repeated brief both times. Sonnet costs half as much, but wrote duplicates on both repeats and kept turning one brief's exit-like sentence into duplicate ideas.

**Cost.** 0.02 to 0.05 USD per brief; a retry doubles it.

**Prompt**: `helper/system_prompt.md`.

## Quality criteria on the ideas
- Each idea meets the definition: we would see it if the theory were true, a trader could take or refuse a trade on its answer, the data can confirm or reject it.
- One direction, never "either".
- It says something happens, never that something does not.
- What we would see, not how to check it: no condition such as what to control for, or which coins it must hold for. A baseline that gives the idea its meaning ("more often than after random points", "more than after neutral readings") is not a test condition.
- Faithful: a consequence of the brief, for the brief's reasons, where its header says it applies.
- Concrete: someone looking at the bars could tell whether it is there.
- About one coin at a time: what we would see in one coin's own bars. A consequence that needs two coins at once is not an idea here; when no consequence of a brief is about one coin, the helper writes `no-ideas` with the reason.
- No setting value, no trading rule, no result, no price.
- Distinct: no two ideas differ only by a setting. A span between two events the brief names (from one cross to the opposite cross) is a situation of its own.
- Together, the ideas cover the brief's consequences, and every answer of a question brief that has a reason.
- Not the same as an idea in the index. A close one is allowed.

## Fixed inputs for the iterations
The five briefs from step 1, exercise 5, run in this order on one index, then `001` a second time. Together they hold every case the prompt has a rule for.

| Brief | Case |
|---|---|
| `001` RSI extremes | a question with two answers that have reasons; mirror situations; a header to copy; a test condition ("for all three coins") |
| `002` moving-average cross | a claim from a source: one direction only; a `source` header; an exit-like sentence that must not become a rule |
| `003` thin and heavy volume | two situations; empty header |
| `004` bitcoin leads altcoins | several consequences; an absence and a test condition ("once their own past returns are accounted for") |
| `005` RSI divergence | a question close to 001 |
| `001` again | a real repeat: every idea is already in the index |

Not covered: a brief with `venue`, `bar`, `period` or `side` in its header (the copy is mechanical, so code covers it), and a brief that gives no idea.

## Variants compared
Exercises 1 to 3: opus and sonnet, each model running the six calls in order on its own index, starting empty. Opus chosen (see The AI).

## Who judges the output
The operator: "would I see this if my theory were true, and would I act on the answer?" and "do these ideas cover my theory?". Code checks the shape. Each exercise has a one-page reading against the criteria and the counts below.

## Done when
On two exercises in a row, on the fixed inputs, every idea meets every criterion and the operator would keep the set. Status: met by opus on exercises 2 and 3 (`exercise_3/reading.md`).

## To observe in the tests
No number of ideas is enforced. A quota would push the model to pad or to cut. The tests count, per brief:
- the ideas written, and how many are padding (a setting, a reason not in the brief, a duplicate);
- the consequences and answers missed;
- the vague ideas, and the ideas with "either";
- the ideas that hold a test condition.

If a count shows a fault, the prompt changes first. A limit in code comes only if the model runs away, as in step 1.

## What this step does not do
It does not say how to trade an idea, set a pass mark, or confirm or reject an idea.
