---
brief: 012_liquidation-flush-partial-rebound
source-idea: 012-02_volume-burst-fall-reversal
line: 7.d not profitable
backtest: 012-02_volume-burst-fall-reversal_1d
instruments: BTC, ETH, LTC, XMR, XRP, ZEC
bar: 1d
period: folds A, B, C, D
---
Idea: Among bars that fall sharply, the larger the bar's volume relative to the coin's 30-day average volume, the larger the price rise over the next 1 day, with the rebound spent by the second day.
Consequence: A trader would take the volume-burst rebound as a one-day move and not keep it on through the following days, where the coin drifts lower.
Why:
- F2: Nearly all of the book's gain comes on the first day after a signal. On those 3040 bars the mean gain is 0.00325 and the coin's next-day return is 0.0057. On days 1 to 3 after the signal the coin's next-day return is negative (−0.0021, −0.0034, −0.0083; 325, 154 and 66 bars).
- F3: Trade length points the same way. Trades of up to 1.5 days net +1.48 % (1859 trades), while trades of 1.5–3.5 days net −4.83 % (433) and trades of 3.5–7.5 days net −6.99 % (196); overall the 2812 trades net −0.17 % on average.
- F4: The rebound sits almost wholly in the strongest forecasts. Signal bars in the top forecast quintile (mean volume ratio 1.89) are followed by a 3-day return of 0.0127. The four lower quintiles give −0.0008 to 0.0042, which is no larger than the coin's own mean.
