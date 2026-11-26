---
line: 7.d confirmed, not profitable
backtest: 032-02.b1.e2_tight-range-breakouts-continue_1d
idea tested: 032-02.b1.e2_tight-range-breakouts-continue
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4742 USD
---
## Findings
- **F1:** The Calmar fails because of a slow chained bleed, not one crash: the book's deepest fall of the chain reaches −9.0 % in w16 from a peak set by w11. Windows w12 to w16 sum to −2.6 %, 0, 0, +0.6 % and −0.5 % of daily returns. No single window falls more than −6.3 %. The yearly return is only +5.7 %, and the gain sits in w10 (+10.0 %) and w17 (+14.9 %).
- **F2:** Most of the gain comes from breakouts out of the tightest ranges, and wide ranges barely pay. By tercile of the prior 60-day range, the 45 trades return a mean of +21.8 % in the tightest (median +10.7 %, worst drawdown during the trade −3.1 %). The middle tercile returns +15.0 % (median −0.7 %, drawdown −10.8 %) and the widest +1.6 % (median −0.4 %, drawdown −9.1 %). The rank correlation of range width with the trade's return is −0.21.
- **F3:** The book does not grade by tightness as the idea says, because the forecast is standardised over its own past 60 values. On active bars, its rank correlation with raw tightness is −0.02. The tightest-range trades carry +1.70 of the summed position-weighted return, against +0.02 for the widest, yet they are not given a larger forecast.
- **F4:** The breakout bar's own signal holds without the book's holding rules. On non-overlapping choppy breakouts (ER(60) ≤ 0.3), the 10-day return is +23.9 % in the tightest tercile (t 1.81, 12 cases, range about 28 %) against +5.3 % and +11.4 % in the wider ones. Those tight breaks closed back below the old high on only 12 % of the next 10 days, against 29 % and 32 % for the wider ones.
- **F5:** The effect strengthens over a longer horizon. Over 20 days, tight-range choppy breakouts return +21.6 % against +4.9 % (mid) and +4.7 % (wide). The rank correlation of range width with the return is −0.33 at 20 days against −0.24 at 10 days.
- **F6:** Tightness alone is not the effect. On the 10-day grid, bars in the tightest-range tercile without a breakout have an unusual move of −0.6 % (131 cases), against +23.2 % with a breakout (7 cases). For choppy bars the figures are −0.7 % (128) against +9.5 % (5). The narrow range only matters through the idea's own situation, the break of the 60-day high.
- **F7:** The losing trades are the ones that fail fast. The 6 trades down more than 5 % two days after entry end at −6.8 % on average, and they earn −0.1 % over the rest of their hold. Trades that are flat or up after two days go on to earn +10 % to +16 % more.
- **F8:** The single worst loss comes from volatility sizing on the calmest coin. A BTC trade in w11 (2021) held 0.93 of the book and lost 19.5 %, costing 18.1 % of the coin's book. BTC's 10 trades average −1.1 %, while its mean position (0.30) is among the largest.
- **F9:** Costs do not explain the shortfall. The total move per case (+5.67 %) is 29.4 times the 0.19 % cost of a trade, so the failure is in which breaks are held and how big, not in fees.

## Ideas
- `032-02.b1.e2.d1_raw-tightness-graded-breakouts` (from F2, F3, F4, F6, F8): In a coin that has gone nowhere over the past 60 days, a daily close above its prior 60-day high is followed by a rise over the next 10 days. The rise grows with how narrow the 60-day range was relative to the price, and the narrower the range, the fewer of those days the coin closes back below the old high.
- `032-02.b1.e2.d2_tight-breakouts-held-longer` (from F1, F5, F6): In a coin that has gone nowhere over the past 60 days, a daily close above its prior 60-day high is followed by a rise over the next 20 days, and the narrower that 60-day range was relative to the price, the larger the rise.
- `032-02.b1.e2.d3_failed-breakouts-give-nothing` (from F1, F4, F7): In a coin that has gone nowhere over the past 60 days, a daily close above its prior 60-day high is followed by a rise over the next 10 days only while the coin holds above that old high. The further the coin has fallen back from its breakout close in the two days after it, the smaller the rise that remains.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
