# Night 10 (2026-11-28): four boxed runs in the new data use, fed first by the earlier untested ideas (written before the runs)

**The operator (2026-11-28, about 01:30 Paris):** "Go for 1, 2. Then possible to do the continuation of 2 with the
research on these ideas? And 3 with 40 usd"; "For the night 100 budget max"; "if you see that we did not reach 100,
you can open a new session or continue ideas existing until 100"; sessions on Sonnet, or Opus when complex; in the
morning, "see also if we do not overspend tokens on top of judging what they add to portfolio". Standing rules:
`NIGHT_RULES.md`.

**Since the pilot** (`PILOT_A4_RUN.md`): the windows counted before the engine runs and the draw among coins with
history, the side read on the idea, the brief's coins by code (A12, joined); the seeded run showed steps 9 and 10, B12's
skip and the direction check; the earlier ideas' sides (324 ideas, 1.82 USD, `BUILD_IDEA_SIDES.md`, joined). No other
change: no pilot is needed again (NIGHT_RULES, before the night, 3).

## Purpose
One question: **do the earlier ideas never tested, and a search held in one box, give strategies that add to the
portfolio where it earns nothing (the falling years), measured by what the night adds to the portfolio (A8)?**
The portfolio before the night: v4, 11 strategies; by year +18 to +54 % in 2016-2021, 2023, 2024; +6.7 % in 2022,
-1.7 % in 2025, +0.8 % in 2026.

## The runs
| Session | Run | Box (named, so that four runs do not all take the rule's one pick) | Earlier ideas it takes (B13) | Budget |
|---|---|---|---|---|
| A | `night10_fallcalmlong_run` | falling calm, long (the rule's first pick) | 8 | 10 USD |
| B | `night10_fallcalmshort_run` | falling calm, short | 62 | 10 USD |
| C | `night10_fallagishort_run` | falling agitated, short | 97 | 10 USD |
| D | `night10_riseagilong_run` | rising agitated, long (the rule's third; its second, rising agitated short, gave 0 of 10 in the pilot, shorts losing on every coin) | 7 | 10 USD |
Each: its own session (Sonnet) and branch `night10-<name>` from the working branch; `run_brief --data-use 2 --target-box
"<box>" --theme "The run's target box: ..." --budget 10` (step 1 writes the brief from the box alone). Choppy boxes:
parked (topic 56). The side pass's 1.82 USD and these 40 make 41.82 of the night's 100.

**The rest of the budget (to 100 USD), decided when the four end, written here before it starts:** first a run that has
a confirmed idea or a candidate is resumed with more budget; otherwise a new run in the box with the most earlier ideas
still untested.

## Expected outcomes (by the counts)
| # | Outcome | Shown by |
|---|---|---|
| N1 | The night adds to the portfolio | `addition.py` on the night's runs: the portfolio with them above the portfolio without, on the whole record or on the weak years (2022, 2025, 2026) |
| N2 | Candidates that add nothing | confirmed and profitable strategies, their common records made, the portfolio unchanged or lower |
| N3 | Nothing confirmed and profitable | as the pilot (0 of 22): the boxes, or the data per run, do not give tests that confirm |
| N4 | The machinery fails | a failed turn, a refused step, a common record or a portfolio update that does not run |
Also counted: per run, tested, confirmed, profitable, "no effect", repairs skipped, 7.g not called, earlier ideas taken
and tested and what they gave against the run's own ideas, ideas outside the box, usable coin-windows; the spend in
research calls per step; **each session's own token cost** (the operator's question).
