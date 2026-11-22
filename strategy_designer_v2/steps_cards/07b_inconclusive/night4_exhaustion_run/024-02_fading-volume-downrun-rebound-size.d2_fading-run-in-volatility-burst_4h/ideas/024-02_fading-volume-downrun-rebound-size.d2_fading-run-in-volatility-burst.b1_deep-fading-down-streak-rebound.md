---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-02_fading-volume-downrun-rebound-size.d2_fading-run-in-volatility-burst
line: 7.b inconclusive
backtest: 024-02_fading-volume-downrun-rebound-size.d2_fading-run-in-volatility-burst_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin has just fallen in an unbroken streak of four-hour periods with the volume across the streak declining, and the streak's loss is large against the coin's typical four-hour move over the past 30 days, it rises over the next three days. The rise is larger the larger that loss, and larger still the higher the coin's volatility over the past 5 days against its volatility over the past 30 days.
Consequence: A trader takes the rebound bet only on deep fading-volume down-streaks, sized up in volatility bursts, and refuses the shallow ones that make up most signals and lose.
Why:
- F2: The rebound shows only in the cases with the largest streak loss in usual moves. The top decile earns +1.86 % over 18 bars (t 4.00) and decile 8 earns +0.75 % (t 1.96), while deciles 0 to 6 range from -0.83 % to +0.01 % and are mostly negative (decile 0 is -0.63 %, t -2.11). The overall Spearman correlation is only 0.08.
- F3: In the top fifth of streak loss (912 cases, mean loss 4.1 % to 6.9 %, about 3.3 to 5.9 usual moves), the rise holds at every horizon: +0.69 % at 6 bars (t 3.99), +0.85 % at 12 (t 3.27), +1.31 % at 18 (t 4.33) and +1.50 % at 36 (t 3.35).
- F4: Inside that top fifth, high 30-bar volatility against its 180-bar average doubles the rise: +1.56 % (t 4.14, 662 cases) against +0.64 % (t 1.38, 250 cases). In the other four fifths, volatility adds nothing (-0.38 % against -0.31 %).
- F5: The top-fifth rise has the idea's sign on all six coins, from LTC +0.22 % to ZEC +2.38 % (t 2.34) and XMR +1.52 % (t 2.84). It is positive in 6 of 8 years, with 2021 at +4.30 % (t 4.40) and 2024 at +1.57 % (t 2.26). It is negative in the bear years 2018 (-0.43 %) and 2022 (-1.04 %).
- F6: The cases outside the top fifth are what drown the pooled result. They fall in 2018 (-1.72 %, t -3.50) and 2022 (-1.26 %, t -3.74), and almost all cases are 2-bar streaks (3808 of 4559, -0.03 %). The long bet therefore mostly carried the market's own falls, with no rebound in it.
- F7: The cost of a trade is 0.19 %. The top-fifth unusual move of +1.31 % per case is about 7 times that cost, while the pooled unusual move is -0.1 times it.
