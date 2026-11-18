---
brief: 005_rsi-divergence-predicts-reversal
source-idea: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence
line: 7.d not profitable
backtest: 005-02_bullish-rsi-divergence-rebound.d1_slow-rebound-after-deep-divergence_1d
instruments: BTC, ETH, BNB
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's close makes a new 30-day low while its 14-day RSI is above its reading at the previous low in that window, the price rebounds over the next 5 days. The rebound is larger the further the RSI stays above its earlier trough.
Consequence: The divergence low is a reason to buy a few-day bounce held long enough to cover fees, not a weeks-long hold through the fall.
Why:
- F2: Fees consume the gain. The 117 trades have a median duration of 1 day (mean 1.67 days). They earn +0.021% on average before fees and -0.079% after, so the book trades one-day holds and not the 20-day hold the idea describes.
- F4: The 20-day rebound is not in the data. On 55 non-overlapping divergence events the mean 20-day return is -1.5%, or -4.1% against the coin's average. The mean 5-day return is +0.86%, so any bounce comes in the first days and is then given back.
- F5: The bounce fades within the episode. Held bars in the first 2 days of the regime earn +0.27% per day above the coin's average (133 bars, summed gain +0.091). Bars more than 10 days in earn -0.91% per day (42 bars, summed gain -0.034).
- F6: The proposed grading carries no information. The 30-day fall has Spearman -0.01 with the 20-day excess return across the events, and the step-5 forecast-vs-outcome Spearman is -0.11.
