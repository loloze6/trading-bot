---
brief: 024_exhaustion-after-an-extended-run
source-idea: 024-03_uprun-volume-fade-depth-giveback.d1_up-run-give-back-in-downtrends
line: 7.d not profitable
backtest: 024-03_uprun-volume-fade-depth-giveback.d1_up-run-give-back-in-downtrends_4h
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 4h
period: folds A, B, C, D
---
Idea: After an unbroken streak of rising four-hour periods whose gain is large relative to the coin's typical four-hour move over the past 30 days, the coin falls over the next three days, the larger the streak's gain the larger the fall, only while the coin's price is below its average price of the past 30 days, except when the coin has fallen far over the past 30 days, where the larger its 30-day fall the smaller the give-back that follows.
Consequence: A trader would short up-runs inside mild 30-day downtrends and refuse to short them after a deep 30-day fall, where the rally keeps rising.
Why:
- F5: The deeper the discount, the worse the short, which runs against the idea's grading. By quartile of depth below the 30-day average, the unusual move is +0.44 %, +0.78 %, +0.48 % and +0.12 %, and the total move falls from +0.37 % (depth 3.6 %) to −0.30 % at the deepest quartile (depth 20.7 %).
- F6: After the steepest 30-day falls, the rally keeps going rather than giving back. For cases in the quartile with the lowest 30-day return (mean −33.6 %, 626 cases), the coin rises +0.78 % over the next 18 bars and +2.94 % over the next 72 bars. In the next quartile (−15.4 %), the coin falls −0.58 % over 18 bars.
- F2: The losses sit in the first three days after the last signal. On short bars 1 to 18 bars after the last negative forecast, the coin rises +3.60 bp a bar and the book loses −2.13 bp a bar (31,689 bars). On the signal bar itself, the coin falls −3.35 bp over the next bar.
- F1: The book loses because it stays short long after the signal has gone: the forecast is negative on only 24 % of bars, yet the book is short on 59 % of them. Short bars with a negative forecast gain +2.14 bp a bar (24,099 bars, +5.16 summed). Short bars carried at a zero forecast lose −1.77 bp a bar (38,095 bars, −6.75 summed), while the coin rises +3.05 bp a bar on them.
