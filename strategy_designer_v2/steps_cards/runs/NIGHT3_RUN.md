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
