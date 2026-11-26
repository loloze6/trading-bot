# Topic 54: the regime calculation, and a verdict on it against what the market really did

Status: parked (the operator, 2026-11-25)  
Where: research: common (`market_profile.md`), step 3 (`add_profile`), a verification like step 5's; the engine's regime
detector (`strategies.regime_detector`, its components)  
Opened: 2026-11-25, the operator, from the questions on where a strategy really trades: "the regime calculation is
static and questionable. It can work, but tomorrow, for coins that do not follow the same standard of return, it will
not identify the regime properly. We have in the strategy config a complete way to calculate various regimes we could
use for a more precise regime calculation. And for verification, as for forecasts and the analysts, we could look at
all the bars to assess whether the regime was correctly calculated."

## Question
Does the market profile an idea names describe the market the coin is really in, on every coin, and how would we know?

## Seen (2026-11-25)
- **One fixed rule for every coin** (`common/market_profile.md`, topic 49): rising above +10 % over 60 days, falling
  below -10 %, choppy between; agitated when the 30-day swing is above its own past year's median. The agitation is
  relative to the coin; the trend is not: +10 % in 60 days is a large move for BTC and noise for a coin that often
  moves 30 % in a month.
- **What is checked today is the build, not the meaning:** the engine's regime equals the profile recomputed from the
  prices (topic 49's proof: 0 differences on 17,524 bars), and a strategy naming a profile trades inside it but for
  its horizon (2026-11-25, after 1l: 034-02 "rising" 94 % inside, 6 % within its 5-day horizon after, 0 other). No
  measure says whether "rising" was a rising market.
- **The tools exist:** the regime detector of a strategy config (`threshold_rules`, vetoes) on any component of the
  catalogue (trend strength, volatility rank, price evolution), the way step 3 builds an idea's situation (N3).

## Options (to weigh when it is opened)
| Option | Gain | Risk |
|---|---|---|
| A. A verdict on the regime first: for every coin and day, the profile announced at the close against what the market did after (for example its return and swing over the next 60 days), counted by coin, like step 5 counts an idea against the bars | measures how wrong the regime is, and where (which coins, which profiles), before changing anything; may look ahead, as a verdict reads the outcome after the fact and decides nothing | none on the strategies |
| B. A per-coin rule: the trend measured against the coin's own usual move (for example the 60-day return in units of its own swing) | the same meaning on every coin | every specialist changes; to choose by A's measure, not by results |
| C. Regimes built from the config's regime detector (several components) | richer, more precise regimes | more settings, so more ways to fit noise; one definition must stay shared |

Recommended when opened: A first; B or C only if A shows the fixed rule misreads some coins or profiles.

## Decisions
| Date | Decision | By | Why | Rejected, and why |
|---|---|---|---|---|
| 2026-11-25 | Parked | the operator | the questions on planned against real regime | |

## Status and next
Parked. Any change of the definition changes every profile specialist (topic 49) and the profile map: after A.

## Links
`common/market_profile.md`; topic 49; topic 53 (coins differ); `03_test_plan/helper/make_test_plan.py` (`add_profile`);
`topics/49_review/profile_book_check.py`.
