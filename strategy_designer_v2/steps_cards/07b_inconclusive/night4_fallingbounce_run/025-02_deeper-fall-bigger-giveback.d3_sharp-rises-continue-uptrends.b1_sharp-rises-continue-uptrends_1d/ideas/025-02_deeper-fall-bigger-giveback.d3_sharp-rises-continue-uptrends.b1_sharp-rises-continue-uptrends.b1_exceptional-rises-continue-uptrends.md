---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-02_deeper-fall-bigger-giveback.d3_sharp-rises-continue-uptrends.b1_sharp-rises-continue-uptrends
line: 7.b inconclusive
backtest: 025-02_deeper-fall-bigger-giveback.d3_sharp-rises-continue-uptrends.b1_sharp-rises-continue-uptrends_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 90-day return is positive, on days whose rise is the largest of its last 60 days measured against the standard deviation of its last 20 daily returns, the larger that rise against the volatility, the larger the coin's rise over the next 10 days.
Consequence: In a rising coin, a trader should follow only the rare up days that stand out against both recent volatility and the past two months' rises, and refuse the continuation on ordinary up days.
Why:
- F1: The test's cases are mostly ordinary up days. Of the 750 cases with a known rise, 358 rose 0–1 usual daily moves (mean unusual move −0.58 %, t −0.73) and 289 rose 1–2 moves (+0.16 %, t 0.15). Together they drown the 82 cases of 2–3 moves (+5.48 %, t 2.14) and the 21 cases above 3 moves (+3.07 %). That is why the main measure ends at −0.16 % with t −0.27 over 930 cases.
- F2: The plan's dead zone did not do its job. The forecast averaged 4.9 on 0–1-move rises and 15.5 on 1–2-move rises, so the 2-point trigger counted ordinary rises as cases. All rises above 2 moves sat at the cap of 20, so the top of the scale was not graded.
- F3: Within the tested cases, the effect is in the strongest forecasts only. The top forecast quartile gained +3.16 % (t 2.22, 230 cases), while the three lower quartiles lost −1.42 % (t −1.50), −1.93 % (t −1.71) and −0.47 % (t −0.40). This is why the supporting check passes at +2.84 % while the mean is zero.
- F4: Measured directly on prices in coins with a positive 90-day return, the 10-day unusual move grows with the day's rise in 20-day volatility units, taking the first rise per 10-day cell. Rises of 0–1 moves gained +0.39 % (t 0.66, 792), 1–2 moves +0.98 % (t 1.13, 500), 2–3 moves +3.97 % (t 2.69, 184) and above 3 moves +4.87 % (t 1.35, 59).
- F6: Rises above 2 moves in rising coins point the same way in every coin, though no single coin reaches t 2 on its own. The 10-day unusual move runs from +0.09 % (XMR, 36 cases) to +8.78 % (XRP, 40), with BTC +1.67 %, ETH +2.96 %, LTC +3.17 % and ZEC +8.37 %.
