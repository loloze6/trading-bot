# Night 3 (2026-11-21): five briefs side by side, one cloud session each (written before the runs)

**The operator's go (2026-11-21, about 01:40 Paris):** "launching parallel research workflow in new session in
autonomy (budget 200): possibly 1h with new features implemented today; possibly 4h (or 2h, or 8h) on different runs
... act in autonomy, creating and closing sessions ... brief and new component freely created following cards
guideline. Possibly brief that would be super innovative (e.g. machine learning, around resistance and support, around
ichimoku cloud)". Then: "Go, launch now."

**Engine and workflow:** the working branch at launch: the holding period, speed A to D, the idea's size (step 5),
step 7 with the size, the recorded cost and the findings, the instruction sentence still in (its A/B test ends this
night: `runs/STEP7_SIZE_AB_RUN.md`), the measured slippage (topic 38).

| Session | Brief | Bar | Run | Budget (model calls) |
|---|---|---|---|---|
| 1 | 018, a daily situation caught on the hour it first holds, held for days (improvement I3) | 1h | `night3_1h_run` | 45 USD |
| 2 | 019, a quiet range then a breakout; first builds the 4h Kraken files from the 1h ones (a data tool, its proof) | 4h | `night3_4h_run` | 35 USD |
| 3 | 020, support and resistance at past turning prices | 1d | `night3_levels_run` | 35 USD |
| 4 | 021, the Ichimoku cloud, against a plain moving-average trend | 1d | `night3_ichimoku_run` | 35 USD |
| 5 | 022, weak effects combined by weights learned on past data only | 1d | `night3_learned_run` | 35 USD |
| designer | the step 7 A/B reading, the clean-up, merges, the morning report | - | - | 15 USD |

Each session: `run_brief` with the brief and its budget, on its own branch (`night3-<name>`); after a cut by the 2-hour
limit it resumes with `loop.py --run` (the night's autonomy, the operator's words above); it stops at its budget or at
07:00 UTC (08:00 Paris), commits its run's files and any component it built (the components step, its standard checks
and proof: the standing go), pushes, and reports to the designer session. Merging into the working branch: by the
designer, once no loop runs on it; into master: the operator's go.

**Measures, per brief:** ideas written; testable (plans); missing components and those built; confirmed; their size
against the cost; profitable enough; holding on the unseen dates; USD and hours.

**Expected outcomes:**
| Outcome | What the counts would show | Meaning |
|---|---|---|
| N1. A new paying family | at least one brief gives a confirmed, profitable idea that holds on the unseen dates and is not a known daily momentum idea | the brief's theory is worth a second round (its step 7 lines' ideas) |
| N2. Real but too small | confirmed ideas whose move per case is below the cost, no profitable book | the theory is real, not tradeable at that horizon: read the sizes, the next brief changes the horizon or the situation |
| N3. Not real | few or no confirmed ideas | the theory fails its own test: recorded, not pursued |
| N4. Blocked | the ideas cannot be tested (missing components not buildable, the 4h data not buildable) | what blocks is the finding: the components or data to build, for the operator |

For brief 022 (learned weights), N4 or a leak is the main risk: the component must learn only from returns already
known at each bar (no lookahead), and its proof must show it.

## During the night
- **03:56 Paris (02:56 UTC):** the account's 5-hour usage limit stopped every session at once (six sessions running,
  the designer's included); it reset at 06:10 Paris. Visible in each session's events ("You've hit your 5-hour limit").
- **06:15 Paris:** the operator: "continue; the other sessions reached the limit as well, so to be resumed". The five
  sessions were told to resume their loops, keep their own turns short, and start nothing after 10:00 Paris (09:00
  UTC) instead of 08:00, to give back the time lost; budgets unchanged.
- **06:20 Paris, a fix (operator: "feel free to fix if necessary"):** two loop defects the limit revealed, fixed on the
  working branch (e9df36fe; tests, and a proof with a model that answers "usage limit"): a refused model call stops the
  loop and marks nothing failed (it had marked 55 + 83 + 39 untested ideas failed in the levels, Ichimoku and learned
  runs); a step that fails stops `run_idea` instead of its old output being read (it had turned one idea about 4,000
  times in the 1h and 4h runs). The levels and learned sessions merged the fix, wrote one "retry" line per idea the limit
  had failed (55 and 39), and resumed with their budgets unchanged (the levels session refused a raise to 50 USD from a
  session: it needs the operator's word). Ichimoku stays closed (1.35 USD left).

## Check: do the resistance breakouts add anything beyond momentum? (06:45 Paris, designer session, no model call)
The levels run's two ideas that pay and hold on both unseen periods pair the new `ResistanceBreakTouchCountComponent`
with a 30-day or 20-day price change (`PriceEvolutionComponent`), in the gate and in the forecast. Control: the same
config, coins, folds, horizon and sizing with the level removed (the price change alone); steps 4 and 6 only.
| Idea | Sharpe | Minus holding's | Calmar | Mean daily return |
|---|---|---|---|---|
| resistance breakout in an uptrend (level + 30-day rise) | 1.26 | +0.68 | 1.35 | 0.086 % |
| control: the 30-day rise alone | 1.18 | +0.58 | 1.30 | 0.09 % |
| breakout after a run (level + 20-day rise) | 1.13 | +0.55 | 1.12 | 0.081 % |
| control: the 20-day rise alone | 1.13 | +0.52 | 1.04 | 0.09 % |
Both controls are profitable enough on all six checks. **The level adds about 0.1 of Sharpe at most; what pays is the
known momentum family.** Not a new paying family (N1 not supported for brief 020); the brief's first claim (a level
turns price again) was not supported by its own ideas either.

