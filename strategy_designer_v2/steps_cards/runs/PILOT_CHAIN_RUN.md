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
Written 2026-11-25 by the pilot session (branch `pilot-chain`). The run started 18:40 UTC and stopped at 19:55 UTC on
its budget, after 13 turns, with no cut and no resume. Step 1 wrote brief `054_reclaimed-monthly-low-in-falling-agitated`
with 4 ideas, all 1d. Turns 1 to 4 stopped at step 3 (missing-components). The components step answered 6 wishes
(3 built: `ReclaimedPriorLowPierceDepthComponent`, `PriorLowReclaimInRangeComponent` and its `nearness` form; 3
already existed; 2.25 USD), and turns 5 to 8 ran the same 4 ideas. Turns 9 to 13 ran follow-ups (7.b) of those ideas.
Of the 9 backtests, step 5 said inconclusive for all 9 and step 6 said not profitable enough for all 9. So no book was
confirmed and no book paid.

| # | Criterion | Count | Result |
|---|---|---|---|
| C1 | The theme's own ideas run first | 10 of the first 10 turns are brief 054's ideas or their follow-ups. Turns 1 to 4 reached only step 3 and were rerun in turns 5 to 8, so 6 distinct ideas were tested in the first 10 turns (night 7: 1 of 10) | pass |
| C2 | A discovery's brief is linked to its discovery | 3 discovery briefs (055, 056, 057), each with its `discovery:` field. `select_next --top 100` ranks all 8 of their ideas with line 7.g and generation 1 (055, from a generation-0 idea) or 2 (056 and 057, from generation-1 ideas). All rank after the theme's own follow-ups (ranks 11 to 22). A 4th discovery became no brief: step 1 said "already indexed: 038" | pass |
| C3 | Discoveries are not the held rebound | 4 discoveries, 0 of them the next-day rebound: a choppy-market 20-day continuation, a calm-market 5-day continuation, a failed monthly high that rises, a monthly-low break after a rise that falls | pass |
| C4 | The profile map is kept and read | Register: the run confirmed no book, so it added 0 books and `register/PROFILE_MAP.md` was correctly left unchanged; the rewrite after an added book is **not exercised**. Line 7.e rerun on night 7's `034-01_rising-nearness-to-high-rises_1d` (0.51 USD): 7 findings, 0 ideas, 0 discoveries. Its reason: "the profile map already holds exactly these ideas as 034-01.e1 ... and 034-01.b1", the two ideas night 7's 7.e wrote from this backtest. It wrote no discovery the map lists; no proposal, so "names a profile" is not tested | pass on what ran; partly untested |
| C5 | A book is flat when its idea says so | 9 backtests of the run, 1,520 coin-windows: 85 bars where the forecast is 0, every bet has left its holding period (`min_holding_bars`: 5 or 10) and the book holds a position under the band. 0 of them still open after the bar. The 7.e rerun's backtest: 306 windows, 66 such bars, 0 open. (Bars inside a holding period keep their position by design and are not counted) | pass |
| C6 | No fault | 0 failed turns (the loop's 19 lines: 13 turns, 1 components call, 4 discovery outcomes, 1 budget stop). 9 of 9 plans: the idea names a profile, and the plan has its `Profile:` line and its config has the gate. The 3 component builds are committed on `pilot-chain` (commit b426f8d, `trading-bot/strategies/strategy_components.py` and `tests/built_components/`). Note: the run's components are on `pilot-chain` only; merging them stays the operator's go | pass |

**Cost:** 15.66 USD for the run: the loop stops after the turn that crosses the budget, so it ended 0.66 above the 15.
Of this, step 1 and step 2 cost 0.96 and the components step 2.25. Plus 0.51 USD for the 7.e rerun. Total 16.17 USD.

**Outcome:** all six pass on what the run exercised. The chain behaved as designed, with no fault.
Untested: the profile map's rewrite after a book is added to the register (no book was confirmed), and a 7.e proposal
naming a profile (7.e proposed nothing). Nothing to fix. One thing a night will show that this pilot could not: C4's
register half, on the first confirmed book.
