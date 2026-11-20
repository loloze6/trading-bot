# Run brief: does step 7 propose larger ideas once it sees the idea's size? (2026-11-20, written before the B run)

**Purpose (operator's go, "go for 1 and 2"):** step 7's lines did not use what made hourly ideas fail: real ideas whose
move per case is smaller than what a trade costs (`runs/RETRO_DIAGNOSIS_RUN.md`: 53 of 103 confirmed non-paying ideas;
none of them paid). Change 1, one rule for every line: step 7 reads the idea's size (step 5's `size.json`, or measured
the same way), the cost of a trade on the backtest, and the findings register (`common/findings.md`), and its shared
rules say how to read the size against the cost. Test 2: does it change what the lines propose?

**How:** line 7.d (not profitable: why, and what would pay) on 4 confirmed ideas whose total move per case is below
the cost of a trade, from 3 briefs:
| Case | Horizon | Total move per case / cost |
|---|---|---|
| late-evening rebound (`slow_1h_run`, 016) | 2 hours | 0.14 % / 0.21 % |
| evening-hour drift (`slow_1h_run`, 016) | 2 hours | 0.06 % / 0.21 % |
| settlement move reverses (`hold_confirmed_1h_run`, 017) | 2 hours | 0.05 % / 0.21 % |
| one-day volatility-scaled reversal (`night_005_run`, 005) | 1 day | 0.15 % / 0.16 % |
A: today's step 7 (run before the change); B: with change 1. Same records, model and rounds. 8 analyses, about 2 USD.

**Measures, read on the analyses:** whether the findings name the move per case against the cost; each proposed idea's
horizon (as it states it); whether an idea proposes a larger move (a longer horizon, a stronger situation) and says why;
whether any idea breaks the definition of an idea (a level, a threshold, a cost or a price in its text).

**Expected outcomes:**
| Outcome | What the counts would show | Meaning |
|---|---|---|
| S1. It works | B's findings name the move against the cost on most cases; B proposes more ideas with a larger move (longer horizons above all) than A; no idea breaks the definition | keep change 1; next, test the ideas it proposes (steps 3 to 6) |
| S2. No effect | A and B propose the same kind of ideas | the line's own prompt (7.d) carries the direction, not the shared rules: read why before any other change |
| S3. It distorts | B's ideas state costs or levels, or B stops proposing ideas | the rule's wording is wrong: rework it |

**Limits:** one analysis per case and version, so a difference of one idea is noise; only clear differences count.

## Reading (2026-11-21; A 3.01 USD, B 2.76 USD; the analyses and ideas in `runs/step7_size_ab/`)

| Case | A (today's step 7): ideas, horizons | B (with the size and the cost): ideas, horizons |
|---|---|---|
| one-day volatility-scaled reversal (1d) | 2: 1 day, 1 day | 3: 1 day, 3 days, 10 days |
| late-evening rebound (1h, 2 h) | 2: 2 days, 24 hours | 3: 3 days, 24 hours, 3 days |
| evening-hour drift (1h, 2 h) | 1: 2 hours | 2: 3 days, 7 days |
| settlement move reverses (1h, 2 h) | **no ideas** ("the move is well under the round-trip cost") | 3: 24 hours, 24 hours, 24 hours |
| **All** | **5 ideas; 4 of a day or more; 0 of 3 days or more** | **11 ideas; 11 of a day or more; 6 of 3 days or more** |

- Both versions name the cost in all 4 analyses: line 7.d already looks at it. B states it per case against the idea's
  size ("the idea's own size is +0.05 % per case, 0.2 times the 0.21 % round trip").
- No idea in either version names a level, a cost or a percentage: the definition of an idea holds.

**Outcome S1: it works, with one thing to watch.** With the size against the cost, the line stops proposing ideas of a
few hours and moves to horizons of days (the median from about 1 day to 3 days), and where A gave up (the settlement
idea) B proposes ideas whose move can be larger. **To watch:** several of B's ideas move away from the tested idea's own
situation towards general multi-day momentum and reversal ("the more a coin has risen over its last 7 days, the more it
rises over the next 3 days", from the evening-hour case). They are ideas, but less tied to the brief's theory, and some
may repeat daily ideas already tested. Whether that matters is what testing them says (steps 3 to 6), the next step.

**Not yet shown:** whether B's ideas pay. That is the end-to-end run (step 3 of the plan agreed): the ideas through
steps 3 to 6 with the holding period, on the faster engine.
