---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-02_fading-volume-downrun-rebound-size
line: 7.d not profitable
backtest: 024-02_fading-volume-downrun-rebound-size_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: When a coin has risen over the past 30 days and then falls in an unbroken streak of four-hour periods on declining volume, it rises over the next three days. The larger its 30-day rise, the larger that rise.
Consequence: A trader treats fading-volume pullbacks as buying chances in proportion to the strength of the coin's 30-day trend.
Why:
- F4: The rebound appears only when the coin has risen over the past 30 days. In the top quartile of the 30-day return (above +16.4 %, 851 cases) the unusual move is +0.98 % with t 2.96. In the other three quartiles it is −0.35 % (t −1.19), −0.30 % (t −1.36) and −0.09 % (t −0.40).
- F6: Inside the 30-day down state, the bets the book takes lose even after drift is removed. Cases with a low forecast lose −0.69 % (t −2.64, 800 cases) and cases with a mid forecast lose −0.89 % (t −2.90, 728). Inside the 30-day up state, the move grows with the forecast: −0.45 % for low, +0.56 % for mid, +0.69 % for high (t 2.55, 984 cases).
- F5: The book's falls sit in the coin's 30-day down states. On days when the coin's 30-day return is negative, the book's mean daily return is −0.011 % (6,411 coin-days), against +0.181 % when it is positive (6,650). Summed bar gains are +0.08 and −0.90 in the two lowest 30-day-return quartiles, against +6.59 and +9.41 in the two highest.
