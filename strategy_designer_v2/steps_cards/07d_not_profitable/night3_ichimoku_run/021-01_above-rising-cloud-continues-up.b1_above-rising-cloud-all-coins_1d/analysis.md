---
line: 7.d not profitable
backtest: 021-01_above-rising-cloud-continues-up.b1_above-rising-cloud-all-coins_1d
idea tested: 021-01_above-rising-cloud-continues-up.b1_above-rising-cloud-all-coins
step 5: inconclusive
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.5288 USD
---
## Findings
- **F1:** The book fails on gain mostly because it is rarely in the market. It holds 0.20 of the book on average and is in only 39 % of coin-days. Its mean daily return is 0.000386 against holding's 0.001344. Of that 0.000386, 0.000279 comes from the coins' own rise and only 0.000108 from timing. Its Sharpe is 0.558 against holding's 0.586.
- **F2:** The forecast's gradation by cloud slope is not in the data. The rank correlation between forecast and excess return is -0.027. By forecast quartile the 26-day excess return runs +10.6 %, +3.6 %, -0.8 % and +17.6 %, so sizing by slope adds risk without adding gain.
- **F3:** The cases just entering the regime lose, and the mature ones carry the gain. At 1 bar in the trending regime the 26-day excess return is -3.2 % and only 29 % of cases rise (70 cases). At about 3 and 13 bars in it is +7.5 % and +6.2 %. At about 36 bars in it is +20.7 % (t 2.0, 65 % rise, 69 cases).
- **F4:** The trades say the same thing. Of 1644 trades the median net return is -0.30 % and 48.6 % win. The 537 trades closed after 13 to 26 days have a median of -6.1 %. The 315 trades held 40 to 80 days have a median of +20.5 % (mean +38.8 %), and the 89 held over 80 days have a mean of +77 %. The gain is in long-lasting stays above the cloud, and the losses are in short-lived crossings.
- **F5:** The Calmar fails on a 55 % fall lasting 646 days across 6 windows. Over the same stretch holding lost only 25.5 %, while the book held 0.23 on average and was in 53 % of coin-days. The fall comes from repeated failed entries, not from a market crash.
- **F6:** The result swings by period. In windows 13 to 18 the cases' excess return is -17.3 % (t -4.19, 29 % rise, mean worst point -30 %, 59 cases). In windows 7 to 12 it is +33.8 % (t 3.09, 67 cases). Window 16 alone cost the book 30.5 % while holding gained 37 %.
- **F7:** Outside the regime the coins do worse than their drift, and the more so the more they fell. Across all 919 out-of-regime cases the 26-day excess return is -2.3 % (t -2.6). For the two lowest quartiles of the past 26-day return (about -30 % and -12 %), it is -5.1 % (t -2.77) and -5.1 % (t -2.57), with about 175 cases each.
- **F8:** Cost is not the cause. The unusual move per case is +1.0 % and the total +6.3 % over 26 days, 4.5 and 28 times the 0.22 % round trip. The mean commission per trade is 0.16 %.

## Ideas
- `021-01_above-rising-cloud-continues-up.b1_above-rising-cloud-all-coins.d1_lasting-stay-above-cloud` (from F1, F2, F3, F4, F5): When a coin closes above its Ichimoku cloud and the cloud is rising, its return over the next 26 days is positive, and larger the more days the coin has stayed continuously above a rising cloud. The cloud is the band between the average of the 9-day and 26-day high-low midpoints and the 52-day high-low midpoint, plotted 26 days ahead.
- `021-01_above-rising-cloud-continues-up.b1_above-rising-cloud-all-coins.d2_off-cloud-fallers-keep-lagging` (from F7, F1): When a coin is not trading above a rising Ichimoku cloud, its return over the next 26 days falls short of its normal drift, and by more the further it has fallen over the past 26 days.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
