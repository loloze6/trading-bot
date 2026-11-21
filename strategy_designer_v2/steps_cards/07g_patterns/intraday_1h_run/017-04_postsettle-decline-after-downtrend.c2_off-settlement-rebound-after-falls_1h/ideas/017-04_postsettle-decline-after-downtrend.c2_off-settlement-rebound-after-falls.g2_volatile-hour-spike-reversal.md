---
brief: 017_funding-settlement-clock-pressure
source-idea: 017-04_postsettle-decline-after-downtrend.c2_off-settlement-rebound-after-falls
line: 7.g patterns
backtest: 017-04_postsettle-decline-after-downtrend.c2_off-settlement-rebound-after-falls_1h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1h
period: folds A, B, C, D
---
Idea: When a coin's hourly volatility over the past 24 hours is high, its last 1-hour return, scaled by that volatility, is followed over the next 2 hours by an opposite move that grows with the size of that hour's move. The reversal is several times larger than in calm periods.
Consequence: A trader should fade single-hour spikes mainly when volatility is high, because only there is the reversal likely to be large enough to pay the trading costs.
Why:
- F3: The reversal grows with volatility. By 24-hour volatility tercile, the bottom-minus-top spread is 1.3 bp (corr t −1.07) in calm bars, 5.0 bp (t −2.58) in middle bars and 29.7 bp (t −11.9) in volatile bars. In the volatile tercile the correlation of the scaled 1-hour return with the next 2 hours is negative in all 6 coins (−0.024 to −0.055, about 11,000 cases each).
- F1: The last hour's move reverses over the next 2 hours, measured on 41,310 non-overlapping 2-bar cases per quintile of the last 1-hour return divided by its 24-hour volatility. The quintile with the largest falls is followed by +6.74 bp of excess return (t 8.3). The quintile with the largest rises is followed by −4.54 bp (t −6.1), and the three middle quintiles fall in order between them (+2.53, −1.84, −3.42 bp).
- F5: The book loses money because of fees, not because its timing is wrong. Its gross gain per bar is 0.02 to 0.32 bp in every coin, against fees of 0.65 to 0.88 bp per bar, at 2.34 trades per day.
