# Topic 49: ideas name the market profile they act in

Status: built 2026-11-24 (option A); proof below  
Where: research: common (`market_profile.md`, `idea_definition.md`, `lib.py`), steps 1, 2, 3, 7; a review tool for the profile map (later)  
Opened: 2026-11-24, the operator, from the P10 pilot ("strategies exploit a market profile and a side: see which are
taken and which are not"); next steps 1d.

## Question
Can the research write and test ideas that act in one market profile only, so that the portfolio gets strategies for
the kinds of market today's strategies do not specialise in?

## Seen
- **No strategy specialises in a profile** (topic 44, P10 pilot, 2026-11-24): the 22 candidates' days in a position
  follow the market's own days in all six profiles (002-03: 32, 13, 24, 4, 18, 9 % against the market's 31, 14, 22, 3,
  17, 11 %). They differ by side only. Every cell of the profile map is empty of specialists.
- **A profile chosen after the fact does not repeat:** a strategy's gain in a profile on 2018-21 keeps its sign on
  2022-25 in 50 % of 132 cells. A profile must therefore be part of the idea before its test, not picked from its
  results.
- **Real books fail where their effect does not hold** (topic 47, study 1): an idea that names where it lives is tested
  where it should work.
- **A coin's own profile** matches the six coins' average on 46 to 63 % of days (`common/market_profile.md`): each coin is
  read on its own bars (the one-coin rule kept).
- **The components exist:** the trend (`PriceEvolutionComponent`) and the agitation
  (`VolatilityPercentileRegimeComponent`); the regime (`threshold_rules`) is how step 3 already builds a situation (N3).

## Why it matters
Without it, every idea acts in every profile, so every strategy is "always on, one side", and no combination can spread
the portfolio across kinds of market.

## The terms (business definitions: `common/market_profile.md`)
Market profile; its trend (rising, choppy, falling) and agitation (calm, agitated); the six profiles; an idea's
profile; a profile specialist; a strategy's home; the profile map.

## What changes, step by step (the design)
| Where | Change | Why |
|---|---|---|
| `common/market_profile.md` | The definition: the six profiles, read on the coin's own bars, and how step 3 builds one | one definition, read by every step |
| `common/idea_definition.md` | One line: an idea may name one market profile as the place its effect lives: its trend, its agitation, or both, only what its theory implies | the regime clause already allows a market condition; the profile is its standard form |
| Step 1 (briefs) | A brief may target a cell of the profile map ("in a falling, agitated market, ..."); the map's empty cells are offered as themes | the search goes where no strategy acts |
| Step 2 (ideas) | When the brief's theory depends on the market's state, the idea names its profile (one of the six) | the profile is part of the idea before the test |
| Step 3 (plans) | A named profile is built by code from the idea's `profile:` line (vetoes to a flat regime, the definition's settings); the model writes the forecast as if it were not there | the book trades the idea where it lives, built the same way for every idea (as the side is) |
| Step 5 (verdict) | Unchanged: the cases are the in-profile bets, since the book trades only there; the direction check (`explore_and_check.md`) reads the in-profile days of folds A and D | the verdict judges the idea where it claims to work |
| Step 7 (lines) | A line may propose "the same idea in one profile" when its findings show the effect lives there; the profile is then named, and checked on folds A and D | a repair or a narrower case, chosen on folds B and C, judged on all |
| The profile map | `topics/44_review/p10_map.py` reused as a review tool: every confirmed strategy by profile and side, the empty cells listed | where the portfolio has nothing; targets for briefs |

## Options
| Option | Gain | Risk |
|---|---|---|
| A. The profile as part of the idea (steps 1, 2, 3, 7), built as a regime | specialists by design; judged where they claim to work; existing components | rare profiles give few cases: choppy agitated is 3 % of days (about 100 days in 8 years per coin on daily bars): often "not observable" on 1d, better on 1h |
| B. A profile filter added to existing strategies after their test | no new ideas needed | the pilot shows the profile picked from results does not repeat (50 %): fitting noise |
| C. Briefs only (step 1 targets cells), steps 2 and 3 unchanged | small change | step 2 may write the idea without its profile, and step 3 build it everywhere |

