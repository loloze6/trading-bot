---
line: 7.g patterns
backtest: 022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d2_momentum-near-recent-highs_1d
idea tested: 022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d2_momentum-near-recent-highs
step 5: inconclusive
step 6: profitable enough
mode: one call
explorations: 2
cost: 0.3806 USD
---
## Findings
- **F1:** The day after a coin's largest falls measured against its 20-day volatility (the lowest tenth of one-day return / 20-day volatility, per coin), its next-day return beats its normal drift by +53 bps (t 3.61, 1422 days); the second-lowest tenth gives +27 bps (t 2.12), and the effect holds in both halves of the windows (w1-12 +50 bps, t 2.60; w13-24 +57 bps, t 2.53). The total move, +66 bps, is about 3.5 times this backtest's 19 bps round trip.
- **F2:** The rebound is graded on down days only. On days the coin fell, each extra standard deviation of fall adds 32 bps to the next day's excess return (slope t -3.68, 6986 days). On days the coin rose, the slope is +9 bps per standard deviation (t 1.10, 7212 days), indistinguishable from zero.
- **F3:** The rebound after the largest falls grows with the level of volatility. By tercile of 20-day volatility, the next-day excess return is -2 bps (t -0.13), +30 bps (t 1.37) and +132 bps (t 3.89), with 474 days each.
- **F4:** The rebound grows when the coin is far below its 60-day high. By tercile of distance from the high, the next-day excess return after the largest falls is +33 bps (t 1.28), +16 bps (t 0.53) and +99 bps (t 2.39), with about 287 days each.
- **F5:** The rebound lasts about two days, then fades. Over the next 2 days the largest falls are followed by +54 bps excess (t 2.13, 730 non-overlapping cases); over 3 days, by +60 bps (t 1.57, 446 cases).
- **F6:** The tested continuation barely shows on the non-overlapping 10-day grid:
- **F7:** The book's gain comes from its long side. It earns +18.2 bps a day while long (10047 coin-days) and -0.2 bps while short (5398 coin-days). Its gain is negative in 2022 (-2.3 bps) and 2023 (-4.7 bps).
- **F8:** Saturdays stand out among the weekdays. The coins' next-day return exceeds their drift by +34 bps on Saturdays (t 4.08, 2484 days), and the excess is positive on all 6 coins, though BTC's is only +5 bps (t 0.40). It is positive in 7 of 8 years, with 2023 at -14 bps (t -1.13). This is only one of seven weekdays looked at, and it describes a day, not a graded situation.

## Ideas
- `022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d2_momentum-near-recent-highs.g1_rebound-after-outsized-daily-falls` (from F1, F2, F5): The larger a coin's one-day fall relative to its 20-day volatility, the higher its return over the next 1 to 2 days.
- `022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d2_momentum-near-recent-highs.g2_volatile-regime-fall-rebound` (from F1, F2, F3): While a coin's 20-day volatility is high, the larger its one-day fall relative to that volatility, the higher its return over the next day. The higher the volatility, the larger the rebound.
- `022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d2_momentum-near-recent-highs.g3_deep-drawdown-fall-rebound` (from F1, F4): The farther a coin trades below its 60-day high, the higher its return over the next day after a large one-day fall relative to its 20-day volatility.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
