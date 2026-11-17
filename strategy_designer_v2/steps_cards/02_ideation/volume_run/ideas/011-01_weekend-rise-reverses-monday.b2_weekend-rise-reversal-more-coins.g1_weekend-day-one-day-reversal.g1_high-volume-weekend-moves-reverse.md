---
brief: 011_weekend-moves-reverse-weekday
source-idea: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g1_weekend-day-one-day-reversal
line: 7.g patterns
backtest: 011-01_weekend-rise-reverses-monday.b2_weekend-rise-reversal-more-coins.g1_weekend-day-one-day-reversal_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO
bar: 1d
period: folds A, B, C, D
---
Idea: A coin's Saturday or Sunday one-day move, scaled by its 20-day volatility, is reversed over the next day, and the reversal is larger the higher that day's volume is relative to the coin's usual volume over the past 20 days.
Consequence: Weight weekend fades toward heavy-volume weekend moves and refuse to fade quiet, low-volume weekend drifts.
Why:
- F1: Weekend reversal is concentrated in weekend days with high relative volume, the opposite of what the brief predicted. The per-unit fade -z x next-day excess return is 0.0071 (t 4.66, n 2936) in the top third of volume relative to its 20-day median, against 0.0012 (t 1.90) in the middle third and 0.0005 (t 1.10) in the bottom third. When the coins are averaged per date first, the three thirds are 0.0040 (t 2.07, 618 dates), 0.0017 (t 1.35) and 0.0003 (t 0.38).
- F2: The weekend size-grading survives the volume weighting. Regressing the next-day excess return on z x relative volume gives a slope of -0.0017 (t -5.80), close in strength to z alone (slope -0.0041, t -6.31). The largest weekend rises (z>2) are followed by -1.52% (t -3.09, n 210), and z in 1 to 2 by -0.37% (t -1.86).
- F4: The weekend fade has faded over time. It was 0.0049 to 0.0066 a year in 2018–2021 (t 2.3 to 4.2) and 0.0006 to 0.0035 in 2022–2025 (t 0.33 to 2.53). Its date-clustered t is only -2.08 on Saturday and -1.76 on Sunday, so much of the pooled t of 4.6 comes from coins moving together.
