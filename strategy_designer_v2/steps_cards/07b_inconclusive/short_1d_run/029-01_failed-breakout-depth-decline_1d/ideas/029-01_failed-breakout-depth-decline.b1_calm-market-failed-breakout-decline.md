---
brief: 029_failed-breakout-traps-late-buyers
source-idea: 029-01_failed-breakout-depth-decline
line: 7.b inconclusive
backtest: 029-01_failed-breakout-depth-decline_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: When a coin's daily close moves above its prior 20-day high and then, within the next 3 days, closes back below that old high, the coin falls over the next 5 days, only while the coin's 20-day volatility of daily returns is low, and the lower that volatility, the larger the fall.
Consequence: A trader would short a failed breakout in a calm market and refuse the short when the coin has been swinging widely, because there failures tend to recover.
Why:
- F5: The effect shows only when the coin's 20-day volatility of daily returns is low, and it reverses when volatility is high. In the low-volatility tercile the 5-day short return is +2.23 % (t 2.54, 78 cases). It is -1.72 % in the middle tercile (t -1.55) and -3.31 % in the high tercile (t -1.91). The Spearman rank correlation between volatility and the 5-day short return is -0.161 (p 0.013, 235 cases).
- F1: Step 5's main measure is essentially zero and slightly on the wrong side: -0.13 % short-direction excess per case over 5 days, t -0.29, on 617 cases. On my own 5-day grid it is -0.16 %, t -0.22, on 272 cases, and no horizon from 1 to 20 days gets past |t| 1.34 (10 days: +1.03 %, t 0.93, 137 cases).
- F3: A deeper failure does not lead to a larger fall. Against the raw depth below the old high, the Spearman rank correlation is 0.005 over 5 days (p 0.93, 272 cases) and 0.100 over 10 days (p 0.25). By depth tercile the 5-day excess is -0.15 % for the shallowest, -0.72 % for the middle and +0.39 % for the deepest.
- F4: Failed breakouts are often followed by a fresh attempt higher, which the brief names as a way the theory fails: 48.5 % of the 235 failures closed above the breakout bar's close within the next 10 days.
