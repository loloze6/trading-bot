---
brief: 025_bounces-fade-in-falling-markets
source-idea: 025-01_downtrend-bounce-given-back.b2_uptrend-surges-keep-rising
line: 7.d not profitable
backtest: 025-01_downtrend-bounce-given-back.b2_uptrend-surges-keep-rising_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: In a coin whose 90-day return is not negative, a one-day rise that is large relative to its usual daily move (its 20-day standard deviation of daily returns) is followed by a further rise over the next 5 days, the larger that rise in units of the usual daily move, and the more so the larger the coin's 90-day return.
Consequence: A trader leans harder on sharp up-days in coins with a strong 90-day rise, and holds back in coins that are only slightly up over 90 days.
Why:
- F1: The Calmar fails because of one long fall. The book's yearly return is 21.5 % against a deepest fall of 40.6 % (Calmar 0.53 over 2898 days). That fall ran from w1 to w8 over 845 days, while holding the coins lost 67.3 %. The next falls, 32.2 % (w15 to w17) and 26.1 % (w18 to w19), also came while holding fell 42.3 % and 41.5 %.
- F6: At entry, the longer trend sorts the trades. Trades entered with a 90-day return of 0 to 16.5 % lose 1.51 % on average after fees (38 % winners, n 127), and those at 16.5 to 34 % lose 2.33 % (39 % winners). Trades entered above 65 % gain 8.06 % (64 % winners, n 125).
- F7: The coin's recent 5-day path sorts the held bars the same way. Bars after a 5-day return below −4.7 % earn −0.059 % (t −1.27, n 1721), while bars after a 5-day return above +9 % earn +0.57 % (t 4.55, n 1721).
