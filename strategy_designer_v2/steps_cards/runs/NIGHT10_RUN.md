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

## During the night (the designer's watch)
- **About 03:10 Paris, runs C and D ended, 03:14 run A** (their sessions' final reports):
  | Run | Box | Spent | Tested | Confirmed | Profitable | "No effect" / unclear | Stopped at step 3 (a measure missing) |
  |---|---|---|---|---|---|---|---|
  | A | falling calm, long | 10.02 | 10 | 1 (050-02.b1, fails Calmar alone; 7.d called on it) | 0 | 4 / 5 | 0 |
  | C | falling agitated, short | 10.19 | 7 | 0 | 0 | 6 / 1 | 3 (the components step answered 3 wishes, 2.59 USD) |
  | D | rising agitated, long | 11.23 | 6 | 0 | 0 | 5 / 1 | 1 (one 7.c call of 21 minutes, 4.45 USD for one idea) |
- **The rest of the budget, first choice (written before it starts, 03:20 Paris):** spent so far 33.26 USD (the side
  pass 1.82, A, C, D), run B still running (10). **Run A is resumed with its budget raised from 10 to 25 USD**, by the
  rule written above: it is the only run with a confirmed idea (050-02.b1, "a week's rise in a calm downtrend
  continues", t +2.15, failing step 6 on Calmar alone, its repairs written) and it has 5 unclear ideas (a sign of an
  effect) against 1 or none in C and D. Expected: (R1) a repair or a clearer test gives a confirmed and profitable
  strategy, its common record and a portfolio update follow; (R2) more confirmed, none profitable; (R3) nothing more
  confirmed. C and D are not continued: nothing confirmed, 1 unclear each.
