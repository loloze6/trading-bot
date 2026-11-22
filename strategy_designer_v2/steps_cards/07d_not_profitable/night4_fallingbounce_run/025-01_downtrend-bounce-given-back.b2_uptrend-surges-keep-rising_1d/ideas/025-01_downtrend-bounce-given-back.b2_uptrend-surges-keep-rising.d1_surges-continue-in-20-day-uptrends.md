---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-01_downtrend-bounce-given-back.b2_uptrend-surges-keep-rising
line: 7.d not profitable
backtest: 025-01_downtrend-bounce-given-back.b2_uptrend-surges-keep-rising_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 90-day return is not negative, a one-day rise that is large relative to its usual daily move (its 20-day standard deviation of daily returns) is followed by a further rise over the next 5 days, the larger that rise in units of the usual daily move, only while the coin's 20-day return is positive, and the more so the larger that 20-day return.
Consequence: A trader keeps a long on a sharp up-day only while the coin's last 20 days are up, and sizes it with how far up they are, so the book is not long through the turn into a fall.
Why:
- F1: The Calmar fails because of one long fall. The book's yearly return is 21.5 % against a deepest fall of 40.6 % (Calmar 0.53 over 2898 days). That fall ran from w1 to w8 over 845 days, while holding the coins lost 67.3 %. The next falls, 32.2 % (w15 to w17) and 26.1 % (w18 to w19), also came while holding fell 42.3 % and 41.5 %.
- F2: The book loses on the bars where the coin's 20-day return is negative and gains only where it is positive. On held bars with a 20-day return below −8.75 %, the mean gain per bar is −0.020 % (t −0.42, n 1504); between −8.75 % and +0.5 % it is −0.009 % (t −0.16, n 1504); from +9.6 % to +24.5 % it is +0.40 % (t 4.23, n 1504).
- F4: Combined, held bars with a positive 20-day return near the 60-day high carry a summed gain of 9.75 of the book's total 12.35, at a mean of +0.41 % a bar. Bars with a negative 20-day return far from the high sum to −0.61 (1811 bars), and those near the high to −0.32 (mean −0.27 %).
- F5: The book stays exposed after its signal is gone. It holds a position on 51 % of bars, and on 52 % of those held bars the forecast is already 0 or below; the mean gain is the same with or without a live forecast (+0.138 % against +0.141 %). The position therefore rides into the coin's later falls.
