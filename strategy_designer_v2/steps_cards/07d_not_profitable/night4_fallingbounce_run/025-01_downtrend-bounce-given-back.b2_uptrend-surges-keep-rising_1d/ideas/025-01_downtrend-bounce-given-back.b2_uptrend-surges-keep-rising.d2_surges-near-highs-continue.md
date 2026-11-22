---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-01_downtrend-bounce-given-back.b2_uptrend-surges-keep-rising
line: 7.d not profitable
backtest: 025-01_downtrend-bounce-given-back.b2_uptrend-surges-keep-rising_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 90-day return is not negative, a one-day rise that is large relative to its usual daily move (its 20-day standard deviation of daily returns) is followed by a further rise over the next 5 days, the larger that rise in units of the usual daily move, and the more so the closer the coin's close is to its highest close of the past 60 days.
Consequence: A sharp up-day near the coin's 60-day high is a reason to go long for the following days, while the same up-day deep below that high is a reason to refuse the trade.
Why:
- F1: The Calmar fails because of one long fall. The book's yearly return is 21.5 % against a deepest fall of 40.6 % (Calmar 0.53 over 2898 days). That fall ran from w1 to w8 over 845 days, while holding the coins lost 67.3 %. The next falls, 32.2 % (w15 to w17) and 26.1 % (w18 to w19), also came while holding fell 42.3 % and 41.5 %.
- F3: The gain also depends on how near the coin is to its 60-day high. Held bars more than 25 % below that high earn −0.012 % a bar (t −0.34, n 1520), and those 13.5–25 % below earn +0.010 % (t 0.20). Bars within 2 % of the high earn +0.38 % (t 2.93) and bars 2–7 % below earn +0.30 % (t 3.62).
- F4: Combined, held bars with a positive 20-day return near the 60-day high carry a summed gain of 9.75 of the book's total 12.35, at a mean of +0.41 % a bar. Bars with a negative 20-day return far from the high sum to −0.61 (1811 bars), and those near the high to −0.32 (mean −0.27 %).
