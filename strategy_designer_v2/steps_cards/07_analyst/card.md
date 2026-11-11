# Step card 7, branch 2: Analyst (2026-11-11, draft for discussion)

## Business objective, one question
Why did the book do what it did, and what one change would a practitioner make?

**Read one backtest the way a practitioner would, book first: where the money came from and went, whether the answers about it can be trusted, and the one change worth trying next, with its reason.**

## Input
One backtest record, with:
- its plan (the idea, its fidelity, its forecast in words, its config, its criterion) and its brief;
- the answers of the two other branches: branch 1's verdict (is the idea real?) and branch 3's assessment (is the book profitable enough?).

## Output
One analysis per backtest: what the book did, whether the answers agree, and one proposed change.

## What an analysis is
**An analysis is a practitioner's reading of one backtest: what the book did and why, in numbers from the record; whether the idea's verdict, the book's profitability and the book itself tell the same story; and the one change a practitioner would make next, with the result that would show it worked.**

- **Book first, referee second.** The equity path and the exposure are read before any statistic: where the book held positions, on which side, how often it traded, and where it rose and fell.
- **Every observation carries a number** from the record's facts. No number, no observation.
- **It proposes; it decides nothing.** The change goes to the operator (and later to the next-idea step). The analyst changes no plan, no config, no rule.
- **It looks for a broken chain as well as a bad idea.** Tonight's runs had three findings of this kind, all from reading the book against the answers: a config on the wrong side, a biased comparison behind five "rejected" verdicts, a book that lost on its own trading.

## The fields of an analysis (first proposal)
1. **What the book did:** time in the market, long and short shares, usual position size, holding time, trades and what they cost; where the equity rose and fell (coins, periods).
   - For: the practitioner's first look.
   - Used by: the operator.
   - Without it: the answers are read without knowing what was traded.
2. **Where the result came from:** gross against net (the cost of trading), by coin, by period, long against short, large positions against small ones.
   - For: knowing whether the result is the idea, the trading or one lucky place.
   - Used by: the operator, field 4.
   - Without it: a result has no source.
3. **Do the answers agree?** Branch 1's verdict, branch 3's status and the book side by side. A disagreement is named with its likely cause: the idea, the test (config or criterion), the data, or a defect in the chain.
   - For: trusting the answers, or not.
   - Used by: the operator.
   - Without it: a wrong answer passes unseen (as the biased comparison did until the book was read).
4. **The one change:** its kind (how the idea trades; the test; the data; a defect to fix; drop the idea), what it is, why (tied to fields 1 to 3), and the result that would show it worked.
   - For: the next move, from evidence.
   - Used by: the operator, and later the next-idea step.
   - Without it: the next move is chosen without reading this one.
5. **The index line:** `<plan id>: <kind of change>: <the change, a few words> [answers agree: yes | no]`.

## Storage and naming (first proposal)
```
07_analyst/
  card.md
  helper/
    book_facts.py        code: the record's facts, the same table for every backtest (no model)
    system_prompt.md     the analyst's instructions
    make_analysis.py     one closed-book call: the facts, the plan, the brief, the two answers -> the analysis
  analyses/
    INDEX.md, REVIEW.md, run_log*.txt
    <plan id>/           analysis.md, book_facts.json
  exercise_k/
```

## The AI (first proposal)
- **Code computes the facts; the model reads them.** A model reading thousands of bars cannot measure reliably (step 5's lesson), so a fixed script turns the record into one standard table of facts (fields 1 and 2), the same for every backtest. The model reads that table, the plan, the brief and the two answers, and writes the analysis.
- **Closed book,** one call per backtest, as in steps 1 to 3 and 5.
- **Model:** opus. **Cost:** about 0.05 to 0.10 USD per backtest (to be measured).
- **Checks in code:** refuse only an answer it cannot read, or one without a change and its kind.

## Open questions for the operator
1. **Does the analyst read the two other answers?** I recommend yes: it runs after branches 1 and 3. The findings that mattered tonight all came from setting the answers against the book. Fully blind and parallel is the alternative.
2. **One change, or one per kind?** I recommend one: the most useful, as in your working rule ("what one change would a practitioner make to this book?").
3. **The change in plain words, or as a ready-to-test idea?** I recommend plain words with its kind. Turning it into an idea is step 2's job, and keeps one job per step. The earlier v2 analyst wrote a ready-to-run claim.
4. **On every backtest, or only on some?** I recommend every backtest: it is cheap, and a profitable book can hide a defect as well as a losing one.

## Still to write, once these are settled
Quality criteria, fixed inputs (tonight's runs are a good set: the wrong-side config, the biased comparison, the RSI books' trading, the identical moving-average books), variants compared, who judges, done when, what this step does not do.
