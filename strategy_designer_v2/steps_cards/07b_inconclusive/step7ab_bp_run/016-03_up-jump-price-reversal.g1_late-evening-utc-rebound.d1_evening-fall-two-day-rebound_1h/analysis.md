---
line: 7.b inconclusive
backtest: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-two-day-rebound_1h
idea tested: 016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-two-day-rebound
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.3557 USD
---
## Findings
- **F1:** The tested relation points the way the idea predicts but is far too small to clear the bar or a trade's cost: step 5's pooled slope t is 1.70 on 4,236 non-overlapping cases. Per case the unusual move is +0.10 % over 48 hours, a strength of 0.016, about a third of the usual 0.05 (findings F10). That is 0.5 times the 0.19 % cost of a buy and a sell (findings F11).
- **F2:** The effect is mixed across coins and drowned by the market's own moves.
- **F3:** The gain sits in the deepest falls only.
- **F4:** The 48-hour horizon is not where the relation is clearest.
- **F5:** The 20:00 UTC hour is not where the rebound shows; it is among the weakest hours.
- **F6:** The rebound follows falls made as a grind, the opposite of the brief's jump story.
- **F7:** The rebound shows mainly while the coin is below its level of 30 days earlier: slope t 1.90 (2,768 cases) there, against -0.53 (1,496 cases) after a 30-day rise.
- **F8:** Without the clip to falls, the evening's raw 24-hour return has no linear relation to the next 48 hours (slope t -0.65, 8,446 cases). The relation is U-shaped: both extreme quintiles are followed by about +0.3 % (falls of -6.2 %: +0.30 %; rises of +6.5 %: +0.27 %), and the middle three by -0.20 % to -0.36 %.

## Ideas
- `016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-two-day-rebound.b1_evening-fall-rebound-more-coins` (from F1, F2): The more a coin has fallen over the 24 hours up to the 20:00 UTC close, the more it rises over the next 2 days.
- `016-03_up-jump-price-reversal.g1_late-evening-utc-rebound.d1_evening-fall-two-day-rebound.b2_evening-grind-fall-rebound` (from F3, F6): The more a coin has fallen over the 24 hours up to the 20:00 UTC close, the more it rises over the next 2 days, only while that fall was made of many small hourly steps rather than a few large hours.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
