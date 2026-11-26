---
line: 7.d confirmed, not profitable
backtest: 039-01_scaled-fall-next-day-rebound_1d
idea tested: 039-01_scaled-fall-next-day-rebound
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 3
cost: 0.5995 USD
---
## Findings
- **F1:** Size swings drive the failing Calmar (0.636 on the record), not losing trades. My rebuild of the book with costs had its deepest fall in w9 (−27.7 %). In that fall, the 36 bars after falls beyond 1.5 usual moves were held at a mean allocation of 1.12 and summed −1.19 of the fall's gain. The bars after falls of 1 to 1.5 moves summed +0.04. Capping the position at 0.5 of the book cut the deepest fall from −27.6 % to −18.6 % and raised the rebuilt Calmar from 0.99 to 1.32 (Sharpe 0.99 to 1.18) for a yearly return only 2.8 points lower (27.3 % to 24.5 %).
- **F2:** The effect is graded but noisy at its top. Next-day excess return rises with the scaled fall:
- **F3:** Big falls rebound most when they come inside a deeper fall. After a fall beyond 1.5 moves with the 5-day return below −15 %, the next-day excess is +2.18 % (143 cases on 52 days, day-clustered t 1.94). With a shallower 5-day return it is +0.50 % (263 cases on 110 days, t 0.97). The 5-day fall alone, without a large scaled fall, is followed by −1.99 % (219 cases), so the condition is not an effect of its own. Keeping the book only when the 5-day return is below −5 % cut its deepest fall to −16.9 % and raised the rebuilt Calmar to 1.14.
- **F4:** The rebound lives where the coin is swinging more than usual. I measured agitation as the coin's 30-day swing against its 90-day swing.
- **F5:** The 60-day trend does not separate the losses, so trend is not the repair. Falls beyond 1.5 moves are followed by +1.09 % in falling trends (155 cases) and +1.69 % in rising ones (72 cases). Leaving out falling-trend bars deepened the rebuilt fall to −34.0 % (Calmar 0.62). Across the deepest fall of each window, held bars lost in every trend: rising −3.2 %, choppy −2.4 %, falling −1.5 % mean excess.
- **F6:** Dropping the shallow falls does not repair the falls either. Keeping only falls beyond 0.5 moves left the deepest fall at −28.1 % and lowered the rebuilt Calmar to 0.87. The small falls under 0.5 moves earn +0.10 % excess, below the 0.19 % cost of a trade.

## Ideas
- `039-01.d1_scaled-fall-rebound-capped` (from F1, F2): After a down day, a coin rises over the next day, more so the larger that day's fall in units of its 30-day daily-return standard deviation, while the next-day rise measured against the next day's own swing stops growing once the fall goes beyond about one usual daily move.
- `039-01.d2_scaled-fall-within-slide` (from F3, F1): After a down day, a coin rises over the next day, more so the larger that day's fall in units of its 30-day daily-return standard deviation and the deeper the coin's 5-day fall up to that day.
- `039-01.d3_agitated-scaled-fall-rebound` (from F4, F2): In an agitated market, after a down day, a coin rises over the next day, more so the larger that day's fall in units of its 30-day daily-return standard deviation.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