## Check: do the 4h breakouts add anything beyond their trend filter? (07:30 Paris, designer session, no model call)
The 4h run's two breakout ideas that pay and hold on 2016-17 trade a breakout (`DistanceFromHighComponent`,
`BreakoutInMeanRangesComponent`) only while the coin's past return is positive (`PriceEvolutionComponent`, 180 or 42
bars). Control: the same gate, coins, folds, horizon and sizing, the forecast from the gate's own return (standardised,
clipped at 0) instead of the breakout; steps 4 and 6 only.
| Idea | Sharpe | Minus holding's | Calmar | Mean daily return | Trades per day |
|---|---|---|---|---|---|
| large breakouts in rising coins (19 coins) | 1.53 | +0.92 | 1.97 | 0.06 % | 0.15 |
| control: the 30-day rise alone | 1.38 | +0.77 | 1.78 | 0.11 % | 0.41 |
| break size in mean ranges (6 coins) | 1.11 | +0.56 | 1.21 | 0.11 % | 0.21 |
| control: the 7-day rise alone | 1.05 | +0.49 | 1.29 | 0.10 % | 0.60 |
Both controls are profitable enough on all six checks. The breakout adds 0.06 to 0.15 of Sharpe (and trades less); the
trend filter carries most of the result. Same reading as the levels run: the paying ideas of night 3 are, at heart, the
known momentum family; what the new components add is small and not yet shown to hold on its own.

## A defect in the designer's own fix: budgets overrun (08:30 Paris)
The retry lines made the re-admitted ideas count as "unfinished", and the loop runs unfinished ideas before its budget
check: the levels run spent about 58 USD on its 35 USD budget (29 ideas run past it), the learned run 41.13 on 35. Found
and reported by the levels session; the learned session was stopped at once on the designer's word. Fixed on the
working branch (the budget holds before every `run_idea` call; a test that fails on the previous loop). The 26 levels
ideas still unrun and the learned run's remaining ones are not resumed. Overspend: about 29 USD over the two budgets.

## Check: the 1h "plunge in an uptrend rebounds" family against its trend filter alone (10:45 Paris)
The 1h run's three rebound ideas buy a sharp 24-hour fall only while the coin is up over 30 days (720 bars), or weight
the fall by that rise. Control: the same gate, coins, folds, horizon and sizing, the forecast from the 30-day rise alone
(standardised, clipped at 0); steps 4 and 6 only.
| Idea | Sharpe | Minus holding's | Calmar | Mean daily return |
|---|---|---|---|---|
| plunge in an uptrend rebounds | 0.87 | +0.31 | 0.83 | 0.07 % |
| dip depth in an uptrend rebounds | 0.96 | +0.40 | 0.93 | 0.10 % |
| depth-graded plunge rebound (fall times rise, no gate) | 1.02 | +0.47 | 1.00 | 0.13 % |
| control: the 30-day rise alone (gated) | 1.19 | +0.64 | 1.34 | 0.10 % |
| control: the 30-day rise alone (no gate) | 1.18 | +0.63 | 1.20 | 0.10 % |
The 30-day rise alone does better than every rebound idea: the plunge takes away from it. Not a new family.

## Reading (2026-11-21, 10:50 Paris)

| Brief | Ideas run | Confirmed | Confirmed and profitable | Held on the unseen dates | USD (budget) |
|---|---|---|---|---|---|
| 018, 1h: a daily situation caught on the hour | 31 | 7 | 6 | 6 of 6 on 2016-17 (no 2026 hourly data) | 40.36 (45) |
| 019, 4h: a quiet range then a breakout | 26 | 10 | 4 | 3 of 4 on 2016-17 (no 2026 data) | 35.75 (35) |
| 020, support and resistance | 47 | 12 | 3 | 2 of 3, on both periods | about 57.8 (35) |
| 021, Ichimoku cloud | 18 | 2 | 0 | - | 33.65 (35) |
| 022, weights learned on past data | 52 | 22 | 6 | 5 of 5, on both periods | 41.13 (35) |
| **All** | **174** | **53** | **19** | **16 of 19 tested** | **about 209 (185 + the designer's 15)** |

**Outcome, against the expected outcomes: N2 for the briefs' own theories, and the paying ideas are momentum.**
- N1 (a new paying family) is **not supported** by the controls: on 7 paying ideas checked (4 breakouts, 3 rebounds), the
  idea's own component adds 0 to 0.15 of Sharpe, or takes some away (the 1h rebounds); every trend filter alone pays on
  all six checks. The other paying ideas of the night are momentum outright (monthly, four-week and 90-day rises; the
  learned run's five, step 7 A/B set B's two).
- The briefs' own claims: 018's (the hour before the daily close) not measured; 019's (narrowness alone) not confirmed;
  020's first claim (a level turns price) not supported, its second (a break continues) supported but carried by
  momentum; 021 (Ichimoku): 2 confirmed, none pays; 022: the learned combinations inconclusive.
- **What the night shows about the workflow:** step 6 compares a book with holding the coin, never with the simplest
  book its own filter makes, so momentum is found again under new names (topic 41, proposed).

**Costs and failures:** about 209 USD for the five runs (budget 185, plus 15 for the designer, 200 in all): about 29 USD
over the levels and learned budgets because of the designer's retry fix (see above), 0.75 over the 4h budget (the loop
finishes an idea once started). 2.3 hours lost to the account's 5-hour limit; the account's 7-day limit shows a warning.
Two loop defects found and fixed (a refused call; a step that fails), one defect of the fix found and fixed (the
budget on resume). Not run: 26 levels ideas, 83 Ichimoku ideas (budgets spent). Not done: the 2026 check of hourly and
4h ideas (hourly data ends 2025-12-31).
