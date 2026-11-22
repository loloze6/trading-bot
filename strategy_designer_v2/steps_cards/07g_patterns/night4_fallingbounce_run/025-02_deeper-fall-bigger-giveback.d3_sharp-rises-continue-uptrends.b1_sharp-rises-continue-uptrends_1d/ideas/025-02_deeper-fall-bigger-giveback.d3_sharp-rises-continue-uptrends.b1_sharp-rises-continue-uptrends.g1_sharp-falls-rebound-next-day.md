---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-02_deeper-fall-bigger-giveback.d3_sharp-rises-continue-uptrends.b1_sharp-rises-continue-uptrends
line: 7.g patterns
backtest: 025-02_deeper-fall-bigger-giveback.d3_sharp-rises-continue-uptrends.b1_sharp-rises-continue-uptrends_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In each coin, the larger the day's fall measured against the standard deviation of its last 20 daily returns, the larger its rise over the next 1 day. Ordinary down days are followed by almost no rebound, and falls of several usual daily moves by the largest.
Consequence: A trader should expect a one-day rebound after a coin's sharp vol-scaled fall, and should refuse to short into it on the next day.
Why:
- F1: Measured over all six coins, a day's fall as a multiple of its 20-day daily volatility goes with a rise the next day. The Spearman correlation of that ratio with the next day's unusual return is -0.078 over 14356 day-cases (p 1e-20). It is negative in every coin (-0.039 to -0.114; p < 0.001 in five of six) and in both 90-day regimes (falling -0.098, rising -0.058).
- F2: The next-day rebound comes from down days, not up days. On z<0 days the Spearman is -0.064 (n 7056, p 7e-8); on z>0 days it is -0.011 (n 7286, p 0.35). The next day's unusual move is +0.48 % (t 3.26, n 1310) after a fall of 1–2 usual daily moves and +0.68 % (t 2.57, n 484) after a fall of more than 2. Both are 2.5–3.5 times the 0.19 % cost of a trade.
- F3: The rebound is short. On a non-overlapping 3-day grid, falls of more than 2 usual moves are followed by only +0.39 % (t 0.67, n 170), and the 3-day Spearman shrinks to -0.035 (p 0.017). It also weakens in later years: Spearman -0.157 in 2018, -0.028 in 2024 and +0.003 in 2025.
