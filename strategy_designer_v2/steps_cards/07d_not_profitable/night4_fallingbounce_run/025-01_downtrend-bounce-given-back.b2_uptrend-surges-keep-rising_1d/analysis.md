---
line: 7.d not profitable
backtest: 025-01_downtrend-bounce-given-back.b2_uptrend-surges-keep-rising_1d
idea tested: 025-01_downtrend-bounce-given-back.b2_uptrend-surges-keep-rising
step 5: confirmed
step 6: not profitable enough
mode: one call
explorations: 2
cost: 0.4087 USD
---
## Findings
- **F1:** The Calmar fails because of one long fall. The book's yearly return is 21.5 % against a deepest fall of 40.6 % (Calmar 0.53 over 2898 days). That fall ran from w1 to w8 over 845 days, while holding the coins lost 67.3 %. The next falls, 32.2 % (w15 to w17) and 26.1 % (w18 to w19), also came while holding fell 42.3 % and 41.5 %.
- **F2:** The book loses on the bars where the coin's 20-day return is negative and gains only where it is positive. On held bars with a 20-day return below −8.75 %, the mean gain per bar is −0.020 % (t −0.42, n 1504); between −8.75 % and +0.5 % it is −0.009 % (t −0.16, n 1504); from +9.6 % to +24.5 % it is +0.40 % (t 4.23, n 1504).
- **F3:** The gain also depends on how near the coin is to its 60-day high. Held bars more than 25 % below that high earn −0.012 % a bar (t −0.34, n 1520), and those 13.5–25 % below earn +0.010 % (t 0.20). Bars within 2 % of the high earn +0.38 % (t 2.93) and bars 2–7 % below earn +0.30 % (t 3.62).
- **F4:** Combined, held bars with a positive 20-day return near the 60-day high carry a summed gain of 9.75 of the book's total 12.35, at a mean of +0.41 % a bar. Bars with a negative 20-day return far from the high sum to −0.61 (1811 bars), and those near the high to −0.32 (mean −0.27 %).
- **F5:** The book stays exposed after its signal is gone. It holds a position on 51 % of bars, and on 52 % of those held bars the forecast is already 0 or below; the mean gain is the same with or without a live forecast (+0.138 % against +0.141 %). The position therefore rides into the coin's later falls.
- **F6:** At entry, the longer trend sorts the trades. Trades entered with a 90-day return of 0 to 16.5 % lose 1.51 % on average after fees (38 % winners, n 127), and those at 16.5 to 34 % lose 2.33 % (39 % winners). Trades entered above 65 % gain 8.06 % (64 % winners, n 125).
- **F7:** The coin's recent 5-day path sorts the held bars the same way. Bars after a 5-day return below −4.7 % earn −0.059 % (t −1.27, n 1721), while bars after a 5-day return above +9 % earn +0.57 % (t 4.55, n 1721).
- **F8:** The size is not the binding problem. The total move per case is 4.9 times the 0.19 % cost of a trade (+0.95 % over 5 days), and the unusual move is 1.9 times that cost.

## Ideas
- `025-01_downtrend-bounce-given-back.b2_uptrend-surges-keep-rising.d1_surges-continue-in-20-day-uptrends` (from F1, F2, F4, F5): In a coin whose 90-day return is not negative, a one-day rise that is large relative to its usual daily move (its 20-day standard deviation of daily returns) is followed by a further rise over the next 5 days, the larger that rise in units of the usual daily move, only while the coin's 20-day return is positive, and the more so the larger that 20-day return.
- `025-01_downtrend-bounce-given-back.b2_uptrend-surges-keep-rising.d2_surges-near-highs-continue` (from F1, F3, F4): In a coin whose 90-day return is not negative, a one-day rise that is large relative to its usual daily move (its 20-day standard deviation of daily returns) is followed by a further rise over the next 5 days, the larger that rise in units of the usual daily move, and the more so the closer the coin's close is to its highest close of the past 60 days.
- `025-01_downtrend-bounce-given-back.b2_uptrend-surges-keep-rising.d3_surges-scale-with-90-day-trend` (from F1, F6, F7): In a coin whose 90-day return is not negative, a one-day rise that is large relative to its usual daily move (its 20-day standard deviation of daily returns) is followed by a further rise over the next 5 days, the larger that rise in units of the usual daily move, and the more so the larger the coin's 90-day return.

Explorations: `exploration/` (each round's function and its result). Ideas: `ideas/`.
