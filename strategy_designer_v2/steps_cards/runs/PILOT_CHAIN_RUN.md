# Pilot of the changed chain (2026-11-25): 1n, 1q and 1l together, before any night (written before the run)

**The operator (2026-11-25):** "We wasted part of the previous night due to a missing test." "Go for 1 in a dedicated
session." Each change was proven alone (1n: night 7 replayed; 1q: line 7.g on 3 backtests; 1l: 7 books on both
engines); the chain has never run with all three. This run does, small and watched, with pass criteria fixed now.

## Purpose
One question: **does a run with 1n, 1q and 1l behave as designed, with no fault, before a night is spent on it?**

## The run
| Run | Branch | Theme (step 1 writes the brief) | Bar | Budget |
|---|---|---|---|---|
| `pilot_panic_run` | `pilot-chain` (from the working branch) | night 7's session 4: "In a falling, agitated market, does a coin's new low over the past month lead to more falling, as forced selling feeds itself, or to a rebound, as sellers run out?" | 1d | 15 USD |

The night 7 panic run is the baseline (`orchestration/loop/night7_panic_run/loop.jsonl`): in its first 10 turns (10.3
USD) 1 turn tested the theme's brief (032) and 11 discoveries became briefs. Plus one line 7.e rerun (about 0.5 USD,
outside the 15): line 7.e never ran in 1q's proof.

## Pass criteria (each counted from the run's files)
| # | Criterion | Pass when | Reads |
|---|---|---|---|
| C1 | The theme's own ideas run first (1n) | at least 5 of the first 10 turns test an idea of the theme's brief or its follow-ups (night 7: 1 of 10) | `loop.jsonl` |
| C2 | A discovery's brief is linked to its discovery (1n) | every brief written from a discovery has its `discovery:` field, and `select_next` ranks its ideas with that discovery's line and a generation of 1 or more | the run's briefs; `select_next.py --run` |
| C3 | Discoveries are not the held rebound (1q) | at most 2 of the run's discoveries are the next-day rebound after a fall (read from their text) | `07e_*/07g_*/pilot_panic_run/*/discoveries/` |
| C4 | The profile map is kept and read (1q) | `register/PROFILE_MAP.md` is rewritten after each book the run adds to the register; line 7.e, rerun on night 7's `034-01_rising-nearness-to-high-rises_1d` (rangefail: profitable enough, not confirmed), writes no discovery the map already lists and names a profile where it proposes one | the register; the 7.e rerun's analysis and ideas |
| C5 | A book is flat when its idea says so (1l) | in every backtest of the run, no bar where the forecast is 0 and a position under the band is refused its close | the backtests' bars |
| C6 | No fault | no failed turn; every plan whose idea names a profile has the profile gate, none without; every component built is committed | `loop.jsonl`, plans, `trading-bot/strategies/` |

**Outcome:** all six pass: the chain is ready for a night. Any fails: the defect is named, fixed, and the failing part
rerun before a night.

## Reading
(the session writes it here: each criterion with its count, pass or fail; cost; what to fix)
