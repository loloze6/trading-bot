# Topic 49: ideas name the market profile they act in

Status: open (designed 2026-11-24; waits for the operator's go)  
Where: research: common (`market_profile.md`), steps 1, 2, 3, 5, 7; a review tool for the profile map  
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
| `common/idea_definition.md` | One line: an idea may name one market profile as the place its effect lives | the regime clause already allows a market condition; the profile is its standard form |
| Step 1 (briefs) | A brief may target a cell of the profile map ("in a falling, agitated market, ..."); the map's empty cells are offered as themes | the search goes where no strategy acts |
| Step 2 (ideas) | When the brief's theory depends on the market's state, the idea names its profile (one of the six) | the profile is part of the idea before the test |
| Step 3 (plans) | A named profile is built as the regime, with the definition's settings, the forecast graded inside it | the book trades the idea where it lives (as N3 does for a situation) |
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
| 2026-11-24 | A coin's profile is read on its own bars, not on the six coins' average | the designer, on the one-coin rule | `idea_definition.md`: each coin is tested on its own bars only; the operator removed "an idea compared with the market" (1e) | the six coins' average (the pilot's measure): it would need a second series in the engine |

## Status and next
Designed; the operator's go on option A, then the build and its proof; then a night with briefs aimed at the map's empty
cells.

## Links
`common/market_profile.md`; topic 44 (P10 pilot), topic 47 (study 1, 1d-12, 1d-13); `common/explore_and_check.md`;
`topics/44_review/p10_map.py`.