Recommended: A. The profile is fixed before the test (B fails that), and every step that writes or builds an idea must
carry it (C does not).

## Proof plan (before the merge)
- Step 3: rerun on 3 fixed ideas that name a profile and 3 that do not: the first get the profile's regime with the
  definition's settings; the others are unchanged (same config as before).
- Step 2: rerun on 2 briefs, one whose theory depends on the market's state and one that does not: the profile is named
  only in the first.
- No change to any past record (the definition is read by the steps that write new ideas only).
- Cost: about 3 to 6 USD of model calls.

## Decisions
| Date | Decision | By | Why | Rejected, and why |
|---|---|---|---|---|
| 2026-11-24 | Option A, built | the operator ("go for that"), on the designer's recommendation | the profile is fixed before the test and carried by every step that writes or builds an idea | B: a profile picked from results repeats in 50 % of cells; C: steps 2 and 3 could drop it |
| 2026-11-24 | Step 3's code builds the profile, not the model: an idea's `profile:` line; one veto per condition the bar does not meet, to a regime with no position | the designer, at the build | one exact build for every idea (the settings cannot drift); the model's own regimes are untouched | the model building it from the definition: settings and forms would vary by idea |
| 2026-11-24 | An idea names only what its theory implies: its trend, its agitation, or both | the designer, from the proof (step 2 on brief 023 gave "choppy calm" where the brief says only "gone nowhere for weeks") | "add nothing the brief does not imply" (step 2); one rule for every case | six full profiles only: forces an element the theory does not state |
| 2026-11-24 | A coin's profile is read on its own bars, not on the six coins' average | the designer, on the one-coin rule | `idea_definition.md`: each coin is tested on its own bars only; the operator removed "an idea compared with the market" (1e) | the six coins' average (the pilot's measure): it would need a second series in the engine |

## Proof (2026-11-24; about 5.6 USD)
- **Step 2, 3 briefs:** 023 ("a coin that has gone nowhere for weeks") gives 2 ideas, `profile: choppy`; 025 ("a coin
  falling for months") 2 ideas, `profile: falling`; 031 (a wide flat day after a run, no market state) 4 ideas, no
  profile. First run on 023, with six full profiles only: 4 ideas `choppy calm`, "calm" stated nowhere in the brief;
  hence the decision above, then the rerun.
- **Step 3, 6 ideas** (`03_test_plan/topic49_proof_run/plans/`): the 2 "falling" ideas get plans whose config has the
  trend component (60 days) and one veto (60-day return at or above -10 % sends the bar to the flat regime), and a
  `Profile:` line; the model built no trend regime of its own. 2 ideas with no profile get plans with no veto. 2 others
  (023-01, 031-03) end "missing components", for reasons unrelated to profiles.
- **A backtest, idea 025-01** (6 coins, folds A to D, 17,524 daily bars; `49_review/profile_book_check.py`): the
  profile recomputed from each coin's own closes, apart from the engine. The engine's regime is the idea's exactly when
  the bar is in a falling market: 0 differences. The forecast is 0 on every bar outside it: 0 exceptions. 6,413 bars
  (37 %) are in the profile; of the book's 6,708 days in a position, 5,545 are in it, 766 are bets still held for the
  idea's 5-day horizon after the market left the profile (the holding period), and 397 are leftovers the engine does
  not close (a position under its rebalance band: topic 51, for every book).
- No past record changes: the definition is read only by the steps that write and plan new ideas.

## Status and next
Built. Next: a night with briefs aimed at profiles (a request naming a profile gets a theory for it); the profile map as
a review tool once profile specialists exist (`44_review/p10_map.py`).

## Links
`common/market_profile.md`; topic 44 (P10 pilot), topic 47 (study 1, 1d-12, 1d-13); `common/explore_and_check.md`;
`topics/44_review/p10_map.py`.
