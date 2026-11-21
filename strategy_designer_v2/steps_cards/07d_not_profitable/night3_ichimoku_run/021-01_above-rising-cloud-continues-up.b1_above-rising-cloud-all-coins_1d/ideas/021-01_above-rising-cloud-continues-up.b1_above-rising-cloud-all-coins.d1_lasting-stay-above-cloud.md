---
brief: 021_ichimoku-cloud-as-a-watched-equilibrium
source-idea: 021-01_above-rising-cloud-continues-up.b1_above-rising-cloud-all-coins
line: 7.d not profitable
backtest: 021-01_above-rising-cloud-continues-up.b1_above-rising-cloud-all-coins_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin closes above its Ichimoku cloud and the cloud is rising, its return over the next 26 days is positive, and larger the more days the coin has stayed continuously above a rising cloud. The cloud is the band between the average of the 9-day and 26-day high-low midpoints and the 52-day high-low midpoint, plotted 26 days ahead.
Consequence: A trader would add to a coin the longer it has held above a rising cloud, and stay small just after it first crosses.
Why:
- F1: The book fails on gain mostly because it is rarely in the market. It holds 0.20 of the book on average and is in only 39 % of coin-days. Its mean daily return is 0.000386 against holding's 0.001344. Of that 0.000386, 0.000279 comes from the coins' own rise and only 0.000108 from timing. Its Sharpe is 0.558 against holding's 0.586.
- F2: The forecast's gradation by cloud slope is not in the data. The rank correlation between forecast and excess return is -0.027. By forecast quartile the 26-day excess return runs +10.6 %, +3.6 %, -0.8 % and +17.6 %, so sizing by slope adds risk without adding gain.
- F3: The cases just entering the regime lose, and the mature ones carry the gain. At 1 bar in the trending regime the 26-day excess return is -3.2 % and only 29 % of cases rise (70 cases). At about 3 and 13 bars in it is +7.5 % and +6.2 %. At about 36 bars in it is +20.7 % (t 2.0, 65 % rise, 69 cases).
- F4: The trades say the same thing. Of 1644 trades the median net return is -0.30 % and 48.6 % win. The 537 trades closed after 13 to 26 days have a median of -6.1 %. The 315 trades held 40 to 80 days have a median of +20.5 % (mean +38.8 %), and the 89 held over 80 days have a mean of +77 %. The gain is in long-lasting stays above the cloud, and the losses are in short-lived crossings.
- F5: The Calmar fails on a 55 % fall lasting 646 days across 6 windows. Over the same stretch holding lost only 25.5 %, while the book held 0.23 on average and was in 53 % of coin-days. The fall comes from repeated failed entries, not from a market crash.
